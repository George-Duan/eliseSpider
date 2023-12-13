import scrapy
from eliseSpider.items import ElisespiderItem


class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["book.douban.com"]
    start_urls = ["https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start=200&type=T"]

    base_url = 'https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start='
    page = 1

    ## parse_tag
    def parse(self, response):
        table_list = response.xpath('//table')
        for table in table_list:
            type_name = table.xpath('./preceding-sibling::a/@name').get()
            tag_list = table.xpath('./tbody/tr/td/a')
            for tag in tag_list:
                href = tag.xpath('./@href').get()
                tag_name = tag.xpath('./@href').get()
                url = 'https://book.douban.com' + href
                yield scrapy.Request(url=url, callback=self.parse_page)


    def parse_page(self, response):
        pass

    def parse_detail(self, response):
        print("===============================================================")
        # print(response.text)
        # print("===============================================================")
        item = ElisespiderItem()
        book_list = response.xpath('/html/body/div/div/div/div/div/ul[@class="subject-list"]/li')
        for book in book_list:
            book_icon_img = book.xpath('./div/a/img//@src').get()
            detail_link = book.xpath('./div[@class="info"]/h2/a//@href').get()
            name = book.xpath('./div[@class="info"]/h2/a//@title').get()
            pub = book.xpath('./div[@class="info"]/div[@class="pub"]/text()').get()
            ratingNum = book.xpath('./div[@class="info"]/div/span[@class="rating_nums"]/text()').get()
            ratingPersonNum = book.xpath('./div[@class="info"]/div/span[@class="pl"]/text()').get()
            tag = '小说'

            item['book_icon_img'] = book_icon_img if book_icon_img is None or len(
                book_icon_img) == 0 else book_icon_img.strip()
            item['detail_link'] = detail_link if detail_link is None or len(detail_link) == 0 else detail_link.strip()
            item['name'] = name if name is None or len(name) == 0 else name.strip()
            item['pub'] = pub if pub is None or len(pub) == 0 else pub.strip()
            item['ratingNum'] = ratingNum if ratingNum is None or len(ratingNum) == 0 else ratingNum.strip()
            item['ratingPersonNum'] = ratingPersonNum if ratingPersonNum is None or len(
                ratingPersonNum) == 0 else ratingPersonNum.strip()
            item['tag'] = tag
            # print(item)

            yield item

        maxPage = int(
            response.xpath('/html/body/div/div/div/div/div/div[@class="paginator"]/a/text()')[-1].extract().strip())
        if self.page < maxPage:
            self.page = self.page + 1
            url = self.base_url + str(self.page * 20) + '&type=T'
            yield scrapy.Request(url=url, callback=self.parse)
