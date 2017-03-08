import re
from urllib import request
import re


#处理页面标签类
class Tool:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()将前后多余内容删除
        return x.strip()


class BDtieba:
    # baseUrl = http://tieba.baidu.com/p/3138733512
    def __init__(self, baseUrl, see_lz):
        self.baseUrl = baseUrl
        self.see_lz = '?see_lz=' + str(see_lz)
        self.tool = Tool()
        self.header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36'
        }
        self.file = None

    # get the web html source
    def getHtml(self,pageNum):
        try:
            url = self.baseUrl + self.see_lz + '&pn=' + str(pageNum)
            req = request.Request(url, None, self.header)
            response = request.urlopen(req, timeout=2000)
            html = response.read().decode('utf-8')
            return html
        except request.URLError as e:
            print("NetWork error，please retry...",e)
            return None

    # get title
    def getTitle(self, pageHtml):
        # pageHtml = self.getHtml(1)
        pattern = re.compile(r'<h3 class="core_title_txt.*?>([\s\S]*?)</h3>', re.S)
        if pageHtml is not None:
            result = re.search(pattern, pageHtml)
            if result:
                print(result)
                return result.group(1).strip()
            else:
                return None
        else:
            return None

    def getPageSize(self,pageHtml):
        if pageHtml is None:
            return
        pattern = re.compile(r'<li class="l_reply_num"[\s\S]*?<span class="red">(\d)</span>',re.S)
        result = re.search(pattern, pageHtml)
        # print(result)
        return result.group(1).strip()

    def getContent(self, pageHtml):
        if pageHtml is None:
            return
        pattern = re.compile(r'<div id="post_content_.*?>(.*?)</div>',re.S)
        items = re.findall(pattern, pageHtml)
        content = []
        for item in items:
            itm = self.tool.replace(item)
            print(itm)
            content.append(itm)
        # print(self.tool.replace(items[2]))
        return content


if __name__ == '__main__':
    #NBA tieba Source
    tieba = BDtieba('http://tieba.baidu.com/p/3138733512', 1)
    txt = tieba.getHtml(1)
    title = tieba.getTitle(txt)
    pageSize = tieba.getPageSize(txt)
    print("TITLE :", title)
    content = tieba.getContent(txt)
    file = open('../resource/tieba.txt', 'w')
    file.write("标题："+ title+"\n")
    floor = 1
    for item in content:
        file.write('\n' + str(floor) + "-" * 100 + '\n')
        file.writelines(item)
        floor += 1




