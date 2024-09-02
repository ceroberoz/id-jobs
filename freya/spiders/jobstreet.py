import scrapy
import json
from datetime import datetime, timezone, timedelta
import random
import urllib.parse
import time
from typing import Dict, Any, List
from scrapy.utils.project import get_project_settings
import uuid
from freya.pipelines import calculate_job_age  # Import the function
from freya.utils import clean_string, format_date

def generate_random_id():
    return str(uuid.uuid4())

def generate_random_query_id():
    return f"{uuid.uuid4().hex}-{random.randint(1000000, 9999999)}"

def format_date(date_string):
    if not date_string or date_string == 'N/A':
        return 'N/A'
    try:
        dt = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return date_string

class JobstreetSpider(scrapy.Spider):
    name = 'jobstreet'
    BASE_URL = 'https://id.jobstreet.com/api/chalice-search/v4/search'
    MAX_PAGES = 1000
    JOBS_PER_PAGE = 30

    def __init__(self, *args, **kwargs):
        super(JobstreetSpider, self).__init__(*args, **kwargs)
        self.settings = get_project_settings()
        self.user_agents = self.settings.get('USER_AGENTS', [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0',
        ])

    def start_requests(self):
        concurrent_requests = self.settings.getint('CONCURRENT_REQUESTS', 16)
        download_delay = self.settings.getfloat('DOWNLOAD_DELAY', 0.25)

        for page in range(1, self.MAX_PAGES + 1):
            params = self.get_request_params(page)
            headers = self.get_headers()

            yield scrapy.Request(
                url=f"{self.BASE_URL}?{urllib.parse.urlencode(params)}",
                headers=headers,
                callback=self.parse,
                meta={'page': page, 'download_delay': download_delay},
                errback=self.errback_httpbin
            )

    def get_request_params(self, page: int) -> Dict[str, str]:
        user_id = generate_random_id()
        return {
            'siteKey': 'ID-Main',
            'sourcesystem': 'houston',
            'userqueryid': generate_random_query_id(),
            'userid': user_id,
            'usersessionid': user_id,
            'eventCaptureSessionId': user_id,
            'page': str(page),
            'seekSelectAllPages': 'true',
            'sortmode': 'ListedDate',
            'pageSize': str(self.JOBS_PER_PAGE),
            'include': 'seodata',
            'locale': 'id-ID',
            'solId': generate_random_id()
        }

    def get_headers(self) -> Dict[str, str]:
        return {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'dnt': '1',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://id.jobstreet.com/id/jobs?sortmode=ListedDate',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'seek-request-brand': 'jobstreet',
            'seek-request-country': 'ID',
            'user-agent': random.choice(self.user_agents),
            'x-forwarded-for': f'1.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}',
            'x-seek-checksum': '129cf744',
            'x-seek-site': 'Chalice'
        }

    def parse(self, response):
        try:
            data = json.loads(response.text)
            jobs = data.get('data', [])

            if not jobs:
                self.logger.info(f"No more jobs found on page {response.meta['page']}. Stopping crawl.")
                return

            for job in jobs:
                yield self.parse_job(job)

            # Add a random delay between requests
            time.sleep(response.meta['download_delay'] + random.uniform(0.5, 1.5))

        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding JSON on page {response.meta['page']}: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error on page {response.meta['page']}: {e}")

    def parse_job(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse a job listing and return a structured dictionary.

        Args:
            job (Dict[str, Any]): Raw job data from the API.

        Returns:
            Dict[str, Any]: Structured job data.
        """
        now = datetime.now(timezone.utc)
        first_seen = now.strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            job_id = str(job.get('id', ''))
            company_name = clean_string(job.get('companyName', ''))
            company_name = company_name if company_name else "Private Advertiser"
            listing_date = job.get('listingDate', '')
            last_seen = format_date(listing_date)
            advertiser_id = job.get('advertiser', {}).get('id', '')
            
            # Calculate job_apply_end_date (listing_date + 30 days)
            if listing_date:
                listing_datetime = datetime.strptime(listing_date, "%Y-%m-%dT%H:%M:%SZ")
                apply_end_date = listing_datetime + timedelta(days=30)
                job_apply_end_date = apply_end_date.strftime("%Y-%m-%d %H:%M:%S")
            else:
                job_apply_end_date = ''
            
            return {
                'job_title': clean_string(job.get('title', '')),
                'job_location': clean_string(job.get('jobLocation', {}).get('label', '')),
                'job_department': clean_string(f"{job.get('classification', {}).get('description', '')}-{job.get('subClassification', {}).get('description', '')}"),
                'job_url': f"https://id.jobstreet.com/job/{job_id}",
                'first_seen': first_seen,
                'base_salary': clean_string(job.get('salary', 'N/A')),
                'job_type': clean_string(job.get('workType', 'N/A')),
                'job_level': self.extract_job_level(job),
                'job_apply_end_date': job_apply_end_date,
                'last_seen': last_seen,
                'is_active': 'True',
                'company': company_name,
                'company_url': f"https://id.jobstreet.com/companies/{company_name.lower().replace(' ', '-')}-{advertiser_id}" if advertiser_id else '', # TODO: Check if this is the correct company URL
                'job_board': 'Jobstreet',
                'job_board_url': 'https://id.jobstreet.com/',
                'job_age': calculate_job_age(first_seen, last_seen),

                # TODO: Add job description, work arrangement, is_premium, advertiser_id, and display_type
                # 'job_description': clean_string(job.get('teaser', '')),
                # 'work_arrangement': self.extract_work_arrangement(job),
                # 'is_premium': str(job.get('isPremium', False)),
                # 'advertiser_id': advertiser_id,
                # 'display_type': job.get('displayType', ''),
            }
        except Exception as e:
            self.logger.error(f"Error parsing job {job_id} from {company_name}: {str(e)}")
            return {}  # Return an empty dict if parsing fails

    def extract_job_level(self, job: Dict[str, Any]) -> str:
        """Extract job level from classification if available."""
        classification = job.get('classification', {}).get('description', '')
        subclassification = job.get('subClassification', {}).get('description', '')
        return f"{classification} - {subclassification}" if classification or subclassification else 'N/A'

    def extract_company_url(self, job: Dict[str, Any]) -> str:
        """Extract company URL from branding if available."""
        return job.get('branding', {}).get('assets', {}).get('logo', {}).get('strategies', {}).get('serpLogo', '')

    def extract_work_arrangement(self, job: Dict[str, Any]) -> str:
        """Extract work arrangement if available."""
        arrangements = job.get('workArrangements', {}).get('data', [])
        return ', '.join([arr.get('label', {}).get('text', '') for arr in arrangements]) if arrangements else 'N/A'

    def errback_httpbin(self, failure):
        self.logger.error(f"HTTP Error: {failure}")