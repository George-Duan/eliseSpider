# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ElisespiderDoubanBookTypeItem(scrapy.Item):
    # 分类名
    type_name = scrapy.Field()
    # 标签名
    tag_name = scrapy.Field()
    # icon 图片链接
    book_icon_img = scrapy.Field()
    # 详情链接
    detail_link = scrapy.Field()
    # book name
    name = scrapy.Field()

class ElisespiderDoubanBookDetailItem(scrapy.Item):
    book_name = scrapy.Field()
    type_name = scrapy.Field()
    tag_name = scrapy.Field()
    #详情链接
    detail_link = scrapy.Field()
    #图片链接
    book_img = scrapy.Field()
    # 书籍图片右边详情列表展示
    author = scrapy.Field()
    #出版社
    press = scrapy.Field()
    # 出版社
    series = scrapy.Field()
    #副标题
    subtitle = scrapy.Field()
    #原名
    origin_title = scrapy.Field()
    #译者
    translator = scrapy.Field()
    #出版年份
    publication_year = scrapy.Field()
    #页数
    page_num = scrapy.Field()
    #定价
    price = scrapy.Field()
    #装帧
    bookbinding = scrapy.Field()
    #isbn号
    isbn = scrapy.Field()
    # 评分
    rating_num = scrapy.Field()
    # 评价人数
    rating_people = scrapy.Field()
    # 内容简介
    intro = scrapy.Field()
    # 作者简介 暂时不爬了
    # 目录
    dir_full = scrapy.Field()


