# -*- coding: utf-8 -*-
import scrapy


class Zhihu1Spider(scrapy.Spider):
    name = 'zhihu1'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/topics']

    def parse(self, response):
        pass
