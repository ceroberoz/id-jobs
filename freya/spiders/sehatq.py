import scrapy
from datetime import datetime

class SehatqSpiderXPath(scrapy.Spider):
    name = 'sehatq-xpath'
    start_urls = ['https://www.sehatq.com/karir']

    # Get timestamp in human readable format
    now = datetime.now()
    timestamp = now.strftime("%d/%m/%Y %H:%M:%S")

    def parse(self, response):
        # Create counter for xpath levels and element indexes
        xpath_level = 5
        element_index = 6

        # Iterate over xpath levels
        for i in range(1, xpath_level):
            # Iterate over element indexes
            # Construct relative xpath job positions
            original = '//*[@id="__next"]/div[1]/div/div/div[1]/div[1]/div[1]'

            # xpath_selector_element = f'//*[@id="__next"]/div[1]/div/div/div[1]/div[{i}]/div[1]'

            job_position = f'{original}+//text()'
            yield {
                'job_position': response.xpath(job_position).get()   
            }

            # # if job_position not empty, continue
            # if job_position:
            #     continue
                    
            # for j in range(1, element_index):
            #     # Construct relative xpath element
            #     xpath_selector_element = f'//*[@id="__next"]/div[1]/div/div/div[1]/div[{i}]/div[{j}]'

            #     # Add for foreach to get all job information
            #     for selector_element in response.xpath(xpath_selector_element):
            #         yield {
            #             'job_title': selector_element.css('h3::text').get(),
            #             # 'job_location': selector_element.css('p::text').get(),

            #             # get job position from previous response
            #             'job_position': job_position

            #         }