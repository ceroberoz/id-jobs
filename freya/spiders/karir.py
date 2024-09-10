import scrapy
import json
from datetime import datetime
import logging
from typing import Dict, Any, Optional
import random
from freya.pipelines import calculate_job_age
from freya.utils import calculate_job_apply_end_date

logger = logging.getLogger(__name__)

class KarirSpiderJson(scrapy.Spider):
    name = 'karir'
    BASE_URL = 'https://gateway2-beta.karir.com/v2/search/opportunities'
    LIMIT = 5  # Number of jobs per page

    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0',
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def start_requests(self):
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json',
            'Origin': 'https://karir.com',
            'Pragma': 'no-cache',
            'Referer': 'https://karir.com/',
            'User-Agent': random.choice(self.USER_AGENTS),
            'dnt': '1',
            'sec-gpc': '1'
        }
        
        payload = self.get_payload(0)  # Start with offset 0

        yield scrapy.Request(
            self.BASE_URL,
            method='POST',
            headers=headers,
            body=json.dumps(payload),
            callback=self.parse
        )

    def get_payload(self, offset):
        return {
            "keyword":"*",
            "location_ids":[],
            "company_ids":[],
            "industry_ids":[],
            "job_function_ids":[],
            "degree_ids":[],
            "locale":"id",
            "limit": self.LIMIT,
            "offset": offset,
            "level":"",
            "min_employee":0,
            "max_employee":50,
            "is_opportunity":True,
            "sort_order":"",
            "is_recomendation":False,
            "is_preference":False,
            "is_choice_opportunity":False,
            "is_subscribe":False,
            "workplace":None
        }

    def parse(self, response):
        try:
            data = json.loads(response.text)
            opportunities = data['data']['opportunities']
            total_opportunities = data['data']['total_opportunities']

            for opportunity in opportunities:
                yield self.parse_job(opportunity)

            # Explosive pagination!
            current_offset = json.loads(response.request.body)['offset']
            next_offset = current_offset + self.LIMIT

            if next_offset < total_opportunities:
                logger.info(f"💥 EXPLOSION! Fetching next page. Current progress: {next_offset}/{total_opportunities} 💥")
                yield scrapy.Request(
                    self.BASE_URL,
                    method='POST',
                    headers=response.request.headers,
                    body=json.dumps(self.get_payload(next_offset)),
                    callback=self.parse
                )
            else:
                logger.info("🎆 ULTIMATE EXPLOSION! All job opportunities have been obliterated... I mean, scraped! 🎆")

        except json.JSONDecodeError as e:
            logger.error(f"💔 Error decoding JSON: {e}")
            logger.debug(f"Response content: {response.text}")
        except Exception as e:
            logger.error(f"💥 Unexpected error: {e}")

    def parse_job(self, job: Dict[str, Any]) -> Dict[str, Any]:
        first_seen = datetime.strptime(self.timestamp, "%d/%m/%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        last_seen = self.format_datetime(job['posted_at'])
        
        return {
            'job_title': self.sanitize_string(job['job_position']),
            'job_location': self.sanitize_string(job['description']),
            'job_department': 'N/A',  # Not provided in the response
            'job_url': f"https://karir.com/opportunities/{job['id']}",  # Assuming this is the correct URL format
            'first_seen': first_seen,
            'base_salary': self.get_salary_info(job),
            'job_type': 'N/A',  # Not provided in the response
            'job_level': 'N/A',  # Not provided in the response
            'job_apply_end_date': calculate_job_apply_end_date(last_seen),
            'last_seen': last_seen,
            'is_active': 'True',
            'company': self.sanitize_string(job['company_name']),
            'company_url': f"https://karir.com/companies/{job['company_id']}",  # Assuming this is the correct URL format
            'job_board': 'Karir.com',
            'job_board_url': 'https://karir.com/',
            'job_age': calculate_job_age(first_seen, last_seen),
            'work_arrangement': 'N/A',  # Not provided in the response

            # Optional fields
            # 'is_urgent': str(job['is_urgent']),
        }

    @staticmethod
    def sanitize_string(s: Optional[str]) -> str:
        if s is None:
            return 'N/A'
        # Strip whitespace, replace commas with hyphens, and handle empty strings
        sanitized = s.strip().replace(',', ' -')
        return sanitized if sanitized else 'N/A'

    @staticmethod
    def format_datetime(date_string: str) -> str:
        try:
            dt = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            try:
                dt = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
                return dt.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                return date_string

    @staticmethod
    def get_salary_info(job: Dict[str, Any]) -> str:
        if job['salary_lower'] and job['salary_upper']:
            return f"{job['salary_lower']} - {job['salary_upper']}"
        elif job['salary_info'] and job['salary_info'] != 'LABEL_COMPETITIVE_SALARY':
            return job['salary_info']
        else:
            return 'N/A'