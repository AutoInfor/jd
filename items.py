# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    referenceName= scrapy.Field()    # 商品名称
    referenceId = scrapy.Field()    # 商品ID
    content = scrapy.Field()    # 评论内容
    creationTime = scrapy.Field()    # 评论时间
    nickname = scrapy.Field()    # 评论人昵称
    userLevelName = scrapy.Field()    # 顾客会员等级
    userClientShow = scrapy.Field()    # 购物使用的平台
    goodRateShow = scrapy.Field()
    generalRateShow = scrapy.Field()
    poorRateShow = scrapy.Field()
    commentCount = scrapy.Field()
    productId = scrapy.Field()
    id           = scrapy.Field()
    score      = scrapy.Field()            
    guid  = scrapy.Field()
