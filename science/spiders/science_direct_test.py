import scrapy
import json
import re
from ..items import ScienceItem


class QuoteSpider(scrapy.Spider):
    name = 'sciencedirect'
    try:
        with open("volume_list.json", "r") as f:
            urls_data = json.load(f)
        start_urls = []
        for volume_url in urls_data:
            start_urls.append(volume_url['volume_list'])
    except:
        print('no volume list')

    def parse(self, response):
        items = ScienceItem()
        all_article_list = response.css('dt')[1:]
        for paper in all_article_list:
            article_name = paper.css('span.js-article-title::text').extract()[0]
            article_link = paper.css('h3 a::attr(href)').extract()[0]
            items['article_name'] = article_name
            items['article_link'] = 'https://www.sciencedirect.com' + article_link
            yield items
        # yield {
        #         'key': keyword_test
        # }
