
# coding: utf-8

# In[1]:

# This notebook is used to create the .py script to run the poll_lgbt.pyweb app.


# ## 1. Match web app user with a friend  
# 
# This will be done by selecting a survey respondent that matches the replies of the webapp user.
# 
# ## 2. Compile a profile for the matched friend
# This will be done by parsing the responses of the pew survey and combining them into a 
# description of the 'friend'.

# # 1. Match web app user with a friend
# 
# ## Loading and parsing responses  
# Here, I will   
# -load the mcrNums for all respondents  
# -split up the respondents based on their matching group  
# -randomly pick one friend from the appropriate group  

# In[1]:

# So that plots are displayed inline, "plt.show()" not needed.
#%pylab inline;

# Python version
import sys
#print('Python: {}'.format(sys.version))
# scipy
import scipy as sp
#print('scipy: {}'.format(sp.__version__))
# numpy
import numpy as np
#print('numpy: {}'.format(np.__version__))
# matplotlib
import matplotlib as plt
#print('matplotlib: {}'.format(plt.__version__))
# pandas
import pandas as pd
#print('pandas: {}'.format(pd.__version__))
# scikit-learn
import sklearn as skl
#print('sklearn: {}'.format(skl.__version__))

#import savReaderWriter as spss
#print('savReaderWriter: {}'.format(spss.__version__))

#import seaborn as sns

import re

#import docx
import random

# In[2]:

# Not needed if I have .txt version of .sav file with the survey data
# #Requires the savReaderWriter package (which can be a pain to install)
# import savReaderWriter as spss
# print('savReaderWriter: {}'.format(spss.__version__))

# def read_sav_to_df(savFile):
# # Read .sav (SPSS) Data File
# # Return df0 pandas dataframe with all data

#     savFile = "./Pew_LGBT/pew2013lgbtpublicdatarelease.sav"

#     with spss.SavReader(savFile, returnHeader=True) as reader:
#         header = reader.next()
#     header = [x.decode('UTF-8') for x in header]
#     header=[e.replace('ppagecat','PPAGECAT') for e in header]

#     #Upload everything
#     data = spss.SavReader(savFile) 
#     df0 = pd.DataFrame(data.all())
#     df0.columns = header
#     data.close()
#     #df0.shape
# #type(df0)
# #print(list(df0.columns[1:40]))
#     return df0
#Usage: 
#df0=read_sav_to_df("./Pew_LGBT/pew2013lgbtpublicdatarelease.sav")


# In[2]:

# Need only once to create txtFile with sav data
def write_df_to_txt(df0,txtFile):
    # Write dataframe out to a .txt file
    # Write it in csv format onto a txt file
    #txtFile='./txtFiles/pewdatasav.txt'
    df0.to_csv(txtFile, header=True, index=True, sep=',', mode='w')
    return
#Usage: 
#write_df_to_txt(df0,'./txtFiles/pewdatasav.txt')


# In[3]:

# Don't need if I have codebook in .txt version
# Need only once to make get text from .doc codebook, if codebook.txt is not available
def read_codebook_doc(docFile):
# Read codebook text directly from .docx file
# Requires the docx package (which can be a big pain...)

    #import docx
    #docFile = "./Pew_LGBT/Pew2013LGBTcodebook.docx"
    doc = docx.Document(docFile)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

#Usage:
#textBlock = read_codebook_doc("./Pew_LGBT/Pew2013LGBTcodebook.docx")
#print('codebook', len(textBlock))


# In[49]:

# Need everytime to read codebook from .txt file
def read_codebook_txt(txtFile):
    # Read codebook with the question text from .txt file  
        myFile  = open('./txtFiles/codebook.txt', 'r')
        fullText=myFile.read()
        return fullText
#Usage:
#textBlock = read_codebook_txt('./txtFiles/codebook.txt')   
#print('codebook len textBlock 47925 =',len(textBlock)) #47925 


# In[23]:

