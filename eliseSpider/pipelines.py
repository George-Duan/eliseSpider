# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from eliseSpider import settings

class ElisespiderPipeline:
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """insert into book(book_name,book_tag,author,publishing_house,publish_date,book_price,detail_link,book_icon_img,rating_nums,rating_person_num)
                  value (%s,%s,%s,%s,%s,%s,%s)""",
                (item['name'],
                 item['tag'],
                 item['pub'],
                 item['detail_link'], item['book_icon_img'], item['ratingNum'], item['ratingPersonNum']))
            self.connect.commit()
        except Exception as err:
            print("重复插入了==>错误信息为：" + str(err))
        return item

