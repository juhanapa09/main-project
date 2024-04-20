from flask import *
from database import*
from public import public
from user import user
from admin import admin
from village_officer import village_officer
from clerk import clerk
from api import api


app=Flask(__name__)



app.secret_key='r7esttu'

app.register_blueprint(public)
app.register_blueprint(user)
app.register_blueprint(admin)
app.register_blueprint(village_officer)
app.register_blueprint(clerk)
app.register_blueprint(api)


app.run(debug=True,host="0.0.0.0",port=5003)