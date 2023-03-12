"""
 @Description:
 @Author: XjCao
 @Date 2020/9/24 17:12
"""
from scrapy.spiders import CSVFeedSpider
from HelloScrapy.items import TutorialItem

class MySpider(CSVFeedSpider):
	name = 'geek-docs1'
	allowed_domains = ['iqianyue.com']
	# 设置要分析的 XML 文件地址
	start_urls = ['http://yum.iqianyue.com/weisuenbook/pyspd/part12/mydata.csv']
	delimiter = ','
	headers = ['name', 'sex', 'addr', 'email']
	
	def parse_row(self, response, row):
		item = TutorialItem()
		item['name'] = row['name']
		item['sex'] = row['sex']
		item['addr'] = row['addr']
		item['email'] = row['email']
		print("姓名是:{}".format(item['name']))
		print("性别是:{}".format(item['sex']))
		print("地址是:{}".format(item['addr']))
		print("邮件是:{}".format(item['email']))
		return item