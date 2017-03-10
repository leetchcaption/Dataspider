from urllib import request
import re

class pictureSpider:
    def __init__(self, url):
        self.url = url
        self.header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36'
        }

    def getHtml(self):
        req = request.Request(self.url, None, self.header)
        response = request.urlopen(req, timeout=3000)
        html = response.read().decode('utf-8')
        return html

    def getPictures(self, html):
        pattern = re.compile(r'<img lowsrc="(.*?)"',re.S)
        items = re.findall(pattern, html)
        print(items)
        return items


if __name__ == '__main__':
    url = "http://www.quanjing.com/search.aspx"
    spider = pictureSpider(url)
    content = spider.getHtml()
    file = open('../resource/tupian.txt', 'w+')
    file.write('this is a file test!')
    file.writelines(content)
    iyems = spider.getPictures(content)
    print(content)