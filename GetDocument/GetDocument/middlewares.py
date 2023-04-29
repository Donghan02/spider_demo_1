# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from fake_useragent import UserAgent
import requests
import json
import random


class GetDocumentSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class AddUserAgent:

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # 实例化一个对象
        ua = UserAgent()
        # 生成一个user_agent
        user_agent = ua.chrome
        # 添加user_agent
        request.headers['User-Agent'] = user_agent
        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class AddProxy:

    def __init__(self):
        self.ip_list = []

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        while len(self.ip_list) <= 3:
            ip = self.get_ip()
            if ip is not None:
                self.ip_list.append(ip)
        ip = random.choice(self.ip_list)
        request.meta["proxy"] = ip
        print(f"本次使用的IP为{ip}")
        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

    def get_ip(self):
        res = requests.get(
            F"http://get.9vps.com/getip.asp?username=13247646722&apikey=c2abf188&pwd=ae3b78b517636c5d80fa80c2ad5dfbc0&geshi=2&fenge=1&fengefu=&Contenttype=2&getnum=1&setcity=&operate=all",
            timeout=5).text.replace("}{", "},{")
        res = json.loads(res)
        if res['code'] == 0 and res['success'] is True:
            return "https://" + str(res['data'][0]['ip']) + ":" + str(res['data'][0]['port'])
        else:
            return None