# Needed everytime to read in sav data from txtFile
def read_surveydata_txt(txtFile):
    # The txtFile should contain the data in csv format
    #txtFile='./txtFiles/pewdatasav.txt'
    df=pd.read_csv(txtFile)
    #print(df.columns[0:4])
    #type(df1.columns[1])
    # Normally, you get the b because you encoded to utf-8 and it's a bytes object.
    # But in this case, the column names are already strings. For some reason the "b'" are there, but I can just remove them
    df.columns = [x.lstrip("b'").rstrip("'") for x in df.columns]
    df=df.iloc[:,1:]
    #df.columns.get_loc('ppagecat') #170
    df.rename(columns = {'ppagecat':'PPAGECAT'}, inplace = True)
    #print(df0.iloc[:,170])
    #df.head()
    return df
#Usage:
#df0=read_surveydata_txt('./txtFiles/pewdatasav.txt') 


# ### Here, we start to process the Pew survey results so that we can subset based on friend type. 

# In[24]:

# Needed everytime to pre-process survey data
def process_survey_data(df0):
# Reduce to questions of interest
# Add 'grade' and 'ftype' columns
# Some needed formatting

# Just questions of interest
    topQsL=['Q1','Q9B', 'Q39', 'Q40', 'PPAGECAT','SNS','SEX','Q24','Q25', 'Q27','Q41', 'NEWCASEID']

    nrows=df0.shape[0]
    df1=df0[topQsL][0:nrows]

    df1=df1.replace('NaN','-100')
    df1=df1.applymap(int)
    for question in ['Q1','Q9B', 'PPAGECAT',
       'SNS','SEX','Q24','Q25', 'Q27']: #excluding ages and IDs
        df1[question]=df1[question]-1

# Translate Pew respondent ages to the schoolgrade categories given in the Q39 poll
    integers = [0 for x in range (len(df1))]
    df1 = df1.assign(grade=integers)
    df1.loc[( ((df1['Q39']>=6.0) & (df1['Q39']<10.0)) |              ((df1['Q40']>=6.0) & (df1['Q40']<10.0))), 'grade'] = 0 

    df1.loc[( ((df1['Q39']>=10.0) & (df1['Q39']<13.0)) |              ((df1['Q40']>=10.0) & (df1['Q40']<13.0))), 'grade'] = 1

    df1.loc[( (df1['Q39']>=13.0) | (df1['Q40']>=13.0) ), 'grade'] = 2
    df1['grade'].unique()

# We have 18 different friend types based on their responses to questions 1, 9b and 'grade'.
#ftype values 0. through 18. ( 3x2x3 )
# I create a column 'ftype' and assign the ftype number, it will be easy to subset based on just this one variable.
    strings = ["" for x in range(len(df1))]
    df1 = df1.assign(ftype=strings)
    #print(df1.columns)
    for i in np.arange(0,3):
        for j in np.arange(0,2):
            for k in np.arange(0,3):
                ftype0=str(i)+str(j)+str(k)+str(k)
                df1.loc[ ((df1['Q1']==i)&(df1['Q9B']==j)&(df1['grade']==k)), 'ftype'] = ftype0
                #print(ftype0,'ijk',i,j,k) 
    return df1
#Usage:
#df1=process_survey_data(df0)


# ## Now read in the data from the WebApp poll user. 

# In[27]:

# Need everytime to get poll user's responses
# Returns the userFtype
def load_user_data(txtFile):
# Load text file from webapp with current user's textual responses
# Match the responses with their index number
# Use index numbers to match user to userftype

    fileIn=open(txtFile,'r')
    data=fileIn.read() 

    # the txt file will contain a string of the user's textual responses.
    dataL=re.sub(',(?=[a-zA-Z0-9])', '*', data).rstrip('\n').split('*')
    #print(dataL)

    userMcrs={'Q1':dataL[0],'Q9B':dataL[1],'Q39':dataL[2], 'Q40':dataL[2]}

