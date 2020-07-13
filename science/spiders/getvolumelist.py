# -*- coding: utf-8 -*-
import scrapy
from ..items import ScienceItem
import requests
import json


class GetvolumelistSpider(scrapy.Spider):
    name = 'getvolumelist'

    url = 'https://www.sciencedirect.com/journal/progress-in-aerospace-sciences/issues'
    start_urls = []
    issbn = '03760421'
    start_year = 1997
    last_year = 2020
    for year in range(start_year, last_year+1, 1):
        start_urls.append('https://www.sciencedirect.com/journal/' + issbn + '/year/' + str(year) + '/issues')

    def parse(self, response):
        items = ScienceItem()
        article_url = 'https://www.sciencedirect.com/journal/progress-in-aerospace-sciences'
        json_data = json.loads(response.body_as_unicode())
        for X in reversed(range(len(json_data['data']))):
            volume_url = article_url + json_data['data'][X]['uriLookup']
            items['volume_list'] = volume_url
            yield items
