#libraries
import numpy as np
import tensorflow as tf
import re
import time

#importing the dataset
lines = open('movie_lines.txt', encoding = 'utf-8', errors = 'ignore').read().split('\n')
conversations = open('movie_conversations.txt', encoding = 'utf-8', errors = 'ignore').read().split('\n')

#dict of all line id
id2line={}
for line in lines:
    line_=line.split(' +++$+++ ')
    if(len(line_)==5):
        id2line[line_[0]]=line_[-1]

#list of all the lines
convo_id=[]
for conv in conversations[:-1]:
    lst_=conv.split(' +++$+++ ')[-1][1:-1].replace( "'", "")
    convo_id.append(lst_.split(","))
    
#getting questions and answers
ques=[]
ans=[]
for conv in convo_id:
    for c in range(len(conv)-1):
         ques.append(id2line[conv[c].replace(' ','')])
         ans.append(id2line[conv[c+1].replace(' ','')])
         
def datapreprocess(text):
    text=text.lower()
    simplify_wrd = { "aren't" : "are not", "can't" : "cannot", "couldn't" : "could not", \
"didn't" : "did not","doesn't" : "does not","don't" : "do not","hadn't" : "had not", \
"hasn't" : "has not","haven't" : "have not","he'd" : "he would","he'll" : "he will", \
"he's" : "he is","i'd" : "I would","i'd" : "I had","i'll" : "I will","i'm" : "I am", \
"isn't" : "is not","it's" : "it is","it'll":"it will","i've" : "I have","let's" : "let us", \
"mightn't" : "might not","mustn't" : "must not","shan't" : "shall not","she'd" : "she would",\
"she'll" : "she will","she's" : "she is","shouldn't" : "should not","that's" : "that is",\
"there's" : "there is","they'd" : "they would","they'll" : "they will","they're" : "they are",\
"they've" : "they have","we'd" : "we would","we're" : "we are","weren't" : "were not",\
"we've" : "we have","what'll" : "what will","what're" : "what are","what's" : "what is",\
"what've" : "what have","where's" : "where is","who'd" : "who would","who'll" : "who will",\
"who're" : "who are","who's" : "who is","who've" : "who have","won't" : "will not",\
"wouldn't" : "would not","you'd" : "you would","you'll" : "you will","you're" : "you are",\
"you've" : "you have","'re": " are","wasn't": "was not","we'll":" will","didn't": "did not"}
    for key,values in simplify_wrd.items():
        text=re.sub(key,values,text)
    text=re.sub(r"[-{}\"+\-#/@;:<>=|.?,~]","",text)
    return text
    
clean_ques=[datapreprocess(q) for q in ques]
clean_ans=[datapreprocess(a) for a in ans]

#creating a dictionary
word_count={}
for sent in clean_ques:
    for word in sent.split():
        if(word not in word_count):
            word_count[word]=1
        else:
            word_count[word]+=1
for sent in clean_ans:
    for word in sent.split():
        if(word not in word_count):
            word_count[word]=1
        else:
            word_count[word]+=1  
    
#mapping ques words
threshold=20
ques_word2int={}
number=0
for word,count in word_count.items():
    if(count>threshold):
        ques_word2int[word]=number
        number+=1
ans_word2int={}
number=0
for word,count in word_count.items():
    if(count>threshold):
        ans_word2int[word]=number
        number+=1
    
#adding tokens to dict
tokens=['<PAD>','<OUT>','<EOS>','<SOS>']
for token in tokens:
    ques_word2int[token]=len(ques_word2int)+1
    ans_word2int[token]=len(ans_word2int)+1

#inverse mapping for sec to sec model
answers_int2word={w_i:w for w,w_i in ans_word2int.items()}

#adding EOS
for ans in range(len(clean_ans)):
    clean_ans[ans]+='<EOS>'
    
ques_data=[]
ans_data=[]
for ques in clean_ques:
    lst=[]
    for words in ques.split():
        if words  in ques_word2int:
            lst.append(ques_word2int[words]) 
        else:
            lst.append(ques_word2int['<OUT>']) 
    ques_data.append(lst)
for ans in clean_ans:
    lst=[]
    for words in ans.split():
        if words  in ans_word2int:
            lst.append(ans_word2int[words])
        else:
            lst.append(ans_word2int['<OUT>'])
            
    ans_data.append(lst)


    
    
    
    
    
    