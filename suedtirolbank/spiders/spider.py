import scrapy

from scrapy.loader import ItemLoader
from ..items import SuedtirolbankItem
from itemloaders.processors import TakeFirst


class SuedtirolbankSpider(scrapy.Spider):
	name = 'suedtirolbank'
	start_urls = ['https://www.suedtirolbank.eu/it/la-banca/media-e-comunicazioni']

	def parse(self, response):
		page_links = response.xpath('//div[@class="pageNav"]/a/@href').getall()
		for link in page_links:
			yield response.follow(link, self.parse_page)

	def parse_page(self, response):
		post_links = response.xpath('//div[@class="newstext"]')
		for post in post_links:
			yield self.parse_post(response, post)

	def parse_post(self, response, post):
		title = post.xpath('./h3/text()').get()
		description = post.xpath('.//p//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = post.xpath('./span[@class="newsdate"]/text()').get()

		item = ItemLoader(item=SuedtirolbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
