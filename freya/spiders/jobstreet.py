# -*- coding: utf-8 -*-
import scrapy
import json
from datetime import datetime
import random
import urllib.parse

def clean_string(text):
    if not isinstance(text, str):
        return text
    return text.replace(',', ' ').replace('\n', ' ').strip()

class JobstreetSpider(scrapy.Spider):
    name = 'jobstreet'
    base_url = 'https://id.jobstreet.com/api/chalice-search/v4/search'

    def start_requests(self):
        headers = {
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
            'user-agent': 'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320',
            'x-forwarded-for': f'1.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}',
            'x-seek-checksum': '129cf744',
            'x-seek-site': 'Chalice'
        }

        for page in range(1, 1001):  # Crawl up to page 1000
            params = {
                'siteKey': 'ID-Main',
                'sourcesystem': 'houston',
                'userqueryid': 'd751713988987e9331980363e24189ce-0531699',
                'userid': 'b2a4f3f8-116d-41de-9dc1-4e7cbb574373',
                'usersessionid': 'b2a4f3f8-116d-41de-9dc1-4e7cbb574373',
                'eventCaptureSessionId': 'b2a4f3f8-116d-41de-9dc1-4e7cbb574373',
                'page': str(page),
                'seekSelectAllPages': 'true',
                'sortmode': 'ListedDate',
                'pageSize': '30',
                'include': 'seodata',
                'locale': 'id-ID',
                'solId': 'a7a7e3ac-ec9c-4845-84d6-5cfb696ae79a'
            }

            yield scrapy.Request(
                url=f"{self.base_url}?{urllib.parse.urlencode(params)}",
                headers=headers,
                callback=self.parse
            )

    def parse(self, response):
        try:
            data = json.loads(response.text)
            jobs = data.get('data', [])

            for job in jobs:
                yield self.parse_job(job)

        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding JSON: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")

    def parse_job(self, job):
        return {
            'job_title': clean_string(job.get('title', '')),
            'job_location': clean_string(job.get('jobLocation', {}).get('label', '')),
            'job_department': clean_string(f"{job.get('classification', {}).get('description', '')}-{job.get('subClassification', {}).get('description', '')}"),
            'job_url': f"https://id.jobstreet.com/job/{job.get('id', '')}",
            'first_seen': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            'base_salary': clean_string(job.get('salary', 'N/A')),
            'job_type': clean_string(job.get('workType', 'N/A')),
            'job_level': 'N/A',
            'job_apply_end_date': clean_string(job.get('listingDate', 'N/A')),
            'last_seen': '',
            'is_active': 'True',
            'company': clean_string(job.get('companyName', '')),
            'company_url': '',
            'job_board': 'Jobstreet',
            'job_board_url': 'https://id.jobstreet.com/',
            'job_description': clean_string(job.get('teaser', '')),
            'advertiser_id': clean_string(job.get('advertiser', {}).get('id', '')),
            'job_id': clean_string(job.get('id', '')),
            'list_date': clean_string(job.get('listingDateDisplay', '')),
            'work_arrangements': clean_string(', '.join([arr.get('label', '') for arr in job.get('workArrangements', {}).get('data', [])])),
            'is_premium': job.get('isPremium', False),
            'is_stand_out': job.get('isStandOut', False),
        }
