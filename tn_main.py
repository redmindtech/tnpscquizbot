from flask import Flask, session, redirect, url_for, request
#from flask import Flask
import json
import os
from flask import Flask, request, jsonify
import tn_course

app = Flask(__name__)
app.secret_key=0
app.secret_code=1
app.secret_count=0
app.secret_ques=0
app.secret_ans=0

@app.route("/webhook",methods=['POST','GET'])
def webhook():
 Req = request.get_json(silent=True, force=True)
 value = (Req.get('queryResult'))
 name=value.get('parameters')
 emailid=name.get('email')
 #email1=emailid
 print(emailid)
 #start=name.get('ready')
 ans=name.get('option')
 close=name.get('exit')
 q_name=name.get('quizname')
 print(q_name)
 


 if emailid is not None:
   e_mail=  ''.join(emailid)
   email1=tn_course.email(e_mail)
   res=jsonify({
      "fulfillmentText":email1,
      "payload":{
         "google":{
            "expectUserResponse":{
               "items":[
                  {
                     "simpleResponse":{
                        "textToSpeech":email1
                     }
                  }
               ]
            }
         }
      }
   })
    
     
 elif q_name is not None:
    app.secret_key=q_name
    quiz=  ''.join(app.secret_key)
    second=tn_course.main(quiz,i=1)
    c=tn_course.ques_count(quiz)
    app.secret_count=c
    w=tn_course.query(quiz)
    app.secret_ques=w
    u=tn_course.fetching(quiz)
    app.secret_ans=u
    s=  ''.join(second)
    q1,opt1,opt2,opt3,opt4=tn_course.ques_split(s)
    Q1=  ''.join(q1)
    op1=  ''.join(opt1)
    op2=  ''.join(opt2)
    op3=  ''.join(opt3)
    op4=  ''.join(opt4)
    res=jsonify({
    "fulfillmentText":Q1,
    "fulfillmentMessages":[
       {
          "text":{
             "text":[
             Q1,
             ]
          }
       },
        {
            "text":{
               "text":[
               "The options are :",
               ]
            }
         },
       {
          "text":{
             "text":[
             op1+"~"+op2+"~"+op3+"~"+op4,
             ]
          }
       }
    ],
    "payload":{
       "google":{
          "expectUserResponse":True,
          "richResponse":{
             "items":[
                {
                   "simpleResponse":{
                      "textToSpeech":Q1
                   }
                }
             ],
             "suggestions":[
                  {
                     "title":op1
                  },
                  {
                     "title":op2
                  },
                  {
                     "title":op3
                  },
                  {
                     "title":op4
                  }
              ]
          }
       }
    }
 })
 elif ans is not None:
    count=app.secret_count
    questions=app.secret_ques
    answers=app.secret_ans
    x=app.secret_key
    quiz=  ''.join(x)
    ques=tn_course.query2(questions,count)
    an=ans.title()
    an1=ans.upper()
    an2=ans.lower()
    an3=ans.capitalize()
    reply,score=tn_course.valid(ans,an,an1,an2,an3,answers)
    if type(ques) is not int:
      str1 =  ''.join(ques)
      str2 =  ''.join(reply)
      str3=str(score)
      q,o1,o2,o3,o4=tn_course.ques_split(str1)
      Q1=  ''.join(q)
      op1=  ''.join(o1)
      op2=  ''.join(o2)
      op3=  ''.join(o3)
      op4=  ''.join(o4)
      res=jsonify({
         "fulfillmentText":Q1,
         "fulfillmentMessages":[
            {
               "text":{
                  "text":[
                  str2,
                  ]
               }
            },
            {
               "text":{
                  "text":[
                  "Next question is --> "+"   "+Q1,
                  ]
               }
            },
            {
               "text":{
                  "text":[
                  "The options are :",
                  ]
               }
            },
            {
               "text":{
                  "text":[
                  op1+"~"+op2+"~"+op3+"~"+op4,
                  ]
               }
            },
            {
               "text":{
                  "text":[
                  "current score = "+str3,
                  ]
               }
            }
         ],
         "payload":{
            "google":{
               "expectUserResponse":True,
               "richResponse":{
                  "items":[
                     {
                        "simpleResponse":{
                           "textToSpeech":Q1
                        }
                     },
                     {
                        "simpleResponse":{
                           "textToSpeech":op1+"|*|"+op2+"|*|"+op3+"|*|"+op4
                        }
                     }
                  ],
                  "suggestions":[
                        {
                           "title":op1
                        },
                        {
                           "title":op2
                        },
                        {
                           "title":op3
                        },
                        {
                           "title":op4
                        }
                  ]
               }
            }
         }
      })
    else:
       tn_course.re_set()
       res=jsonify({
          "fulfillmentText":"Do you want to take quiz again?",
          "fulfillmentMessages":[
             {
               "text":{
                  "text":[
                  reply,
                  ]
               }
            },
            {
               "text":{
                  "text":[
                  "QUIZ ENDED-->Your total score is {} out of {}".format(score,count),
                  ]
               }
            },
            {
               "text":{
                  "text":[
                  "Do you want to take Quiz again?",
                  ]
               }
            }
          ],
          "payload":{
             "google":{
                "expectUserResponse":{
                   "items":[
                      {
                         "simpleResponse":{
                            "textToSpeech":"Do you want to take quiz again?"
                         }
                      }
                   ],
                   "suggestions":[
                      {
                         "title":"Yes"
                      },
                      {
                         "title":"No"
                      }
                   ]
                }
             }
          }
       })

 elif close is not None:
    tn_course.re_set()

 return res


if __name__=="__main__":
    app.run()