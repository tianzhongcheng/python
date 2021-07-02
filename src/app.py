import requests
import time
import pymysql
from lxml import etree
requests.adapters.DEFAULT_RETRIES = 5
#伪装浏览器
HEADERS ={
    'User-Agent' : 'Mozilla/5.(Windows NT 10.0;WOW64) AppleWebKit/537.3(KHTML,like Gecko) Chrome/63.3239.13Safar/537.36',
    'Host' : 'www.dy2018.com'
}
#定义全局变量
BASE_DOMAIN = 'https://www.dy2018.com'
#获取首页网页信息并解析
def getUrlText(url,coding):
    s = requests.session()
    #print("获取首页网页信息并解析:" , url)
    respons = s.get(url,headers=HEADERS)
    print("请求URL:",url)
    if(coding=='c'):
        urlText = respons.content.decode('gbk')
        html = etree.HTML(urlText)      #使用lxml解析网页
    else:
        urlText = respons.text
        html = etree.HTML(urlText)      # 使用lxml解析网页
    s.keep_alive = False
    return html

#获取电影详情页的href，text解析
def getHref(url):
    html = getUrlText(url,'t')
    aHref = html.xpath('//table[@class="tbspan]//a/@href')
    print("获取电影详情页的href,text解析```")
    htmlAll = map(lambda url:BASE_DOMAIN+url,aHref)
    return htmlAll

#使用content解析电影详情页，并获取详细信息数据
def getPage(url):
    html = getUrlText(url,'c')
    moveInfo = {} #定义电影信息
    mName = html.xpath('//div[@class="title_all"]//h1/text()')[0]
    moveInfo['movie_name'] = mName
    mDiv = html.xpath('//div[@id="Zoom]')[0]
    mImgSrc = mDiv.xpath('//img/@src')
    moveInfo['image_path'] = mImgSrc[0] #获取电影海报src
    if len(mImgSrc) >= 2:
        moveInfo['screeshot'] = mImgSrc[1] #获取电影截图src地址
    mContnent = mDiv.xpath('.//text(')
    def pares_info(info,rule):
        '''
        :param info:    字符串
        :param rule:    替换字串
        :return:        指定字符串替换为空，并剔除左右空格
        '''
        return info.replace(rule,'').strip()
        for index,t in enumerate(mContnent):
            if t.startswith('@译    名'):
                moveInfo['translation'] = name
            elif t.startswith('@片  名'):
                name = pares_info(t,'@片    名')
                moveInfo['movie_title'] = name
            elif t.startswith('@年代'):
                name = pares_info(t,'@年代')
                moveInfo['movie_age'] = name
            elif t.startswith('@产地'):
                name = pares_info(t,'@产地')
                moveInfo['movie_place'] = name
            elif t.startswith('@类别'):
                name = pares_info(t,'@类别')
                moveInfo['category'] = name
            elif t.startswith('@语言'):
                name = pares_info(t,'@语言')
                moveInfo['language'] = name
            elif t.startswith('@字幕'):
                name = pares_info(t,'@字幕')
                moveInfo['subtitle'] = name
            elif t.startswith('@上映日期'):
                name = pares_info(t,'@上映日期')
                moveInfo['release_date'] = name
            elif t.startswith('@豆瓣评分'):
                name = pares_info(t,'@豆瓣评分')
                moveInfo['douban_score'] = name
            elif t.startswith('@时长'):
                name = pares_info(t,'@时长')
                moveInfo['file_length'] = name
            elif t.startswith('@导演'):
                name = pares_info(t,'@导演')
                moveInfo['director'] = name
            elif t.startswith('@编剧'):
                name = pares_info(t,'@编剧')
                writers = [name]
                for i in range(index + 1,len(mContnent)):
                    writer = mContnent[i].stript()
                    if writer.staetswith('@'):
                        break
                    writers.append(writer)
                moveInfo['screenwriter'] = writers
            elif t.startswith('@主演'):
                name = pares_info(t,'@主演')
                moveInfo['movie_age'] = name
            elif t.startswith('@标签'):
                name = pares_info(t,'@标签')
                moveInfo['movie_age'] = name
            elif t.startswith('@简介'):
                name = pares_info(t,'@简介')
                moveInfo['movie_age'] = name
            elif t.startswith('@获奖情况'):
                name = pares_info(t,'@获奖情况')
                moveInfo['movie_age'] = name