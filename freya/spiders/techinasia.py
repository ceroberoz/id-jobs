import scrapy
import json
from datetime import datetime
import logging
from typing import Dict, Any, Optional
from urllib.parse import urlencode  # Add this import
from freya.pipelines import calculate_job_age
from freya.utils import calculate_job_apply_end_date

logger = logging.getLogger(__name__)

class TechInAsiaSpider(scrapy.Spider):
    name = 'techinasia'
    BASE_URL = 'https://219wx3mpv4-dsn.algolia.net/1/indexes/*/queries'

    custom_settings = {
        'DOWNLOAD_DELAY': 0.2,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'content-type': 'application/x-www-form-urlencoded',
            'Origin': 'https://www.techinasia.com',
            'Connection': 'keep-alive',
            'Referer': 'https://www.techinasia.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'DNT': '1',
            'Sec-GPC': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }

        params = {
            'x-algolia-agent': 'Algolia for vanilla JavaScript 3.30.0;JS Helper 2.26.1',
            'x-algolia-application-id': '219WX3MPV4',
            'x-algolia-api-key': 'b528008a75dc1c4402bfe0d8db8b3f8e',
        }

        payload = {
            "requests": [
                {
                    "indexName": "job_postings",
                    "params": "query=&hitsPerPage=20&maxValuesPerFacet=1000&page=0&facets=%5B%22*%22%2C%22city.work_country_name%22%2C%22position.name%22%2C%22industries.vertical_name%22%2C%22experience%22%2C%22job_type.name%22%2C%22is_salary_visible%22%2C%22has_equity%22%2C%22currency.currency_code%22%2C%22salary_min%22%2C%22taxonomies.slug%22%5D&tagFilters=&facetFilters=%5B%5B%22city.work_country_name%3AIndonesia%22%5D%5D"
                },
                {
                    "indexName": "job_postings",
                    "params": "query=&hitsPerPage=1&maxValuesPerFacet=1000&page=0&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&analytics=false&clickAnalytics=false&facets=city.work_country_name"
                }
            ]
        }

        yield scrapy.Request(
            f"{self.BASE_URL}?{urlencode(params)}",
            method='POST',
            headers=headers,
            body=json.dumps(payload),
            callback=self.parse,
            dont_filter=True
        )

    def parse(self, response):
        try:
            data = json.loads(response.text)
            hits = data['results'][0]['hits']
            total_pages = data['results'][0]['nbPages']

            for job in hits:
                yield self.parse_job(job)

            # Handle pagination
            current_page = data['results'][0]['page']
            if current_page < total_pages - 1:
                payload = json.loads(response.request.body)
                params_str = payload['requests'][0]['params']
                new_params_str = params_str.replace(f"page={current_page}", f"page={current_page + 1}")
                payload['requests'][0]['params'] = new_params_str

                yield scrapy.Request(
                    response.url,
                    method='POST',
                    headers=response.request.headers,
                    body=json.dumps(payload),
                    callback=self.parse,
                    dont_filter=True
                )

        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            logger.debug(f"Response content: {response.text}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

    def parse_job(self, job: Dict[str, Any]) -> Dict[str, Any]:
        first_seen = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        last_seen = self.sanitize_string(job.get('published_at', 'N/A'))

        def format_salary(min_salary, max_salary, currency):
            min_sal = self.sanitize_string(str(min_salary)) if min_salary is not None else 'N/A'
            max_sal = self.sanitize_string(str(max_salary)) if max_salary is not None else 'N/A'
            curr = self.sanitize_string(currency) if currency else 'N/A'
            return f"{min_sal} - {max_sal} {curr}".replace(',', '')

        return {
            'job_title': self.sanitize_string(job.get('title')),
            'job_location': f"{self.sanitize_string(job.get('city', {}).get('name'))} - {self.sanitize_string(job.get('city', {}).get('work_country_name'))}",
            'job_department': self.sanitize_string(job.get('position', {}).get('name')),
            'job_url': self.sanitize_string(f"https://www.techinasia.com/jobs/{job.get('id')}"),
            'first_seen': self.sanitize_string(first_seen),
            'base_salary': format_salary(job.get('salary_min'), job.get('salary_max'), job.get('currency', {}).get('currency_code')),
            'job_type': self.sanitize_string(job.get('job_type', {}).get('name')),
            'job_level': f"{self.sanitize_string(str(job.get('experience_min', 'N/A')))} - {self.sanitize_string(str(job.get('experience_max', 'N/A')))} years",
            'job_apply_end_date': self.sanitize_string(calculate_job_apply_end_date(last_seen)),
            'last_seen': last_seen,
            'is_active': 'True',
            'company': self.sanitize_string(job.get('company', {}).get('name')),
            'company_url': self.sanitize_string(f"https://www.techinasia.com/companies/{job.get('company', {}).get('entity_slug')}"),
            'job_board': 'Tech in Asia Jobs',
            'job_board_url': 'https://www.techinasia.com/jobs',
            'job_age': self.sanitize_string(str(calculate_job_age(first_seen, last_seen))),
            'work_arrangement': 'Remote' if job.get('is_remote') else 'On-site',
        }

    @staticmethod
    def sanitize_string(s: Optional[str]) -> str:
        if s is None:
            return 'N/A'
        return s.strip().replace(',', ' -').replace('\n', ' ').replace('\r', '')
