# encoding=utf-8
import pymongo
from items import InformationItem, TweetsItem, FollowsItem, FansItem


class MongoDBPipleline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["Sina"]
        self.fan_list = db["fan_list"]

    def process_item(self, item, spider):
        fans = [dict(_id=id, name=name, url=url) for id, name, url in item['fans']]
        self.fan_list.update(
            {'_id': item['_id'], 'name': item['name']},
            {'$addToSet':{'fans':{'$each': fans }}},
            upsert=True)
        return item
