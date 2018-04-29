# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from tencent.items import TencentItem


class TencentjobSpider(CrawlSpider):
    """
    腾讯招聘职位信息爬虫
    """
    name = 'tencentJob'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['http://hr.tencent.com/position.php?&start=0']
    # 指定处理的管道
    custom_settings = {
        'ITEM_PIPELINES': {'tencent.pipelines.TencentPipeline': 300},
    }

    # 初始化链接提取匹配'http://hr.tencent.com/position.php?&start=\d+'的链接
    page_lx = LinkExtractor(allow=('start=\d+'))

    # 提取链接，并使用方法进行解析，并跟进
    rules = [
        Rule(page_lx, callback='parse_content', follow=True)
    ]


    # 不能使用parse来作为解析方法，因为crawlspider依靠spider的parse来实现逻辑，覆盖了parse方法crawlspider会运行失败

    def parse_content(self, response):

        for each in response.xpath('//tr[@class="even"]|//tr[@class="odd"]'):
            name = each.xpath('./td[1]/a/text()').extract()[0]
            detail_link = each.xpath('./td[1]/a/@href').extract()[0]
            position_info = each.xpath('./td[2]/text()').extract()[0]
            people_number = each.xpath('./td[3]/text()').extract()[0]
            work_location = each.xpath('./td[4]/text()').extract()[0]
            publish_time = each.xpath('./td[5]/text()').extract()[0]

            item = TencentItem()

            item['name'] = name
            item['detail_link'] = detail_link
            item['position_info'] = position_info
            item['people_number'] = people_number
            item['work_location'] = work_location
            item['publish_time'] = publish_time

            yield item
