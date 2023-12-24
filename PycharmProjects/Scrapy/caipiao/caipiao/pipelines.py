# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

"""
存储数据的方案:
    1.数据要存储在csv文件中
    2.数据存储在mysql数据库中
    3.数据存储在mongodb数据库中
    4.文件的存储
"""
import pymysql
import pymongo
import cx_Oracle
from caipiao.settings import MySql


class CaipiaoPipeline:
    def open_spider(self, spiders):
        # print("开始")
        self.f = open("./双色球.csv", mode="a", encoding="utf-8")

    def process_item(self, item, spider):
        # print("中间")
        self.f.write(f"{item['qihao']},{'_'.join(item['red_ball'])},{item['blue_ball']}\n")
        return item

    def close_spider(self, spiders):
        # print("结束")
        if self.f:
            self.f.close()


class CaipiaoMySQLPipeline:
    def open_spider(self, spiders):
        self.conn = pymysql.connect(
            host=MySql["host"],
            port=MySql["port"],
            user=MySql["user"],
            password=MySql["password"],
            database=MySql["database"],
        )

    def process_item(self, item, spider):
        try:
            cursor = self.conn.cursor()
            sql = "insert into caipiao(qihao,red_ball,blue_ball)values(%s,%s,%s)"
            # 执行sql时传值必须是元组
            cursor.execute(sql, (item['qihao'], '_'.join(item['red_ball']), item['blue_ball']))
            # 提交事务
            self.conn.commit()
        except:
            # 事务回滚
            self.conn.rollback()
        finally:
            if cursor:
                cursor.close()
        return item

    def close_spider(self, spiders):
        if self.conn:
            self.conn.close()


class CaipiaoMongoDBPipeline:
    def open_spider(self, spiders):
        self.client = pymongo.MongoClient(host="localhost", port=27017)
        db = self.client['python']  # 用哪个数据库
        db.authenticate("python_admin", "123456")  # 用户名密码
        self.collection = db["caipiao2"]  # 指定彩票集合

    def process_item(self, item, spider):
        self.collection.insert({"qihao": item['qihao'], "red_ball": item['red_ball'], "blue_ball": item['blue_ball']})
        return item

    def close_spider(self, spiders):
        self.client.close()


class CaipiaoOraclePipeline:
    def open_spider(self, spiders):
        # 设置链接参数
        user_name = 'JCZT'
        password = 'JCZT'
        connect_str = '192.168.137.2:1521/helowin'
        # 先建立连接
        self.conn = cx_Oracle.connect(user_name, password, connect_str)

    def process_item(self, item, spider):
        # 定义游标
        cursor = self.conn.cursor()
        # 定义sql
        sql = 'select * from BIP_DATA_ENTITY_MGR'
        # 向数据库发送sql
        cursor.execute(sql)
        # 获取数据, fetchall()获取全部数据
        results = cursor.fetchall()
        # 获取字段名称
        fields = [field[0] for field in cursor.description]
        # print(fields)
        # 把数据与字段关连起来
        res = [dict(zip(fields, result)) for result in results]
        # 从数据列表中取出每段数据
        for rlt in res:
            print(rlt)
        # 关闭游标
        cursor.close()
        return item

    def close_spider(self, spiders):
        # 关闭连接
        self.conn.close()
