# -*- coding: utf-8 -*-
import scrapy
import json
from datetime import datetime

class KalibrrSpiderJson(scrapy.Spider):
    name = 'kalibrr' #json
    base_url = 'https://www.kalibrr.com/kjs/job_board/search?limit=2000&offset={}'

    def start_requests(self):
        yield scrapy.Request(self.base_url.format(0), headers={'Content-Type': 'application/json'})

    def parse(self, response):
        try:
            data = json.loads(response.text)
            jobs = data.get('jobs', [])

            for job in jobs:
                yield self.parse_job(job)

            # Implement pagination
            total_jobs = data.get('total', 0)
            current_offset = data.get('offset', 0)
            if current_offset + len(jobs) < total_jobs:
                next_offset = current_offset + len(jobs)
                yield scrapy.Request(self.base_url.format(next_offset), callback=self.parse)

        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding JSON: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")

    def parse_job(self, job):
        return {
            'job_title': job.get('name', '').replace(", ", " - "),
            'job_location': job.get('google_location', {}).get('address_components', {}).get('city', 'N/A'),
            'job_department': 'N/A',
            'job_url': f"https://www.kalibrr.com/c/{job.get('company_info', {}).get('code', '')}/jobs/{job.get('id', '')}",
            'first_seen': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            'base_salary': job.get('base_salary'),
            'job_type': job.get('tenure'),
            'job_level': 'N/A',
            'job_apply_end_date': job.get('application_end_date'),
            'last_seen': '',
            'is_active': 'True',
            'company': job.get('company_name'),
            'company_url': f"https://www.kalibrr.com/id-ID/c/{job.get('company_info', {}).get('code', '')}/jobs",
            'job_board': 'Kalibrr',
            'job_board_url': 'https://www.kalibrr.com/id-ID/home'
        }
