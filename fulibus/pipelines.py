# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class FlhzPipeline(object):
    def __init__(self):
        self.file = open("/mnt/hgfs/Ubuntu8Windows/articles.json", "w")
        self.file.write("[")

    def process_item(self, item, spider):
        data = json.dumps(dict(item), ensure_ascii=False)
        self.file.write(data.encode("utf-8")+", ")
        return item

    def close_spider(self, spider):
        self.file.write("]")
        self.file.close()
