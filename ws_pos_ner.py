from ckiptagger import data_utils, construct_dictionary, WS, POS, NER
import json

# data_utils.download_data_gdown("./") ＃只要下載一次就好
ws= WS("./data")
pos= POS("./data")
ner= NER("./data")

# sentence_list = [
#     '你可以先知道：這是老謠言組合改編，並沒有這種狀況。\n這是一則資深謠言的組合，來自「早安、晚安問候圖片影片，暗藏中美俄日駭客釣魚程式竊取個資」和\
#     「未接到的電話都不要回撥，可能來自 ISIS」這兩則謠言，是相同的片段內容改編。\n  \n過去 MyGoPen 在 2017 年也分別澄清過，警政署 165 反詐騙以及\
#     資安人員調查都澄清過。關於「問候圖片和影片的釣魚暗藏釣魚程式」的說法，資安人員表示這類多隱藏在網址當中，藏在影片或文章中的釣魚程式，應該是\
#     「不太可能」。刑事局人員對此也表示，個人資料並不會下載或觀看影片就騙，即使被騙也不會因為刪除照片或影片就安全無虞。\n\n另外關於「威脅到您手機\
#     的恐怖份子來電」的說法，過去 165 反詐騙表示：經查證此為網路謠言，請勿再轉傳。但有提醒來電號碼前有 + 字號為境外來電，經常遭詐騙集團利用竄改門號\
#     技術撥入國內實施詐騙（如解除分期付款），而響聲掛斷亦係常見的詐騙手法，切勿輕易回撥造成損失。'
# ]

# word_sentence_list = ws(
#     sentence_list,
    # sentence_segmentation = True, # To consider delimiters
    # segment_delimiter_set = {",", "。", ":", "?", "!", ";"}), # This is the defualt set of delimiters
    # recommend_dictionary = dictionary1, # words in this dictionary are encouraged
    # coerce_dictionary = dictionary2, # words in this dictionary are forced
# )

# pos_sentence_list = pos(word_sentence_list)

# entity_sentence_list = ner(word_sentence_list, pos_sentence_list)

# def print_word_pos_sentence(word_sentence, pos_sentence):
#     assert len(word_sentence) == len(pos_sentence)
#     for word, pos in zip(word_sentence, pos_sentence):
#         print(f"{word}({pos})", end="\u3000")
#     print()
#     return
    
# for i, sentence in enumerate(sentence_list):
#     print()
#     print(f"'{sentence}'")
#     print_word_pos_sentence(word_sentence_list[i],  pos_sentence_list[i])
#     for entity in sorted(entity_sentence_list[i]):
#         print(entity)

def getWsPos(wsList, posList, sentenceList):
    resultStr=""
    for i, sentence in enumerate(sentenceList):
        assert len(wsList[i])==len(posList[i])
        for word, pos in zip(wsList[i], posList[i]):
            resultStr += f'{word}({pos}) '
            # print("resultStr: "+resultStr+"\n")
    return resultStr

resultList = []
with open ('test.json') as jf:
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
                resultDic['src_ner'] = ner(wsList, posList).replace('(', '[').replace(')',']')
                print(resultDic['src_ner'])
            elif k == "source" and m=="":
                resultDic['src_ws_pos'] = ""
                resultDic['src_ner'] = ""
            elif k == "truth" and m!= "":
                sentenceList=[m]
                wsList = ws(sentenceList)
                posList = pos(wsList)
                resultDic['truth_ws_pos'] = getWsPos(wsList, posList, sentenceList)
                resultDic['truth_ner'] = ner(wsList, posList).replace('(', '[').replace(')',']')
                print(resultDic['truth_ner'])
            elif k == "truth" and m=="":
                resultDic['truth_ws_pos'] = ""
                resultDic['truth_ner'] = ""
        resultList.append(resultDic)
# print(resultList)
jf.close()

output = json.dumps(resultList, ensure_ascii=False).encode('utf8')
with open("test_ws.json", 'w', encoding='utf-8')as f:
    f.write(output.decode())
f.close()