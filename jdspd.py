# -*- coding: utf-8 -*-
import scrapy
import re
import requests
from jd.items import JdItem
from scrapy.http import Request
import json
'''
 https://item.jd.com/5242942.html   https://item.jd.com/6088404.html https://item.jd.com/8674691.html https://item.jd.com/25533160226.html https://item.jd.com/100001467225.html https://item.jd.com/100000650837.html https://item.jd.com/100001906474.html https://item.jd.com/100000304401.html'''

class JdspdSpider(scrapy.Spider):
    name = 'jdspd'
    allowed_domains = ['jd.com']
    commentVersion=''
    productID=''
    # def __init__(self,myurl='',*args, **kwargs):
        # super(JdspdSpider,self).__init__(*args, **kwargs)
        # self.url=myurl
        
    start_urls=['https://item.jd.com/100000766433.html', 'https://item.jd.com/100001550349.html', 'https://item.jd.com/100000322894.html', 'https://item.jd.com/5924266.html', 'https://item.jd.com/100001693805.html', 'https://item.jd.com/100001319136.html', 'https://item.jd.com/7081550.html', 'https://item.jd.com/1861102.html', 'https://item.jd.com/5706773.html', 'https://item.jd.com/6735790.html', 'https://item.jd.com/8457421.html', 'https://item.jd.com/5089267.html', 'https://item.jd.com/5089253.html', 'https://item.jd.com/100000822981.html', 'https://item.jd.com/8656283.html', 'https://item.jd.com/8264407.html', 'https://item.jd.com/6600216.html', 'https://item.jd.com/5089273.html', 'https://item.jd.com/7421462.html', 'https://item.jd.com/100000177748.html', 'https://item.jd.com/8051124.html', 'https://item.jd.com/8058010.html', 'https://item.jd.com/100000177756.html', 'https://item.jd.com/6755976.html', 'https://item.jd.com/7596939.html', 'https://item.jd.com/6558982.html', 'https://item.jd.com/5835281.html', 'https://item.jd.com/7651947.html', 'https://item.jd.com/7437564.html', 'https://item.jd.com/7029523.html', 'https://item.jd.com/100000982034.html', 'https://item.jd.com/100000503295.html', 'https://item.jd.com/100000773889.html', 'https://item.jd.com/100001364210.html', 'https://item.jd.com/100000650837.html', 'https://item.jd.com/7652027.html', 'https://item.jd.com/100000745034.html', 'https://item.jd.com/7694071.html', 'https://item.jd.com/100001790805.html', 'https://item.jd.com/29044581674.html', 'https://item.jd.com/100000727128.html', 'https://item.jd.com/100002852992.html', 'https://item.jd.com/6946625.html', 'https://item.jd.com/8735304.html', 'https://item.jd.com/28245104630.html', 'https://item.jd.com/100002727566.html', 'https://item.jd.com/100000015166.html', 'https://item.jd.com/3133847.html', 'https://item.jd.com/100002544828.html', 'https://item.jd.com/7120000.html', 'https://item.jd.com/7920226.html', 'https://item.jd.com/28751842981.html', 'https://item.jd.com/7437788.html', 'https://item.jd.com/8535863.html', 'https://item.jd.com/100000177760.html', 'https://item.jd.com/100000287117.html', 'https://item.jd.com/100000047504.html', 'https://item.jd.com/7694047.html', 'https://item.jd.com/7321794.html', 'https://item.jd.com/28331229416.html', 'https://item.jd.com/8240587.html']
     
    def start_requests(self):
        for url in self.start_urls[20:40]:
            product_url=url+"#comment"
            print(product_url)
            self.productID =product_url.split('/')[-1].split('.')[0]
            self.commentVersion=self.get_comment_version(product_url)
            yield Request(self.generate_product_comment_url(self.commentVersion,self.productID,0),callback=self.parse)

    def parse(self, response):
        comments_json = response.text[len('fetchJSON_comment98vv'+self.commentVersion+'('):-2]
        
        productCommentSummary = json.loads(comments_json).get('productCommentSummary')
        comments = json.loads(comments_json).get('comments')
        item=JdItem()
        
        item['goodRateShow']=productCommentSummary.get('goodRateShow')
        item['generalRateShow']=productCommentSummary.get('generalRateShow')
        item['poorRateShow']=productCommentSummary.get('poorRateShow')
        item['commentCount']=productCommentSummary.get('commentCount') 
        item['productId']=productCommentSummary.get('productId')
        item['referenceName']=[]
        item['referenceId']=[] 
        item['content']=[]
        item['creationTime']=[]
        item['nickname']=[]
        item['userLevelName']=[]
        item['userClientShow']=[]
        item['id']=[]         
        item['score']=[]                
        item['guid']=[]
        
        for comment in comments:
            # 商品名称
            item['referenceName'].append(comment.get('referenceName'))
            # 商品ID
            item['referenceId'].append(comment.get('referenceId'))  
            # 评论内容
            item['content'].append(comment.get('content'))
            
            # 评论时间
            item['creationTime'].append(comment.get('creationTime'))
            # 评论人昵称
            item['nickname'].append(comment.get('nickname'))
            # 顾客会员等级
            item['userLevelName'].append(comment.get('userLevelName'))
            # 购物使用的平台
            item['userClientShow'].append(comment.get('userClientShow'))
            # 用户id
            item['id'].append(comment.get('id'))        
            # 评分
            item['score'].append(comment.get('score'))                 
            # guid"13cd40e8-93b0-4078-96e9-d33748566516"
            item['guid'].append(comment.get('guid'))          
        yield item
        
        maxPage=json.loads(comments_json).get('productCommentSummary').get('commentCount')
        
        if maxPage % 10 == 0:  # 算出评论的页数，一页10条评论
            page = maxPage/10           
        else:
            page = maxPage/10 + 1
        for k in range(1,50):

            yield Request(self.generate_product_comment_url(self.commentVersion,self.productID,k),callback=self.parse)
        
    # 根据参数生成商品评论url
    def generate_product_comment_url(self,commentVersion,productID,page):
        #url='https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv'+commentVersion+'&productId='+productID+'&score=0&sortType=6&page='+str(page)+'&pageSize=10&isShadowSku=0&rid=0&fold=1'
        
        url='https://club.jd.com/comment/skuProductPageComments.action?callback=fetchJSON_comment98vv'+commentVersion+'&productId='+productID+'&score=0&sortType=6&page='+str(page)+'&pageSize=10&isShadowSku=0&rid=0&fold=1'
        
        return url
        
    def get_html(self,url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        }
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            return resp.text
        else:
            return None
    # 获取commentVersion，用于构造评论页的url
    def get_comment_version(self,product_url):
        resp=self.get_html(product_url)
        pattern = re.compile(r"commentVersion:'(.*?)'")
        commentVersion = re.search(pattern, resp).group(1)
        return commentVersion      
