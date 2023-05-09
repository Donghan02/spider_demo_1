# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import os


class GetdocumentPipeline:
    def __init__(self):
        self.mark = None
        self.data = None
        self.cnt = None
        self.file_size = None

    def open_spider(self, spider):
        # 创建存放数据的文件夹
        dir_path = r".\data"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # 初始化各参数
        self.data = {'data': []}
        self.mark = 0
        self.file_size = 50

    def close_spider(self, spider):
        # 在关闭时对已获取的数据进行保存
        with open(f'.\\data\\{self.mark}.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.data['data'], ensure_ascii=False))
        print(1)

    def process_item(self, item, spider):
        for i in item['data']:
            self.data['data'].append(i)
            # 如果数据数量大于file_size则存储为json文件
            if len(self.data['data']) >= self.file_size:
                # 存储
                with open(f'.\\data\\{self.mark}.json', 'w', encoding='utf-8') as f:
                    f.write(json.dumps(self.data['data'], ensure_ascii=False))
                # 存储完后对个参数进行处理
                self.data = {'data': []}
                self.mark += 1
        return item
