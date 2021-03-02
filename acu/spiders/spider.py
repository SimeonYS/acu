import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import AcuItem
from itemloaders.processors import TakeFirst
pattern = r'(\xa0)?'

class AcuSpider(scrapy.Spider):
	name = 'acu'
	start_urls = ['https://www.acu.cw/news/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="post_info_left"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):

		date = response.xpath('//span[@class="date"]//text()').get()
		date = re.findall(r'\s\d+\s\w+',date)
		title = response.xpath('//h2/text()').get()
		content = response.xpath('//div[@class="post_text"]//text()[not (ancestor::h2) and not (ancestor::div[@class="post_description"])]').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))


		item = ItemLoader(item=AcuItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		return item.load_item()
