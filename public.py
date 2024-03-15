from flask import *
from database import*

app=Flask(__name__)

public=Blueprint('public',__name__)

@public.route("/")
def home():
    return render_template("new_home.html")

@public.route("/login",methods=['get','post'])
def login():
    if 'log' in request.form:
        uname=request.form['username']
        passw=request.form['password']
        qry="select * from login where username='%s' and password='%s'"%(uname,passw)
        res=select(qry)
        session['log']=res[0]['login_id']
        if res[0]['usertype']=='admin':
            return redirect(url_for('admin.adminhome'))
        if res[0]['usertype']=='village_officer':
             qry1="select * from login where login_id='%s'"%(session['log'])
             res1=select(qry1)
             print(res1)
             if res1:
                    session['village_officer']=res1[0]['login_id']
                    return redirect(url_for('village_officer.voffice'))
                
        if res[0]['usertype']=='clerk':
            return redirect(url_for('clerk.clerkhome'))

            
            
            
    return render_template("login.html")



