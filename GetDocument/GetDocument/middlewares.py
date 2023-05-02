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
        print(self.ip_list)
        while len(self.ip_list) <= 0:
            ip = self.get_ip()
            if ip is not None:
                self.ip_list.append(ip)
                # 实例化一个对象
                ua = UserAgent()
                # 生成一个user_agent
                user_agent = ua.chrome

                # 请求nginx相关
                # 创建session对象
                http = requests.Session()
                # 返回结果数组
                rep = []
                h1 = {'Host': 'www.chachawenshu.com',
                     'Connection': 'keep-alive',
                     'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
                     'sec-ch-ua-mobile': '?0',
                     'User-Agent': user_agent,
                     'sec-ch-ua-platform': "Windows",
                     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                     'Sec-Fetch-Site': 'cross-site',
                     'Sec-Fetch-Mode': 'navigate',
                     'Sec-Fetch-Dest': 'document',
                     'Referer': 'https://cn.bing.com/',
                     'Accept-Encoding': 'gzip, deflate, br',
                     'Accept-Language': 'zh-CN,zh;q=0.9'}
                rep.append(http.get(url="https://www.chachawenshu.com/", headers=h1, proxies={'http': ip}))
                h2 = {'Host': 'www.chachawenshu.com',
                     'Connection': 'keep-alive',
                     'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
                     'sec-ch-ua-mobile': '?0',
                     'User-Agent': user_agent,
                     'sec-ch-ua-platform': "Windows",
                     'Accept': 'text/css,*/*;q=0.1',
                     'Sec-Fetch-Site': 'same-origin',
                     'Sec-Fetch-Mode': 'no-cors',
                     'Sec-Fetch-Dest': 'style',
                     'Referer': 'https://www.chachawenshu.com/',
                     'Accept-Encoding': 'gzip, deflate, br',
                     'Accept-Language': 'zh-CN,zh;q=0.9'}
                rep.append(http.get(url="https://www.chachawenshu.com/public/static/css/chunk-common.417b2cca.css", headers=h2, proxies={'http': ip}))
                rep.append(http.get(url="https://www.chachawenshu.com/public/static/css/index.c8e17bdc.css", headers=h2, proxies={'http': ip}))
                h2['Sec-Fetch-Dest'] = 'script'
                h2['Accept'] = '*/*'
                rep.append(http.get(url="https://www.chachawenshu.com/public/static/js/chunk-vendors.b6047c3c.js", headers=h2, proxies={'http': ip}))
                rep.append(http.get(url="https://www.chachawenshu.com/public/static/js/chunk-common.25693a67.js", headers=h2, proxies={'http': ip}))
                rep.append(http.get(url="https://www.chachawenshu.com/public/static/js/index.f27a0dd3.js", headers=h2, proxies={'http': ip}))
                h2['Accept'] = 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'
                h2['Sec-Fetch-Dest'] = 'image'
                h2['Referer'] = 'https://www.chachawenshu.com/public/static/css/index.c8e17bdc.css'
                rep.append(http.get(url="https://www.chachawenshu.com/public/static/img/case_searchbg.67e9e1c0.png", headers=h2, proxies={'http': ip}))
                rep.append(http.get(url="https://www.chachawenshu.com/public/static/img/preloader.3bd417c0.gif", headers=h2, proxies={'http': ip}))
                rep.append(http.get(url="https://www.chachawenshu.com/public/static/img/class-bg2.f8513906.jpg", headers=h2, proxies={'http': ip}))
                rep.append(http.get(url="https://www.chachawenshu.com/public/static/img/class-bg3.5a3ef5d9.jpg", headers=h2, proxies={'http': ip}))
                h2['Referer'] = 'https://www.chachawenshu.com/'
                rep.append(http.get(url="https://www.chachawenshu.com/public/static/img/logo2.10cf5c0e.png", headers=h2, proxies={'http': ip}))
                h2['Sec-Fetch-Dest'] = 'empty'
                h2['Sec-Fetch-Mode'] = 'cors'
                h2['Accept'] = 'application/json, text/plain, */*'
                rep.append(http.get(url="https://www.chachawenshu.com/api/v1/index/list?page=1&pageSize=7", headers=h2, proxies={'http': ip}))
                rep.append(http.get(url="https://www.chachawenshu.com/api/v1/index/citiao-hit?pageSize=5", headers=h2, proxies={'http': ip}))
                h2['Referer'] = 'https://www.chachawenshu.com/public/static/css/index.c8e17bdc.css'
                h2['Sec-Fetch-Dest'] = 'image'
                h2['Sec-Fetch-Mode'] = 'no-cors'
                h2['Accept'] = 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'
                rep.append(http.get(url="https://www.chachawenshu.com/public/static/img/dftt_ztbg.7b3a3c28.png", headers=h2, proxies={'http': ip}))
                rep.append(http.get(url="https://www.chachawenshu.com/favicon.ico", headers=h2, proxies={'http': ip}))
                for x in rep:
                    print(x)
                    print(x.text)
                time.sleep(5)
                print(ip)
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
            return "http://" + str(res['data'][0]['ip']) + ":" + str(res['data'][0]['port'])
        else:
            return None
