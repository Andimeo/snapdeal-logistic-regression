'''
Created on Jul 13, 2015

@author: ylu
'''

from scrapy import Spider, Request
from snapdeal_spider.items import SnapdealSpiderItem

class SnapdealSpider(Spider):
    name = 'snapdeal_spider'
    allowed_domains = ['snapdeal.com']
    start_url_template = 'http://www.snapdeal.com/acors/json/product/get/search/0/%d/%d?q=&sort=rlvncy&gs=3&keyword=%s&viewType=List&snr=false'
    
    batch_num = 40
    max_retrieve_num = 40 * 300
    def __init__(self, *args, **kwargs): 
        super(SnapdealSpider, self).__init__(*args, **kwargs) 
        self.start_urls = self.parse_start_urls(kwargs.get('queries')) 
    
    def parse_start_urls(self, fn):
        with open(fn, 'r') as f:
            return [self.start_url_template % (0, self.batch_num, x.strip().split(' ', 1)[1].strip()) for x in f.readlines()]
            
        
    def parse(self, response):
        start_pos = int(response.url.split('?')[0].split('/')[-2]) + self.batch_num
        query = response.url.split('&')[-3].split('=', 2)[1]
        total_num = int(response.xpath('//div[2]/text()').extract()[0])

        l = response.xpath('//div[@class="product_grid_cont hoverProdCont gridLayout3"]')
        
        rows = response.xpath('//div[@class="product_grid_row prodGrid"]')
        start = response.meta.get('rank', 1)
        for row in rows:
            grids = row.xpath('div')
            for grid in grids:
                item = SnapdealSpiderItem()
                item['product_id'] = int(grid.xpath('@id').extract()[0])
                item['query'] = query
                item['rank'] = start
                start += 1
                yield item
        
        if start_pos <= total_num and start_pos < self.max_retrieve_num:
            yield(Request(url = self.start_url_template % (start_pos, self.batch_num, query), callback = self.parse, meta={'rank':start}))
