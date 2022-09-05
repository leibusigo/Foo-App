# coding=utf-8
import db
from flask import Flask
from flask import request
from flask import redirect
from controllers.basic import basic_api

app = Flask(__name__)
# 基本功能路由
app.register_blueprint(basic_api, url_prefix='/api/py27/basic')

white_list = ['/api/py27/basic/connect']


# 请求拦截
@app.before_request
def before():
    ip = db.session.find_one()
    request.ip = 1
    if ip is not None:
        request.ip = ip['ip']
    elif request.path not in white_list:
        return redirect('/login')


# 响应拦截
@app.after_request
def after(response):
    print(response.status)
    return response


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4018)
