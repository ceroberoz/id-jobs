import scrapy
import json

class EvermosJsonSpider(scrapy.Spider):
    name = 'evermos-json'
    start_urls = ['https://evermos-talent.freshteam.com/hire/widgets/jobs.json']

    # override ROBOTSTXT_OBEY = False
    custom_settings = {
        'ROBOTSTXT_OBEY': False   
    }

    def parse(self, response):
        try:
            data = json.loads(response.text)
            # Process the JSON data as needed
            yield data
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding JSON: {e}")