import os

from flask import Flask, render_template,redirect,request,url_for
import sqlite3

from Crawler import params, get_page, parse_page
from comment import runx
from mongo import save_to_mongo
from test import analysis_by_keyword

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/index', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        global keyword
        keyword=request.form.get('keyword')


    # analysis_by_keyword(keyword)
    #     #
    #     # os.system("python ./ciyun.py")
    #     # os.system("python ./zhifangtu.py")
    return render_template('loading.html')



@app.route('/loading')
def loading():
    analysis_by_keyword(keyword)

    os.system("python ./ciyun.py")
    os.system("python ./zhifangtu.py")
    return render_template("index.html")

@app.route('/zhifangtu')
def tiaoxingtu():
    return render_template("zhifangtu.html")

@app.route('/hot')
def hot():
    return render_template("hot.html")

@app.route('/bing')
def bing():
    return render_template("bing.html")

@app.route('/word')
def word():
    return render_template("word.html")


if __name__ == '__main__':
    app.run()
