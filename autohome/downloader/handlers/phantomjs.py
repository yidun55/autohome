from scrapy.http import Headers, HtmlResponse
from scrapy.utils.decorator import inthread
from selenium import webdriver
import time

class PhantomJSDownloadHandler(object):
    def __init__(self, settings):
        pass

    @inthread
    def download_request(self, request, spider):
        # args = ['--ignore-ssl-errors=true', '--load-images=false']
        # Remove 'phantomjs-' prefix
        url = request.url[10:]
        # driver = webdriver.PhantomJS(service_args=args,
        #     executable_path=\
        #     'E:/learn/software/phantomjs-2.0.0-windows/bin/phantomjs',
        #     port=65000)
        # driver = webdriver.PhantomJS(executable_path=\
        #     'E:/learn/software/phantomjs-2.0.0-windows/bin/phantomjs')  #windows
        driver = webdriver.PhantomJS(executable_path=\
            'phantomjs')   #centos
        # driver = webdriver.Chrome(executable_path="C:/Users/LENOVO/Desktop/to/chromedriver.exe")

        # time.sleep(20)  #dyh did it
        driver.get(url)
        # body = driver.find_element_by_xpath('//*').get_attribute("outerHTML") #dyh did it
        body = driver.find_element_by_xpath('//body').get_attribute("innerHTML")
        driver.quit()

        # Set header so httpcache chooses the appropriate Response class
        headers = Headers({'Content-Type': 'text/html'})
        body = body.encode('utf-8')

        return HtmlResponse(url=url, headers=headers, body=body)
