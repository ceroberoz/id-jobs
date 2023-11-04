# -*- coding: utf-8 -*-
import scrapy
import json
from datetime import datetime


class GotoSpiderJson(scrapy.Spider):
    name = 'goto-json'
    base_url = 'https://api.tokopedia.com/ent-hris/career/job?company=HoldCo&search=&location=&department='

    # Get timestamp in human readable format
    now = datetime.now()
    timestamp = now.strftime("%d/%m/%Y %H:%M:%S")

    # override ROBOTSTXT_OBEY = False
    custom_settings = {
        'ROBOTSTXT_OBEY': False   
    }

    def start_requests(self):
        headers = {
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            # 'Accept-Language': 'en-US,en;q=0.9',
            # 'Cache-Control': 'max-age=0',
            # 'Connection': 'keep-alive',
            # 'Sec-Fetch-Dest': 'document',
            # 'Sec-Fetch-Mode': 'navigate',
            # 'Sec-Fetch-Site': 'cross-site',
            # 'Sec-Fetch-User': '?1',
            # 'Upgrade-Insecure-Requests': '1',
            # 'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            # 'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            # 'sec-ch-ua-mobile': '?0',
            # 'sec-ch-ua-platform': '"Chrome OS"'
            'Content-Type': 'application/json'
        }

        # GET request, remove Playwright as it cause breaking in JSON parsing
        yield scrapy.Request(self.base_url, headers=headers)

    def parse(self, response):
        # Parse JSON response
        data = json.loads(response.text)

        try:
            ## Data source
            jobs_data = data['data']['items']

            # for selector in jobs:
            for selector in jobs_data:

                yield {
                    'job_title': selector['job_list']['text'],
                    # 'job_location': self.sanitize_job_location,
                    # 'job_department': selector['job_list']['categories']
                    # 'job_url': selector['url'],
                    # 'first_seen': self.timestamp, # timestamp job added

                    # # Add job metadata
                    # 'base_salary': '', # salary of job
                    # 'job_type': self.sanitize_job_type, # type of job, full-time, part-time, intern, remote
                    # 'job_level': selector['position_level'], # level of job, entry, mid, senior
                    # 'job_apply_end_date': selector['closing_date'], # end date of job
                    # 'last_seen': '', # timestamp job last seen
                    # 'is_active': 'True', # job is still active, True or False

                    # # Add company metadata
                    # 'company': 'Evermos', # company name
                    # 'company_url': 'https://evermos.com/', #company url

                    # # Add job board metadata
                    # 'job_board': 'N/A', # name of job board
                    # 'job_board_url': 'N/A' # url of job board
                }

        except json.JSONDecodeError as e:
            # Handle JSON decoding errors
            self.logger.error(f"Error decoding JSON: {e}")
            self.logger.debug(f"Response content: {response.text}")

        # # Go to next page, if applicable
        # next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        # if next_page_url is not None:
        #     yield scrapy.Request(response.urljoin(next_page_url))
