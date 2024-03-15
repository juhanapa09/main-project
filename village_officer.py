from flask import *
from database import *

village_officer=Blueprint('village_officer',__name__)

@village_officer.route('/village')
def voffice():
    return render_template("village_officer.html")

@village_officer.route("/viewprofile",methods=['get','post'])
def viewprofile():
    data={}
    qry2="select * from village_officer"
    data['view']=select(qry2)
    
    return render_template("viewprofile.html",data=data)

@village_officer.route("/viewdepartment",methods=['get','post'])
def viewdepartment():
    data={}
    qry3="select * from department"
    data['view']=select(qry3)
    
    

   
    
    return render_template("viewdepartment.html",data=data)

@village_officer.route("/viewclerk",methods=['get','post'])
def viewclerk():
    data={}
    qry4="select * from clerk"
    data['view']=select(qry4)
    
    return render_template("viewclerk.html",data=data)

@village_officer.route("/viewnotification",methods=['get','post'])
def viewnotification():
    data={}
    qry5="select * from notification"
    data['view']=select(qry5)
    
    return render_template("view.html",data=data)

