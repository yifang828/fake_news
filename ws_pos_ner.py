from ckiptagger import data_utils, construct_dictionary, WS, POS, NER

# data_utils.download_data_gdown("./") ＃只要下載一次就好
ws= WS("./data")
pos= POS("./data")
ner= NER("./data")

sentence_list = [
    # "明天開始，就不發了網絡圖片了，看看下面的文章就明白了。請儘快刪除所有“早上好”、“晚上好”等問候內容的照片和視頻。仔細閱讀下面的文章，\
    # 你就會很清楚爲什麼我要作這個提示。從現在開始，我將只發送個人自己製作的問候照片和視頻。閱讀全部！請緊急向儘可能多的朋友發送此消息，\
    # 以阻止不法的入侵。奧爾加·尼古拉耶夫娜（Olga Nikolaevna）律師的警告：注意！對於那些喜歡發送“早安”！“美好的一天！”、“晚上好！”\
    # 圖片的人，請你不要發送這些“好”消息。今天，《上海中國國際新聞》向所有訂閱者發送了SOS（這是第三次提醒），專家建議：請勿發送早安，晚安的圖片和視頻等。\
    # 報告顯示，攻擊中國的黑客設計了這些圖像，這些圖片和視頻都很美，但是，其中隱藏了網絡釣魚代碼，當每個人發送這些消息時，黑客們就使用您的設備來竊取個人\
    # 信息，例如銀行卡信息和數據，並可破解您的手機。據報道，已有超過500,000名受害者受欺詐，上當受騙。如果您想與其他人打招呼，請您自己寫下您自己的祝福和\
    # 問候，發送自己製作的問候圖片和視頻，這樣您可以保護您自己以及您的家人和朋友。重要！爲了安全起見，請您務必刪除手機上所有外來的問候留言和圖片。如果有人向\
    # 您發送了此類圖片，請立即將其從設備上刪除。惡意代碼需要花費一些時間來部署，因此，如果您立即採取行動，將不會造成任何危害。告訴您所有的朋友，以防止被\
    # 黑客入侵。用自己的話打招呼，只發送您自己創建的圖像和視頻來問候，這對您自己，您的家人和朋友，都是完全安全的。請正確理解我的意思！所有人的手機都附有\
    # 銀行卡，每個人的手機都有很多聯繫人。這種黑客製作的問候圖片，不僅會對您自己構成威脅，而且還會威脅到您的手機，朋友和熟人中的所有聯繫人！ 這是一個\
    # 殘酷的現實！️！️！️有些人已經收到以下號碼的電話：電話：+375602605281，電話：+37127913091電話：+37178565072電話：+56322553736電話：+37052529259\
    # 電話：+255901130460或來自+371至+375 * 381❗❗❗如果您回電，他們可以在3秒鐘內複製您的聯繫人列表，並且如果您的電話包含銀行卡或信用卡信息，\
    # 它也可以複製。代碼+375-白俄羅斯。代碼+371-拉脫維亞。+381-塞爾維亞+ 563-瓦爾帕萊索+ 370-維爾紐斯+ 255-坦桑尼亞這些電話可能來自ISIS。❗❗❗\
    # *永遠不要回答*和*不要回電*❗❗❗另外，❗❗}❗}不要按90號或09號，不要應任何訂戶的請求在您的手機上顯示。這是恐怖分子用來探訪您手機SIM卡的一種\
    # 新技巧，使您成爲其同夥！！！***將此消息發送給您儘可能多的親戚和朋友，以阻止任何未經授權的入侵！！！"
    "你可以先知道：這是老謠言組合改編，並沒有這種狀況。\n這是一則資深謠言的組合，來自「早安、晚安問候圖片影片，暗藏中美俄日駭客釣魚程式竊取個資」和\
    「未接到的電話都不要回撥，可能來自 ISIS」這兩則謠言，是相同的片段內容改編。\n  \n過去 MyGoPen 在 2017 年也分別澄清過，警政署 165 反詐騙以及\
    資安人員調查都澄清過。關於「問候圖片和影片的釣魚暗藏釣魚程式」的說法，資安人員表示這類多隱藏在網址當中，藏在影片或文章中的釣魚程式，應該是\
    「不太可能」。刑事局人員對此也表示，個人資料並不會下載或觀看影片就騙，即使被騙也不會因為刪除照片或影片就安全無虞。\n\n另外關於「威脅到您手機\
    的恐怖份子來電」的說法，過去 165 反詐騙表示：經查證此為網路謠言，請勿再轉傳。但有提醒來電號碼前有 + 字號為境外來電，經常遭詐騙集團利用竄改門號\
    技術撥入國內實施詐騙（如解除分期付款），而響聲掛斷亦係常見的詐騙手法，切勿輕易回撥造成損失。"
]

word_sentence_list = ws(
    sentence_list,
    # sentence_segmentation = True, # To consider delimiters
    # segment_delimiter_set = {",", "。", ":", "?", "!", ";"}), # This is the defualt set of delimiters
    # recommend_dictionary = dictionary1, # words in this dictionary are encouraged
    # coerce_dictionary = dictionary2, # words in this dictionary are forced
)

pos_sentence_list = pos(word_sentence_list)

entity_sentence_list = ner(word_sentence_list, pos_sentence_list)

def print_word_pos_sentence(word_sentence, pos_sentence):
    assert len(word_sentence) == len(pos_sentence)
    for word, pos in zip(word_sentence, pos_sentence):
        print(f"{word}({pos})", end="\u3000")
    print()
    return
    
for i, sentence in enumerate(sentence_list):
    print()
    print(f"'{sentence}'")
    print_word_pos_sentence(word_sentence_list[i],  pos_sentence_list[i])
    for entity in sorted(entity_sentence_list[i]):
        print(entity)