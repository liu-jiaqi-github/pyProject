import scrapy
import re
from GBT.items import GbtItem


class GbtgamespaceSpider(scrapy.Spider):
    name = 'GBTGameSpace'
    allowed_domains = ['ysepan.com']
    start_urls = ['http://ysepan.com/']


    def start_requests(self):
        urls = ['http://ck.ysepan.com/f_ht/ajcx/ml.aspx?cz=ml_dq&_dlmc=gbtgame&_dlmm=']
        for url in urls:
            yield scrapy.Request(url, headers={
                'Referer': 'http://ck.ysepan.com/f_ht/ajcx/000ht.html?bbh=1166'  # 修改Referer
            })

    def parse(self, response, *args, **kwargs):
        rep = str(response.text).strip()
        id_list = re.findall('<li id="ml_(.*?)" class', rep)
        youxiliebiao_list = re.findall('<a class="ml" href="javascript:;">【(.*?)】</a>', rep)

        i = 0
        for id in id_list:
            headers = {'Referer': 'http://ck.ysepan.com/f_ht/ajcx/000ht.html?bbh=1166'}
            yield scrapy.Request(
                f"http://ck.ysepan.com/f_ht/ajcx/wj.aspx?cz=dq&jsq=0&mlbh={id}&wjpx=1&_dlmc=gbtgame&_dlmm=",
                callback=self.parse_torrent,
                headers=headers,
                meta={"youxiliebiao":youxiliebiao_list[i]}
            )
            i += 1


    def parse_torrent(self, response):
        rep = str(response.text).strip()
        # print(rep)
        gbt = GbtItem()
        for href_list, title_list, name in re.findall('<a href="(.*?)"(.*?)">(.*?)</a>', rep):
            gbt["game_time"] = response.meta["youxiliebiao"]
            gbt["game_BT_URL"] = href_list
            gbt["game_name"] = name
            # print(href_list)
            # print(name)
            yield gbt
