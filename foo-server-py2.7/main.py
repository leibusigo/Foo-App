# coding=utf-8
import db
import os
import sys
from flask import Flask,request
from libs import stats
from controllers.basic import basic_api
from controllers.algorithm import algorithm_api
from dotenv import load_dotenv

app = Flask(__name__)
# 基本功能路由
app.register_blueprint(basic_api, url_prefix='/api/py27/basic')
app.register_blueprint(algorithm_api, url_prefix='/api/py27/algorithm')

# 自动搜索.env文件
load_dotenv(verbose=True)
# 指定env文件
if getattr(sys, 'frozen', False):
    root_dir = os.path.dirname(sys.executable)
else:
    bundle_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(bundle_dir)
load_dotenv(os.path.join(root_dir, '.env'))

white_list = ['/api/py27/basic/connect']


# 请求拦截
@app.before_request
def before():
    ip = db.session.find_one()
    request.ip = 1
    if ip is not None:
        request.ip = ip['ip']
    elif request.path not in white_list:
        return stats.err['ErrSessionNotFound']


# 响应拦截
@app.after_request
def after(response):
    print(response.status)
    return response


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4018)