# This is the exact text on the flask poll code.
# pollDF lets us match poll response to 'fields' index number

    #Q1
    poll1_data = {
   'question' : 'Generally, how would you say things are these days in your life? Would you say that you are...',
   'fields'   : ['Very happy', 'Pretty happy', 'Not too happy']
    }
    #Q9B
    poll2_data = {
   'question' : 'Which statement comes closer to your own views — even if neither is exactly right?',
   'fields'   : ['Generally speaking, most people can be trusted', 'You can’t be too careful in dealing with people']
    }
    #Q39 or Q40
    poll3_data = {
   'question' : 'Around what grade were you in when you had your first childhood crush?',
   'fields'   : ['3rd grade', '6th grade', '8th grade or higher']
    }    

    # Turning user data into a dataframe.
    # pollDf contains the words for all the possible fields
    pollDf=pd.DataFrame(index=['question','fields'], columns=['Q1','Q9B','Q39','Q40'])
    for index in pollDf.index.values:  #'question', 'fields'
        pollDf['Q1'][index]=poll1_data[index]
        pollDf['Q9B'][index]=poll2_data[index]
        pollDf['Q39'][index]=poll3_data[index]
        pollDf['Q40'][index]=poll3_data[index] 
    #pollDf

# Below, we match the user response with the poll field index number    
# userNum contains the index numbers corresponding to the user's poll responses.
# userNum is used to construct the userFtype of the poll user.
# I will use the userFtype to identify the matching survey respondents
    userNum={}
    userFtype=""
    for question in pollDf.columns: #iterate over columns 'Q1', etc.
        userNum[question]=pollDf[question]['fields'].index(userMcrs[question])
        #print(question,'userNum', userNum[question])
        userFtype=userFtype+str(userNum[question])    
    return userFtype
    

#Usage:
#userFtype = load_user_data("./txtFiles/data1.txt")
#rename file pollFtype.txt


# # 2. Compile a profile for the matched friend
# 
# ## Loading and parsing the question and response options from the Pew survey codebook.
# In this section, I take the question text from the Pew survey codebook, I create a dataframe with the questions, responses, and the phrases to connect the responses into a blurb about the respondent. 
# 
# allQs and topQs will contain question, fields (mcrs), and connector for each question. 
# df0 will contain numeric choices of all respondents
# mcrNum will be the numbers for each question chosen by friend.

# In[54]:

# Need everytime to process textBlock and 
# return allQs, a dictionary with question and field text
def process_survey_text(textBlock):
#for num in [1]: (To run code but not as a function)
# Parse the text to construct a dictionary allQs with all the questions and their fields.

    # Split the textBlock into blocks corresponding to each question
    allQs={} #This will be a dictionary with a key for each question
    #I only care about the questions asked to all respondents
    # Insert a '***' at every kind of place where I want to split, then split
    textBlock = textBlock.replace('ASK ALL:','***').replace('\n\n\n','***').replace('Q.','***Q')
    textList = textBlock.split('***')
    textList=[item for item in textList if len(item)>=4] 
    #print('len textList',len(textList))

# Creating dictionary allQs with question, and fields for every question.
# This wording comes from the Pew survey codebook.
    sortedkeys=[]
    for item in textList:
        spitem=str(item)  #Had to turn it into a string again to split('\n')
        #print('first ',spitem)
        spitem=spitem.replace('\n','***').split('***')
        #spitem=spitem.split('***')
        spitem=[piece for piece in spitem if len(piece)>=3]
        #skip rest of loop for spitem with len<2
        if len(spitem)<2:
            continue
        #print('spitem',spitem)
        if '\t' in spitem[0]:
            #print('before key')
            key,question=spitem[0].split('\t')[0:2]
            if key=='Q9b':
                key='Q9B'
            sortedkeys.append(key)
            #print('KEY',key)
            #print('QUESTION', question)
            mcrlist=[piece.split('\t')[1] for piece in spitem[1:] if piece[0].isdigit()]
            mcrlist=[piece.rstrip(' ').lower() for piece in mcrlist]
            #print('MCRLIST', repr(mcrlist))
            #mcroptions  #lists of options a,b,c...
            allQs[key]={'question': question, 'fields':mcrlist, 'connector':""}
    #print(sortedkeys)
    
    # Some customizations
    # Changing age ranges to individual age number
    allQs['PPAGECAT']['fields']=[e.replace('under ','').split('-')[0] for e in allQs['PPAGECAT']['fields']]
    #SNS and Q24 change from yes/no to do/don't
    allQs['SNS']['fields']=[e.replace('yes','').replace('no','don\'t') for e in allQs['SNS']['fields']]
    allQs['Q25']['fields']=[e.replace('yes','do').replace('no','don\'t') for e in allQs['Q25']['fields']]
    return allQs

