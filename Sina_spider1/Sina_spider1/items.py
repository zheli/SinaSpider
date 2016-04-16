# encoding=utf-8

from scrapy import Item, Field


class FansItem(Item):
    """ 粉丝列表 """
    _id = Field()  # 用户ID
    name = Field() # 用户名称
    fans = Field() # 粉丝
