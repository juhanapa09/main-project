import uuid
from flask import *
from database import *
from blk import *
import qrcode


api=Blueprint("api",__name__)


@api.route("/userlogin")
def login():
    data={}

    username=request.args['uname']
    pwd=request.args['pwd']

    print(username,pwd)

    qry="select * from login where username='%s' and password='%s'"%(username,pwd)
    res=select(qry)

    

    if res:
        data['status']='success'
        data['data']=res
    else:
        data['status']='failed'


    return str(data)



@api.route("/userreg")
def userreg():
    data={}
    fname=request.args['fname']
    lname=request.args['lname']
    place=request.args['place']
    phone=request.args['no']
    email=request.args['mail']
    username=request.args['username']
    pwd=request.args['pass']

    qry="insert into login values(null,'%s','%s','user')"%(username,pwd)
    print(qry)
    id=insert(qry)

    qry1="insert into user values(null,'%s','%s','%s','%s','%s','%s')"%(id,fname,lname,place,phone,email)
    res=insert(qry1)
    print(qry1)

    if res:
        data['status']="success"
    else :
        data['status']='failled'

    return str(data)




@api.route('/view_category')
def view_category():

    data={}

    qry="select * from application_category"
    res=select(qry)
    print(res)

    if res:
        data['status']="success"
        data['data']=res
    else:
        data['status']='failed'
    data['method']="view_category"

    return str(data)


@api.route('/viewcomplaint')
def viewcomplaint():

    data={}
    sender_id=request.args['sender_id']
    qry="select * from complaint where sender_id='%s'"%(sender_id)
    res=select(qry)
    print(res)

    if res:
        data['status']="success"
        data['data']=res
    else:
        data['status']='failed'
    data['method']="viewenquiry"

    return str(data)


@api.route('/sendcomplaint')
def sendcomplaint():
    data={}
    sender_id=request.args['sender_id']
    title=request.args['title']
    descr=request.args['enquiry']
    
    qry="insert into complaint values(null,'%s','%s','%s','pending',curdate())"%(sender_id,title,descr)
    res=insert(qry)

    if res:
        data['status']="success"
    else:
        data['status']='failed'
    data['method']='sendenquiry'
   
    return str(data)




@api.route('/sendfeedback')
def sendfeedback():
    data={}
    sender_id=request.args['sender_id']
    feedback=request.args['feedback']
   
    
    qry="insert into feedback values(null,'%s','%s',curdate())"%(sender_id,feedback)
    res=insert(qry)

    if res:
        data['status']="success"
    else:
        data['status']='failed'
    data['method']='sendfeedback'
   
    return str(data)



@api.route('/recchangepass')
def recchangepass():
    data={}
    curpas=request.args['curpas']
    newpas=request.args['newpas']
    confpas=request.args['confpas']
    lid=request.args['log_id']

    q="select * from login where login_id='%s' and password='%s'"%(lid,curpas)
    res=select(q)

    if res:
        if newpas == confpas:
            q="update login set password='%s' where login_id='%s'"%(newpas,lid)
            update(q)
            data['status']='success'
        else:
            data['status']='mismatch'
    else:
        data['status']='failed'

    return str(data)



@api.route('/apply_for_application')
def apply_for_application():
    data={}

    reason=request.args['reason']
    title=request.args['title']
    user_id=request.args['user_id']
    application_category_id=request.args['application_category_id']

    qrt="insert into application values(null,'%s',(select user_id from user where login_id='%s'),'%s','%s',curdate(),'pending')"%(application_category_id,user_id,title,reason)
    res=insert(qrt)


    if res:
        data['status']='success'
    else:
        data['status']='failed'
    data['method']='apply'

    return str(data)


# @api.route('/viewappliedapplication')
# def viewappliedapplication():
#     data={}
#     application_categoryid=request.args['catid']
#     qry="select * from application where application_category_id='%s'"%(application_categoryid)
#     res=select(qry)

#     if res:
#         data['status']="success"
#         data['data']=res
#     else:
#         data['status']='failed'
#     data['method']='view'

#     return str(data)



@api.route('/view_forward_certificat')
def view_forward_certificat():
    data={}

    applicationid=request.args['applicationid']

    qry="select * from forward_certificate_qr where application_id='%s'"%(applicationid)
    res=select(qry)

    if res:
        data['status']="success"
        data['data']=res
    else:
        data['status']='failed'
    data['method']='view'

    return str(data)


