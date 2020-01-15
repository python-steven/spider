# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
from  scrapy_redis.spiders import RedisSpider
import time
import urllib
import pprint
class DangdangSpider(RedisSpider):
    name = 'dangdang'
    allowed_domains = ['dangdang.com']
    # start_urls = ['http://book.dangdang.com/']
    redis_key = "dangdang"

    def parse(self, response):
        #大分类
        div_list = response.xpath("//div[@class='con flq_body']/div")
        print(len(div_list))
        for div in div_list:
            item={}
            item["b_cate"] = div.xpath("./dl/dt//text()").getall()
            item["b_cate"] =[i.strip() for i in item["b_cate"] if len(i.strip())>0]
            #中间分类
            # print("中间分类的获取：",item)
            dl_list = div.xpath("./div//dl[@class='inner_dl']")
            for dl in dl_list:
                item["m_cate"] = dl.xpath("./dt//text()").getall()
                item["m_cate"] = [i.strip() for i in item["m_cate"] if len(i.strip())>0][0]
                #小分类分组
                a_list = dl.xpath("./dd/a")
                # print("小分类的获取：",item)
                for a in a_list:
                    item["s_href"] = a.xpath("./@href").get()
                    item["s_cate"] = a.xpath("./text()").get()
                    if item["s_href"] is not None:
                        yield scrapy.Request(
                            item["s_href"],
                            callback=self.parse_book_list,
                            meta={"item":deepcopy(item)}

                        )
    def parse_book_list(self,response):
        item = response.meta["item"]
        li_list = response.xpath("//ul[@class='bigimg']/li")
        for li in li_list:
            item["book_img"] = li.xpath("./a[@class='pic']/img/@src").get()
            if item["book_img"] == "images/model/guan/url_none.png":
                item["book_img"] = li.xpath("./a[@class='pic']/img/@data-original").get()
            item["book_name"] = li.xpath("./p[@class='name']/a/@title").get()
            item["book_desc"] = li.xpath("./p[@class='detail']/text()").get()
            item["book_price"] = li.xpath(".//span[@class='search_now_price']/text()").get()
            item["book_author"] = li.xpath("./p[@class='search_book_author']/span[1]/a/text()").getall()
            item["book_publish_date"] = li.xpath("./p[@class='search_book_author']/span[2]/text()").get()
            item["book_press"] = li.xpath("./p[@class='search_book_author']/span[3]/a/text()").get()
            # time.sleep(1)
            pprint.pprint(item)
        #下一页的url地址
        next_url = response.xpath("//li[@class='next']/a/@href").get()
        if next_url is not None:
            next_url = urllib.parse.urljoin(response.url,next_url)
            yield scrapy.Request(
                next_url,
                callback=self.parse,
                meta={"item":item}

            )



