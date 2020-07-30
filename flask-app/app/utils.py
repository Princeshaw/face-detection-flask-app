import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn 
import cv2
import pickle

# load all data and models
haar = cv2.CascadeClassifier('./model/haarcascade_frontalface_default.xml')

mean = pickle.load(open('./model/mean_preprocess.pickle','rb'))
model_svm = pickle.load(open('./model/mode_svc.pickle','rb'))
model_pca = pickle.load(open('./model/pca_50.pickle','rb'))

print('model load sucessfully')
mean.shape

gender_pre = ['Male','Female']
font = cv2.FONT_HERSHEY_SIMPLEX
gender_pre = ['Male','Female']
font = cv2.FONT_HERSHEY_SIMPLEX
def pipeline_model(path,filename,color = 'bgr'):
    #step 1: read the image
    img = cv2.imread(path)
    # step 2 : convert into gray scale
    if color=='bgr':
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    else:
        gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    #step 3: crop the faces using haar cascade classifier
    faces = haar.detectMultiScale(gray,1.5,3)
    for x,y,w,h in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2) # drawing rectangle
        roi = gray[y:y+h,x:x+w]
        #step 4 : normalizating
        roi = roi/255.0
        #atep-5 : reshape image as 100 X 100
        if roi.shape[1] >100:
            roi_resize = cv2.resize(roi,(100,100),cv2.INTER_AREA)
            #print(roi_resize.shape)
        else:
            roi_resize = cv2.resize(roi,(100,100),cv2.INTER_CUBIC)
        #step 6: Flattening (1x10000)
        roi_reshape = roi_resize.reshape(1,-1)
        #print(roi_reshape.shape)
        # step 7: Subtract with mean
        roi_mean = roi_reshape-mean
        #step 8: get eigen image
        eigen_img = model_pca.transform(roi_mean)
        #step 9: pass to ML model
        results = model_svm.predict_proba(eigen_img)[0]
        #step 10 
        predict = results.argmax()
        score = results[predict]
        #step: 11
        text = "%s: %0.2f"%(gender_pre[predict],score)
        cv2.putText(img,text,(x,y),font,1,(0,255,0),2)
    cv2.imwrite('./static/predict/{}'.format(filename),img)    
        #return(img)
