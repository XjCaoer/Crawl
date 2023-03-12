import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from HelloScrapy.items import TutorialItem

class MySpider(CrawlSpider):
	name = 'yiibai'
	allowed_domains = ['yiibai.com']
	start_urls = ['https://www.yiibai.com/cplusplus/what-is-cpp.html']
	
	rules = (
		# 提取匹配 'yiibai.com/cplusplus' (但不匹配 'subsection.php') 的链接并跟进链接(没有callback意味着follow默认为True)
		Rule(LinkExtractor(allow=('yiibai.com/cplusplus',), deny=('subsection\.php',))),
		
		# 提取匹配 'item.php' 的链接并使用spider的parse_item方法进行分析
		Rule(LinkExtractor(allow=('item\.php',)), callback='parse_item'),
	)
	
	def parse_item(self, response):
		self.log('Hi, this is an item page! %s' % response.url)
		item = TutorialItem()
		item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
		item['name'] = response.xpath('//td[@id="item_name"]/text()').extract()
		item['description'] = response.xpath('//td[@id="item_description"]/text()').extract()
		return item
