# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from eliseSpider import settings
import os


class DoubanBookItemElisespiderPipeline:
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8mb4',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """insert into book(book_name,tag_name,detail_link,book_img,author,press,subtitle,origin_title,translator,publication_year,page_num,price,bookbinding,isbn,rating_num,rating_people,intro,dir_full)
                  value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (item['book_name'],
                 #item['type_name'],
                 item['tag_name'],
                 item['detail_link'], item['book_img'], item['author'], item['press'],
                 item['subtitle'], item['origin_title'], item['translator'], item['publication_year'], item['page_num'],
                 item['price'], item['bookbinding'], item['isbn'], item['rating_num'], item['rating_people'],
                 item['intro'], item['dir_full']))
            self.connect.commit()
        except Exception as err:
            print("重复插入了==>错误信息为：" + str(err))
        return item


import urllib.request


# 多管道下载书籍图片
class DoubanBookImgDownloadPipeline:
    def process_item(self, item, spider):
        try:
            url = item.get('book_img')
            path = 'D:\\doubanBookImg\\' + item.get('tag_name')
            if not os.path.exists(path):  # 判断是否存在文件夹如果不存在则创建为文件夹
                os.makedirs(path)
            filename = path + '\\' + item.get('book_img').split('/')[-1]
            urllib.request.urlretrieve(url=url, filename=filename)
        except Exception as err:
            print("下载书籍图片文件异常：" + str(err))
        return item
