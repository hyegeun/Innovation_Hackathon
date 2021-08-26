#flaskapp/__init__.py
from flask import Flask, g, request, Response, make_response, session, render_template
from flask import Markup, redirect, url_for
from datetime import datetime, date, timedelta
from werkzeug.utils import secure_filename
import os

app=Flask(__name__)

app.debug = True
@app.route("/project05_04", methods=['GET', 'POST'])
def project05_04():
    
    if request.method=='POST':
        global kind1
        kind1=request.form['style']
        kind1=str(kind1)

    cmd=("python ./AI/yolov5/detect.py --source ./flaskapp/static/images/input_img/ --classes 0 --nosave --save-crop")
    os.system(cmd)
    cmd1=("python ./flaskapp/removebg.py")
    os.system(cmd1)
    cmd2=("python ./AI/imgconv/convolution.py --back_img festival")
    os.system(cmd2)

    if kind1=='Hosoda':
        cmd3=("python ./AI/cartoongan/test.py --style Hosoda")
    elif kind1=='Shinkai':
        cmd3=("python ./AI/cartoongan/test.py --style Shinkai")
    elif kind1=='Hayao':
        cmd3=("python ./AI/cartoongan/test.py --style Hayao")
    os.system(cmd3)
    return render_template("project05_04.html")

@app.route('/project05_02', methods=['GET', 'POST'])
def project05_02():

    
    if request.method=='POST':
        
        kind1=request.form['style']
        kind1=str(kind1)
        cmd=("python ./AI/yolov5/detect.py --source ./flaskapp/static/images/input_img/ --classes 0 --nosave --save-crop")
        os.system(cmd)

        cmd1=("python AI/yolov5/detect.py --source AI/yolov5/result/exp --weight AI/yolov5/face_yolov5s.pt --save-txt --nosave")
        os.system(cmd1)

        cmd2=("python ./flaskapp/removebg.py")
        os.system(cmd2)

        cmd3=("python ./AI/imgconv/ocean.py")
        os.system(cmd3)
        
        
        if kind1=='Hosoda':
            cmd4=("python ./AI/cartoongan/test.py --style Hosoda")
        elif kind1=='Shinkai':
            cmd4=("python ./AI/cartoongan/test.py --style Shinkai")
        elif kind1=='Hayao':
            cmd4=("python ./AI/cartoongan/test.py --style Hayao")
        os.system(cmd4)
        
        
    
    return render_template("project05_02.html")

@app.route('/project04_04')
def project04_04():
    return render_template("project04_04.html")

@app.route('/project04_02')
def project04_02():
    return render_template("project04_02.html")

@app.route('/fileUpload', methods=['GET', 'POST'])
def upload_file():
    if request.method=='POST':
        f=request.files['file']
        inputname = ('inputimg%s' %f.filename[-4:])
        f.save('./flaskapp/static/images/input_img/' + secure_filename(inputname))
        files=os.listdir("./flaskapp/static/images/input_img/")
        
        
        
        return render_template('project04_02.html') 

@app.route('/project03_04')
def project03_04():
    return render_template("project03_04.html")


@app.route('/project03_03')
def project03_03():
    return render_template("project03_03.html")

@app.route('/project03_02')
def project03_02():
    return render_template("project03_02.html")

@app.route('/project03_01')
def project03_01():
    return render_template("project03_01.html")

@app.route('/project02')
def select_2():
    return render_template("project02.html")

@app.route('/')
def main_1():
    return render_template("project01.html")

@app.route('/about')
def about():
    return render_template("about.html")
@app.route('/loading_02', methods=['GET', 'POST'])
def loading():
    if request.method == 'POST':
        kind = request.form['style']
        kind = str(kind)

        #form1 = ('<input type="hidden" name="style" value="%s">' %kind)
        #form2 = '<input type="image" value="시작하기" alt="버튼">'
        #form = [form1, form2]
        
    return render_template("loading_02.html", value1 = kind)