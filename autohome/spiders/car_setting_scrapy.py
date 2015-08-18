#coding: utf-8

from scrapy import Spider
from scrapy import Request
from scrapy import log
from scrapy import Selector
from scrapy import signals
from autohome.xpaths import xpath_sentence
import re
from autohome.items import *

import sys

reload(sys)
sys.setdefaultencoding("utf-8")

class AatoHome(Spider):
    """
    从http://www.autohome.com.cn/上抓取信息
    """
    name = 'auto'
    start_urls = ['http://www.autohome.com.cn/a00/']
    use_phantomjs = True
    writeInFile = "E:/DLdata/auto.txt"
    download_delay = 10

    def __init__(self):
        self.xpathSen = xpath_sentence()  #取含有xpath语句的字典

    def set_crawler(self,crawler):
        super(AatoHome, self).set_crawler(crawler)
        self.bind_signal()


    def bind_signal(self):
        self.crawler.signals.connect(self.open_file, \
            signal=signals.spider_opened)  #爬虫开启时，打开文件
        self.crawler.signals.connect(self.close_file, \
            signal=signals.spider_closed)  #爬虫关闭时，关闭文件

    def open_file(self):
        self.file_handler = open(self.writeInFile, "a")

    def close_file(self):
        self.file_handler.close()

    def parse(self, response):
        """
        提取不级别(如微型车)的车的url
        """
        sel = Selector(text=response.body.decode("utf-8"))
        urls_caricon = sel.xpath(self.xpathSen["urls_caricon"]).extract()
        name_caricon = sel.xpath(self.xpathSen["name_caricon"]).extract()
        urls_caricon_suv = sel.xpath(self.xpathSen["urls_caricon_suv"]).extract()
        name_caricon_suv = sel.xpath(self.xpathSen["name_caricon_suv"]).extract()
        urls = urls_caricon + urls_caricon_suv
        urls = ['http://www.autohome.com.cn'+url for url in urls]
        name = name_caricon + name_caricon_suv
        its = zip(urls, name)   #its == items
        for it in its[0:1]:
            yield Request(it[0], dont_filter=True,\
                callback=self.extract_id,meta={"name":it[1]})

    def extract_id(self, response):
        """
        提取不同车的id
        """
        sel = Selector(text=response.body.decode("utf-8"))
        auto_ids = sel.xpath(self.xpathSen['auto_ids']).extract()   #汽车的id是唯一的
        conf_url = 'http://car.autohome.com.cn/config/series/%s.html'
        for auto_id in auto_ids[0:10]:
            url = conf_url %str(auto_id[1:])
            yield Request(url, callback=self.detail,\
             dont_filter=True,meta=response.meta)

    def detail(self, response):
        """
        extract detail info
        """
        sel = Selector(text=response.body)
        
        condition = sel.xpath(self.xpathSen["brand"]).extract()
        if len(condition) != 0:
            xpath_keys = ["type_auto","brand","level","BSX",
                 "CSJG","ZWGS","PL","RLXS","QDFS"]
            xpath_conf = ["DDTC","DDTJZY","ESP","GPS","DSXH",
                 "DCLD","DGLFXP"]
            keys_info = []
            for xpath_str in xpath_keys:
                tmp = sel.xpath(self.xpathSen[xpath_str]).extract()
                try:
                    keys_info.append(tmp[0])
                except Exception, e:
                    keys_info.append("")
                    log.msg("error info=%s keys_info=%s" %(e, "\001".join(keys_info)), level=log.ERROR)
            
            conf_info = []
            for xpath_s in xpath_conf:
                tmp = sel.xpath(self.xpathSen[xpath_s]).extract()
                try:
                    conf_info.append(tmp[0])
                except Exception, e:
                    conf_info.append("")
                    log.msg("error info=%s conf_info=%s"%(e, \
                        "\001".join(conf_info)), level=log.ERROR)
            
            XQDD = self.if_not(sel, 'XQDD', ur"氙气")
            conf_info.append(XQDD)
            ZPZY = self.if_not(sel, "ZPZY", ur"真皮")
            conf_info.append(ZPZY)
            QZDKT = self.if_not(sel, "QZDKT", "自动")
            conf_info.append(QZDKT)

            keys_info.append(",".join(conf_info))

            item = AutohomeItem()
            item['content'] = "\001".join(keys_info)+"\n"
            yield item
        else:
            pass 


    def if_not(self, sel, xpath_s, grep_str):
        """
        sel = sel.xpath(text=response)
        xpath_s = 'XQDD' or "ZPZY" or "QZDKT"
        grep_str = "氙气" or '真皮' or '自动'
        """
        #处理是否有氙气大灯，真皮坐椅，全自动空调
        try:
            result = sel.xpath(self.xpathSen[xpath_s]).extract()[0]
        except:
            result = " "
        pat = grep_str
        if len(re.findall(pat, result)) != 0:
            return "●"
        else:
            return "-"


