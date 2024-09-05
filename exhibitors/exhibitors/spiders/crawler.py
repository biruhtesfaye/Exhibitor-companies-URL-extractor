from typing import Iterable
from urllib.parse import urljoin
import scrapy


class CrawlerSpider(scrapy.Spider):
    name = "crawler"
    allowed_domains = ["lasvegasaug.fashionresource.com"]

    def start_requests(self):
        url = "https://lasvegasaug.fashionresource.com/newfront/marketplace/exhibitors?pageNumber=1"
        yield scrapy.Request(url, callback=self.parse, meta={"playwright": True})

    def parse(self, response):
        with open("exhibitors.html", "w") as f:
            f.write(response.text)
            
        list_links = response.xpath('(//div[contains(@class, "MuiGrid-item")]//a[contains(@class, "MuiTypography-root")])[position()>1]/@href').getall()
        for link in list_links:
            yield {scrapy.Request(urljoin("https://lasvegasaug.fashionresource.com", link), callback=self.parse_detail)}

    def parse_detail(self, response):
        yield {
            "name": response.xpath('//h2/text()').get(),
            "website": response.xpath('//h6/text()').get(),
        }