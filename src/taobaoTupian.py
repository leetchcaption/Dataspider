# -*- coding:utf-8 -*-
from urllib import request
import re
import os
class Spider:

    #页面初始化
    def __init__(self):
        self.siteURL = 'http://mm.taobao.com/json/request_top_list.htm'
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36'
        }

    def getPage(self,pageIndex):
        url = self.siteURL + "?page=" + str(pageIndex)
        req = request.Request(url, None, self.headers)
        response = request.urlopen(req)
        return response.read().decode('gbk')

    def getContents(self, pageIndex):
        page = self.getPage(pageIndex)
        pattern = re.compile(
            r'<div class="list-item".*?pic-word.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name.*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',re.S)
        items = re.findall(pattern,page)
        contents = []
        for item in items:
            contents.append([item[0],item[1],item[2],item[3],item[4]])
        return contents

    def getDetailPage(self,infoURL):
        response = request.urlopen(infoURL)
        return response.read().decode('utf-8')

    # getBrief
    def getBrief(self,page):
        pattern = re.compile(
            r'<div class="mm-aixiu-content".*?>(.*?)<!--',re.S)
        result = re.search(pattern,page)
        return result.group(1)

    # get all pictures
    def getAllImg(self,page):
        pattern = re.compile(
            r'<div class="mm-aixiu-content".*?>(.*?)<!--',re.S)
        content = re.search(pattern,page)
        patternImg = re.compile(
            r'<img.*?src="(.*?)"',re.S)
        images = re.findall(patternImg,content.group(1))
        return images

    # save images
    def saveImgs(self,images,name):
        number = 1
        print(u"发现",name,u"共有",len(images),u"张照片")
        for imageURL in images:
            splitPath = imageURL.split('.')
            fTail = splitPath.pop()
            if len(fTail) > 3:
                fTail = "jpg"
            fileName = name + "/" + str(number) + "." + fTail
            self.saveImg(imageURL,fileName)
            number += 1

    def saveIcon(self,iconURL,name):
        splitPath = iconURL.split('.')
        fTail = splitPath.pop()
        fileName = name + "/icon." + fTail
        self.saveImg(iconURL,fileName)

    def saveBrief(self,content,name):
        fileName = name + "/" + name + ".txt"
        f = open(fileName,"w+")
        print (u"正在保存她的个人信息为",fileName)
        f.write(content.encode('utf-8'))

    def saveImg(self,imageURL,fileName):
         u = request.urlopen(imageURL)
         data = u.read()
         f = open(fileName, 'wb')
         f.write(data)
         print (u"正在悄悄保存她的一张图片为",fileName)
         f.close()

    def mkdir(self,path):
        path = path.strip()
        isExists=os.path.exists(path)
        if not isExists:
            print(u"新建了名字叫做",path,u'的文件夹')
            os.makedirs(path)
            return True
        else:
            print(u"名为",path,'的文件夹已经创建成功')
            return False

    def savePageInfo(self,pageIndex):
        contents = self.getContents(pageIndex)
        for item in contents:
            print (u"发现一位模特,名字叫",item[2],u"芳龄",item[3],u",她在",item[4])
            print (u"正在偷偷地保存",item[2],"的信息")
            print (u"又意外地发现她的个人地址是",item[0])
            detailURL = item[0]
            detailPage = self.getDetailPage(detailURL)
            brief = self.getBrief(detailPage)
            images = self.getAllImg(detailPage)
            self.mkdir(item[2])
            #保存个人简介
            self.saveBrief(brief,item[2])
            #保存头像
            self.saveIcon(item[1],item[2])
            #保存图片
            self.saveImgs(images,item[2])

    #传入起止页码，获取MM图片
    def savePagesInfo(self,start,end):
        for i in range(start,end+1):
            print (u"正在偷偷寻找第",i,u"个地方，看看MM们在不在")
            self.savePageInfo(i)


#传入起止页码即可，在此传入了2,10,表示抓取第2到10页的MM
if __name__ == "__main__":
    spider = Spider()
    spider.savePagesInfo(2,10)