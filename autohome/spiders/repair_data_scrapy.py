#coding: utf-8

from scrapy import Spider
from scrapy import Request
from scrapy import log
from scrapy import Selector
from scrapy import signals
from autohome.xpaths import *
import re
from autohome.items import *

import sys

reload(sys)
sys.setdefaultencoding("utf-8")

class AatoHome(Spider):
    """
    从http://www.autohome.com.cn/上抓取信息
    """
    name = 'repair'
    start_urls = ['http://www.autohome.com.cn/a00/']
    use_phantomjs = True
    writeInFile = "E:/DLdata/repair_auto.txt"
    download_delay = 3

    def __init__(self):
        self.xpathSen = xpath_repair()  #取含有xpath语句的字典


    def parse(self, response):
        """
        直接post需要请求的id
        """
        f = open("E:/spiders/autohome/id_repair.txt")
        auto_ids = [i.strip()[1:] for i in f]   #汽车的id是唯一的
        conf_url = 'http://car.autohome.com.cn/config/series/%s.html'
        for auto_id in auto_ids:
            url = conf_url %str(auto_id)
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

            keys_info = []
            for xpath_str in xpath_keys:
                tmp = sel.xpath(self.xpathSen[xpath_str]).extract()
                try:
                    keys_info.append(tmp[0])
                except Exception, e:
                    keys_info.append("")
                    log.msg("error info=%s keys_info=%s" %(e, "\001".join(keys_info)), level=log.ERROR)

            item = AutohomeItem()
            item['content'] = "\001".join(keys_info)+"\n"
            yield item
        else:
            pass 

