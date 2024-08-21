import scrapy
from datetime import datetime

class SehatqSpiderXPath(scrapy.Spider):
    name = 'sehatq' #xpath
    start_urls = ['https://www.sehatq.com/karir']

    # Get timestamp in human readable format
    now = datetime.now()
    timestamp = now.strftime("%d/%m/%Y %H:%M:%S")

    def parse(self, response):
        # Create counter for xpath levels and element indexes
        xpath_level = 6
        element_index = 7

        # Iterate over xpath levels
        for i in range(1, xpath_level):
            # Iterate over element indexes

            # Construct xpath for Job Position
            xpath_selector_job_position = f'//*[@id="__next"]/div[1]/div/div/div[1]/div[{i}]/div[1]'
            self.job_position = f'{xpath_selector_job_position}//text()'

            for j in range(1, element_index):
                # Construct xpath for Job Location
                xpath_selector_location = f'//*[@id="__next"]/div[1]/div/div/div[1]/div[{i}]/div[{j}]/div[1]/div/span[1]'
                job_location = f'{xpath_selector_location}//text()'

                # Construct xpath for Job Type
                xpath_selector_job_type = f'//*[@id="__next"]/div[1]/div/div/div[1]/div[{i}]/div[{j}]/div[1]/div/span[2]'
                job_type = f'{xpath_selector_job_type}//text()'

                # Construct xpath for Job URL
                # /html/body/div[1]/div[1]/div/div/div[1]/div[4]/div[2]/div[2]/a[1]
                xpath_selector_job_url = f'//*[@id="__next"]/div[1]/div/div/div[1]/div[{i}]/div[{j}]/div[2]/a[1]'
                job_url = f'{xpath_selector_job_url}/@href'

                # Construct relative xpath element
                xpath_selector_element = f'//*[@id="__next"]/div[1]/div/div/div[1]/div[{i}]/div[{j}]'

                # Add for foreach to get all job information
                for selector_element in response.xpath(xpath_selector_element):

                    # Continue only if job_title is not empty
                    job_title = selector_element.css('h3::text').get()
                    if job_title:

                        yield {
                            'job_title': selector_element.css('h3::text').get(),
                            'job_location': selector_element.xpath(job_location).get(),
                            'job_position': selector_element.xpath(self.job_position).get(),
                            'job_url': 'https://www.sehatq.com'+selector_element.xpath(job_url).get(),
                            'first_seen': self.timestamp, # timestamp job added

                            # Add job metadata
                            'base_salary': 'N/A', # salary of job
                            'job_type': selector_element.xpath(job_type).get(), # type of job, full-time, part-time, intern, remote
                            'job_level': 'N/A', # level of job, entry, mid, senior
                            'job_apply_end_date': 'N/A', # end date of job
                            'last_seen': '', # timestamp job last seen
                            'is_active': 'True', # job is still active, True or False

                            # Add company metadata
                            'company': 'SehatQ', # company name
                            'company_url': 'https://www.sehatq.com', # company url

                            # Add job board metadata
                            'job_board': 'N/A', # name of job board
                            'job_board_url': 'N/A' # url of job board

                        }
