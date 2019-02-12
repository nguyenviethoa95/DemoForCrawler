__author__ = 'IMMOWELTAG\vnguyen'

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy_spiders.items import ScrapperItem
from scrapy.crawler import CrawlerProcess
import requests
from scrapy.http import Request
import os

class URL_Spider(CrawlSpider):
    # the name of the spider
    name ='urlspider'


    # the domain that are allowed
    allowed_domains=["landkreishildesheim.de"]
    # the url to start with
    start_urls = [u"https://www.landkreishildesheim.de/Politik-Verwaltung/Verwaltung/Amtsblätter"]
    # this spider has one rule: extract all (unique and cannonicalized ) links, follow them and follow them and parse them using the parse_items method
    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True,
                allow_domains=('landkreishildesheim.de'),
                tags=('a'),
                attrs=('href'),
                deny_extensions=('jpg','png')
            ),
            follow=False,
            callback="parse_media_content"
        )
    ]

    def parse_media_content (self,response):
        link = response.url
        item = ScrapperItem()
        item['url_from']= link
        try:
            res =requests.get(link)
            if res.headers['Content-Type']=='application/pdf':
                item = ScrapperItem()
                item['url_from']= link
                item['url_to']='pdf found'
                save_pdf(link)
        except requests.RequestException  as a :
            print (a)

def save_pdf(url):
        #name for the file
        print(url)
        name = url.split('/')[-1]
        print(name)
        path = str(os.getcwd())+'/temp/'+name+'.pdf'
        print(path)
        with open( path,'wb') as file:
            r = requests.get(url)
            file.write(r.content)
            print(r.headers)

if __name__=="__main__":
    process =CrawlerProcess({
        'USER_AGENT': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0",
        'FEED_URI':'output_csv'
    })
    process.crawl(URL_Spider)
    process.start()

