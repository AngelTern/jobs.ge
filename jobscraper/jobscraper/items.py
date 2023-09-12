# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_title = scrapy.Field()
    company_link = scrapy.Field()
    company_name = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    pass