#Usage:
#allQs = process_survey_text(textBlock)
#print('len(allQs) 102 =',len(allQs))


# ### Pick the interesting questions to construct the friend blurb.
# 
# Here, I take a subset allQs with just the questions that interest me right now.
# 
# Other interesting questions I may want to add later:
# 5, 10, oftvote, sns (social media), sex, 24(orientation), 25, 27 (attraction),31, 32, 32Apos and 32Aneg, 41 (sure age), 42, (44 if yes, 44b,c), 52, 53, 63(a-f,1-2 imp), 67, 68, 70, 71, 74, 80, 
# 82 a-f if 1 or 2 for any of them, 17 (a-g reasons and 1-3 importance, randomized) 
# 

# In[56]:

def process_textual_data(allQs):
# Take a subset with only the questions that I'm interested in right now.
# Add column for 'connector' phrases and enter text

    topQsL=['Q1','Q9B', 'Q39', 'Q40', 'PPAGECAT','SNS','SEX','Q24','Q25', 'Q27','Q41','NEWCASEID']

#TODO: add grade and fields to allQs, then switch to using blurbQsL in loop below.
# don't have newcaseid in blurbQsL.
    topQs={}
    for question in topQsL:
        if question=='NEWCASEID':
            continue
        topQs[question]= allQs[question]

# Create the appropriate text to connect the responses to form a paragraph

    topQs['Q1']['connector']="Hi, it's nice to meet you. I see you're feeling %s today, same here!"
    topQs['Q9B']['connector']="It looks like we were matched up because we both think that %s...\n" 
    topQs['SEX']['connector']="As you know, I'm a proud member of the LGBT community. In terms of my gender identity, I am %s and my name is %s."
    topQs['Q25']['connector']="In case you're wondering, I %s consider myself transgender."

# Blurb will only include either 39 or 40
    topQs['Q39']['connector']="Similar to how you had your first crush around the %s, I was %s years old when I first felt that I was not straight or heterosexual.\n" 
    topQs['Q40']['connector']="Similar to how you had your first crush around the %s, I was %s years old when I first felt that my gender was different from my birth sex.\n"

    topQs['PPAGECAT']['connector']= "I'm now %s years old, and "
    topQs['Q24']['connector']="having gotten to know myself better through the years, I can tell you for sure that I'm %s." #lgbt self-id
    # "Being %s is defined as %s. % (pickedMrc['Q24'], suppText['lgbtDef'][mcrNum])
    topQs['Q27']['connector']="In my particular case, I'm %s." #attracted to
    topQs['Q41']['connector']="In fact, I was sure of this by the time I was %s years old.\n"

    topQs['SNS']['connector']="Anyway, to tell you a little more about myself, I %s really enjoy using Facebook, Twitter, or other social media, what about you?"

    blurbQsL=['Q1','Q9B', 'SEX','Q25','grade','Q39', 'Q40', 'PPAGECAT',
             'Q24','Q27','Q41','SNS']

    return topQs, blurbQsL

#Usage:
#topQs, blurbQsL = process_textual_data(allQs)


# In[58]:

# Don't need to run, this was just to run a simple test 
def test_phrases(topQs, blurbQsL):
# Here, I preview the phrases using the codebook fields rather than 
# from the survey responses.
# For age questions, the codebook doesn't provide a value so I have to make one up. 
    phrases=[]
    for question in blurbQsL:
        #print('QUESTION', question)
        #print(topQs[question]['fields'])
        if question=='grade': #skipping this one for now
            grade='4th' #ftypeDf['grade']
            continue   
        if question=='Q39' or question=='Q40':
            pickedMcr = ('9', grade)
            connector = topQs[question]['connector']
            phrase= connector % pickedMcr
            #print(phrase) 
        for field in topQs[question]['fields']:
            pickedMcr = field
            if question=='SEX':
                print('SEX',pickedMcr)
                name='Jane'
                pickedMcr=(pickedMcr, name)
            #print('MCR',pickedMcr)
            connector = topQs[question]['connector']
            #print('CONNECTOR',connector)
            phrase= connector % pickedMcr
            #print(phrase) 
            phrases.append(phrase)
        return phrases
