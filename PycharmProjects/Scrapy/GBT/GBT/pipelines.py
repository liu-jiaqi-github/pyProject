# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.utils.project import get_project_settings
import cx_Oracle as cx  # oracle驱动


class GbtPipeline:
    def open_spider(self, spider):
        # self.f = open("./a.csv", mode="a", encoding="utf-8")

        settings = get_project_settings()
        self.use = 'JCZT'
        self.password = 'JCZT'
        self.host = '192.168.137.2:1521/helowin'
        self.conn = cx.connect(self.use, self.password, self.host)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # self.f.write(f"{item['game_time']},{item['game_name']},{item['game_BT_URL']}\n")
        sql = "insert into GBT (GAME_TIME,GAME_NAME,GAME_BT_URL) values('{}','{}','{}')".format(
            item["game_time"], item["game_name"], item["game_BT_URL"])
        print(sql)
        # 执行sql语句
        self.cursor.execute(sql)
        # 提交
        self.conn.commit()

        return item

    def close_spider(self, spider):
        # if self.f:
        #     self.f.close()
        self.cursor.close()
        self.conn.close()