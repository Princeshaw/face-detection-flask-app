from flask import render_template, request
from flask import redirect, url_for
import os
from PIL import Image
from app.utils import pipeline_model
UPLOAD_FOLDER= 'static/uploads'

def base():
    return render_template('base.html')

def index():
    return render_template('index.html')

def faceApp():
    return render_template('faceapp.html') 

def getWidth(path):
    img = Image.open(path)
    size = img.size #width and height
    aspect = size[0]/size[1]
    w = 300*aspect
    return w

def gender():
    if request.method=='POST':
        f = request.files['image']
        filename = f.filename
        path = os.path.join(UPLOAD_FOLDER,filename)
        f.save(path)
        w = getWidth(path)
        #get the prediction
        img = pipeline_model(path,filename ,color="bgr")
        return render_template('gender.html',fileupload=True,image = filename,w=w)
    return render_template('gender.html', fileupload=False)        