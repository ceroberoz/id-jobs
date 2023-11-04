import scrapy
import json
from datetime import datetime

class BlibliSpiderJson(scrapy.Spider):
    name = 'blibli-json'
    base_url = 'https://careers.blibli.com/ext/api/job/list.json?format=COMPLETE&groupBy=true'

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
            jobs = data['responseObject']

            for selector in jobs:

                for job in selector['jobs']:

                    # Create URL with format https://careers.blibli.com/job-detail/junior-engineer-officer?job=f1f4505d-27ef-469e-a9d5-de6d6e199aee
                    url_path_job_title = job['title'].lower().replace(' ', '-')
                    url_path_job_id = job['id']

                    # Merge url_path_job_title and url_path_job_id to url format https://careers.blibli.com/job-detail/{url_path_job_title}?job={url_path_job_id}
                    url = f"https://careers.blibli.com/job-detail/{url_path_job_title}?job={url_path_job_id}"

                    # Check if job['employmentType'] is exists
                    employment_type = job['employmentType'].replace("Ph-", "").replace("-", " ").capitalize() if 'employmentType' in job else 'N/A'

                    # Check if job['experience'] is exists
                    experience = job['experience'] if 'experience' in job else 'N/A'

                    # Check if job['location'] is exists
                    location = job['location'] if 'location' in job else 'N/A'

                    yield {
                        'job_title': job['title'],
                        'job_location': location,
                        'job_department': job['departmentName'],
                        'job_url': url ,
                        'first_seen': self.timestamp, # timestamp job added

                        # Add job metadata
                        'base_salary': 'N/A', # salary of job
                        'job_type': employment_type, # type of job, full-time, part-time, intern, remote
                        'job_level': experience, # level of job, entry, mid, senior
                        'job_apply_end_date': 'N/A', # end date of job
                        'last_seen': '', # timestamp job last seen
                        'is_active': 'True', # job is still active, True or False

                        # Add company metadata
                        'company': 'Blibli', # company name
                        'company_url': 'https://careers.blibli.com/', #company url

                        # Add job board metadata
                        'job_board': 'N/A', # name of job board
                        'job_board_url': 'N/A' # url of job board
                    }

        except json.JSONDecodeError as e:
            # Handle JSON decoding errors
            self.logger.error(f"Error decoding JSON: {e}")
            self.logger.debug(f"Response content: {response.text}")