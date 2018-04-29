from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from tencent.items import SunDongguanItem


class SunDongguanSpider(CrawlSpider):
    """
    东莞阳关热线平台爬虫
    """
    name = 'sundongguan'
    allow_domains = ['wz.sun0769.com']

    # 指定处理的管道
    custom_settings = {
        'ITEM_PIPELINES': {'tencent.pipelines.DongguanPipeline': 300}
    }
    start_urls = ['http://wz.sun0769.com/index.php/question/questionType?type=4&page=']

    page_lx = LinkExtractor(allow=('type=4&page=\d+'))

    rules = [
        Rule(page_lx, callback='dongguan_parse', follow=True),
    ]

    def dongguan_parse(self, response):

        for each in response.xpath('//div[@class="greyframe"]/table[2]//td//tr'):

            id = each.xpath('./td[1]/text()').extract()[0]
            title = each.xpath('./td[2]/a[2]/@title').extract()[0]
            target = each.xpath('./td[2]/a[3]/text()').extract()[0]
            info_link = each.xpath('./td[2]/a[2]/@href').extract()[0]
            state = each.xpath('./td[3]/span/text()').extract()[0]
            person = each.xpath('./td[4]/text()').extract()[0]
            time = each.xpath('./td[5]/text()').extract()[0]

            item = SunDongguanItem()

            item['id'] = id
            item['title'] = title
            item['target'] = target
            item['info_link'] = info_link
            item['state'] = state
            item['person'] = person
            item['time'] = time

            yield item
