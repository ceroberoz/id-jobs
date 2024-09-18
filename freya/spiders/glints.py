import scrapy
import json
from datetime import datetime
import logging
from typing import Dict, Any, Optional, List
import random
from freya.pipelines import calculate_job_age
from freya.utils import calculate_job_apply_end_date

logger = logging.getLogger(__name__)

class GlintsSpider(scrapy.Spider):
    name = 'glints'
    BASE_URL = 'https://glints.com'
    API_URL = f'{BASE_URL}/api/v2/graphql?op=searchJobs'

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
        yield self.create_request(0)

    def create_request(self, offset):
        headers = {
            'accept': '*/*',
            'accept-language': 'id',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'dnt': '1',
            'origin': 'https://glints.com',
            'pragma': 'no-cache',
            'referer': 'https://glints.com/id/opportunities/jobs/explore?keyword=*&country=ID&locationName=All+Cities%2FProvinces&lowestLocationLevel=1',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': random.choice(self.USER_AGENTS),
            'x-glints-country-code': 'ID'
        }

        payload = {
            "query": "query searchJobs($data: JobSearchConditionInput!) {\n  searchJobs(data: $data) {\n    jobsInPage {\n      id\n      title\n      workArrangementOption\n      status\n      createdAt\n      updatedAt\n      isActivelyHiring\n      isHot\n      isApplied\n      shouldShowSalary\n      educationLevel\n      type\n      fraudReportFlag\n      salaryEstimate {\n        minAmount\n        maxAmount\n        CurrencyCode\n        __typename\n      }\n      company {\n        ...CompanyFields\n        __typename\n      }\n      citySubDivision {\n        id\n        name\n        __typename\n      }\n      city {\n        ...CityFields\n        __typename\n      }\n      country {\n        ...CountryFields\n        __typename\n      }\n      salaries {\n        ...SalaryFields\n        __typename\n      }\n      location {\n        ...LocationFields\n        __typename\n      }\n      minYearsOfExperience\n      maxYearsOfExperience\n      source\n      type\n      hierarchicalJobCategory {\n        id\n        level\n        name\n        children {\n          name\n          level\n          id\n          __typename\n        }\n        parents {\n          id\n          level\n          name\n          __typename\n        }\n        __typename\n      }\n      skills {\n        skill {\n          id\n          name\n          __typename\n        }\n        mustHave\n        __typename\n      }\n      traceInfo\n      __typename\n    }\n    numberOfJobsCreatedInLast14Days\n    totalJobs\n    expInfo\n    __typename\n  }\n}\n\nfragment CompanyFields on Company {\n  id\n  name\n  logo\n  status\n  isVIP\n  IndustryId\n  industry {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment CityFields on City {\n  id\n  name\n  __typename\n}\n\nfragment CountryFields on Country {\n  code\n  name\n  __typename\n}\n\nfragment SalaryFields on JobSalary {\n  id\n  salaryType\n  salaryMode\n  maxAmount\n  minAmount\n  CurrencyCode\n  __typename\n}\n\nfragment LocationFields on HierarchicalLocation {\n  id\n  name\n  administrativeLevelName\n  formattedName\n  level\n  slug\n  parents {\n    id\n    name\n    administrativeLevelName\n    formattedName\n    level\n    slug\n    parents {\n      level\n      formattedName\n      slug\n      __typename\n    }\n    __typename\n  }\n  __typename\n}",
            "variables": {
                "data": {
                    "SearchTerm": "*",
                    "CountryCode": "ID",
                    "limit": 30,
                    "offset": offset,
                    "includeExternalJobs": True,
                    "searchVariant": "VARIANT_A"
                }
            }
        }

        return scrapy.Request(
            self.API_URL,
            method='POST',
            headers=headers,
            body=json.dumps(payload),
            callback=self.parse,
            meta={'offset': offset}
        )

    def parse(self, response):
        try:
            data = json.loads(response.text)
            jobs = data['data']['searchJobs']['jobsInPage']

            if not jobs:
                logger.info("No more jobs to scrape. Stopping.")
                return

            for job in jobs:
                yield self.parse_job(job)

            # Request next page
            current_offset = response.meta['offset']
            next_offset = current_offset + 30
            yield self.create_request(next_offset)

        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            logger.debug(f"Response content: {response.text}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

    def parse_job(self, job: Dict[str, Any]) -> Dict[str, Any]:
        first_seen = datetime.strptime(self.timestamp, "%d/%m/%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        last_seen = self.format_iso_time(job.get('updatedAt'))

        return {
            'job_title': self.sanitize_string(job.get('title')),
            'job_location': self.sanitize_string(f"{job.get('city', {}).get('name', 'N/A')}, {job.get('country', {}).get('name', 'N/A')}"),
            'job_department': self.sanitize_string(job.get('hierarchicalJobCategory', {}).get('name')),
            'job_url': f"{self.BASE_URL}/id/opportunities/jobs/{job.get('id')}",
            'first_seen': first_seen,
            'base_salary': self.get_salary(job.get('salaries', [])),
            'job_type': self.sanitize_string(job.get('type')),
            'job_level': f"{job.get('minYearsOfExperience', 'N/A')}-{job.get('maxYearsOfExperience', 'N/A')} years",
            'job_apply_end_date': calculate_job_apply_end_date(last_seen),
            'last_seen': last_seen,
            'is_active': 'True' if job.get('isActivelyHiring') else 'False',
            'company': self.sanitize_string(job.get('company', {}).get('name')),
            'company_url': f"{self.BASE_URL}/id/companies/{job.get('company', {}).get('id')}",
            'job_board': 'Glints',
            'job_board_url': self.BASE_URL,
            'job_age': calculate_job_age(first_seen, last_seen),
            'work_arrangement': self.sanitize_string(job.get('workArrangementOption')),
        }

    def sanitize_string(self, s: Optional[str]) -> str:
        if s is None:
            return 'N/A'
        return s.replace(',', '').strip()

    def get_salary(self, salaries: List[Dict[str, Any]]) -> str:
        if not salaries:
            return 'N/A'
        basic_salary = next((s for s in salaries if s.get('salaryType') == 'BASIC'), None)
        if basic_salary:
            min_amount = basic_salary.get('minAmount', 'N/A')
            max_amount = basic_salary.get('maxAmount', 'N/A')
            currency = basic_salary.get('CurrencyCode', 'N/A')
            return f"{currency} {min_amount}-{max_amount}"
        return 'N/A'

    def format_iso_time(self, time_str: Optional[str]) -> str:
        if time_str is None:
            return 'N/A'
        try:
            dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            return 'N/A'
