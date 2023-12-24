# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy


class TupianzhijiaPipeline:
    def process_item(self, item, spider):
        return item


# 想要使用ImagesPipeline 必须单独设置一个配置, 用来保存文件的文件夹
# settings中间加入IMAGES_STORE = "./meinvtupian"(meinvtupian: 文件夹名)
class MeinvSavePipeline(ImagesPipeline):  # 利用图片管道帮我们完成数据下载操作
    def get_media_requests(self, item, info):  # 负责下载的
        print("图片管道_下载")
        return scrapy.Request(item['img_src'])  # 直接返回一个请求即可

    def file_path(self, request, response=None, info=None, *, item=None):  # 准备文件路径
        print("图片管道_名称")
        file_name = request.url.split("/")[-1]  # request.url可以直接获取刚刚请求的url
        return f"img/{file_name}"  # img/xxx.jpg

    def item_completed(self, results, item, info):  # 返回文件的详细信息
        print("图片管道_详情")
        ok, finfo = results[0]
        item['local_path'] = finfo["path"]
