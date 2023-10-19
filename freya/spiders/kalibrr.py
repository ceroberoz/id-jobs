# -*- coding: utf-8 -*-
import scrapy
import json
from datetime import datetime


class KalibrrSpiderJson(scrapy.Spider):
    name = 'kalibrr-json'
    base_url = 'https://www.kalibrr.com/kjs/job_board/featured_jobs?limit=1000&offset=1&country=Indonesia'

    # Get timestamp in human readable format
    now = datetime.now()
    timestamp = now.strftime("%d/%m/%Y %H:%M:%S")

    def start_requests(self):
        # GET request
        yield scrapy.Request(self.base_url, meta={"playwright": True})

    def parse(self, response):
        selector = json.loads(response.body_as_unicode())
        for selector in response.xpath('//div[contains(@class, "b-job")]/a'):
            yield {
                'job_title': selector.css('.b-job__name::text').get(),
                'job_location': selector.css('.b-job__location::text').get(),
                'job_department': selector.css('.b-job__department::text').get(),
                'job_url': self.base_url+selector.css('a::attr(href)').get(),
                'first_seen': self.timestamp, # timestamp job added

                # Add job metadata
                'base_salary': 'N/A', # salary of job
                'job_type': 'N/A', # type of job, full-time, part-time, intern, remote
                'job_level': 'N/A', # level of job, entry, mid, senior
                'job_apply_end_date': 'N/A', # end date of job
                'last_seen': '', # timestamp job last seen
                'is_active': 'True', # job is still active, True or False

                # Add company metadata
                'company': 'Vidio', # company name
                'company_url': self.base_url, # company url

                # Add job board metadata
                'job_board': 'N/A', # name of job board
                'job_board_url': 'N/A' # url of job board

            }

        # Go to next page, if applicable
        # next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        # if next_page_url is not None:
        #     yield scrapy.Request(response.urljoin(next_page_url))
