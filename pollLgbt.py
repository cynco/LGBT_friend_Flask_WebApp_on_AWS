
# coding: utf-8

# In[9]:

from flask import Flask, render_template, request
from pollLgbtFunctions import read_surveydata_txt, process_survey_data, load_user_data, read_codebook_txt, process_survey_text, process_textual_data, make_blurb, write_blurb
import os
app = Flask(__name__)

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

#Q27 ask about who one is attracted to
yesno_data = {
   'question' : 'Ready to meet your new friend?',
   'fields'   : ['Yes', 'No']
}


# In[10]:

filename1 = 'data1.txt'
filename2 = 'data2.txt'
filename3 = 'blurb.txt'


# In[11]:

@app.route('/')
def root():
    return render_template('poll.html', data=poll1_data)

@app.route('/poll')
def poll():
    vote = request.args.get('field')

    out = open(filename1, 'w')
    out.write( vote + ',' )
    out.close()
#   out = open(filename2, 'a')
#   out.write(  mytype )
#   out.close()

    return render_template('poll2.html', data=poll2_data)

@app.route('/poll2')
def poll2():
    vote = request.args.get('field')

    out = open(filename1, 'a')
    out.write( vote + ',' )
    out.close()

    return render_template('poll3.html', data=poll3_data)

@app.route('/poll3')
def poll3():
    vote = request.args.get('field')

    out = open(filename1, 'a')
    out.write( vote )
    out.close()

    return render_template('thankyou.html', data=yesno_data)


# In[ ]:

@app.route('/thankyou')
def thankyou():
    response = request.args.get('field')
    print('FIELD', response)
    if response=="No":
       blurb=["Well, this is awkward..."]
    else:
        df0=read_surveydata_txt('./txtFiles/pewdatasav.txt') 
        #df0 = load_survey_data("./Pew_LGBT/pew2013lgbtpublicdatarelease.sav")
        df1 = process_survey_data(df0)
        print('SHAPE df1',df1.shape)
        userFtype = load_user_data("./txtFiles/data1.txt")
        textBlock = read_codebook_txt('./txtFiles/codebook.txt')
        allQs = process_survey_text(textBlock)
        #allQs = load_survey_text("./Pew_LGBT/Pew2013LGBTcodebook.docx")
        topQs, blurbQsL = process_textual_data(allQs)
        blurb = make_blurb(userFtype, topQs, df1, blurbQsL)
        write_blurb('./txtFiles/blurb.txt', blurb)
        file2  = open('./txtFiles/blurb.txt', 'r')
        blurb=[]
        for line in file2:
            nextline = line
            blurb.append(nextline)
        print('len blurb',len(blurb))
    return render_template('results.html', data=poll1_data, blurb=blurb)


if __name__ == "__main__":
    app.run(debug=True)
    


# In[12]:

print('hello')

