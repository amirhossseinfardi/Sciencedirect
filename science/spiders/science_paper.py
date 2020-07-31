import glob
import scrapy
import json
from crossref.restful import Works
from ..items import ScienceItem
from scidownl.scihub import *
import os
import shutil
from functools import reduce
import operator

counting = 0


# get dictionary tag value with list
def getFromDict(dataDict, mapList):
    return reduce(operator.getitem, mapList, dataDict)


# get country tag address in json
def find_in_obj(obj, condition, tagpath=None):
    if tagpath is None:
        tagpath = []
    # In case this is a list
    if isinstance(obj, list):
        for index, value in enumerate(obj):
            new_path = list(tagpath)
            new_path.append(index)
            for result in find_in_obj(value, condition, tagpath=new_path):
                yield result
    # In case this is a dictionary
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_path = list(tagpath)
            new_path.append(key)
            for result in find_in_obj(value, condition, tagpath=new_path):
                yield result

            if condition == value:
                new_path = list(tagpath)
                new_path.append(key)
                yield new_path


class QuoteSpider(scrapy.Spider):
    name = 'Papersciencedirect'
    try:
        with open('volume.json', 'r') as db_file:
            data = json.load(db_file)
        # start_urls = [parameter['article_link'] for parameter in data]
        start_urls = []
        for parameter in data:
            # print('******************')
            start_urls.append(parameter['article_link'])
            # print(type(start_urls))

        # start_urls = [
        #     'https://www.sciencedirect.com/science/article/abs/pii/S1270963815001583'
        # ]`
    except:
        print("no article list")

    def parse(self, response):
        items = ScienceItem()
        global counting
        counting = counting + 1
        download_article = False
        # article index
        items['article_index'] = str(counting)

        # journal name
        journal_name = response.css('.publication-title-link::text').extract()[0]
        items['journal_name'] = journal_name

        # article date include year and month
        article_date = response.css('#publication .text-xs::text').extract()[0]
        article_date_temp1 = article_date.split(',')[-2]
        article_date_temp = article_date_temp1.split(' ')
        items['article_date_year'] = article_date_temp[-1]
        items['article_date_month'] = article_date_temp[-2]

        # article volume
        article_volume = response.css('#publication .text-xs a::text').extract()[0]
        items['article_volume'] = article_volume

        # article name
        article_name_temp = response.css('.title-text::text').extract()[0]
        article_name = article_name_temp.translate({ord(c): "" for c in "*:/<>?\\|"})
        items['article_name'] = article_name

        # article abstract
        article_abstract_part = response.css('.author p::text').extract()
        article_abstract = ' '.join([str(elem) for elem in article_abstract_part])
        items['article_abstract'] = article_abstract

        # article doi
        article_doi = response.css('.doi::text').extract()[0]
        items['article_doi'] = article_doi

        # article keyword
        article_keyword = response.css('.keyword span::text').extract()
        items['article_keyword'] = article_keyword

        # article authors
        try:
            works = Works()
            artdoi = article_doi
            article_author_temp = works.doi(artdoi)
            article_authors = [article_author_temp['author'][x]['given'] + " " + article_author_temp['author'][x]['family']
                               for x in range(len(article_author_temp['author']))]
            items['article_authors'] = article_authors
        except:
            pass
        # article country
        try:
            raw_html_json = response.xpath("//script[@type='application/json']/text()").extract()[0]
            article_json = json.loads(raw_html_json)
            article_country = []
            for item in find_in_obj(article_json, 'country'):
                country_temp = item
                country_temp[-1] = '_'
                article_country.append(getFromDict(article_json, country_temp))
            items['article_country'] = article_country
            article_organization = []
            for item in find_in_obj(article_json, 'organization'):
                organization_temp = item
                organization_temp[-1] = '_'
                article_organization.append(getFromDict(article_json, organization_temp))
            items['article_organization'] = article_organization
        except:
            pass
        # download article
        if download_article:
            try:
                file_temp_address = 'paper_download'
                sci = SciHub(article_doi, file_temp_address).download(choose_scihub_url_index=3)
                arr = os.listdir(file_temp_address)
                # os.chdir('..')
                # os.chdir('..')
                current_dir = os.getcwd().replace('\\', '/')
                oldfile = current_dir + '/' + file_temp_address + '/' + arr[0]
                newfile = current_dir + '/' + file_temp_address + '/' + str(counting) + '-' + article_name + '.pdf'
                os.rename(oldfile, newfile)
                #
                path = journal_name + '/' + article_date_temp[-1] + '/' + article_volume
                #
                if not os.path.exists(path):
                    os.makedirs(path)
                    print("Directory ", path, " Created ")
                else:
                    print("Directory ", path, " already exists")
                files = os.listdir(file_temp_address)
                for f in files:
                    shutil.move(file_temp_address + '/' + f, path)
            except:
                print('paper no available')
                items['download_fail'] = 'not downloaded'

        # yielding items
        yield items
