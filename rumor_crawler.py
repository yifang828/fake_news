import urllib.request as req
import json
import bs4
import math
import time
import re
import emoji

def getHtmlData(url):
    request=req.Request(url, headers={
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
    })
    with req.urlopen(request) as resp:
        data=resp.read().decode("utf-8")
    return data

def getEmoji(data):
    result = ''
    rumor = data.find("blockquote", class_="tr_bq")
    if(rumor!=None):
        result.join(c for c in rumor.get_text() if c in emoji.UNICODE_EMOJI)
    quoteStyle = data.find("div", class_="quote_style")
    if(quoteStyle!=None):
        result.join(c for c in quoteStyle.get_text() if c in emoji.UNICODE_EMOJI)
    yestrue = data.find("blockquote", class_="yestrue")
    if(yestrue!=None):
        result.join(c for c in yestrue.get_text() if c in emoji.UNICODE_EMOJI)
    return result

def textFilter(str):
    filtEscapeChar = re.sub("\s", "", str)
    text = emoji.demojize(filtEscapeChar)
    filted = re.sub(':\S+?:', '', text)
    return filted

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
    label4NTitle.append(textFilter(label4))
    label4NTitle.append(textFilter(title))
    return label4NTitle
            
#source:
def rumorSrc(data):
    rumor = data.find("blockquote", class_="tr_bq")
    if(rumor==None):
        global noRumor
        noRumor += 1
        return ""
    else:
        return textFilter(rumor.get_text())

#truth:
def truth(data):
    quoteStyle = data.find("div", class_="quote_style")
    if(quoteStyle==None):
        quoteStyle =""
    else:
        quoteStyle = textFilter(quoteStyle.get_text())
    yestrue = data.find("blockquote", class_="yestrue")
    if(yestrue==None):
        yestrue =""
    else:
        yestrue = textFilter(yestrue.get_text())
    if((quoteStyle + yestrue)==""):
        global noTruth
        noTruth += 1
    return quoteStyle + yestrue

def main(jsonData):
    entries = jsonData["feed"]["entry"]
    for entry in entries:
        link = entry["link"][-1]["href"].replace(' ', '%20')
        rawTitle = entry["link"][-1]["title"]

        dic = {
            "label 1": "謠言澄清"
        }
        try:
            dic["label 2"] = entry["category"][0]["term"]
            dic["label 3"] = getLabel3(rawTitle)
            dic["label 4"] = getLabel4NTitle(rawTitle)[0]
            dic["title"] = getLabel4NTitle(rawTitle)[1]
            
            rumorData = getHtmlData(link)
            root=bs4.BeautifulSoup(rumorData, "html.parser")
            dic["emoji"] = getEmoji(root)
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
noRumor = 0
noTruth = 0
for p in range(pages):
    idx = 7*p+1
    print(idx)
    url = "https://www.mygopen.com/feeds/posts/default/-/%E8%AC%A0%E8%A8%80?alt=json-in-script&start-index="+str(idx)+"&max-results=7"
    htmlData = getHtmlData(url)
    splited = htmlData.split('(',1)[1].rsplit(')',1)[0]
    jsonData = json.loads(splited)
    main(jsonData)
    time.sleep(3)
##test
# noRumor = 0
# noTruth = 0
# url = "https://www.mygopen.com/feeds/posts/default/-/%E8%AC%A0%E8%A8%80?alt=json-in-script&start-index=554&max-results=7"
# htmlData = getHtmlData(url)
# splited = htmlData.split('(',1)[1].rsplit(')',1)[0]
# jsonData = json.loads(splited)
# main(jsonData)
# print(result)
##
print("no rumor:"+str(noRumor)+",  no truth:"+str(noTruth))

output = json.dumps(result, ensure_ascii=False).encode('utf8')
with open("mygopen/rumor.json",'w',encoding="utf-8") as f:
    f.write(output.decode())