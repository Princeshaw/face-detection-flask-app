from flask import render_template, request
from flask import redirect, url_for

def base():
    return render_template('base.html')

def index():
    return render_template('index.html')

def faceApp():
    return render_template('faceapp.html')    