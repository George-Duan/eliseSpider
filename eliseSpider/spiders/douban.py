import scrapy
from eliseSpider.items import ElisespiderItem


class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["book.douban.com"]
    start_urls = ["https://www.douban.com/tag/%E5%B0%8F%E8%AF%B4/book?start=0"]

    def parse(self, response):
        print("===============================================================")
        item = ElisespiderItem()
        book_list = response.xpath('//ul[@class="subject-list"]')
        for book in book_list:
            item['book_icon_img'] = book.xpath('/li/div/a/img//@src').text()
            item['detail_link'] = book.xpath('/dt/a//@href').text()
