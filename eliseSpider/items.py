# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ElisespiderItem(scrapy.Item):
    # icon 图片链接
    book_icon_img = scrapy.Field()
    # 详情链接
    detail_link = scrapy.Field()
    # book name
    name = scrapy.Field()
    # 作者
    #author = scrapy.Field()
    # 出版社
    #publishingHouse = scrapy.Field()
    # 出版时间
    #publishedDate = scrapy.Field()
    # 价格
    #price = scrapy.Field()
    pub = scrapy.Field()
    # 评价分数
    ratingNum = scrapy.Field()
    # 评价人数
    ratingPersonNum = scrapy.Field()
    # 评价人数
    tag = scrapy.Field()

