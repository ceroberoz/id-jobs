import scrapy
import json
from datetime import datetime
import logging
from typing import Dict, Any, Optional
import random
from freya.pipelines import calculate_job_age
from freya.utils import calculate_job_apply_end_date

# Set up the logger for this spider
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
        # Initialize the spider and set the current timestamp
        super().__init__(*args, **kwargs)
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def start_requests(self):
        # Start the scraping process by sending the initial request
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
        # Create the payload for the API request
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
                yield scrapy.Request(
                    f"https://karir.com/_next/data/3t_6puNZeaT81JcSVqzwu/opportunities/{opportunity['id']}.json?index={opportunity['id']}",
                    headers={
                        'User-Agent': random.choice(self.USER_AGENTS),
                        'Accept': '*/*',
                        'Referer': 'https://karir.com/search-lowongan?keyword=*'
                    },
                    callback=self.parse_job_details,
                    meta={'job': opportunity}
                )

            # Handle pagination
            current_offset = json.loads(response.request.body)['offset']
            next_offset = current_offset + self.LIMIT

            if next_offset < total_opportunities:
                # Log progress: show how many jobs have been processed out of the total
                logger.info(f"Progress update: Processed {next_offset} out of {total_opportunities} jobs")
                yield scrapy.Request(
                    self.BASE_URL,
                    method='POST',
                    headers=response.request.headers,
                    body=json.dumps(self.get_payload(next_offset)),
                    callback=self.parse
                )
            else:
                # Log completion: all jobs have been processed
                logger.info(f"Finished processing all {total_opportunities} jobs")

        except json.JSONDecodeError as e:
            # Log error: couldn't understand the JSON response
            logger.error(f"Couldn't read the JSON response: {e}")
            logger.debug(f"The response we couldn't understand: {response.text}")
        except Exception as e:
            # Log error: something unexpected went wrong
            logger.error(f"An unexpected problem occurred: {e}")

    def parse_job_details(self, response):
        try:
            job = response.meta['job']
            job_detail = json.loads(response.text)['pageProps']['responseData']

            first_seen = self.timestamp
            last_seen = self.format_datetime(job['posted_at'])

            yield {
                'job_title': self.sanitize_string(job['job_position']),
                'job_location': self.sanitize_string(job_detail['location']),
                'job_department': ' - '.join(job_detail['job_functions']),
                'job_url': f"https://karir.com/opportunities/{job['id']}",
                'first_seen': first_seen,
                'base_salary': self.get_salary_info(job_detail),
                'job_type': job_detail['job_type'],
                'job_level': ' - '.join(job_detail['job_levels']),
                'job_apply_end_date': self.format_datetime(job_detail['expires_at']),
                'last_seen': last_seen,
                'is_active': str(not job_detail['is_expired']),
                'company': self.sanitize_string(job_detail['company_name']),
                'company_url': f"https://karir.com/companies/{job_detail['company']['id']}",
                'job_board': 'Karir.com',
                'job_board_url': 'https://karir.com/',
                'job_age': calculate_job_age(first_seen, last_seen),
                'work_arrangement': job_detail['workplace'],
            }
        except Exception as e:
            logger.error(f"Error processing job details: {e}")

    @staticmethod
    def sanitize_string(s: Optional[str]) -> str:
        # Clean up a string by removing unwanted characters
        if s is None:
            return 'N/A'
        sanitized = s.strip().replace(',', ' -')
        return sanitized if sanitized else 'N/A'

    @staticmethod
    def format_datetime(date_string: str) -> str:
        # Convert a date string to a standard format
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
        # Extract salary information from the job data
        if job['salary_lower'] and job['salary_upper']:
            return f"{job['salary_lower']} - {job['salary_upper']}"
        elif job['salary_info'] and job['salary_info'] != 'LABEL_COMPETITIVE_SALARY':
            return job['salary_info']
        else:
            return 'N/A'
