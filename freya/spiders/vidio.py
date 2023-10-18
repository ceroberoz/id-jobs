import scrapy


class VidioSpider(scrapy.Spider):
    name = "vidio"
    allowed_domains = ["career.video.com"]
    start_urls = ["https://career.video.com/careers"]

    def parse(self, response):
        pass
