from flask import Flask
from app import views
import os

UPLOAD_FOLDER= 'static/uploads'
app = Flask(__name__,static_url_path='/static')

#url
app.add_url_rule('/base','base',views.base)
app.add_url_rule('/','index',views.index)
app.add_url_rule('/faceapp','faceapp',views.faceApp)
app.add_url_rule('/gender','gender',views.gender, methods=['GET','POST'])



#run
if __name__ =="__main__":
    app.run(debug=True)