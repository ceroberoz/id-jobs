# -*- coding: utf-8 -*-
import scrapy
import json
from datetime import datetime


class DeallsSpiderJson(scrapy.Spider):
    name = 'dealls'
    base_url = 'https://api.sejutacita.id/v1/explore-job/job?page=1&limit=18&published=true&status=active&prioritizeNonFilledApplicantQuota=true&sortBy=asc&sortParam=mostRelevant&includeNegotiableSalary=true&salaryMax=0'

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

        # Parse JSON
        try:
            data = json.loads(response.text)
            jobs = data['data']['docs']

            for selector in jobs:
                # Sanitise string from selector['name'] to remove "," in results
                original_job_title = selector['role']
                self.sanitize_job_title = original_job_title.replace(", ", " - ")

                # Sanitize string from selector['categorySlug'] to remove "-" to " " and make the first letter as uppercase in result
                original_job_department = selector['categorySlug']
                if original_job_department is not None:
                    self.sanitize_job_department = original_job_department.replace("-", " ").title()
                else:
                    self.sanitize_job_department = 'N/A'

                #  Sanitize salaryRange if None return N/A
                if selector['salaryRange'] is None:
                    self.sanitize_job_salary = 'N/A'
                else:
                    self.sanitize_job_salary = selector['salaryRange']['start']

                # Sanitize job location if None return N/A
                if 'city' in selector and selector['city'] is not None:
                    self.sanitize_job_location = selector['city']['name']
                else:
                    # If city is not present, return Remote
                    self.sanitize_job_location = 'Remote'

                # Yield job
                yield {
                    'job_title': self.sanitize_job_title,
                    'job_location': self.sanitize_job_location, # location of job,
                    'job_department': self.sanitize_job_department, # department of job
                    'job_url': f"https://dealls.com/role/{selector['slug']}",
                    'first_seen': self.timestamp, # timestamp job added

                    # Add job metadata
                    'base_salary': self.sanitize_job_salary, # salary of job
                    'job_type': selector['employmentTypes'], # type of job, full-time, part-time, intern, remote
                    'job_level': 'N/A', # level of job, entry, mid, senior
                    'job_apply_end_date': '', # end date of job
                    'last_seen': selector['latestUpdatedAt'], # timestamp job last seen
                    'is_active': 'True', # job is still active, True or False

                    # Add company metadata
                    'company': selector['company']['name'], # company name
                    'company_url': 'N/A', #company url

                    # Add job board metadata
                    'job_board': 'Dealls', # name of job board
                    'job_board_url': 'https://dealls.com/' # url of job board

                }

            # Get max pages count
            max_pages = data['data']['totalPages']

            # Go to next page and stop if page value is equal to max_pages
            if data['data']['page'] == max_pages:
                return

            next_page = data['data']['page'] + 1    # Get next max_pages
            next_page_url = f"https://api.sejutacita.id/v1/explore-job/job?page={next_page}&limit=18&published=true&status=active&prioritizeNonFilledApplicantQuota=true&sortBy=asc&sortParam=mostRelevant&includeNegotiableSalary=true&salaryMax=0"
            yield scrapy.Request(next_page_url)

        except json.JSONDecodeError as e:
            # Handle JSON decoding errors
            self.logger.error(f"Error decoding JSON: {e}")
            self.logger.debug(f"Response content: {response.text}")
