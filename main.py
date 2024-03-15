from flask import *
from database import*
from public import public
from user import user
from admin import admin
from village_officer import village_officer
from clerk import clerk


app=Flask(__name__)
app.secret_key='r7esttu'

app.register_blueprint(public)


app.register_blueprint(user)

app.register_blueprint(admin)
app.register_blueprint(village_officer)
app.register_blueprint(clerk)



app.run(debug=True)