# Don't need, just a test    
#Usage:
#phrases = test_phrases(topQs, blurbQsL)    


# In[60]:

# Need everytime to make blurb
def make_blurb(userFtype, topQs, df1, blurbQsL):
# Select a survey respondent randomly from his ftype group in df1.
# Construct phrases using survey results (df1) and text (topQs). 
# Construct blurb in the sentence order given in blurbQsL.

    random.seed(101) #optional
    ftype0= userFtype
    #print('ftype0',ftype0)
    ftypeDf=df1[df1['ftype']==ftype0]
    idL=list(ftypeDf['NEWCASEID'])
    #print('len IdL',len(idL))
    if len(idL)==0:
        blurb="Sorry, there was no friend match at this time."
        return blurb
    else:
        friendID=random.choice(idL)

    # The row of numeric responses of the chosen friend (survey respondent)
    friendDf=ftypeDf[ftypeDf['NEWCASEID']==friendID]
    #print('len friendDf',len(friendDf))
    
    gradeNum=int(ftype0[2]) #going by the number chosen by the poll user
    gradeL=('3rd grade', '6th grade','8th grade or higher')
    grade0=gradeL[gradeNum]
    #print('grade0',grade0)

    # Some fake names
    names=pd.DataFrame(columns=('female','male'))
    names['female']=['Anna','Maria','Olivia','Emma']
    names['male']=['Lucas','Alex','Francisco','Oscar']

    blurb=""
    for question in blurbQsL:
        pickedNum=friendDf[question].item()
        if question=='grade':
            #grade0 = topQs[question]['fields'][pickedNum]
            continue
        elif question=='Q39' or question=='Q40':
            pickedMcr = (grade0, pickedNum)
            #print(question,'MCR',pickedMcr) 
            if pickedNum<=0:
                continue
        elif question=='SEX':
            pickedMcr = topQs[question]['fields'][pickedNum]
            name=random.choice(names[pickedMcr])
            pickedMcr=(pickedMcr, name)
        elif question=='Q41':
            pickedMcr=pickedNum
        else:
            pickedMcr = topQs[question]['fields'][pickedNum] 
        #print('MCR',pickedMcr)
        #print('QUESTION',question)
        connector = topQs[question]['connector']
        phrase= connector % pickedMcr
        blurb=blurb+" "+phrase
    #print(blurb) 
    return blurb
#Usage:
#blurb = make_blurb(userFtype, topQs, df1, blurbQsL)


# In[61]:

def write_blurb(txtBlurbFile, blurb):
#Write out blurb to blurb.txt

    #fileOut=open('blurb.txt','w')
    fileOut=open(txtBlurbFile,'w')
    fileOut.write(blurb)
    fileOut.close()
    return 

#Usage:
#write_blurb('./txtFiles/blurb.txt', blurb)


# In[ ]:

#         df0=read_surveydata_txt('./txtFiles/pewdatasav.txt') 
#         #df0 = load_survey_data("./Pew_LGBT/pew2013lgbtpublicdatarelease.sav")
#         df1 = process_survey_data(df0)
#         print('SHAPE df1',df1.shape)
#         userFtype = load_user_data("./txtFiles/data1.txt")
#         textBlock = read_codebook_txt('./txtFiles/codebook.txt')
#         allQs = process_survey_text(textBlock)
#         #allQs = load_survey_text("./Pew_LGBT/Pew2013LGBTcodebook.docx")
#         topQs, blurbQsL = process_textual_data(allQs)
#         blurb = make_blurb(userFtype, topQs, df1, blurbQsL)
#         write_blurb('./txtFiles/blurb.txt', blurb)

