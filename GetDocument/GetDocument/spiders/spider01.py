import scrapy
import json
from fake_useragent import UserAgent
from ..get_X_AUTHORIZE_KEY import getWW, getV, getTime, getX_AUTHORIZE_KEY


class Spider01Spider(scrapy.Spider):
    name = "spider01"
    allowed_domains = ["chachawenshu.com"]
    start_urls = ["http://www.chachawenshu.com/api/v1/wenshu/list"]

    def start_requests(self):
        # 请求数据
        data = {
            "urlpath": "/wenshu/list",
            "keyword": "中共",
            "page": str(1),
            "pageSize": str(20),
            "t": str(1),
            "key": "qwemnbuy6ejfods8",
            "type": "token",
            "ww": getWW(),
            "v": getV(),
            "time": getTime(),
        }
        # # 实例化一个对象
        # ua = UserAgent()
        # # 生成一个user_agent
        # user_agent = ua.chrome
        # 设置请求头
        headers = {
            "Host": "www.chachawenshu.com",
            "X-AUTHORIZE-KEY": getX_AUTHORIZE_KEY(data["ww"], data["v"]),
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded",
            "Proxy-Connection": "keep-alive",
            "Origin": "http://www.chachawenshu.com",
        }
        # 发送post请求
        yield scrapy.FormRequest(
            url=self.start_urls[0],
            formdata=data,
            headers=headers,
            callback=self.parse
        )

    def parse(self, response):
        json_response = json.loads(response.text)
        try:
            # print(json_response)
            data = json_response['data']
            group_items = json_response['groupItems']
            item = {'data': data, 'group_items': group_items}
            print(json_response)
            yield item
        except:
            print(json_response)
