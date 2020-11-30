import json

# str= "吃葡萄不吐葡萄皮,不吃葡萄倒吐葡萄皮"

### test ###
def ngram(context, n):
     return [str[i:i+n] for i in range(0, len(str)-1)]

# bigram = ngram(str, 3)
# print(bigram)

resultList = []
with open ('test_ws.json') as jf:
# with open ('truth_ws.json') as jf:
    data = json.load(jf)
    for dic in data:
        resultDic = {}
        for k, m in dic.items():
            resultDic[k] = m
            if k == "source" and m!="":
                str = m
                resultDic['sourc_bigram'] = ngram(str, 2)
                resultDic['source_trigram'] = ngram(str, 3)
            elif k == "source" and m=="":
                resultDic['sourc_bigram'] = ""
                resultDic['source_trigram'] = ""
            elif k == "truth" and m!= "":
                str = m
                resultDic['truth_bigram'] = ngram(str, 2)
                resultDic['truth_trigram'] = ngram(str, 3)
            elif k == "truth" and m=="":
                resultDic['truth_bigram'] = ""
                resultDic['truth_trigram'] = ""
        print("title: ", resultDic['title'])
        resultList.append(resultDic)
jf.close()

output = json.dumps(resultList, ensure_ascii=False).encode('utf-8')
with open('test_ws_ngram.json', 'w', encoding='utf-8') as f:
# with open('truth_ws_ngram.json', 'w', encoding='utf-8') as f:
    f.write(output.decode())
f.close()