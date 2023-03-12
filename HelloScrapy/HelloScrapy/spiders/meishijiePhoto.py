"""
 @Description:
 @Author: XjCao
 @Date 2020/9/24 19:40
"""
import scrapy
from HelloScrapy.items import MeishiItem

class MeiSpider(scrapy.Spider):
	name = 'meishijie'
	allowed_domains = ['meishij.net']
	start_urls = ['https://www.meishij.net/china-food/caixi/chuancai/']
	
	def parse(self, response):
		src_list = response.xpath('//div[@class="listtyle1"]/a/img/@src').extract()
		for src in src_list:
			item = MeishiItem()
			item['src'] = [src]
			yield item