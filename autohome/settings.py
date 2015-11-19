# -*- coding: utf-8 -*-

# Scrapy settings for autohome project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'autohome'

SPIDER_MODULES = ['autohome.spiders']
NEWSPIDER_MODULE = 'autohome.spiders'

DEFAULT_ITEM_CLASS = 'autohome.items.AutohomeItem'
ITEM_PIPELINES=['autohome.pipelines.AutohomePipeline']

DOWNLOAD_HANDLERS = {
    'http': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
    'https': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
    'phantomjs-http': 'autohome.downloader.handlers.phantomjs.PhantomJSDownloadHandler',
    'phantomjs-https': 'autohome.downloader.handlers.phantomjs.PhantomJSDownloadHandler'
}

SPIDER_MIDDLEWARES = {
    'autohome.middlewares.PhantomJSMiddleware': 10
}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'autohome (+http://www.yourdomain.com)'
