import scrapy
from eliseSpider.items import ElisespiderItem


class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["book.douban.com"]
    start_urls = ["https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4"]

    def parse(self, response):
        print("===============================================================")
        item = ElisespiderItem()
        book_list = response.xpath('//ul[@class="subject-list"]')
        for book in book_list:
            item['book_icon_img'] = book.xpath('/li/div/a/img//@src').extract_first()
            item['detail_link'] = book.xpath('/li/div[@class="info"]/a//@href').extract_first()
            item['name'] = book.xpath('/li/div[@class="info"]/h2/a//@title').extract_first()
            pub = book.xpath('/li/div[@class="info"]/div[@class="pub"]').extract_first().split('/')

            item['auther'] = pub[0]
            item['publishingHouse'] = pub[1]
            item['publishedDate'] = pub[2]
            item['price'] = pub[3]

            item['ratingNums'] = book.xpath('/li/div[@class="info"]/div/span[@class="rating_nums"]').extract_first()
            item['ratingPersonNub'] = book.xpath('/li/div[@class="info"]/div/span[@class="pl"]').extract_first()
            print(item)

            yield item