import scrapy
import json
from datetime import datetime
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class EvermosSpiderJson(scrapy.Spider):
    name = 'evermos'
    BASE_URL = 'https://evermos-talent.freshteam.com/hire/widgets/jobs.json'
    COMPANY_URL = 'https://evermos.com/'

    JOB_TYPE_MAPPING = {
        1: "Contract",
        2: "Full Time",
        3: "Intern"
    }

    custom_settings = {
        'ROBOTSTXT_OBEY': False
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def start_requests(self):
        headers = self.get_headers()
        yield scrapy.Request(self.BASE_URL, headers=headers, callback=self.parse)

    def get_headers(self):
        return {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Chrome OS"'
        }

    def parse(self, response):
        try:
            data = json.loads(response.text)
            branch_lookup = self.create_branch_lookup(data['branches'])
            job_roles_lookup = self.create_job_roles_lookup(data['job_roles'])
            
            for job in data['jobs']:
                yield self.parse_job(job, branch_lookup, job_roles_lookup)
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            logger.debug(f"Response content: {response.text}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

    @staticmethod
    def create_branch_lookup(branches_data):
        return {branch['id']: branch['city'] for branch in branches_data}

    @staticmethod
    def create_job_roles_lookup(job_roles_data):
        return {job_role['id']: job_role['name'] for job_role in job_roles_data}

    def parse_job(self, job: Dict[str, Any], branch_lookup: Dict[int, str], job_roles_lookup: Dict[int, str]) -> Dict[str, Any]:
        return {
            'job_title': self.sanitize_string(job['title']),
            'job_location': branch_lookup.get(job['branch_id'], 'N/A'),
            'job_department': job_roles_lookup.get(job['job_role_id'], 'N/A'),
            'job_url': job['url'],
            'first_seen': self.timestamp,
            'base_salary': '',
            'job_type': self.get_job_type(job['job_type']),
            'job_level': job['position_level'],
            'job_apply_end_date': job['closing_date'],
            'last_seen': '',
            'is_active': 'True',
            'company': 'Evermos',
            'company_url': self.COMPANY_URL,
            'job_board': 'N/A',
            'job_board_url': 'N/A'
        }

    @staticmethod
    def sanitize_string(s: Optional[str]) -> str:
        return s.replace(", ", " - ") if s else 'N/A'

    def get_job_type(self, job_type_id: int) -> str:
        return self.JOB_TYPE_MAPPING.get(job_type_id, 'N/A')