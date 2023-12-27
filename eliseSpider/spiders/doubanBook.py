import scrapy
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from eliseSpider.items import ElisespiderDoubanBookDetailItem


class DoubanbookSpider(CrawlSpider):
    name = "doubanBook"
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/tag/?view=type&icn=index-sorttags-all']
    #start_urls = ['https://book.douban.com/tag/%E7%BC%96%E7%A8%8B']

    rules = (
        Rule(
            LxmlLinkExtractor(allow=(r"/tag/.+",), restrict_xpaths=("//table/tbody/tr/td/a"), ),
            # 修改这里的 restrict_xpaths 为有效的 XPath 表达式
            callback="parse_item",
            follow=True
        ),
        Rule(
            LxmlLinkExtractor(allow=(r"/tag/编程\?start=\d+\&type=T",), restrict_xpaths=('/html/body/div/div/div/div/div/div[@class="paginator"]/a'), ),
            callback="parse_item",
            follow=True
        )
        # ,
        # Rule(
        #     LxmlLinkExtractor(allow=(r"https://book\.douban\.com/subject/\d+/",), restrict_xpaths=('/html/body/div/div/div/div/div/ul[@class="subject-list"]/li/div[@class="info"]/h2/a'), ),
        #     callback="parse_item",
        #     follow=False
        # )
    )

    def parse_item(self, response):

        tag_name = response.xpath('//div[@id="content"]/h1/text()').get()
        if tag_name:
            tag_name = tag_name.strip().split(":")[1].strip()

        book_list = response.xpath('/html/body/div/div/div/div/div/ul[@class="subject-list"]/li')
        for book in book_list:
            detail_link = book.xpath('./div[@class="info"]/h2/a//@href').get()
            print('分页页面解析到的详情页url是：' + detail_link)
            item = ElisespiderDoubanBookDetailItem()
            item['tag_name'] = tag_name
            item['detail_link'] = detail_link
            yield scrapy.Request(url=detail_link, meta={'item': item}, callback=self.parse_detail)

    def parse_detail(self, response):
        print("===============================================================")
        item = response.meta['item']

        urlArray = response.url.split('/')
        subjectId = urlArray[-2]

        book_name = response.xpath('//span[@property="v:itemreviewed"]/text()').get()

        article = response.xpath('//div[@class="article"]')
        # 图书图片，取大图
        book_img = article.xpath('//div[@id="mainpic"]/a/@href').get()
        #tag_name = "小说"
        #type_name = '文学'
        # 书籍图片右边详情列表展示
        info = article.xpath('//div[@id="info"]')
        authorArray = info.xpath('//span[contains(text(), "作者")]/following-sibling::a/text()').getall()
        if not authorArray:
            authorArray = info.xpath('/span[contains(text(), "作者")]/following-sibling::text()').getall()
        author = ' | '.join(authorArray) if authorArray else ''

        press = info.xpath('//span[contains(text(), "出版社")]/following-sibling::a/text()').get()
        if not press:
            press = info.xpath('/span[contains(text(), "出版社")]/following-sibling::text()').get()
        if press:
            press = press.strip()

        subtitle = info.xpath('//span[contains(text(), "副标题")]/following-sibling::a/text()').get()
        if not subtitle:
            subtitle = info.xpath('/span[contains(text(), "副标题")]/following-sibling::text()').get()
        if subtitle:
            subtitle = subtitle.strip()

        origin_title = info.xpath('//span[contains(text(), "原作名")]/following-sibling::a/text()').get()
        if not origin_title:
            origin_title = info.xpath('/span[contains(text(), "原作名")]/following-sibling::text()').get()
        if origin_title:
            origin_title = origin_title.strip()

        translatorArray = info.xpath('//span[contains(text(), "译者")]/following-sibling::a/text()').getall()
        if not translatorArray:
            translatorArray = info.xpath('/span[contains(text(), "译者")]/following-sibling::text()').getall()
        translator = ' | '.join(translatorArray) if translatorArray else ''

        publication_year = info.xpath('//span[contains(text(), "出版年")]/following-sibling::text()').get()
        if publication_year:
            publication_year = publication_year.strip()

        page_num = info.xpath('//span[contains(text(), "页数")]/following-sibling::text()').get()
        if page_num:
            page_num = page_num.strip()

        price = info.xpath('//span[contains(text(), "定价")]/following-sibling::text()').get()
        if price:
            price = price.strip()

        bookbinding = info.xpath('//span[contains(text(), "装帧")]/following-sibling::text()').get()
        if bookbinding:
            bookbinding = bookbinding.strip()

        isbn = info.xpath('//span[contains(text(), "ISBN")]/following-sibling::text()').get()
        if isbn:
            isbn = isbn.strip()

        # 评分
        rating_num = article.xpath('//div[@id="interest_sectl"]//strong[@class="ll rating_num "]/text()').get()
        if rating_num:
            rating_num = rating_num.strip()

        # 评价人数
        rating_people = article.xpath(
            '//div[@id="interest_sectl"]//div[@class="rating_sum"]//a[@class="rating_people"]/span/text()').get()
        if rating_people:
            rating_people = rating_people.strip()

        # 内容简介
        intro_array = (article.xpath('//div[@id="link-report"]/span[@class="all hidden"]//div[@class="intro"]/p/text()')
                       .getall())
        intro = '\r\n'.join(intro_array) if intro_array else ''

        # 作者简介 暂时不爬了

        # 目录 36104107
        dir_full_xpath = '//div[@class="related_info"]//div[@id="dir_' + subjectId + '_full"]/text()'
        dir_full_array = article.xpath(dir_full_xpath).getall()
        dir_full = '\r\n'.join(dir_full_array) if dir_full_array else ''

        item['book_name'] = book_name
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
