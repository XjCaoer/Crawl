"""
 @Description:
 @Author: XjCao
 @Date 2020/9/24 16:51
"""
from scrapy.spiders import XMLFeedSpider
from HelloScrapy.items import TutorialItem

class MySpider(XMLFeedSpider):
	name = 'geek-docs'
	allowed_domains = ['sina.com.cn']
	# 设置要分析的 XML 文件地址
	start_urls = ['http://blog.sina.com.cn/rss/1615888477.xml']
	iterator = 'iternodes'  # This is actually unnecessary, since it's the default value
	# 此时将开始迭代的节点设置为第一个节点 rss
	itertag = 'rss'  # change it accordingly
	
	def parse_node(self, response, selector):
		i = TutorialItem()
		i['title'] = selector.xpath("/rss/channel/item/title/text()").extract()
		i['link'] = selector.xpath("/rss/channel/item/link/text()").extract()
		i['author'] = selector.xpath("/rss/channel/item/author/text()").extract()
		# 通过 for 循环以遍历出提取出来的存在在 item 中的信息并输出
		for j in range(len(i['title'])):
			print("第 %s 篇文章" % str(j + 1))
			print("标题是：%s" % i['title'][j])
			print("对应链接是：%s" % i['link'][j])
			print("对应作者是：%s" % i['author'][j])
			print("-" * 20)
		return i