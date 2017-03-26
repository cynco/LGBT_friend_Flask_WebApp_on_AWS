from flask import Flask, render_template, request
import os
app = Flask(__name__)


poll1_data = {
   'question' : 'Generally, how would you say things are these days in your life? Would you say that you are...',
   'fields'   : ['Very happy', 'Pretty happy', 'Not too happy']
}

poll2_data = {
   'question' : 'Which statement comes closer to your own views — even if neither is exactly right?',
   'fields'   : ['Generally speaking, most people can be trusted', 'You can’t be too careful in dealing with people']
}

poll3_data = {
   'question' : 'In what grade were you when you had your first childhood crush?',
   'fields'   : ['2nd - 4th grade', '5th- 7th grade']
}

yesno_data = { 
   'question' : 'Ready to meet your new friend?',
   'fields'   : ['Yes', 'No']
}

filename1 = 'data1.txt'
filename2 = 'data2.txt'

types=['0a0','1a0','2a0','0b0','1b0','2b0',
       '0a1','1a1','2a1','0b1','1b1','2b1']

@app.route('/')
def root():
    return render_template('poll.html', data=poll1_data)

@app.route('/poll')
def poll():
    vote = request.args.get('field')

    out = open(filename1, 'a')
    out.write( '\n'+ vote + ',' )
    out.close()
    if vote==poll1_data['fields'][0]:
       mytype = '0'
    elif vote==poll1_data['fields'][1]:
       mytype = '1'
    else:
       mytype = '2'
    print('MYTYPE',mytype)
    out = open(filename2, 'a')
    out.write(  mytype )
    out.close()

    return render_template('poll2.html', data=poll2_data)

@app.route('/poll2')
def poll2():
    vote = request.args.get('field')

    out = open(filename1, 'a')
    out.write( vote + ',' )
    out.close()

    if vote==poll2_data['fields'][0]:
       mytype = 'a'
    else:
       mytype = 'b'
    out = open(filename2, 'a')
    out.write( mytype )
    out.close()
    return render_template('poll3.html', data=poll3_data)

@app.route('/poll3')
def poll3():
    vote = request.args.get('field')

    out = open(filename1, 'a')
    out.write( vote + '\n' )
    out.close()

    if vote==poll2_data['fields'][0]:
       mytype = '0'
    else:
       mytype = '1'
    out = open(filename2, 'a')
    out.write( mytype+'\n' )
    out.close()

    return render_template('thankyou.html', data=yesno_data)

@app.route('/thankyou')
def thankyou():
    response = request.args.get('field')
    print('FIELD', response)
    if response=="No":
       print("Well, this is awkward...")
    else:
# will make lists of six types in this file
# will count only if entry matches one in list
       counts = {}
       for f in types:
          counts[f] = 0
#   Later add the other files
       file2  = open(filename2, 'r')
       for line in file2:
          mytype = line.rstrip('\n')
          if mytype=="":
             continue
          if mytype not in types:
             continue
          print('TYPE',mytype)
# will need to strip commas too
          print('CALCULATING TOTALS')
          counts[mytype] += 1
    print('COUNTS', counts[mytype])
    print('RENDERING RESULTS')
    return render_template('results.html', data=poll1_data, counts=counts)


if __name__ == "__main__":
    app.run(debug=True)

