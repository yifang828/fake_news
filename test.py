import re
import emoji

def getEmoji(str):
    return ''.join(c for c in str if c in emoji.UNICODE_EMOJI)

str="\n\n要回電*❗❗❗另外，❗❗}❗}\t不要按90號或09號"

print(getEmoji(str))

# filtEscapeChar = re.sub("\s", "", str)
# text = emoji.demojize(filtEscapeChar)
# filted = re.sub(':\S+?:', '', text)