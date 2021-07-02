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
            if t.startswith('◎译    名'):
                moveInfo['translation'] = name
            elif t.startswith('◎片  名'):
                name = pares_info(t,'◎片    名')
                moveInfo['movie_title'] = name
            elif t.startswith('◎年代'):
                name = pares_info(t,'◎年代')
                moveInfo['movie_age'] = name
            elif t.startswith('◎产地'):
                name = pares_info(t,'◎产地')
                moveInfo['movie_place'] = name
            elif t.startswith('◎类别'):
                name = pares_info(t,'◎类别')
                moveInfo['category'] = name
            elif t.startswith('◎语言'):
                name = pares_info(t,'◎语言')
                moveInfo['language'] = name
            elif t.startswith('◎字幕'):
                name = pares_info(t,'◎字幕')
                moveInfo['subtitle'] = name
            elif t.startswith('◎上映日期'):
                name = pares_info(t,'◎上映日期')
                moveInfo['release_date'] = name
            elif t.startswith('◎豆瓣评分'):
                name = pares_info(t,'◎豆瓣评分')
                moveInfo['douban_score'] = name
            elif t.startswith('◎时长'):
                name = pares_info(t,'◎时长')
                moveInfo['file_length'] = name
            elif t.startswith('◎导演'):
                name = pares_info(t,'◎导演')
                moveInfo['director'] = name
            elif t.startswith('◎编剧'):
                name = pares_info(t,'◎编剧')
                writers = [name]
                for i in range(index + 1,len(mContnent)):
                    writer = mContnent[i].stript()
                    if writer.staetswith('◎'):
                        break
                    writers.append(writer)
                moveInfo['screenwriter'] = writers
            elif t.startswith('◎主演'):
                name = pares_info(t,'◎主演')
                actor = [name]
                for i in range(index + 1,len(mContnent)):
                    actor = mContnent[i].stript()
                    if actor.startswith('◎'):
                        break
                    actor.append(actor)
                moveInfo['stars'] = "".join(actor)
            elif t.startswith('◎标签'):
                name = pares_info(t,'◎标签')
                moveInfo['tags'] = name
            elif t.startswith('◎简介'):
                name = pares_info(t,'◎简介')
                prfiles = []
                for i in range(index + 1,len(mContnent)):
                    profile = mContnent[i].stript()
                    if profile.startswith('◎获奖情况') or '【下载地址】' in profile:
                        break
                    profile.append(profile)
                moveInfo['introduction'] = " ".join(profile)
            elif t.startswith('◎获奖情况'):
                name = pares_info(t,'◎获奖情况')
                awards = []
                for i in range(index + 1,len(mContnent)):
                    awards = mContnent[i].strip()
                    if '【下载地址】'in award:
                        break
                    awards.append(award)
                moveInfo['awards'] = " ".join(awards)
        moveInfo['movie_url'] = url
        return moveInfo
    
#获取前n页中所有电影的详情页href
def spider():
    #链接数据库
    base_url = 'https://www.dy2018.com/html/gndy/dyzz/index_{}.html'
    moves = []
    m = int(input('请输入您要获取的开始页：'))
    n = int(input('请输入您要获取的结束页：'))
    print('即将写入第{}页到第{}页的电影信息，请稍后...'.format(m, n))
    for i in range(m,n+1):
        print('******* 第{}页电影 正在写入 ********'.format(i))
        if i == 1:
            url = "https://www.dy2018.com/html/gndy/dyzz/"
        else:
            url = base_url.format(i)
        moveHref = getHref(url)
        print("休息2s后再进行操作")
        time.sleep(2)
        for index,mhref in enumerate(moveHref):
            print('---- 正在处理第{}部电影----'.format(index+1))
            move = getPage(mhref)
            moves.append(move)
    # 将电影信息写入数据库
    db = pymysql.connect(host='127.0.0.1',user='root', password='123456', port=3306, db='你的数据库名称')
    table = 'movies'
    i = 1
    for data in moves:
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'INSERT INTO {table}(id,{keys}) VALUES (null,{values})'.format(table=table, keys=keys, values=values)
        try:
            cursor = db.cursor()
            cursor.execute(sql, tuple(data.values()))
            print('本条数据成功执行!')
            if i%10==0:
                db.commit()
        except Exception as e:
            print('将电影信息写入数据库发生异常!',repr(e))
            db.rollback()
        cursor.close()
        i = i + 1
    db.commit()
    db.close()
    print('写入数据库完成！')

if __name__ == '__main__':
    spider()