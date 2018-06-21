import slate
from collections import OrderedDict,Counter
import re
import nltk
import rake
import string
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
import math
from textblob import TextBlob

ls=[]
stopwords_=[]
raw=""
temp=[]
score={}
dict1={}

#--------------------------------------------------------remove duplicate--------------------------------------------------#
def remove_dup(text):
        st=str(text).split(" ")
        st=list(set(st))
        return (' ').join(i for i in st)



#--------------------------------------------------------end-----------------------------------------------------------------#



#-----------------------------------------------------SPLIT UPPERCASE----------------------------------------------------------#


def split_uppercase(text):
        r=[]
        l=False
        for c in text:
                if l and c.isupper():
                        r.append(' ')
                l=not c.isupper()
                r.append(c)
        return ''.join(r)

#--------------------------------------------------------END---------------------------------------------------------------------#




#-------------------------------------------------GET CONTINUOUS CHUNK---------------------------------------------------------#


def get_continuous_chunks(text):
        chunked = ne_chunk(pos_tag(word_tokenize(text)))
        continuous_chunk=[]
        current_chunk=[]
        for i in chunked:
                if type(i) == Tree:
                        current_chunk.append(" ".join([token for token, pos in i.leaves()]))
                elif current_chunk:
                        named_entity = " ".join(current_chunk)
                        if named_entity not in dict1:
                                dict1[named_entity]=1
                        else:
                                dict1[named_entity]=dict1[named_entity]+1
                        if named_entity not in continuous_chunk:
                                continuous_chunk.append(named_entity)
                                current_chunk = []
                        else:
                                continue
        return continuous_chunk

#---------------------------------------------------------END----------------------------------------------------------#

#---------------------------------------------------CALCULATE WORD SCORES------------------------------------------------#


def calculate_word_scores(phraseList):
        word_frequency = {}
        word_degree = {}
        for phrase in phraseList:
                word_list = phrase
                word_list_length = len(word_list)
                word_list_degree = word_list_length - 1
                #if word_list_degree > 3: word_list_degree = 3 #exp.
                for word in word_list:
                        word_frequency.setdefault(word, 0)
                        word_frequency[word] += 1
                        word_degree.setdefault(word, 0)
                        word_degree[word] += word_list_degree  #orig.
                        #word_degree[word] += 1/(word_list_length*1.0) #exp.
        for item in word_frequency:
                word_degree[item] = word_degree[item] + word_frequency[item]

        # Calculate Word scores = deg(w)/frew(w)
        word_score = {}
        for item in word_frequency:
                word_score.setdefault(item, 0)
                word_score[item] = word_degree[item] / (word_frequency[item] * 1.0)  #orig.
        #word_score[item] = word_frequency[item]/(word_degree[item] * 1.0) #exp.
        return word_score



#----------------------------------------------------------END---------------------------------------------------------------#



#----------------------------------------------------------REMOVE ALL---------------------------------------------------#




def remove_all(substr, str):
        index = 0
        length = len(substr)
        while string.find(str, substr) != -1:
                index = string.find(str, substr)
                str = str[0:index] + str[index+length:]
        return str


#----------------------------------------------------------------END------------------------------------------------------#
with open("JavaBasics-notes.pdf") as f:
        raw=str(slate.PDF(f))
ls=raw.split(".")

stop=['xc','xa','x0c','x80','xe2','xa2','\\n','--',',','|','`',' +','..','...','- ',' -',' + ','//','\\','\'','@','#','$','%','&','*','(',')','?','{','}','[',']','<','>','\"','=',':',';','!','0','1','2','3','4','5','6','7','8','9']


for i in ls:
        st=str(i)
        for j in stop:
                st=remove_all(str(j),st)
        temp.append(st)


ls=temp
temp=[]

printable = set(string.printable)
#raw=string.replace(raw,"."," ")
for i in ls:
        st=str(i)
        st=string.replace(st,"/"," ")
        st=filter(lambda x: x in printable, st)
        temp.append(st)


ls=temp
temp=[]

ls=[i for i in ls if not str(i).isdigit()]

for i in ls:
        if(len(i)>10):
                temp.append(str(split_uppercase(str(i))))

ls=temp
temp=[]

keyword=[]


for i in ls:
        temp.append(TextBlob(i))


#-------------------------------------------------------tf idf-----------------------------------------------#


def tf(word,blob):
        return blob.words.count(word)/len(blob.words)
def n_containing(word,blob_list):
        return sum(1 for blob in blob_list if word in blob.words)
def idf(word,blob_list):
        return math.log(len(blob_list)/(1+n_containing(word,blob_list)))
def tfidf(word,blob,blob_list):
        return tf(word,blob)*idf(word,blob_list)
for i,blob in enumerate(temp):
        #print("top word {}".format(i+1))
        scores={word:tfidf(word,blob,temp) for word in blob.words}
        sorted_words=sorted(scores.items(),key=lambda x: x[1], reverse=True)
        for word,score in sorted_words[:3]:
                keyword.append(word)



#----------------------------------------------------------end---------------------------------------------#



temp=[]



for i in ls:
        keyword=keyword+get_continuous_chunks(str(i))

keyword=[i.lower().encode("utf-8") for i in keyword]
temp=keyword
keyword=[]
for i in temp:
        keyword.append(str(remove_dup(i)).encode("utf-8"))

#for i in keyword:
#       print i
with open("SmartStoplist.txt","r")as in_file:
        for lines in in_file:
                stopwords_.append(lines.strip())

temp=[]
for i in keyword:
        if i not in stopwords_:
                temp.append(i)

score={}

score=Counter(temp)
score = OrderedDict(sorted(score.items(), key=lambda(k,v):(v,k),reverse=True))

with open('my_file.csv', 'w') as f:
    [f.write('{0},{1}\n'.format(key, value)) for key, value in score.items()]
                                                                                                                                                                                                                                                         

exam6.py
Displaying exam6.py.
