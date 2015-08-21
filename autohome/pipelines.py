# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AutohomePipeline(object):
    def process_item(self, item, spider):
        writeInFile = "E:/DLdata/auto.txt"
        f = open(writeInFile,"a")
        # spider.file_handler.write(item['content'])
        f.write(item['content'])
        f.close()
