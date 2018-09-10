# -*- coding: utf-8 -*-
import scrapy
import re
import json


class Zhihu1Spider(scrapy.Spider):
    name = 'zhihu1'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/topics']

    def parse(self, response):
        """
        解析话题广场,获取每个话题的url
        :param response:
        :return:
        """
        self.base_url = "https://www.zhihu.com"
        topic_id_list = response.xpath('//li[@class="zm-topic-cat-item"]/@data-id').extract()
        for topic_id in topic_id_list:
            formdata = {
                "method": "next",
                'params': '{"topic_id":%s,"offset":0,"hash_id":""}' % topic_id
            }
            yield scrapy.FormRequest(
                url="https://www.zhihu.com/node/TopicsPlazzaListV2",
                formdata=formdata,
                callback=self.parse_topic_all
            )
            # TODO 所有的topic获取

    def parse_topic_all(self, response):
        """
        解析话题,获取话题url
        :param response:
        :return:
        """
        data_list = json.loads(response.text)['msg']
        for data in data_list:
            topic_url = re.findall(r'<a target="_blank" href="(.*?)"', data)[0]
            topic_name = re.findall(r'<strong>(.*?)</strong>', data)[0]

            yield scrapy.Request(
                url=self.base_url + topic_url,
                callback=self.parse_topic_list,
                meta={
                    "topic_name": topic_name
                }
            )

    def parse_topic_list(self, response):
        """
        解析所有问答的 回答者,进入回答者的主页
        :param response:
        :return:
        """
        author_info_url_list = response.xpath('//a[@class="UserLink-link"]/@href').extract()
        for author_info_url in author_info_url_list:
            yield scrapy.Request(
                url="https:" + author_info_url + "/activities",
                callback=self.parse_user_detail_info
            )
        # TODO 获取所有页问答的作者

    def parse_user_detail_info(self, response):
        """
        解析个人主页
        :param response:
        :return:
        """
        print(response.xpath('//div[@id="data"]/@data-state').extract_first())
        answers_list = response.xpath('//h2[@class="ContentItem-title"]//a/@href').extract()
        for answers in answers_list:
            yield scrapy.Request(
                url=self.base_url + answers,
                callback=self.parse_answer_info
            )

    def parse_answer_info(self, response):
        """
        解析回答的文章的 标签
        获得每个人关注的问题-
        :param response:
        :return:
        """
        tag_list = response.xpath('//div[@class="QuestionHeader-topics"]//div[@class="Popover"]/div/text()').extract()
        # print(tag_list)

