import scrapy
from urllib.parse import urlencode, urljoin
from amazon_scraper.items import AmazonScraperItem
import random
import re

USER_AGENTS_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
]


class MobilesSpider(scrapy.Spider):
    name = "mobiles"
    # allowed_domains = ["amazon.in"]
    # start_urls = ["https://amazon.in/"]
    queries = ["mobile phones"]
    user_agent_list = USER_AGENTS_LIST

    def start_requests(self):
        for query in self.queries:
            url = 'https://www.amazon.in/s?' + urlencode({'k': query})
            yield scrapy.Request(url, callback=self.parse, dont_filter=True, headers={"User-Agent": self.user_agent_list[random.randint(0, len(self.user_agent_list) - 1)]})

    def parse(self, response):
        products = response.xpath('.//div[@data-asin]')
        print(len(products))
        for product in products:
            product_title_href = product.xpath(
                './/div[@class="a-section a-spacing-none puis-padding-right-small s-title-instructions-style"]/h2/a/@href').get()
            if product_title_href is not None:
                yield scrapy.Request(url=f"https://www.amazon.in{product_title_href}", dont_filter=True, callback=self.parse_items, headers={"User-Agent": self.user_agent_list[random.randint(0, len(self.user_agent_list) - 1)]})

        next_page = response.xpath(
            './/a[@class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]/@href').get()

        if next_page is not None:
            next_page_url = f'https://www.amazon.in{next_page}'
            yield scrapy.Request(next_page_url, dont_filter=True, callback=self.parse, headers={"User-Agent": self.user_agent_list[random.randint(0, len(self.user_agent_list) - 1)]})

    def parse_items(self, response):
        item = AmazonScraperItem()
        item['title'] = response.xpath(
            './/span[@id="productTitle"]/text()').get()
        item['category'] = "Mobile"
        item['ratings'] = response.xpath(
            './/a[@class="a-popover-trigger a-declarative"]/span[@class="a-size-base a-color-base"][1]/text()').get()
        item['ratings_count'] = response.xpath(
            './/span[@id="acrCustomerReviewText"]/text()').get()
        product_specs = response.xpath(
            './/span[@class="a-size-base po-break-word"]').getall()
        print(product_specs)
        print(len(product_specs))

        if len(product_specs) > 0:
            item['brand'] = self.extract_product_specs(product_specs[0])
            item['model_name'] = self.extract_product_specs(product_specs[1])
            item['os'] = self.extract_product_specs(product_specs[3])
            item['cellular_technology'] = self.extract_product_specs(product_specs[4])

        item['price'] = response.xpath(
            './/span[@class="a-price-whole"]/text()').get()
        item['mrp'] = response.xpath(
            './/span[@class="a-price a-text-price"]/span/text()').get()
        item['image'] = response.xpath(
            './/div[@id="main-image-container"]/ul/li/span/span/div[@id="imgTagWrapperId"]/img/@src').get()
        yield item

    def extract_product_specs(self, input_string):
        # Define a regular expression pattern to match text between <span> tags
        pattern = r'<span[^>]*>(.*?)</span>'

        # Use re.search to find the match
        match = re.search(pattern, input_string)

        # Check if a match was found
        if match:
            # Extract the content between <span> tags
            extracted_text = match.group(1)
            return extracted_text
        else:
            return None
