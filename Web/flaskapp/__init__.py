#flaskapp/__init__.py
from flask import Flask, g, request, Response, make_response, session, render_template
from flask import Markup, redirect, url_for
from datetime import datetime, date, timedelta
from werkzeug.utils import secure_filename
import os

app=Flask(__name__)

app.debug = True

@app.route('/')
def main_1():
    return render_template("project01.html")

@app.route('/about')
def about():
    return render_template("about.html")
@app.route('/loading_02')
def loading():
    return render_template("loading_02.html")