import jieba
import jieba.posseg
import pandas as pd
import collections                  # 词频统计库
from wordcloud import WordCloud
import matplotlib.pyplot as plt

df = pd.read_excel('微博-凤凰博文评论1.xlsx')
df = df[['评论时间','评论内容','二级评论内容','二级评论时间']]
print(df.head(3))

firstC=df[['评论时间','评论内容']]
firstC=firstC.drop_duplicates(subset='评论内容')    #不重复的一级评论
firstC.dropna(axis=0,subset = ["评论内容"])   # 丢弃"评论内容"列中有缺失值的行
print(firstC.head(3))
print(len(firstC))


secC=df[['二级评论时间','二级评论内容']]

secC=df.drop_duplicates(subset='二级评论内容')    #不重复的二级评论
secC.dropna(axis=0,subset = ["二级评论内容"])  # 丢弃"评论内容"列中有缺失值的行

print(secC.head(3))
firstCdata = firstC['评论内容'].astype({'评论内容':'string'})

firstCdata = firstCdata.astype(str)
a=firstCdata.to_string()

import re
pattern = re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|"[1-9]\\d{0,2}|"') # 定义正则表达式匹配模式（空格等）
a = re.sub(pattern, '', a)     # 将符合模式的字符去除

seg_list_exact = jieba.cut(a)


object_list = []
number=1000
with open('停用词库.txt', 'r', encoding='UTF-8') as meaninglessFile:
    stopwords = set(meaninglessFile.read().split('\n'))
stopwords.add(' ')
for word in seg_list_exact:         # 循环读出每个分词
    if word not in stopwords:       # 如果不在去除词库中
        object_list.append(word)    # 分词追加到列表
word_counts = collections.Counter(object_list)       # 对分词做词频统计
word_counts_top = word_counts.most_common(number)    # 获取前number个最高频的词
#中英转换
En2Cn = {
    'a'    : '形容词',
    'ad'   : '形容词',
    'ag'   : '形容词',
    'al'   : '形容词',
    'an'   : '形容词',
    'b'    : '区别词',
    'bl'   : '区别词',
    'c'    : '连词',
    'cc'   : '连词',
    'd'    : '副词',
    'e'    : '叹词',
    'eng'  : '英文',
    'f'    : '方位词',
    'g'    : '语素',
    'h'    : '前缀',
    'i'    : '成语',
    'j'    : '简称略语',
    'k'    : '后缀',
    'l'    : '习用语',
    'm'    : '数词',
    'mq'   : '数量词',
    'n'    : '名词',
    'ng'   : '名词',
    'nl'   : '名词',
    'nr'   : '名词',
    'nr1'  : '名词',
    'nr2'  : '名词',
    'nrf'  : '名词',
    'nrfg' : '名词',
    'nrj'  : '名词',
    'ns'   : '名词',
    'nsf'  : '名词',
    'nt'   : '名词',
    'nz'   : '名词',
    'o'    : '拟声词',
    'p'    : '介词',
    'pba'  : '介词',
    'pbei' : '介词',
    'q'    : '量词',
    'qt'   : '量词',
    'qv'   : '量词',
    'r'    : '代词',
    'rg'   : '代词',
    'rr'   : '代词',
    'rz'   : '代词',
    'rzs'  : '代词',
    'rzt'  : '代词',
    'rzv'  : '代词',
    'ry'   : '代词',
    'rys'  : '代词',
    'ryt'  : '代词',
    'ryv'  : '代词',
    's'    : '处所词',
    't'    : '时间词',
    'tg'   : '时间词',
    'u'    : '助词',
    'ude1' : '助词',
    'ude2' : '助词',
    'ude3' : '助词',
    'udeng': '助词',
    'udh'  : '助词',
    'uguo' : '助词',
    'ule'  : '助词',
    'ulian': '助词',
    'uls'  : '助词',
    'usuo' : '助词',
    'uyy'  : '助词',
    'uzhe' : '助词',
    'uzhi' : '助词',
    'v'    : '动词',
    'vd'   : '动词',
    'vf'   : '动词',
    'vg'   : '动词',
    'vi'   : '动词',
    'vl'   : '动词',
    'vn'   : '动词',
    'vshi' : '动词',
    'vx'   : '动词',
    'vyou' : '动词',
    'w'    : '标点符号',
    'wb'   : '标点符号',
    'wd'   : '标点符号',
    'wf'   : '标点符号',
    'wj'   : '标点符号',
    'wh'   : '标点符号',
    'wkz'  : '标点符号',
    'wky'  : '标点符号',
    'wm'   : '标点符号',
    'wn'   : '标点符号',
    'wp'   : '标点符号',
    'ws'   : '标点符号',
    'wt'   : '标点符号',
    'ww'   : '标点符号',
    'wyz'  : '标点符号',
    'wyy'  : '标点符号',
    'x'    : '字符串',
    'xu'   : '字符串',
    'xx'   : '字符串',
    'y'    : '语气词',
    'z'    : '状态词',
    'un'   : '未知词',
}
# 输出至工作台，并导出“词频.txt”文件
print ('\n词语\t词频\t词性')
print ('——————————')
fileOut = open('词频.txt','w',encoding='UTF-8')     # 创建文本文件；若已存在，则进行覆盖
fileOut.write('词语\t词频\n')
fileOut.write('——————————\n')
number= 100
count=0
for TopWord,Frequency in word_counts_top:                       # 获取词语和词频
                           # 获取词性
        if count == number:
            break
        print(TopWord + '\t',str(Frequency) )                    # 逐行输出数据
        fileOut.write(TopWord + '\t' + str(Frequency)+'\n') # 逐行写入str格式数据
        count += 1
fileOut.close()                                                 # 关闭文件


# 词频展示
import numpy
import wordcloud
from PIL import Image
print ('\n开始制作词云……')                    # 提示当前状态
mask = numpy.array(Image.open("background.png"))      # 定义词频背景
wc = wordcloud.WordCloud(
    font_path = 'C:/Windows/Fonts/simfang.ttf', # 设置字体（这里选择“仿宋”）
    background_color='white',                   # 背景颜色
    mask = mask,                                # 文字颜色+形状（有mask参数再设定宽高是无效的）
    max_words = number,                         # 显示词数
    max_font_size = 150                         # 最大字号
)

wc.generate_from_frequencies(word_counts)                                        # 从字典生成词云
wc.recolor(color_func=wordcloud.ImageColorGenerator(mask))                       # 将词云颜色设置为背景图方案
plt.figure('词云')                                                               # 弹框名称与大小
plt.subplots_adjust(top=0.99,bottom=0.01,right=0.99,left=0.01,hspace=0,wspace=0) # 调整边距
plt.imshow(wc, cmap=plt.cm.gray, interpolation='bilinear')                       # 处理词云
plt.axis('off')                                                                  # 关闭坐标轴
print ('制作完成！')                                                             # 提示当前状态
print ('\n作者：丨小小花丨')
print ('日期：2020.01.16')
plt.savefig("wordcloud.png")
plt.show()