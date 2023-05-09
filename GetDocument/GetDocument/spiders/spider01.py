import os
import time
import urllib
import scrapy
import json
import requests as req
from fake_useragent import UserAgent
from ..get_X_AUTHORIZE_KEY import getWW, getV, getTime, getX_AUTHORIZE_KEY
from datetime import datetime, timedelta


class Spider01Spider(scrapy.Spider):
    name = "spider01"
    allowed_domains = ["chachawenshu.com"]
    start_urls = ["http://www.chachawenshu.com/api/v1/wenshu/list"]
    custom_settings = {
        'DOWNLOAD_DELAY': 1,  # 延时最低为2s
        'AUTOTHROTTLE_ENABLED': True,  # 启动[自动限速]
        'AUTOTHROTTLE_DEBUG': True,  # 开启[自动限速]的debug
        'AUTOTHROTTLE_MAX_DELAY': 10,  # 设置最大下载延时
        'DOWNLOAD_TIMEOUT': 10,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 10  # 限制对该网站的并发请求数
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 代理池
        self.proxy_pool = []
        # user_agent池
        self.ua_pool = []
        # 请求参数列表
        self.params_list = []
        # ua池大小
        self.ua_num = 150
        # 代理池大小
        self.proxy_num = 10

    def start_requests(self):
        # 获取请求参数列表
        self.get_params()

        # 建立一个代理池
        self.get_proxy_pool(self.proxy_num)

        # 建立一个ua池
        self.get_ua_pool(self.ua_num)

        # 基于参数列表请求api
        for t in self.params_list:
            # 构造请求数据
            data = {
                "urlpath": "/wenshu/list",
                "courtName": t[0],
                "judgeDateBegin": t[1],
                "judgeDateEnd": t[2],
                "keyword": "",
                "page": str(1),
                "pageSize": str(20),
                "t": str(1),
                "key": "qwemnbuy6ejfods8",
                "type": "token",
                "ww": getWW(),
                "v": getV(),
                "time": getTime(),
            }

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
        try:
            # 判断是否成功请求
            if response.status == 200:
                # 请求返回的数据
                json_response = json.loads(response.text)

                # 本次请求使用部分可变参数
                params_ = urllib.parse.parse_qs(urllib.parse.unquote(response.request.body))
                court_name = params_['courtName'][0]
                begin_date = params_['judgeDateBegin'][0]
                end_date = params_['judgeDateEnd'][0]
                page = params_['page']

                # 状态码
                status = json_response['code']

                # 针对状态码做下一步处理
                if status == 200:
                    # 正常访问
                    # 判断data是否为空，为空则对请求参数进行记录
                    if len(json_response['data']) == 0:
                        # 判断是否存在日志文件夹
                        if not os.path.exists('.\\log'):
                            os.makedirs('.\\log')
                        with open('.\\log\\empty_log.txt', 'a+', encoding='utf-8') as f:
                            f.write('[\'' + court_name + '\', \'' + begin_date + '\', \'' + end_date + '\']' + '\n')
                    else:
                        # 获取总数量
                        total_num = json_response['totalNum']
                        # 如果小于显示限制，则进一步处理，否则记录下请求参数，作进一步处理
                        if total_num <= 50:
                            if page == 1:
                                # 如果本次请求是第一页，则考虑是否需要请求剩余页数
                                # 判断是否需要进一步请求, 如若页数大于1则需要请求
                                if total_num > 10:
                                    # 总页数
                                    pages_num = total_num / 10 + 1
                                    # 请求剩余页数
                                    for p in range(2, pages_num + 1):
                                        # 构造请求数据
                                        data = {
                                            "urlpath": "/wenshu/list",
                                            "courtName": court_name,
                                            "judgeDateBegin": begin_date,
                                            "judgeDateEnd": end_date,
                                            "keyword": "",
                                            "page": p,
                                            "pageSize": str(20),
                                            "t": str(1),
                                            "key": "qwemnbuy6ejfods8",
                                            "type": "token",
                                            "ww": getWW(),
                                            "v": getV(),
                                            "time": getTime(),
                                        }

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
                                else:
                                    pass
                            else:
                                pass
                            # 对获取的数据进行提取并传入管道进行处理
                            data = json_response['data']
                            item = {'data': data}
                            yield item
                        else:
                            if begin_date != end_date:
                                date_range = self.get_date_range(begin_date, end_date)
                                for date in date_range:
                                    # 重新请求
                                    # 构造请求数据
                                    data = {
                                        "urlpath": "/wenshu/list",
                                        "courtName": court_name,
                                        "judgeDateBegin": date,
                                        "judgeDateEnd": date,
                                        "keyword": "",
                                        "page": page,
                                        "pageSize": str(20),
                                        "t": str(1),
                                        "key": "qwemnbuy6ejfods8",
                                        "type": "token",
                                        "ww": getWW(),
                                        "v": getV(),
                                        "time": getTime(),
                                    }

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
                            else:
                                # 以天为单位请求数量还超过50，对该请求参数进行记录
                                # 判断是否存在日志文件夹
                                if not os.path.exists('.\\log'):
                                    os.makedirs('.\\log')
                                with open('.\\log\\out_of_show_log.txt', 'a+', encoding='utf-8') as f:
                                    f.write('[\'' + court_name + '\', \'' + begin_date + '\', \'' + end_date + '\']' + '\n')
                else:
                    # 本次请求使用的ua
                    ua = str(response.request.headers['User-Agent'])[2:]
                    # 删除本次使用的ua
                    self.remove_unavailable_ua(ua)

                    # 本次请求使用的代理
                    proxy = response.meta['proxy']
                    # 删除本次使用的代理
                    self.remove_unavailable_proxies(proxy)

                    # 更新代理池
                    self.get_proxy_pool(self.proxy_num)

                    # 更新ua池
                    self.get_ua_pool(self.ua_num)

                    # 重新请求
                    # 构造请求数据
                    data = {
                        "urlpath": "/wenshu/list",
                        "courtName": court_name,
                        "judgeDateBegin": begin_date,
                        "judgeDateEnd": end_date,
                        "keyword": "",
                        "page": page,
                        "pageSize": str(20),
                        "t": str(1),
                        "key": "qwemnbuy6ejfods8",
                        "type": "token",
                        "ww": getWW(),
                        "v": getV(),
                        "time": getTime(),
                    }

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
            else:
                # 请求失败，进行相应的处理

                # 本次请求使用的ua
                ua = str(response.request.headers['User-Agent'])[2:]
                # 删除本次使用的ua
                self.remove_unavailable_ua(ua)

                # 本次请求使用的代理
                proxy = response.meta['proxy']
                # 删除本次使用的代理
                self.remove_unavailable_proxies(proxy)

                # 更新代理池
                self.get_proxy_pool(self.proxy_num)

                # 更新ua池
                self.get_ua_pool(self.ua_num)

                # 重新请求
                request = response.request.copy()
                request.meta['proxy'] = ''
                request.headers['User-Agent'] = ''
                yield request
        except Exception:
            try:
                # 请求失败，进行相应的处理

                # 本次请求使用的ua
                ua = str(response.request.headers['User-Agent'])[2:]
                # 删除本次使用的ua
                self.remove_unavailable_ua(ua)

                # 本次请求使用的代理
                proxy = response.meta['proxy']
                # 删除本次使用的代理
                self.remove_unavailable_proxies(proxy)

                # 更新代理池
                self.get_proxy_pool(self.proxy_num)

                # 更新ua池
                self.get_ua_pool(self.ua_num)

                # 重新请求
                request = response.request.copy()
                request.meta['proxy'] = ''
                request.headers['User-Agent'] = ''
                yield request
            except Exception as e:
                print(f"出现了异常{e}")
                # 判断是否存在日志文件夹
                if not os.path.exists('.\\log'):
                    os.makedirs('.\\log')
                # 对请求参数进行记录
                with open('.\\log\\wrong_log.txt', 'a+', encoding='utf-8') as f:
                    f.write('[\'' + court_name + '\', \'' + begin_date + '\', \'' + end_date + '\']' + '\n')
        time.sleep(1.5)


    def get_proxy_pool(self, proxies_num):
        # 建立一个代理池

        # 判断代理池内的代理数量是否小于需要的代理数量
        if len(self.proxy_pool) < proxies_num:
            # 获取代理
            res = req.get(
                F"http://get.9vps.com/getip.asp?username=13247646722&apikey=c2abf188&pwd=ae3b78b517636c5d80fa80c2ad5dfbc0"
                F"&geshi=2&fenge=1&fengefu=&Contenttype=2&getnum=1&setcity=&operate=all",
                timeout=5).text.replace("}{", "},{")
            res = json.loads(res)

            # 对返回的内容进行判断
            if res['code'] == 0 and res['success'] is True:
                # 拼接代理
                proxy = "http://" + str(res['data'][0]['ip']) + ":" + str(res['data'][0]['port'])

                # 白名单相关操作

                # 定义请求头
                h2 = {
                    "Host": "www.chachawenshu.com",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.0.0"
                }

                # 请求白名单链接
                req.get("http://www.chachawenshu.com/ccws.png", headers=h2, proxies={'http': proxy}, timeout=5)

                p = {
                    'proxy': proxy,
                    'time': 0
                }

                # 判断该代理是否存在于ip池中
                if p not in self.proxy_pool:
                    # 将代理加入代理池
                    self.proxy_pool.append(p)

            # 进行休眠
            time.sleep(1)

    def remove_unavailable_proxies(self, proxy_del):
        # 删除特定代理
        self.proxy_pool = [proxy for proxy in self.proxy_pool if proxy != proxy_del]

    def get_ua_pool(self, ua_num):
        # 判断ua池中的数量是否少于指定数量
        if len(self.ua_pool) < ua_num:
            # 生成一个user_agent
            ua = UserAgent().chrome

            # 将ua加入ua池
            self.ua_pool.append(ua)

    def remove_unavailable_ua(self, ua_del):
        # 删除特定ua
        self.ua_pool = [ua for ua in self.ua_pool if ua != ua_del]

    def get_params(self):
        # 获取请求参数列表
        dir_path = r'./params'
        # 判断是否存在参数文件夹
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print("请导入参数！！！")

        # 扫描参数文件夹并读取参数
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            # 判断是否为文件
            if os.path.isfile(file_path):
                with open(file_path, "r", encoding='utf8') as f:
                    content = f.readlines()
                    # 去除每行的换行符并将其加入至参数列表
                    # cnt = 1
                    for l in content:
                        l.strip('\n')
                        self.params_list.append(eval(l))
                        # if cnt == 20:
                        #     break
                        # cnt += 1

    def get_date_range(self, start_date_str, end_date_str):
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        delta = end_date - start_date

        date_range = []
        for i in range(delta.days + 1):
            date = start_date + timedelta(days=i)
            date_range.append(date.strftime('%Y-%m-%d'))

        return date_range