import scrapy
import json
from datetime import datetime
import logging
from typing import Dict, Any, Optional
from freya.pipelines import calculate_job_age  # Import the function


logger = logging.getLogger(__name__)

class KalibrrSpiderJson(scrapy.Spider):
    name = 'kalibrr'
    BASE_URL = 'https://www.kalibrr.com/kjs/job_board/search?limit=2000&offset={}'
    JOB_URL_TEMPLATE = "https://www.kalibrr.com/c/{}/jobs/{}"
    COMPANY_URL_TEMPLATE = "https://www.kalibrr.com/id-ID/c/{}/jobs"
    JOB_BOARD_URL = 'https://www.kalibrr.com/id-ID/home'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def start_requests(self):
        yield scrapy.Request(
            self.BASE_URL.format(0),
            headers={'Content-Type': 'application/json'},
            callback=self.parse
        )

    def parse(self, response):
        try:
            data = json.loads(response.text)
            jobs = data.get('jobs', [])

            for job in jobs:
                yield self.parse_job(job)

            self.handle_pagination(data)

        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

    def handle_pagination(self, data: Dict[str, Any]):
        total_jobs = data.get('total', 0)
        current_offset = data.get('offset', 0)
        jobs = data.get('jobs', [])
        if current_offset + len(jobs) < total_jobs:
            next_offset = current_offset + len(jobs)
            yield scrapy.Request(
                self.BASE_URL.format(next_offset),
                callback=self.parse
            )

    def parse_job(self, job: Dict[str, Any]) -> Dict[str, Any]:
        first_seen = datetime.strptime(self.timestamp, "%d/%m/%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        last_seen = self.format_datetime(job['created_at'])
        
        return {
            'job_title': self.sanitize_string(job['name']),
            'job_location': self.get_location(job['google_location']),
            'job_department': job['function'],
            'job_url': self.JOB_URL_TEMPLATE.format(job['company']['code'], job['id']),
            'first_seen': first_seen,
            'base_salary': str(job['base_salary']) if job['base_salary'] else '',
            'job_type': job['tenure'],
            'job_level': self.get_job_level(job['education_level']),
            'job_apply_end_date': self.format_datetime(job['application_end_date']),
            'last_seen': last_seen,
            'is_active': 'True',
            'company': job['company_name'],
            'company_url': self.COMPANY_URL_TEMPLATE.format(job['company']['code']),
            'job_board': 'Kalibrr',
            'job_board_url': self.JOB_BOARD_URL,
            'job_age': calculate_job_age(first_seen, last_seen)  # Ensure this line is present
        }

    @staticmethod
    def sanitize_string(s: Optional[str]) -> str:
        return s.replace(", ", " - ") if s else 'N/A'

    @staticmethod
    def get_job_location(job: Dict[str, Any]) -> str:
        return job.get('google_location', {}).get('address_components', {}).get('city', 'N/A')

    def get_job_url(self, job: Dict[str, Any]) -> str:
        company_code = job.get('company_info', {}).get('code', '')
        job_id = job.get('id', '')
        return self.JOB_URL_TEMPLATE.format(company_code, job_id)

    def get_company_url(self, job: Dict[str, Any]) -> str:
        company_code = job.get('company_info', {}).get('code', '')
        return self.COMPANY_URL_TEMPLATE.format(company_code)

    def get_location(self, google_location: Dict[str, Any]) -> str:
        if google_location and 'address_components' in google_location:
            components = google_location['address_components']
            city = components.get('city', '')
            region = components.get('region', '')
            country = components.get('country', '')
            return f"{city}, {region}, {country}".strip(', ')
        return 'N/A'

    def get_job_level(self, education_level: int) -> str:
        # You may need to adjust this mapping based on Kalibrr's education level codes
        education_map = {
            200: 'High School',
            550: 'Bachelor',
            650: 'Master',
            # Add more mappings as needed
        }
        return education_map.get(education_level, 'N/A')

    def format_datetime(self, date_string: str) -> str:
        try:
            dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return date_string