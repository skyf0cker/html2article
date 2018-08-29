'''
需要什么就去做，不懂什么就去思考
                            ——————编程界的贝克汉姆
'''
from sklearn import preprocessing
from bs4 import BeautifulSoup
import re
import jieba
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


'''
这里我们需要计算一下，文本字符数，超链接字符数
'''
def get_denisity(html):
    reg_0 = r'<script.*?>[\s\S]*?</script>'
    reg_1 = r'<style.*?>[\s\S]*?</style>'
    reg_8 = r'<!--.*?>'
    html = re.sub(reg_0, '', html)
    html = re.sub(reg_1, '', html)
    html = re.sub(reg_8, '', html)
    soup = BeautifulSoup(html,'lxml')
    content = soup.prettify()
    all_sen_list= content.split("。")
    all_sen_num = len(all_sen_list)
    con_list = content.split("\n")

    hash_table = {}

    with open('stopword.txt',encoding='utf-8') as stp:
        stp_list = [word.replace('\n', '') for word in stp.readlines()]
        reg_6 = r'[\u4e00-\u9fa5]'
        chi_list = re.findall(reg_6, content)
        all_chi_sen = ''.join(chi_list)
        all_chi_word_list = jieba.cut(all_chi_sen, cut_all=True)
        all_stop_word_list = list(set(stp_list) & set(all_chi_word_list))
        all_stp_num = len(all_stop_word_list)

    con2_list = []

    for i in range(0, len(con_list),3):
        temp = ''.join(con_list[i:i+3])
        con2_list.append(temp)
    con_list = con2_list

    data = []

    for con in con_list:
        #--------------------------------------------
        reg_7 = r'[^\x00-\xff]'
        char_list = re.findall(reg_7, con)
        hash_table["word_num"] = len(char_list)
        #--------------------------------------------
        reg_2 = 'href="(.*?)"'
        reg_3 = 'src="(.*?)"'
        url_list = re.findall(reg_2,con)
        url_list.extend(re.findall(reg_3,con))
        hash_table["url_num"] = len(''.join(url_list))
        #--------------------------------------------
        reg_4 = '<.*?>'
        reg_5 = '</.*?>'
        label_list = re.findall(reg_4,con)
        label_list.extend(re.findall(reg_5,con))
        hash_table["label_num"] = len(label_list)
        # --------------------------------------------
        sen_list = con.split('。')
        hash_table["sen_num"] = len(sen_list)
        # --------------------------------------------
        reg_6 = r'[\u4e00-\u9fa5]'
        chi_list = re.findall(reg_6, con)
        if len(chi_list) == 0:
            hash_table['stp_num'] = 0
        else:
            chi_sen = ''.join(chi_list)
            chi_word_list = jieba.cut(chi_sen, cut_all=True)
            stop_word_list = list(set(stp_list) & set(chi_word_list))
            hash_table['stp_num'] = len(stop_word_list)
        # ------------------------------------------
        hash_table['word_num'] = float(hash_table['word_num'])
        hash_table['url_num'] = float(hash_table['url_num'])
        hash_table['label_num'] = float(hash_table['label_num'])
        hash_table['sen_num'] = float(hash_table['sen_num'])
        hash_table['stp_num'] = float(hash_table['stp_num'])
        if hash_table["word_num"] == 0:
            TD = math.log(1/(hash_table["label_num"]+1))
        else:
            if hash_table['url_num'] == 0:
                hash_table['url_num'] = 1
            if hash_table['word_num']-hash_table['url_num'] == 0:
                TD = math.log(1/hash_table['url_num'])*(hash_table['sen_num']/all_sen_num+1)*(hash_table['stp_num']/all_stp_num+1)*abs(math.log((hash_table['word_num']+1)/(hash_table['label_num']+1)))
            else:
                try:
                    TD = math.log(abs((hash_table['word_num'])-(hash_table['url_num']))/hash_table['url_num'])*(hash_table['sen_num']/all_sen_num+1)*(hash_table['stp_num']/all_stp_num+1)*abs(math.log((hash_table['word_num']+1)/(hash_table['label_num']+1)))
                except:
                    print(hash_table['word_num'],hash_table['url_num'],hash_table['sen_num'],all_sen_num,hash_table['stp_num'],all_stp_num)
                if TD >= 0:
                    data.append(con)
    return data

    # ax = plt.subplot()
    # ax.plot(data)
    # plt.show()


with open("test.html",encoding='utf-8') as r:
    html = r.read()
get_denisity(html)
article_html = ''.join(data)
asoup = BeautifulSoup(article_html,'lxml')
print(re.sub('\s','',asoup.text))













