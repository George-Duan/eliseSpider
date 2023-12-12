import scrapy
from eliseSpider.items import ElisespiderItem


class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["book.douban.com"]
    start_urls = ["https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4"]

    def parse(self, response):
        print("===============================================================")
        # print(response.text)
        # print("===============================================================")
        item = ElisespiderItem()
        book_list = response.xpath('//ul[@class="subject-list"]/li')
        for book in book_list:
            item['book_icon_img'] = book.xpath('./div/a/img//@src').extract_first().strip()
            item['detail_link'] = book.xpath('./div[@class="info"]/h2/a//@href').extract_first().strip()
            item['name'] = book.xpath('./div[@class="info"]/h2/a//@title').extract_first().strip()
            item['pub'] = book.xpath('./div[@class="info"]/div[@class="pub"]/text()').extract_first().strip()

            item['ratingNum'] = (book.xpath('./div[@class="info"]/div/span[@class="rating_nums"]/text()').extract_first().strip())
            item['ratingPersonNum'] = (book.xpath('./div[@class="info"]/div/span[@class="pl"]/text()').extract_first().strip())

            item['tag'] = '小说'
            #print(item)

            yield item