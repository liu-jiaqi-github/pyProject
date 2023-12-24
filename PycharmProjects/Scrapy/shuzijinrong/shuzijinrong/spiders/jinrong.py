import scrapy


class JinrongSpider(scrapy.Spider):
    name = 'jinrong'
    allowed_domains = ['www.fintechinchina.com']
    start_urls = [
        'https://www.fintechinchina.com/index/article/index.html?type=2&keyword=&page=1&search=%E6%95%B0%E6%8D%AE']

    def parse(self, response, **kwargs):
        lbs = response.xpath("/html/body/div[3]/div/div[2]/div[1]/a")
        for lb in lbs:
            href = lb.xpath("./@href").extract_first()
            # 获取详情链接
            yield scrapy.Request(
                url=response.urljoin(href),  # 把resp中的url和我刚刚获取的url进行拼接整合,
                callback=self.parse_detail  # 回调函数, 当响应回馈之后, 如何进行处理响应那日容
            )
            break
        # 获取下一页链接

    def parse_detail(self, resp, **kwargs):
        h1 = resp.xpath("/html/body/div[1]/div[1]/div[1]/p[1]/text()").extract_first()
        p_list = resp.xpath("/html/body/div[1]/div[1]/div[1]/div[1]/p")
        text_list = []
        for p in p_list:
            strong_text = p.xpath("./strong/text()").extract_first()
            if strong_text is not None:
                text_list.append(strong_text)
            p_text = p.xpath("./text()").extract_first()
            if p_text is not None:
                text_list.append(p_text)
            img_src = p.xpath("./img/@src").extract_first()
            if img_src is not None:
                text_list.append(resp.urljoin(img_src))
        print(text_list)
