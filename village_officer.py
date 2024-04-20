import uuid
from flask import *
from database import *
from blk import *

village_officer=Blueprint('village_officer',__name__)

@village_officer.route('/village')
def villagehome():
    return render_template("village_officer.html")

@village_officer.route("/viewprofile",methods=['get','post'])
def viewprofile():
    data={}
    qry2="select * from village_officer where village_office_id='%s'"%(session['vid'])
    data['view']=select(qry2)
    
    return render_template("viewprofile.html",data=data)

@village_officer.route("/viewdepartment",methods=['get','post'])
def viewdepartment():
    data={}
    qry3="select * from department"
    data['view']=select(qry3)

    return render_template("viewdepartment.html",data=data)


@village_officer.route("/village_view_clerk",methods=['get','post'])
def village_view_clerk():
    id=request.args['id']
    data={}
    qry="select * from clerk where department_id='%s'"%(id)
    res=select(qry)
    data['view']=res
    return render_template("village_view_clerk.html",data=data)



@village_officer.route("/viewnotification",methods=['get','post'])
def viewnotification():
    data={}
    qry5="select * from notification"
    data['view']=select(qry5) 
    return render_template("village_view_notification.html",data=data)





@village_officer.route("/village_officer_change_password",methods=['get','post'])
def village_officer_change_password():
    if 'add' in request.form:
        newpass=request.form['pwd']
        repass=request.form['pass']
        if newpass==repass:
            qry="update login set password='%s' where login_id='%s'"%(repass,session['lid'])
            update(qry)
            return ("<script>alert('Update Success');window.location='/village'</script>")

        else:
            return ("<script>alert('reenter password is not matching');window.location='/village_officer_change_password'</script>")
        
    return render_template("village_officer_change_password.html")



@village_officer.route("/village_view_application",methods=['get','post'])
def village_view_application():
    data={}
    qrt="SELECT * FROM `application`  INNER JOIN `forward_certificate_qr` USING(application_id) INNER JOIN `resubmit_certificate` USING (forward_id)  WHERE  resubmit_certificate.status='Forward To Village Officer'"
    res=select(qrt)
    data['view']=res

    return render_template("village_view_application.html",data=data)


# @village_officer.route('/village_add_certificate',methods=['get','post'])
# def village_add_certificate():
#     id=request.args['id']
#     if 'add' in request.form:
#         title=request.form['tit']
#         image=request.files['files']
#         path="static/"+str(uuid.uuid4())+image.filename
#         image.save(path)

#         qry="insert into add_block values (null,'%s','%s','%s','%s',curdate())"%(id,session['vid'],title,path)
#         insert(qry)

#     return render_template("village_add_certificate.html")


@village_officer.route('/village_add_certificate',methods=['get','post'])
def village_add_certificate():
    apid=request.args['id']
    if 'add' in request.form:
        title=request.form['tit']
        image=request.files['files']
        path="static/"+str(uuid.uuid4())+image.filename
        image.save(path)
        with open(compiled_contract_path) as file:
            contract_json = json.load(file)  # load contract info as JSON
            contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
        contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
        id=web3.eth.get_block_number()
        message = contract.functions.add_blocks_files(int(id),int(apid),int(session['vid']),title,path).transact()
        print(message)

        # qry="insert into add_block values (null,'%s','%s','%s','%s',curdate())"%(id,session['vid'],title,path)
        # insert(qry)

    return render_template("village_add_certificate.html",ids=apid)



@village_officer.route('/view_details', methods=['GET', 'POST'])
def view_details():
    ap_id=request.args['aid']
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
    data['med'] = res
    return render_template("view_files_uploads.html", data=data)