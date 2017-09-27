# coding=UTF-8
'''
Created on 2017
@author: XYJ
'''
import jieba
import os
import random
import math


def TextProcessing(floder_path,train_size =0.8):
    floder_list = os.listdir(floder_path)
    train_data_list = []
    train_class_list = [] 
    test_data_list = []
    test_class_list = [] 
    for floder in floder_list:
        new_floder_path = os.path.join(floder_path,floder)
        new_floder_list = os.listdir(new_floder_path)
        word_list = []
        for file in new_floder_list:
            txt_list =[]
            with open(os.path.join(new_floder_path,file),'rb') as f:
                raw = f.read().decode('ANSI','ignore')
            txt_list = list(jieba.cut(raw,cut_all = False))
            
            while '\u3000' in txt_list:
                txt_list.remove('\u3000')
            while '\r\n' in txt_list:
                txt_list.remove('\r\n')
            while '\x00' in txt_list:
                txt_list.remove('\x00')
            while '\n' in txt_list:
                txt_list.remove('\n')
            word_list.append(txt_list)
        random.shuffle(word_list)
        size = int(len(word_list)*train_size)
        print(floder)
        print(size)
        
        tem_train_list = word_list[:size]
        tem_test_list = word_list[size:]
        tem_train_word = []
        for a in tem_train_list :
            for b in a:
                tem_train_word.append(b)
        3
        ##生成训练数据集和测试数据集
        train_data_list.append(tem_train_word)
        train_class_list.append(floder)
        test_data_list.append(tem_test_list)
        test_class_list.append(floder)
        
    return train_data_list,test_data_list,train_class_list,test_class_list

'''
@param  param is stopwords's filename: 
@return: a set of stopwords_file
'''
def makeStopwordsSet(stopwords_file):
    words_set = set()
    with open(stopwords_file,'rb') as f:
        lines = f.readlines()
    for line in lines:
        word = line[:-2].decode('UTF-8')
        if len(word)>0 and word not in words_set:
            words_set.add(word)
    return words_set

def listToDict(data_list,stopwords_set=set()):
    data_dict = {}
    for word in data_list:
        if word not in stopwords_set and not word.isdigit():
            if word in data_dict:
                data_dict[word] += 1
            else:
                data_dict[word] = 1
    
    return data_dict

def clearlist(test_list,stopwords_set = set()):
    test = []
    for word in test_list:
        if word not in stopwords_set and not word.isdigit():
            test.append(word)
    return test

def predicted(test_list,train_data_list_dict,train_class_list,train_data_count):
    predicte = []
    for dic ,count in zip(train_data_list_dict,train_data_count):
        laplace = 0
        for word in test_list:
            laplace += P(word,dic,count)
        predicte.append(laplace)
    ma = max(predicte)
    return train_class_list[list.index(predicte,ma)]
            
def P(word,dic,count):
    if word in dic:
        laplace = math.log(((dic[word]+1)/(count + len(dic))))/math.log(10)
    else:
        laplace = math.log((1/(count + len(dic))))/math.log(10)
    return laplace
    
  
def main():
    abspath = os.path.abspath(os.path.dirname(os.getcwd()))
    ##########获取不关键单词集合##########
    stopwords_file = abspath + '\\stopwords_cn.txt'
    stopwords_set = makeStopwordsSet(stopwords_file)
    
    ###########获取数据集################
    folder_path = abspath+'/Reduced'
    train_data_list,test_data_list,train_class_list,test_class_list = TextProcessing(folder_path,train_size = 0.8)
    
    ##处理训练数据集#####################
    train_data_list_dict = []
    for word_list in train_data_list:
        train_data_list_dict.append(listToDict(word_list, stopwords_set))
    print('训练数据集处理完成')
    
    ##处理测试训练集########
    for test_list in test_data_list:
        for test in test_list:
            test = clearlist(test,stopwords_set)
    print('测试数据集处理完成')
    
    ##对每一类的关键词按照递减顺序排列
    for a in train_data_list_dict:
        internet_list = sorted(a.items(),key = lambda f : f[1],reverse = True)
        print(internet_list[:200])
    
    ##统计每一类的单词数，为了方便计算P(Bi/A)
    train_data_count = []
    for dic in train_data_list_dict:
        count = 0
        for v in dic.values():
            count += v
        train_data_count.append(count) 
        
    ###test###########################################
    
    for li,classtpye in zip(test_data_list,test_class_list):
        corr = 0
        count = 0
        for lis in li:
            name = predicted(lis, train_data_list_dict, train_class_list, train_data_count)
            count += 1
            if name == classtpye:
                corr += 1
                
        print(classtpye+'类预测成功率为 %.3f %%'%(corr*100/count))
     
       
if __name__  == '__main__':
    main()
    
    
    
    
    