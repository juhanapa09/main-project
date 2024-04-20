from flask import *
from database import *



clerk=Blueprint('clerk',__name__)

@clerk.route('/clerkhome')
def clerkhome():
    return render_template("clerk_home.html")


@clerk.route('/clerk_view_category')
def clerk_view_category():
    data={}
    qry="select * from application_category"
    res=select(qry)
    data['view']=res
    return render_template("clerk_view_application_category.html",data=data)

@clerk.route('/clerk_view_notification')
def clerk_view_notification():
    data={}
    qry="select * from notification"
    res=select(qry)
    data['view']=res

    return render_template("clerk_view_notification.html",data=data)



@clerk.route('/clerk_view_feedback')
def clerk_view_feedback():
    data={}
    qry="select * from feedback"
    res=select(qry)
    data['view']=res

    return render_template("clerk_view_feedback.html",data=data)


@clerk.route('/clerk_view_application')
def clerk_view_application():
    data={}
    qry="select * from application "
    res=select(qry)
    data['view']=res
    
    return render_template("clerk_view_application.html",data=data)



@clerk.route('/clerk_forward_to_user',methods=['get','post'])
def clerk_forward_to_user():
    id=request.args['id']
    data={}
    qry1="select * from forward_certificate_qr where application_id='%s'"%(id)
    res=select(qry1)
    data['view']=res
    
    if 'req' in request.form:
        title=request.form['file']
        qry="insert into  forward_certificate_qr values (null,'%s','%s','%s','forward')"%(id,session['cid'],title)
        insert(qry)
        qrt="update application set status='request for certificate' where application_id='%s'"%(id)
        update(qrt)
        qrtt="update forward_certificate_qr set status='request for certificate' where application_id='%s'"%(id)
        update(qrtt)
        return ("<script>alert('Send successfull');window.location='/clerk_view_application'</script>")

        

    return render_template("clerk_forward_to_user.html",data=data)


@clerk.route('/clerk_view_certificate')
def clerk_view_certificate():
    id1=request.args['id1']
    id=request.args['id']
    data={}
    qry="select * from resubmit_certificate inner join certificate using(certificate_id) where forward_id='%s'"%(id)  
    res=select(qry)
    data['view']=res

    return render_template("clerk_view_certificate.html",data=data,id1=id1)





@clerk.route('/clerk_view_certificate_image', methods=['GET', 'POST'])
def clerk_view_certificate_image():

    # Get the detected QR code ID from the request
    certificate_id = request.args['id']
    data = {}
    qry = "select * from certificate where certificate_id='%s'"%(certificate_id)
    res = select(qry)
    data['view'] = res
    print(data['view'],"/////////////////////")

    # return redirect(url_for('clerk.clerkhome'))
    
    return render_template("clerk_view_certificate_image.html",data=data)
    




@clerk.route('/qrcode_scan_result', methods=['POST'])
def qrcode_scan_result():
    # Get the QR code data from the request
    result = {}
    data = request.json
    qr_code_data = data['qrCodeData']
    
    # Process the QR code data as needed
    print("QR Code Data Received:", qr_code_data)
    qry = "select * from certificate where certificate_id='%s'" % qr_code_data
    res = select(qry)
    result['view'] = res

    # Return JSON response with the message
    response_data = {'message': 'QR Code data received successfully', 'view': res}
    return jsonify(response_data)


@clerk.route('/clerk_forward_to_village')
def clerk_forward_to_village():
    aid=request.args['aid']
    if 'id' in request.args:
        id=request.args['id']
        ids=request.args['ids']

    qry="update resubmit_certificate set status='Forward To Village Officer' where resubmit_certificate_id='%s'"%(id)
    update(qry)
    qrtt="update forward_certificate_qr set status='Forward To Village Officer' where forward_id='%s'"%(ids)
    update(qrtt)
    qrt="update application set status='Forward To Village Officer' where application_id='%s'"%(aid)
    update(qrt)
     
    return ("<script>alert('Forward successfull');window.location='/clerkhome'</script>")
