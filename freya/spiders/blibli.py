import scrapy
from datetime import datetime

class BlibliSpiderJson(scrapy.Spider):
    name = 'blibli-json'
    start_urls = ['https://careers.blibli.com/ext/api/job/list']

    # Get timestamp in human readable format
    now = datetime.now()
    timestamp = now.strftime("%d/%m/%Y %H:%M:%S")

    def start_requests(self):
        headers = {
            'Content-Type': 'application/json'
        }

        # GET request, remove Playwright as it cause breaking in JSON parsing
        yield scrapy.Request(self.base_url, headers=headers)

    def parse(self, response):
        try:
            data = json.loads(response.text)
            jobs = data['jobs']

            for selector in jobs:
                # sanitise string from selector['name'] to remove "," in results
                original_job_title = selector['name']
                self.sanitize_job_title = original_job_title.replace(", ", " - ")

                yield {
                    'job_title': self.sanitize_job_title,
                    'job_location': selector['google_location']['address_components']['city'],
                    'job_department': 'N/A',
                    'job_url': f"https://www.kalibrr.com/c/{selector['company_info']['code']}/jobs/{selector['id']}",
                    'first_seen': self.timestamp, # timestamp job added

                    # Add job metadata
                    'base_salary': selector['base_salary'], # salary of job
                    'job_type': selector['tenure'], # type of job, full-time, part-time, intern, remote
                    'job_level': 'N/A', # level of job, entry, mid, senior
                    'job_apply_end_date': selector['application_end_date'], # end date of job
                    'last_seen': '', # timestamp job last seen
                    'is_active': 'True', # job is still active, True or False

                    # Add company metadata
                    'company': selector['company_info']['company_name'], # company name
                    'company_url': f"https://www.kalibrr.com/id-ID/c/{selector['company_info']['code']}/jobs", #company url

                    # Add job board metadata
                    'job_board': 'Kalibrr', # name of job board
                    'job_board_url': 'https://www.kalibrr.com/id-ID/home' # url of job board
                }

        except json.JSONDecodeError as e:
            # Handle JSON decoding errors
            self.logger.error(f"Error decoding JSON: {e}")
            self.logger.debug(f"Response content: {response.text}")