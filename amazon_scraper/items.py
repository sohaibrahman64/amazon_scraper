# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    ratings = scrapy.Field()
    ratings_count = scrapy.Field()
    brand = scrapy.Field()
    model_name = scrapy.Field()
    os = scrapy.Field()
    size = scrapy.Field()
    cellular_technology = scrapy.Field()
    price = scrapy.Field()
    mrp = scrapy.Field()
    image = scrapy.Field()
    pass
