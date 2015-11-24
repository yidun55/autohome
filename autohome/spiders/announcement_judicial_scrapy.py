#!usr/bin/env python
#coding: utf-8

from scrapy import Spider
from scrapy import log
from scrapy import Request, FormRequest
from scrapy import Selector
from scrapy import signals
from scrapy.utils.request import request_fingerprint
from autohome.items import *
import re
import redis

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class JudicialOpinions(Spider):
    """
    从http://rmfygg.court.gov.cn/psca/lgnot/bulletin/page/0_10.html
    上抓取法院公告数据并写入到文件中
    """
    name = 'announcement'
    download_delay = 3
    use_phantomjs = True
    start_urls = ['http://www.baidu.com']
    myRedis = redis.StrictRedis(host='localhost',port=6379) #connected to redis
    model_urls = "http://rmfygg.court.gov.cn/psca/lgnot/bulletin/page/0_%s.html"
    writeInFile = "/home/dyh/data/auto/announcement/announce.txt"
    # writeInFile = "E:/DLdata/judicial_url.txt"
    haveRequested = "/home/dyh/data/auto/announcement/haveRequestedUrl.txt"
    # haveRequested = "E:/DLdata/haveRequestedUrl.txt"

    def set_crawler(self,crawler):
        super(JudicialOpinions, self).set_crawler(crawler)
        self.bind_signal()


    def bind_signal(self):
        self.crawler.signals.connect(self.open_file, \
            signal=signals.spider_opened)  #爬虫开启时，打开文件
        self.crawler.signals.connect(self.close_file, \
            signal=signals.spider_closed)  #爬虫关闭时，关闭文件

    def open_file(self):
        self.file_handler = open(self.writeInFile, "a")  #写内容
        self.file_haveRequested = open(self.haveRequested, "a+")  #写入已请求成功的url
        self.url_have_seen = "dup_ann"
        for line in self.file_haveRequested:
            fp = self.url_fingerprint(line)
            self.myRedis.sadd(self.url_have_seen,fp)

    def url_fingerprint(self, url):
        req = Request(url.strip())
        fp = request_fingerprint(req)
        return fp 

    def close_file(self):
        self.file_handler.close()

    def parse(self, response):
        """
        从零开始到3055页，^*^偷懒
        """
        pages = 3056
        # print response.body
        for i in xrange(3056):
            url = self.model_urls %str(i)
            yield Request(url, callback=self.urls,\
                dont_filter=True, meta={"not_phantomjs":'yes'})

    def urls(self, response):
        """
        提取页面的url
        """
        sel = Selector(text=response.body)
        blocks = sel.xpath("//div[@class='contentDiv']//table//\
            tr[position()>1]")
        # print blocks.extract()
        items = {}
        for bloc in blocks:
            tag = True
            fragment = ""
            key = ""
            for small in bloc.xpath("./td")[0:4]:
                fragment = fragment + "\001" + small.xpath("string(.)").extract()[0]
                if tag == True:
                    key = small.xpath("./a/@href").extract()[0]
                    tag = False
            items[key] = fragment
        try:
            for url, fragment in items.iteritems():
                url = "http://rmfygg.court.gov.cn" + url
                # print url, "url$$$$$$$$$$$$$$$$$$$$$$$$$$$"
                # yield Request(url, callback=self.detail,\
                #         dont_filter=True, meta={"values":fragment})
                fp = self.url_fingerprint(url)
                isexist = self.myRedis.sadd(self.url_have_seen,fp)
                if isexist:
                    #如果redis set ppai_dup_redis没有则插入并返回1，否则
                    #返回0
                    yield Request(url, callback=self.detail,\
                        dont_filter=True, meta={"values":fragment})
                else:
                    pass
        except Exception,e:
            log.msg("urls error_info=%s"%e)

    def detail(self, response):
        """
        提取页面信息
        """
        item = AutohomeItem()
        self.file_haveRequested.write(response.url+"\n")
        sel = Selector(text=response.body)
        # print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>",sel.xpath("string(//div[@id='ggnr'])").extract()
        con_body = sel.xpath("string(//div[@id='ggnr']//\
            div[@class='d22 pt10'])").extract()
        con_foot = sel.xpath("string(//div[@id='ggnr']//\
            div[@class='d23 fr '])").extract()
        try:
            con_b = self.clean(con_body)
            con_f = self.clean(con_foot)
            # print con_b, con_f, "*********************"
            item["content"] = response.meta["values"] +"\001"+response.url+\
              "\001" + con_b + "\001" + con_f + "\n"
        except Exception, e:
            log.msg("detail error_info=%s"%e, level=log.ERROR)
        yield item

    def clean(self, input_list):
        """
        去除"\n\t\r"符号
        """
        assert isinstance(input_list, list), "input_list must be list"
        # print input_list, "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        return "".join([i.strip() for i in "\n".join(input_list).split("\n")])  #去除"\n"

