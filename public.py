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

        if res:
            session['lid']=res[0]['login_id']
        
            if res[0]['usertype']=='admin':
                
                return ("<script>alert('login successfull');window.location='/adminhome'</script>")
            
            elif res[0]['usertype']=='village_officer':
                
                qry1="select * from village_officer where login_id='%s'"%(session['lid'])
                res1=select(qry1)
                print(res1)

                session['vid']=res1[0]['village_office_id']

                return ("<script>alert('login successfull');window.location='/village'</script>")
            
            elif res[0]['usertype']=='clerk':
                
                qry2="select * from clerk where login_id='%s' "%(session['lid'])
                res2=select(qry2)
            
                session['cid']=res2[0]['clerk_id']

                return ("<script>alert('login successfull');window.location='/clerkhome'</script>")      
        else:
            return ("<script>alert('invalid password');window.location='/login'</script>")

        
    return render_template("login.html")



