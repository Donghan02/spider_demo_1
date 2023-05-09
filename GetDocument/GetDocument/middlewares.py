from scrapy import signals
from itemadapter import is_item, ItemAdapter
from fake_useragent import UserAgent
import random
import time



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
        # 从ua池中随机抽取一个ua
        ua = random.choice(spider.ua_pool)

        # 添加user_agent
        request.headers['User-Agent'] = ua
        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class AddProxy:

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # 随机抽取一个代理
        p = random.choice(spider.proxy_pool)
        request.meta["proxy"] = p['proxy']
        try:
            for i in range(len(spider.proxy_pool)):
                if p == spider.proxy_pool[i]:
                    if spider.proxy_pool[i]['time'] <= 1:
                        spider.proxy_pool[i]['time'] += 1
                    else:
                        spider.remove_unavailable_proxies(p)
                        spider.get_proxy_pool(spider.proxy_num)
                    break
        except Exception:
            try:
                for i in range(len(spider.proxy_pool)):
                    if p == spider.proxy_pool[i]:
                        if spider.proxy_pool[i]['time'] <= 1:
                            spider.proxy_pool[i]['time'] += 1
                        else:
                            spider.remove_unavailable_proxies(p)
                            spider.get_proxy_pool(spider.proxy_num)
                        break
            except:
                pass
        # print(f"本次使用的代理为{proxy}")

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)



