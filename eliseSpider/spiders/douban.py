import scrapy
from eliseSpider.items import ElisespiderItem


class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["book.douban.com"]
    start_urls = ["https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start=200&type=T"]

    # base_url = 'https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start='
    # page = 1

    def parse(self, response):
        print("===============================================================")
        # print(response.text)
        # print("===============================================================")
        item = ElisespiderItem()
        book_list = response.xpath('/html/body/div/div/div/div/div/ul[@class="subject-list"]/li')
        for book in book_list:
            book_icon_img = book.xpath('./div/a/img//@src').extract_first()
            detail_link = book.xpath('./div[@class="info"]/h2/a//@href').extract_first()
            name = book.xpath('./div[@class="info"]/h2/a//@title').extract_first()
            pub = book.xpath('./div[@class="info"]/div[@class="pub"]/text()').extract_first()
            ratingNum = book.xpath('./div[@class="info"]/div/span[@class="rating_nums"]/text()').extract_first()
            ratingPersonNum = book.xpath('./div[@class="info"]/div/span[@class="pl"]/text()').extract_first()
            tag = '小说'

            item['book_icon_img'] = book_icon_img if len(book_icon_img) == 0 or book_icon_img == None else book_icon_img.strip()
            item['detail_link'] = detail_link if len(detail_link) == 0 or detail_link == None else detail_link.strip()
            item['name'] = name if len(name) == 0 or name == None else name.strip()
            item['pub'] = pub if len(pub) == 0 or pub == None else pub.strip()
            item['ratingNum'] = ratingNum if len(ratingNum) == 0 or ratingNum == None else ratingNum.strip()
            item['ratingPersonNum'] = ratingPersonNum if len(ratingPersonNum) == 0 or ratingPersonNum == None else ratingPersonNum.strip()
            item['tag'] = tag
            #print(item)

            yield item

        # maxPage = int(response.xpath('/html/body/div/div/div/div/div/div[@class="paginator"]/a/text()')[-1].extract().strip())
        # if self.page < maxPage:
        #     self.page = self.page + 1
        #     url = self.base_url + str(self.page*20) + '&type=T'
        #     yield scrapy.Request(url = url, callback=self.parse)

