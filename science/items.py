# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScienceItem(scrapy.Item):
    # define the fields for your item here like:
    article_name = scrapy.Field()
    article_link = scrapy.Field()
    article_abs = scrapy.Field()
    journal_name = scrapy.Field()
    article_volume = scrapy.Field()
    article_date_year = scrapy.Field()
    article_date_month = scrapy.Field()
    article_abstract = scrapy.Field()
    article_doi = scrapy.Field()
    article_keyword = scrapy.Field()
    article_country = scrapy.Field()
    article_authors = scrapy.Field()
    article_index = scrapy.Field()
    download_fail = scrapy.Field()
    article_organization = scrapy.Field()
    volume_list = scrapy.Field()
    pass
