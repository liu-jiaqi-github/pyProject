import scrapy
from caipiao.items import CaipiaoItem


class ShuangseqiuSpider(scrapy.Spider):
    name = 'shuangseqiu'
    allowed_domains = ['500.com']
    start_urls = ['http://datachart.500.com/ssq/']

    def parse(self, resp, **kwargs):
        trs = resp.xpath("//tbody[@id='tdata']/tr")
        for tr in trs:
            if tr.xpath("./@class").extract_first() == 'tdbck':
                continue
            red_ball = tr.css(".chartBall01::text").extract()
            blue_ball = tr.css(".chartBall02::text").extract_first()
            qihao = tr.xpath("./td[1]/text()").extract_first().strip()

            cai = CaipiaoItem()
            cai['qihao'] = qihao
            cai['red_ball'] = red_ball
            cai['blue_ball'] = blue_ball
            yield cai
            break
