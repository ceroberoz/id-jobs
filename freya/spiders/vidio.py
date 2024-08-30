import scrapy
import logging
from datetime import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class VidioSpiderXPath(scrapy.Spider):
    name = 'vidio'
    BASE_URL = 'https://careers.vidio.com'
    CAREERS_URL = f"{BASE_URL}/careers"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def start_requests(self):
        yield scrapy.Request(self.CAREERS_URL, meta={"playwright": True}, callback=self.parse)

    def parse(self, response):
        try:
            for selector in response.xpath('//div[contains(@class, "b-job")]/a'):
                yield self.parse_job(selector)

            self.handle_pagination(response)
        except Exception as e:
            logger.error(f"Error parsing page: {e}")

    def parse_job(self, selector) -> Dict[str, Any]:
        return {
            'job_title': self.sanitize_string(selector.css('.b-job__name::text').get()),
            'job_location': self.sanitize_string(selector.css('.b-job__location::text').get()),
            'job_department': self.sanitize_string(selector.css('.b-job__department::text').get()),
            'job_url': self.get_job_url(selector),
            'first_seen': self.timestamp,
            'base_salary': 'N/A',
            'job_type': 'N/A',
            'job_level': 'N/A',
            'job_apply_end_date': 'N/A',
            'last_seen': '',
            'is_active': 'True',
            'company': 'Vidio',
            'company_url': self.BASE_URL,
            'job_board': 'Vidio',
            'job_board_url': self.CAREERS_URL,
            # 'job_id': self.get_job_id(selector),
            # 'number_of_openings': self.get_number_of_openings(selector),
        }

    def get_job_url(self, selector) -> str:
        return self.BASE_URL + selector.css('a::attr(href)').get()

    @staticmethod
    def sanitize_string(s: Optional[str]) -> str:
        return s.strip() if s else 'N/A'

    def handle_pagination(self, response):
        next_page_url = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)

    # Reserved for future use
    # def get_job_id(self, selector) -> str:
    #     return selector.attrib.get('id', '').replace('career_', '')

    # def get_number_of_openings(self, selector) -> str:
    #     openings_text = selector.css('.b-job__openings::text').get()
    #     if openings_text:
    #         return openings_text.split()[0]
    #     return 'N/A'