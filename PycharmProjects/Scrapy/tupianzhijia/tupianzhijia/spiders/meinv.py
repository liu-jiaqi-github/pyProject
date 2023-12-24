import scrapy
from tupianzhijia.items import MeinvItem


class MeinvSpider(scrapy.Spider):
    name = 'meinv'
    allowed_domains = ['tupianzj.com', 'img.lianzhixiu.com']

    def start_requests(self):
        print("开始请求")
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.139 Safari/537.36"
        }
        self.cookies = {
            "t": "c4b8615510440bafe76495b06e621900",
            "r": "9048",
            "Hm_lvt_f5329ae3e00629a7bb8ad78d0efb7273": "1681823363",
            "Hm_lpvt_f5329ae3e00629a7bb8ad78d0efb7273": "1681830186"

        }
        start_urls = [
            "https://www.tupianzj.com/bizhi/zhiwu/",
            "https://www.tupianzj.com/bizhi/DNmeinv/",
            "https://www.tupianzj.com/bizhi/dongwu/"
        ]
        for start_url in start_urls:
            yield scrapy.Request(start_url, method='get', cookies=self.cookies, headers=self.headers)

    def parse(self, response, **kwargs):
        print("进入方法parse")
        # print(resp.text)
        # resp_text = resp.content.decode("gb2312", "ignore")
        li_list = response.xpath("//ul[@class='list_con_box_ul']/li")
        for li in li_list:
            href = li.xpath("./a/@href").extract_first()
            # 理论上应该开始进行一个网络请求了
            # 根据scrapy的运行原理, 此处应该对应href进行处理. 处理成一个请求,交给引擎
            yield scrapy.Request(
                url=response.urljoin(href),  # 把resp中的url和我刚刚获取的url进行拼接整合,
                method='get',
                cookies=self.cookies,
                headers=self.headers,
                callback=self.parse_detail  # 回调函数, 当响应回馈之后, 如何进行处理响应那日容
            )

        next_href = response.xpath("//div[@class='pages']/ul/li/a[contains(text(),'下一页')]/@href").extract_first()
        if next_href:
            # 进行下一页的请求
            yield scrapy.Request(
                url=response.urljoin(next_href),
                callback=self.parse,
                method='get',
                cookies=self.cookies,
                headers=self.headers,
            )

    def parse_detail(self, response, **kwargs):
        print("进入方法parse_detail")
        name = response.xpath('//*[@id="container"]/div/div/div[2]/h1').extract_first()
        img_src = response.xpath("//div[@id='bigpic']/a/img/@src").extract_first()
        # print(name, img_src)
        item = MeinvItem()
        item['name'] = name
        item['img_src'] = img_src
        yield item
