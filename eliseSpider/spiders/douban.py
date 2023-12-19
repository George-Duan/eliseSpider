import scrapy
from eliseSpider.items import ElisespiderDoubanBookDetailItem


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
                item = ElisespiderDoubanBookDetailItem()
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
            item['detail_link'] = detail_link
            yield scrapy.Request(url=detail_link, meta={'item': item}, callback=self.parse_detail)


    def parse_detail(self, response):
        print("===============================================================")
        item = response.meta['item']

        article = response.xpath('//div[@class="article"]')
        #图书图片，取大图
        book_img = article.xpath('//div[@id="mainpic"]/a/@href').get()

        #书籍图片右边详情列表展示
        info = article.xpath('//div[@id="info"]')
        author = info.xpath('//span[text()=" 作者"]/following-sibling::a/@text()').get()
        if not author:
            author = info.xpath('/span[text()=" 作者"]/following-sibling::text()').get()
        if author:
            author = author.strip()

        press = info.xpath('//span[text()="出版社:"]/following-sibling::a/@text()').get()
        if not press:
            press = info.xpath('/span[text()="出版社:"]/following-sibling::text()').get()
        if press:
            press = press.strip()

        subtitle = info.xpath('//span[text()="副标题:"]/following-sibling::a/@text()').get()
        if not subtitle:
            subtitle = info.xpath('/span[text()="副标题:"]/following-sibling::text()').get()
        if subtitle:
            subtitle = subtitle.strip()

        origin_title = info.xpath('//span[text()="原作名:"]/following-sibling::a/@text()').get()
        if not origin_title:
            origin_title = info.xpath('/span[text()="原作名:"]/following-sibling::text()').get()
        if origin_title:
            origin_title = origin_title.strip()

        translator = info.xpath('//span[text()=" 译者"]/following-sibling::a/@text()').get()
        if not translator:
            translator = info.xpath('/span[text()=" 译者"]/following-sibling::text()').get()
        if translator:
            translator = translator.strip()

        publication_year = info.xpath('/span[text()="出版年:"]/following-sibling::text()').get()
        if publication_year:
            publication_year = publication_year.strip()

        page_num = info.xpath('/span[text()="页数:"]/following-sibling::text()').get()
        if page_num:
            page_num = page_num.strip()

        price = info.xpath('/span[text()="定价:"]/following-sibling::text()').get()
        if price:
            price = price.strip()

        bookbinding = info.xpath('/span[text()="装帧:"]/following-sibling::text()').get()
        if bookbinding:
            bookbinding = bookbinding.strip()

        isbn = info.xpath('/span[text()="ISBN:"]/following-sibling::text()').get()
        if isbn:
            isbn = isbn.strip()

        # 评分
        rating_num = article.xpath('//div[@id="interest_sectl"]//strong[@class="ll rating_num "]/text()').get()
        if rating_num:
            rating_num = rating_num.strip()

        #评价人数
        rating_people = article.xpath('//div[@id="interest_sectl"]//div[@class="rating_right"]//a[@class="rating_people"]/text()').get()
        if rating_people:
            rating_people = rating_people.strip()

        # 内容简介
        intro_array = article.xpath('//div[@id="link-report"]//div[@class="intro"]/p/text()').getAll()
        intro = intro_array.join('\r\n') if intro_array else ''

        # 作者简介 暂时不爬了

        #目录
        dir_full_array = article.xpath('//div[@class="related_info"]//div[@id="dir_35575892_full"]/text()').getAll()
        dir_full = dir_full_array.join('\r\n') if dir_full_array else ''

        item['detail_link'] = response.request.url
        # 图片链接
        item['book_img'] = book_img
        # 书籍图片右边详情列表展示
        item['author'] = author
        # 出版社
        item['press'] = press
        # 副标题
        item['subtitle'] = subtitle
        # 原名
        item['origin_title'] = origin_title
        # 译者
        item['translator'] = translator
        # 出版年份
        item['publication_year'] = publication_year
        # 页数
        item['page_num'] = page_num
        # 定价
        item['price'] = price
        # 装帧
        item['bookbinding'] = bookbinding
        # isbn号
        item['isbn'] = isbn
        # 评分
        item['rating_num'] = rating_num
        # 评价人数
        item['rating_people'] = rating_people
        # 内容简介
        item['intro'] = intro
        # 作者简介 暂时不爬了
        # 目录
        item['dir_full'] = dir_full
        yield item

    def parse_book_info(self, xpath):

        pass

