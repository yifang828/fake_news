from ckiptagger import data_utils, construct_dictionary, WS, POS, NER
import json

# data_utils.download_data_gdown("./") ＃只要下載一次就好
ws= WS("./data")
pos= POS("./data")
ner= NER("./data")

def getWsPos(wsList, posList, sentenceList):
    resultStr=""
    for i, sentence in enumerate(sentenceList):
        assert len(wsList[i])==len(posList[i])
        for word, pos in zip(wsList[i], posList[i]):
            resultStr += f'{word}({pos}) '
    return resultStr

def getNer(wsList, posList):
    nerList = ner(wsList, posList)
    nerList = list(nerList[0])
    return nerList

resultList = []
with open ('rumor.json') as jf:
    data = json.load(jf)
    for dic in data:
        resultDic ={}
        for k, m in dic.items():
            resultDic[k] = m
            if k == "source" and m!="":
                sentenceList=[m]
                wsList = ws(sentenceList)
                posList = pos(wsList)
                resultDic['src_ws_pos'] = getWsPos(wsList, posList,sentenceList)
                resultDic['src_ner'] = getNer(wsList, posList)
            elif k == "source" and m=="":
                resultDic['src_ws_pos'] = ""
                resultDic['src_ner'] = ""
            elif k == "truth" and m!= "":
                sentenceList=[m]
                wsList = ws(sentenceList)
                posList = pos(wsList)
                resultDic['truth_ws_pos'] = getWsPos(wsList, posList, sentenceList)
                resultDic['truth_ner'] = getNer(wsList, posList)
            elif k == "truth" and m=="":
                resultDic['truth_ws_pos'] = ""
                resultDic['truth_ner'] = ""
        print(resultDic)
        resultList.append(resultDic)
jf.close()

output = json.dumps(resultList, ensure_ascii=False).encode('utf8')
with open("rumor_ws.json", 'w', encoding='utf-8')as f:
    f.write(output.decode())
f.close()