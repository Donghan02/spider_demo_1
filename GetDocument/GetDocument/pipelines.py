# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json


class GetdocumentPipeline:
    def __init__(self):
        self.cnt = None

    def open_spider(self, spider):
        # self.file = open('items.json', 'w')
        self.cnt = 0

    def close_spider(self, spider):
        # self.file.close()
        pass

    def process_item(self, item, spider):
        with open(f'{self.cnt}.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(item, ensure_ascii=False))
        self.cnt += 1
        return item
