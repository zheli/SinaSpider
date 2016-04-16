# -*- coding: utf-8 -*-
import re
import datetime
from scrapy.spider import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from Sina_spider1.items import InformationItem, TweetsItem, FollowsItem, FansItem


class Spider(CrawlSpider):
    name = "sinaSpider"
    host = "http://weibo.cn"
    start_urls = [
        5235640836, 5676304901, 5871897095, 2139359753, 5579672076, 2517436943, 5778999829, 5780802073, 2159807003,
        1756807885, 3378940452, 5762793904, 1885080105, 5778836010, 5722737202, 3105589817, 5882481217, 5831264835,
        2717354573, 3637185102, 1934363217, 5336500817, 1431308884, 5818747476, 5073111647, 5398825573, 2501511785,
    ]
    scrawl_ID = set(start_urls)  # 记录待爬的微博ID

    def start_requests(self):
        while True:
            if len(self.scrawl_ID)==0:
               return
            main_id, weibo_name = self.scrawl_ID.pop()
            main_id = str(main_id)
            fans_item = FansItem()
            fans_item["_id"] = main_id
            fans_item["name"] = weibo_name
            fans_item["fans"] = set()
            url_fans = "http://weibo.cn/%s/fans" % main_id

            yield Request(url=url_fans, meta={"fans_item": fans_item}, callback=self.parse)  # 去爬粉丝

    def parse(self, response):
        """ 抓取关注或粉丝 """
        item = response.meta['fans_item']
        sel = Selector(response)
        rows = sel.xpath(u'//table//tr/td')
        fan_number = len(rows)/2
        for i in xrange(0, fan_number):
            fan_id = re.findall('uid=(\d+)', rows[i*2+1].xpath(u'a/@href').extract()[1])[0]
            fan_url = rows[i*2].xpath(u'a/@href').extract_first()
            fan_name = rows[i*2+1].xpath(u'a/text()').extract_first()
            print(u'Found %s (%s) at %s' % (fan_name, fan_id, fan_url))
            item['fans'].add((fan_id, fan_name, fan_url))

        url_next = sel.xpath(
            u'body//div[@class="pa" and @id="pagelist"]/form/div/a[text()="\u4e0b\u9875"]/@href').extract()
        if url_next:
            yield Request(url=self.host + url_next[0], meta={'fans_item':item}, callback=self.parse)
        yield item
