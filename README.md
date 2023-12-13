# eliseSpider
学习scrapy爬虫而建立的一个工程，其中实现包含爬取豆瓣读书的所有书籍评分等

## scrapy工程创建

创建项目
myproject为项目名，project_dir可选指定，未指定情况下，与myproject相同
> scrapy startproject myproject [project_dir]

项目结构
> myproject/
    scrapy.cfg            # 项目结构配置文件,默认情况下指定SCRAPY_SETTINGS_MODULE：settings.py位置等，
                            其他配置参数有：SCRAPY_PROJECT，项目之间的共享根目录；
                            该文件存放位置和优先级类似mysql的my.cnf
    myproject/             # 模块, 主要逻辑代码在这个模块里面
        __init__.py
        items.py          # 定义数据结构的地方，继承自scrapy.Item类
        middlewares.py    # 中间件，代理
        pipelines.py      # 管道文件，里面只有一个类，用于处理下载数据的后续处理，默认是300优先级，值越小优先级越高
        settings.py       # 配置文件，是否遵守robots协议，消息头定义，管道优先级配置，甚至数据库等一些自定义配置；

        spiders/          # 爬虫逻辑存放路径，spider1.py，spider2.py都可以由命令创建
            __init__.py
            spider1.py
            spider2.py



