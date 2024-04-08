from flask import *
from database import *



admin=Blueprint('admin',__name__)

@admin.route('/adminhome')
def adminhome():
    return render_template("admin_home.html")


@admin.route("/viewfeedback",methods=['get','post'])
def viewfeedback():
    data={}
    qry="select * from feedback"
    res=select(qry)
    data['view']=res
    
    return render_template("viewfeedback.html",data=data)

@admin.route("/complaint_reply",methods=['get','post'])
def complaint_reply():
    data={}
    qry="select * from complaint"
    res=select(qry)
    data['view']=res
    

    
    if 'submit' in request.form:
        c_id=request.form['c_id']
        reply=request.form['reply']
        up="update complaint set reply='%s' where complaint_id='%s'"%(reply,c_id)
        update(up)
        return """<script>alert('Replyed');window.location='/complaint_reply'</script>"""
    
    return render_template("complaint_reply.html",data=data)

@admin.route("/notification",methods=['get','post'])
def notification():
    if 'submit' in request.form:
        title=request.form['title']
        description=request.form['description']
        qry="insert into notification values(null,'%s','%s',curdate())"%(title,description)
        insert(qry)
    
    
        
    return render_template("notification.html")


@admin.route("/department_registration",methods=['get','post'])
def dept_registration():
    data={}
    
    qry6="select * from department"
    res=select(qry6)
    data['view']=res
  
    if 'action' in request.args:
          action=request.args['action']
          id=request.args['id']
    else:
        action=None
    if action=='delete':
        qry3="delete from department where department_id='%s'"%(id)
        delete(qry3)
        return redirect(url_for('admin.dept_registration'))
        
    if action=='update':
        qry4="select * from department where department_id='%s'"%(id)
        res5=select(qry4)
        data['up']=res5
    if 'update' in request.form:
        dname=request.form['dname']
        qry8="update department set department_name='%s' where department_id='%s'"%(dname,id)
        update(qry8)

        return redirect(url_for('admin.dept_registration'))
        
    
    if 'submit' in request.form:
        dname=request.form['dname']
        qry="insert into department values(null,'%s')"%(dname)
        insert(qry)
        return redirect(url_for('admin.dept_registration'))
        
    return render_template("department_registration.html",data=data)

@admin.route("/villageoffice_registration",methods=['get','post'])
def villageoffice_registration():
    
    data={}
    qry7="select * from village_officer"
    res=select(qry7)
    data['view']=res
    if 'action' in request.args:
          action=request.args['action']
          id=request.args['id']
    else:
        action=None
    if action=='delete':
        qry8="delete from village_officer where village_office_id='%s'"%(id)
        delete(qry8)
        return redirect(url_for('admin.villageoffice_registration'))
    
    if action=='update':
        qry9="select * from village_officer where village_office_id='%s'"%(id)
        res5=select(qry9)
        data['up']=res5
    if 'update' in request.form:
        fname=request.form['fname']
        
        qry10="update village_officer set fname='%s' where village_office_id ='%s'"%(fname,id)
        update(qry10)
        lname=request.form['lname']
        qry11="update village_officer set lname='%s' where village_office_id ='%s'"%(lname,id)
        update(qry11)
        place=request.form['place']
        qry12="update village_officer set place='%s' where village_office_id ='%s'"%(place,id)
        update(qry12)
        phone=request.form['phone']
        qry13="update village_officer set phone='%s' where village_office_id ='%s'"%(phone,id)
        update(qry13)
        email=request.form['email']
        qry14="update village_officer set email='%s' where village_office_id ='%s'"%(email,id)
        update(qry14)

        return redirect(url_for('admin.villageoffice_registration'))
    
    if 'submit' in request.form:
        fname=request.form['fname']
        lname=request.form['last']
        place=request.form['place']
        phone=request.form['phone']
        email=request.form['email']





        qry="insert into village_officer values(null,null,'%s','%s','%s','%s','%s')"%(fname,lname,place,phone,email)
        insert(qry)
        return redirect(url_for('admin.villageoffice_registration'))
        
    
    return render_template("villageoffice_registration.html",data=data)

@admin.route("/clerk_registration",methods=['get','post'])
def clerk_registration():
    data={}
    qry7="select * from clerk"
    res=select(qry7)
    data['view']=res
    if 'action' in request.args:
          action=request.args['action']
          id=request.args['id']
    else:
        action=None
    if action=='delete':
        qry8="delete from clerk where clerk_id='%s'"%(id)
        delete(qry8)
        return redirect(url_for('admin.clerk_registration'))
    
    if action=='update':
        qry9="select * from clerk where clerk_id='%s'"%(id)
        res5=select(qry9)
        data['up']=res5
    if 'update' in request.form:
        fname=request.form['fname']
        
        qry10="update clerk set fname='%s' where clerk_id ='%s'"%(fname,id)
        update(qry10)
        lname=request.form['lname']
        qry11="update clerk set lname='%s' where clerk_id ='%s'"%(lname,id)
        update(qry11)
        place=request.form['place']
        qry12="update clerk set place='%s' where clerk_id ='%s'"%(place,id)
        update(qry12)
        phone=request.form['phone']
        qry13="update clerk set phone='%s' where clerk_id ='%s'"%(phone,id)
        update(qry13)
        email=request.form['email']
        qry14="update clerk set email='%s' where clerk_id ='%s'"%(email,id)
        update(qry14)

        return redirect(url_for('admin.clerk_registration'))
    
    if 'submit' in request.form:
        fname=request.form['fname']
        lname=request.form['last']
        place=request.form['place']
        phone=request.form['phone']
        email=request.form['email']





        qry="insert into clerk values(null,null,null,'%s','%s','%s','%s','%s')"%(fname,lname,place,phone,email)
        insert(qry)
        return redirect(url_for('admin.clerk_registration'))
        
    
    return render_template("clerk_registration.html",data=data)
