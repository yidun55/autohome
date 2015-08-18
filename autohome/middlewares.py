from scrapy.http import Request

class PhantomJSMiddleware(object):

    def _rewrite_url(self, r):
        if isinstance(r, Request):
            url = 'phantomjs-' + r.url
            r = r.replace(url=url)
        return r

    def process_start_requests(self, start_requests, spider):
        if not hasattr(spider, 'use_phantomjs') or not spider.use_phantomjs:
            return start_requests

        return (self._rewrite_url(r) for r in start_requests or ())

    def process_spider_output(self, response, result, spider):
        if not hasattr(spider, 'use_phantomjs') or not spider.use_phantomjs:
            return result

        return (self._rewrite_url(r) for r in result or ())
