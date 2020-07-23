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

    # start_urls = ['https://www.sciencedirect.com/journal/journal-of-alloys-and-compounds/vol/827/suppl/C']

    def parse(self, response):
        items = ScienceItem()
        all_article_list = response.css('dt')[1:]
        for paper in all_article_list:
            article_name = paper.css('span.js-article-title::text').extract()[0]
            article_link = paper.css('h3 a::attr(href)').extract()[0]
            items['article_name'] = article_name
            items['article_link'] = 'https://www.sciencedirect.com' + article_link
            yield items
        # check for next page
        next_page = response.xpath('/html/head/link[1]/@rel').extract()
        if next_page and next_page[0] == 'next':
            print("im am in next page")
            next_page_url = response.xpath('/html/head/link[1]/@href').extract()[0]
            yield scrapy.Request(url=next_page_url, callback=self.parse)
