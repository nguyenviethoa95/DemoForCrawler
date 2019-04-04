from selenium import webdriver
import boto3
import requests
import config
import scrapy

# scrape object implementation
class ScrapperItem(scrapy.Item):
    # the source URL
    url_from = scrapy.Field()

    # the destination url
    url_to= scrapy.Field()

