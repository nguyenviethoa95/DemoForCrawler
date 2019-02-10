__author__ = 'IMMOWELTAG\vnguyen'

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy_spiders.items import ScrapperItem
from scrapy.crawler import CrawlerProcess


class URL_Spider(CrawlSpider):
    # the name of the spider
    name ='urlspider'
    # the domain that are allowed
    allowed_domains=["gelsenkirchen.de"]
    # the url to start with
    start_url = ["www.gelsenkirchen.de/de/rathaus/informationen/amtsblatt/index.aspx"]
    # this spider has one rule: extract all (unique and cannonicalized ) links, follow them and follow them and parse them using the parse_items method
    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True
            ),
            follow=True,
            callback="parse_items"
        )
    ]

    def parse_items(self,response):
    # the list of items that are found on the particular page
        items=[]
    #only extract cannocalized and unique links (with respect to the current page)
        links = LinkExtractor(canonicalize= True, unique= True).extract_links(response)
    # Now go through all the found links
        for link in links:
            # check whether the domain of the url of the link is allowed
            is_allowed =False
            for allowed_domain in self.allowed_domains:
                if allowed_domain in link.url:
                    is_allowed = True

            #if it is allowed, create a new item and add it to the list of found items
            if is_allowed:
                item= ScrapperItem()
                item['url_from']=response.url
                item['url_to']=link.url
                items.append(item)
        yield items

if __name__=="__main__":
    process =CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0',
        'FEED_URI':'output_csv'
    })
    process.crawl(URL_Spider)
    process.start()

