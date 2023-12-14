import scrapy
from eliseSpider.items import ElisespiderItem


class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["book.douban.com"]
    start_urls = ["https://book.douban.com/tag/?view=type&icn=index-sorttags-all"]

    base_url = 'https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start='

    ## parse_tag
    def parse(self, response):
        table_list = response.xpath('//table')
        for table in table_list:
            type_name = table.xpath('./preceding-sibling::a/@name').get()
            tag_list = table.xpath('./tbody/tr/td/a')
            for tag in tag_list:
                item = ElisespiderItem()
                href = tag.xpath('./@href').get()
                tag_name = tag.xpath('./@href').get()
                item['type_name'] = type_name
                item['tag_name'] = tag_name
                url = 'https://book.douban.com' + href
                print('已爬取url:' + url + ', 向下级页面请求中......')
                yield scrapy.Request(url=url, meta={'item': item}, callback=self.parse_page)

    def parse_page(self, response):

        item = response.meta['item']

        maxPage = int(
            response.xpath('/html/body/div/div/div/div/div/div[@class="paginator"]/a/text()')[-1].get().strip())
        for i in range(0, maxPage, 1):
            url = self.base_url + str(i * 20) + '&type=T'
            print('分页请求中，当前页是：' + url)
            yield scrapy.Request(url=url, meta={'item': item}, callback=self.parse_book_list)


    def parse_book_list(self, response):

        item = response.meta['item']

        book_list = response.xpath('/html/body/div/div/div/div/div/ul[@class="subject-list"]/li')
        for book in book_list:
            detail_link = book.xpath('./div[@class="info"]/h2/a//@href').get()
            print('分页请求中，当前页是：' + detail_link)
            yield scrapy.Request(url=detail_link, meta={'item': item}, callback=self.parse_detail)


    def parse_detail(self, response):
        print("===============================================================")
        item = response.meta['item']

        book_subject = response.xpath('//div[@class="subjectwrap clearfix"]')
        book_img = book_subject.xpath('./div/div/a/img/@src').get()
        author = book_subject.xpath('./div/div[@id="info"]/span/a/text()').get()

        details = book_subject.xpath('./div/div[@id="info"]/span[@class="pl"]')
        print(details)


