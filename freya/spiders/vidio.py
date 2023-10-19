# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime


class VidioSpiderXPath(scrapy.Spider):
    name = 'vidio-xpath'
    base_url = 'https://careers.vidio.com'

    # Get timestamp in human readable format
    now = datetime.now()
    timestamp = now.strftime("%d/%m/%Y %H:%M:%S")

    def start_requests(self):
        # GET request
        yield scrapy.Request(self.base_url+"/careers", meta={"playwright": True})

    def parse(self, response):
        for selector in response.xpath('//div[contains(@class, "b-job")]/a'):
            yield {
                'job_title': selector.css('.b-job__name::text').get(),
                'job_location': selector.css('.b-job__location::text').get(),
                'job_department': selector.css('.b-job__department::text').get(),
                'job_url': self.base_url+selector.css('a::attr(href)').get(),
                'first_seen': self.timestamp # timestamp job added

                # Add job metadata
                # 'base_salary': # salary of job
                # 'job_type': # type of job, full-time, part-time, intern, remote
                # 'job_level': # level of job, entry, mid, senior
                # 'job_apply_end_date': # end date of job
                # 'last_seen': # timestamp job last seen
                # 'is_active': # job is still active, True or False

                # Add company metadata
                # 'company': # company name
                # 'company_url': # company url

                # Add job board metadata
                # 'job_board': # name of job board
                # 'job_board_url': # url of job board

            }

        # Go to next page, if applicable
        # next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        # if next_page_url is not None:
        #     yield scrapy.Request(response.urljoin(next_page_url))
