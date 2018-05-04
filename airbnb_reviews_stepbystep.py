# -*- coding: utf-8 -*-
import re
import jieba
import operator
import pandas as pd
from collections import Counter
from hanziconv import HanziConv

#keywords = ['棒','好','讚']

# 常見且和正負向非常相關的詞
keywords = ['nice', '711','7-11','夜市','捷運']

# 常見但和正負向較無關的詞
stopwords = ['房客','房主','屋主','主人','房子','房間','房東','高雄','台北','桃園','北市','台中','台南','入住','就是','可以','我們','阿姨','大姐','地方','附近','民宿','位置','地點','住宿','老板','台灣', '機會', '一定']

#stopwords = ['房主','屋主','主人','房子','房間','房间','房東','房东','高雄','台北','桃園','北市','台中','台南','入住','就是','可以','我們','我们','阿姨','大姐','地方','附近','民宿','位置','地點','住宿','老板','台灣','台湾', '機會', '一定']

#with open('四川大学机器智能实验室停用词库.txt', 'rb') as f:
#    s_han = [linestr.decode('gb2312').strip() for linestr in f.readlines()]

# 簡體stopwords(轉繁)
with open('四川大学机器智能实验室停用词库.txt', 'rb') as f:
    s_han = [HanziConv.toTraditional(linestr.decode('gb2312').strip()) for linestr in f.readlines()]

# 手動生成繁體字stopwords
with open('dict.txt.big.txt','r') as f:
    s_big = [line.split()[0] for line in f.readlines() if ( int(line.split()[1])>5000 and len(line.split()[0])>1 and 'a' not in line.split()[2])]

stopwords.extend(s_han)
stopwords.extend(s_big)
stopwords = list(set(stopwords))
stopwords.extend(['的','也'])


def LongTermFirst(cmt_sent_Ary, max_n, DICT):
    for i in range(max_n, 1, -1):
        print('n-gram:', i)
        words = []
        for ix, cmt_sent in enumerate(cmt_sent_Ary):
            #if ix % 100000 == 0:
            #    print(ix)
            part_cmt = remove(cmt_sent, map(operator.itemgetter(0), DICT) )
            words.extend(ngram(part_cmt, i))
        c = Counter(words)
        print(c.most_common(100))
        DICT.extend([(k,v) for k,v in c.items() if v > 500])
        print(len(DICT))
    return DICT


def preprocess(df, stopwords):
    #split and remove stopwords
    cmt_sent_Ary = []
    for row in df.iterrows():
        if row[0] % 100000 == 0: 
            print(row[0])
            
        # 只處理中文
        if row[1].language not in ['zh-TW', 'zh-CN', 'zh']:
            continue
        
        # 把簡體評價轉繁
        if row[1].language in ['zh', 'zh-CN']:
            #print(row[0], row[1].comments)
            row[1].comments = HanziConv.toTraditional(row[1].comments)
            #print(row[1].comments)
        cmt = remove(row[1].comments, stopwords)
        cmt_seg = re.split('~|\*|\.|\r|\n|,|，|。|（|）|〕|〔|／|《|》|、|」|!|！|「|：', cmt) # 利用分隔符號切分語句
        #print(cmt_seg)
        cmt_sent_Ary.extend(cmt_seg)
    return cmt_sent_Ary


def remove(text, words):
    ret = text
    for kw in words:
        ret = ret.replace(kw, '')
    return ret


def ngram(text, n=2):
    words = []
    for i in range( len(text) - n + 1 ):
        if ' ' not in text[i:i+n]:
            words.append(text[i:i+n])
    return words


def main(df):
    cmt_sent_Ary = preprocess(df, stopwords)
    keywords = LongTermFirst(cmt_sent_Ary, 4, keywords)
    return keywords


if __name__ == '__main__':
    kw = main(df)

## 離捷運站近 乾淨整潔 乾淨舒適 
## 改善簡轉繁 "合" "台" ""
## 簡轉繁 取兩字形容詞
## Prediction 
## 英文 
## 架構for cmt in cmts  ->  cmt_sent_ary  ->  cmt_sent_arys  -> keywords  -> manually distinguish 
# ### keywords 選出來後，篩詞性？
# ### 篩詞性 (只留形容詞?)
# ### 更多的留言
# ## 目前問題：只能抓到正向詞，沒辦法抓到負向詞
# # 有點 隔音 可惜 美中不足 雖然 雖小 缺點 遺憾 不方便
# ## 可以再接回去使用 jieba內部的function? ex.hmm(?)
# ## 想移除英文但"nice" 第一名？
# ### stopwords? (1-gram most_common: 的 了 有 很 好 住)
# ### 超級 超 非常 很 aware-word? 要注意接續的字？
## default keywords? ex. 乾淨 熱情？
## 711 7-11 捷運 夜市屬於正向詞
## 手工跑出來的 如何標詞性？ 若可標，則可找出形容詞+'超,非常,很'

adj = [w for w in kw if (len(w[0])==3 and w[1]>800 and not re.search('[a-zA-Z0-9]', w[0])) ]
sorted(adj_2, key=operator.itemgetter(1), reverse=True)

[w for w in kw if (w[1]>1000 and not re.search('[a-zA-Z]', w[0])) ]
filter(lambda w: w[1]>900, kw)
