from flask import *
from database import *



clerk=Blueprint('clerk',__name__)

@clerk.route('/clerkhome')
def clerkhome():
    return render_template("clerk_home.html")