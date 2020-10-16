import urllib.request as req
import json
import bs4
import math
import time
import re

def getHtmlData(url):
    request=req.Request(url, headers={
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
    })
    with req.urlopen(request) as resp:
        data=resp.read().decode("utf-8")
    return data
#label 3:
def getLabel3(rawTitle):
    label3=""
    if '】'in rawTitle and '【'in rawTitle:
        label3 = rawTitle.split('】', 1)[0].split('【', 1)[1]
    return label3

#label 4
def getLabel4NTitle(rawTitle):
    label4NTitle = []
    label4 = ""
    title = ""
    if '？'in rawTitle and '】'in rawTitle:
        label4 = rawTitle.rsplit('？',1)[1]
        title = rawTitle.rsplit('？',1)[0].split('】', 1)[1]
    elif '？'in rawTitle:
        label4 = rawTitle.rsplit('？',1)[1]
        title = rawTitle.rsplit('？',1)[0]
    elif '】'in rawTitle:
        label4 = ""
        title = rawTitle.split('】', 1)[1]
    else:
        label4 = ""
        title = rawTitle
    label4NTitle.append(label4)
    label4NTitle.append(title)
    return label4NTitle
            
#source:
def rumorSrc(data):
    rumor = data.find("blockquote", class_="tr_bq")
    if(rumor==None):
        return ""
    else:
        return rumor.get_text()

#truth:
def truth(data):
    yestrue = data.find("blockquote", class_="yestrue")
    return yestrue.get_text()


def main(jsonData):
    entries = jsonData["feed"]["entry"]
    for entry in entries:
        link = entry["link"][-1]["href"].replace(' ', '%20')
        rawTitle = entry["link"][-1]["title"]

        dic = {
            "label 1": "謠言改編"
        }
        try:
            dic["label 2"] = entry["category"][0]["term"]
            dic["label 3"] = getLabel3(rawTitle)
            dic["label 4"] = getLabel4NTitle(rawTitle)[0]
            dic["title"] = getLabel4NTitle(rawTitle)[1]
            
            rumorData = getHtmlData(link)
            root=bs4.BeautifulSoup(rumorData, "html.parser")
            dic["source"] = rumorSrc(root)
            dic["truth"] = truth(root)
            result.append(dic)
        except Exception as e:
            print(e)
            print("this is dic:")
            print(dic)

def getPages(page):
    htmlData = getHtmlData(page)
    splited = htmlData.split('(',1)[1].rsplit(')',1)[0]
    jsonData = json.loads(splited)
    pages = math.ceil(int(jsonData["feed"]["openSearch$totalResults"]["$t"])/7)
    return pages

result=[]
pageUrl = "https://www.mygopen.com/feeds/posts/default/-/%E8%AC%A0%E8%A8%80?alt=json-in-script&start-index=1&max-results=7"
pages = getPages(pageUrl)
for p in range(pages):
    idx = 7*p+1
    print(idx)
    url = "https://www.mygopen.com/feeds/posts/default/-/%E8%AC%A0%E8%A8%80?alt=json-in-script&start-index="+str(idx)+"&max-results=7"
    htmlData = getHtmlData(url)
    splited = htmlData.split('(',1)[1].rsplit(')',1)[0]
    jsonData = json.loads(splited)
    main(jsonData)
    time.sleep(15)

##test
# url = "https://www.mygopen.com/feeds/posts/default/-/%E8%AC%A0%E8%A8%80?alt=json-in-script&start-index=288&max-results=7"
# htmlData = getHtmlData(url)
# splited = htmlData.split('(',1)[1].rsplit(')',1)[0]
# jsonData = json.loads(splited)
# main(jsonData)
##
output = json.dumps(result, ensure_ascii=False).encode('utf8')
with open("rumor.json",'w',encoding="utf-8") as f:
    f.write(output.decode())