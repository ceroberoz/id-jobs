# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime


class SehatqSpiderXPath(scrapy.Spider):
    name = 'sehatq-xpath'
    base_url = 'https://www.sehatq.com/karir'

    # Get timestamp in human readable format
    now = datetime.now()
    timestamp = now.strftime("%d/%m/%Y %H:%M:%S")

    def start_requests(self):
        # GET request
        yield scrapy.Request(
                self.base_url, 
                meta={
                "playwright": True
                }
            )

    def parse(self, response):
        # Create counter for xpath and element selector
        counter_xpath = 1 # max 5
        counter_element = 2 # max 6

        # Create foreach with range(1, 5) for counter_xpath
        for i in range(1, counter_xpath):
            # Create foreach with range(1, 6) for counter_element
            for j in range(1, counter_element):
                # xpath format //*[@id="__next"]/div[1]/div/div/div[1]/div[1]/div[2]
                self.xpath_selector = f'//*[@id="__next"]/div[1]/div/div/div[1]/div[{i}]/div[{j}]' # Autogen xpath selector for jobs

                # write self.xpath_selector to console
                print(self.xpath_selector)

            # # Check if xpath_selector return empty
            # if response.xpath(self.xpath_selector).get() is not None:
            #     self.xpath_selector

            #     for selector in response.xpath(self.xpath_selector):
            #         yield {
            #             'job_title': selector.css('h3::text').get(),
            #             # 'job_location': selector.css('.b-job__location::text').get(),
            #             # 'job_department': selector.css('.b-job__department::text').get(),
            #             # 'job_url': self.base_url+selector.css('a::attr(href)').get(),
            #             # 'first_seen': self.timestamp, # timestamp job added

            #             # # Add job metadata
            #             # 'base_salary': 'N/A', # salary of job
            #             # 'job_type': 'N/A', # type of job, full-time, part-time, intern, remote
            #             # 'job_level': 'N/A', # level of job, entry, mid, senior
            #             # 'job_apply_end_date': 'N/A', # end date of job
            #             # 'last_seen': '', # timestamp job last seen
            #             # 'is_active': 'True', # job is still active, True or False

            #             # # Add company metadata
            #             # 'company': 'Vidio', # company name
            #             # 'company_url': self.base_url, # company url

            #             # # Add job board metadata
            #             # 'job_board': 'N/A', # name of job board
            #             # 'job_board_url': 'N/A' # url of job board

            #         }

        # Go to next page, if applicable
        # next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        # if next_page_url is not None:
        #     yield scrapy.Request(response.urljoin(next_page_url))