@api.route('/user_uploads_file',methods=['get','post'])
def user_uploads_file():
    data={}
    login_id=request.form['user_id']
    title=request.form['title']
    image=request.files['image']
    path="static/"+str(uuid.uuid4())+image.filename
    image.save(path)
    qrt="insert into certificate values(null,(select user_id from user where login_id='%s'),'%s','%s','pending',curdate())"%(login_id,title,path)
    res=insert(qrt)
    if res:
            o="select * from certificate where certificate_id='%s'"%(res)
            e=select(o)
            if e:
                session['name']=e[0]['title']
            qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
            )
            qr.add_data(res)
            qr.make(fit=True)

            # Create an image of the QR code
            img = qr.make_image(fill_color="black", back_color="white")
            rr="static/qr_image/"+ session['name'] +".png" # Save the QR code image to a file
            img.save(rr)
            
            up="update certificate set qr_code='%s' where certificate_id='%s'"%(rr,res)
            update(up)

            data['status']='success'
            data['data']=res
    else:
        data['status']='failed'

    return str(data)



@api.route("/view_certicate")
def view_certicate():
    data={}
    id=request.args['id']
    qry="select * from certificate where user_id=(select user_id from user where login_id='%s')"%(id)
    res=select(qry)
    if res:
        data['status']='success'
        data['data']=res
    else:
        data['status']='failed'
    data['method']='view'
    return str(data)


@api.route("/resubmit_certificate")
def resubmit_certificate():
    data={}
    cid=request.args['cid']
    fid=request.args['fid']

    qry="insert into resubmit_certificate values(null,'%s','%s',curdate(),'pending')"%(fid,cid)
    insert(qry)
    qrtt="update forward_certificate_qr set status='certificate submitted' where forward_id='%s'"%(fid)
    res=update(qrtt)
    if res:
        data['status']='success'
    else:
        data['status']='failed'
    data['method']='send'
    return str(data)

###############################qrcode############################

@api.route("/admin_manage_table",methods=['get','post'])
def admin_manage_table():
    data={}
    if 'submit' in request.form:
        table=request.form['table']
        
        
        qry="insert into tables values(null,'%s','pending','pending')"%(table)
        res=insert(qry)
        
        if res:
            o="select * from tables where table_id='%s'"%(res)
            e=select(o)
            if e:
                session['name']=e[0]['table_number']
            qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
            )
            qr.add_data(res)
            qr.make(fit=True)

            # Create an image of the QR code
            img = qr.make_image(fill_color="black", back_color="white")
            rr="static/qr_image/"+ session['name'] +".png" # Save the QR code image to a file
            img.save(rr)
            
            up="update tables set qr_image='%s' where table_id='%s'"%(rr,res)
            update(up)
        
        return '''<script>alert("Added Successfully");window.location='/admin_manage_table'</script>'''
    
    q="select * from tables"
    r=select(q)
    data['view']=r
    
    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']
    else:
        action=None
    
    if action=='delete':
        qr="delete from tables where table_id='%s'"%(id)
        delete(qr)
        return '''<script>alert("Deleted Successfully");window.location='/admin_manage_table'</script>'''
    if action=='free':
        qr1="update tables set status='assigned' where table_id='%s'"%(id)
        update(qr1)
        return '''<script>alert("Table is free now");window.location='/admin_manage_table'</script>'''

    
    if action=='update':
        q1="select * from tables where table_id='%s'"%(id)
        r1=select(q1)
        data['upd']=r1
    if 'update' in request.form:
        table=request.form['table']
        
        
        q2="update tables set table_number='%s' where table_id='%s'"%(table,id)
        update(q2)
        return '''<script>alert("Updated Successfully");window.location='/admin_manage_table'</script>'''

    return render_template("admin_manage_table.html",data=data)




@api.route('/view_applied_application')
def view_applied_application():
    data={}

    user_id=request.args['user_id']

    qry="select * from application where user_id=(select user_id from user where login_id='%s')"%(user_id)
    res=select(qry)

    if res:
        data['status']="success"
        data['data']=res
    else:
        data['status']='failed'
    data['method']='view'


    return str(data)




@api.route('/view_blk_certificates')
def view_blk_certificates():
    ap_id=request.args['applicationid']
    # if not session.get('lid') is None:
    data = {}
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    blocknumber = web3.eth.get_block_number()
    res = []
    try:
        for i in range(blocknumber, 0, -1):
            a = web3.eth.get_transaction_by_block(i, 0)
            decoded_input = contract.decode_function_input(a['input'])
            print(decoded_input, "///////////////////")
            if str(decoded_input[0]) == "<Function add_blocks_files(uint256,uint256,uint256,string,string)>":
                if int(decoded_input[1]['application_id']) == int(ap_id):
                    res.append(decoded_input[1])
    except Exception as e:
        print("", e)
    data['data'] = res

    if res:
        data['status']="success"
        data['data']=res
    else:
        data['status']='failed'
    data['method']='view'
    return str(data)