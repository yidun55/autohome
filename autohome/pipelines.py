# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs

class AutohomePipeline(object):
    def process_item(self, item, spider):
        #writeInFile = "E:/DLdata/judicial_url.txt"
        writeInFile = "/home/dyh/data/auto/announcement/announce.txt"
        with codecs.open(writeInFile, "a", "utf-8-sig") as f:
            f.write(item["content"], )

        spider.file_handler.write(item["content"])
