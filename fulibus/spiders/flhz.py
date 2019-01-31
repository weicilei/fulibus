# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from fulibus.items import ArticleItem
import os


class FlhzSpider(CrawlSpider):
    name = 'flhz'
    allowed_domains = ['fulibus.net', 'sinaimg.cn', ]
    start_urls = ['http://fulibus.net/category/flhz']

    pages_list = LinkExtractor("category/flhz")
    # http://fulibus.net/2019004.html http://fulibus.net/tugirl.html
    articles_list = LinkExtractor(allow="2019\d{3}\.html",
                                  restrict_xpaths="//article[contains(@class, 'excerpt')]")
    images_list = LinkExtractor(allow="sinaimg\.cn/mw690/", restrict_xpaths="//article",
                                tags="img", attrs="src", deny_extensions="")
    rules = (
        Rule(pages_list),
        Rule(articles_list, callback='parse_content', follow=True),
        Rule(images_list, callback="parse_image")
        # 提取福利文中的图片链接，发送请求，用parse_images解析响应
    )

    def parse_content(self, response):
        article = ArticleItem()
        article["title"] = response.xpath("//h1/a/text()")[0].extract()
        article["publish_time"] = response.xpath('//span[@class="item"][1]/text()')[0].extract()

        video_list = []
        video_title_list = response.xpath('//blockquote//a/text()').extract()
        video_link_list = response.xpath('//blockquote//a/@href').extract()
        video_tuple_list = zip(video_title_list, video_link_list)
        for video_title, video_link in video_tuple_list:
            video_list.append({video_title: video_link})
        article["videos"] = video_list

        yield article

    def parse_image(self, response):
        dirname = response.request.headers['Referer'][-12:-5]
        try:
            with open(dirname + "/" + response.url[-10:], "w") as f:
                f.write(response.body)
        except:
            os.mkdir(dirname)
            with open(dirname + "/" + response.url[-10:], "w") as f:
                f.write(response.body)

