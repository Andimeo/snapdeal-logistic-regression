'''
Created on Jul 13, 2015

@author: ylu
'''

from scrapy import Spider, Request
from snapdeal_spider.items import SnapdealQueryResultNumItem

class SnapdealQueryResultNumSpider(Spider):
    name = 'snapdeal_query_result_num_spider'
    allowed_domains = ['snapdeal.com']
    start_url_template = 'http://www.snapdeal.com/acors/json/product/get/search/0/%d/%d?q=&sort=rlvncy&gs=3&keyword=%s&viewType=List&snr=false'
    
    batch_num = 40
    
    def __init__(self, *args, **kwargs): 
        super(SnapdealQueryResultNumSpider, self).__init__(*args, **kwargs) 
        self.start_urls = self.parse_start_urls(kwargs.get('queries')) 
    
    def parse_start_urls(self, fn):
        with open(fn, 'r') as f:
            return [self.start_url_template % (0, self.batch_num, x.strip().split(' ', 1)[1].strip()) for x in f.readlines()]
            
        
    def parse(self, response):
        start_pos = int(response.url.split('?')[0].split('/')[-2]) + self.batch_num
        query = response.url.split('&')[-3].split('=', 2)[1]
        total_num = int(response.xpath('//div[2]/text()').extract()[0])
        
        item = SnapdealQueryResultNumItemSpiderItem()
        item['query'] = query
        item['num'] = total_num
        yield item