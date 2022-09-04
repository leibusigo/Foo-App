# coding=utf-8
from flask import Flask
from controllers.basic import basic_api

app = Flask(__name__)
# 基本功能路由
app.register_blueprint(basic_api, url_prefix='/basic')


# 请求拦截
# @app.before_request
# def before():


# 响应拦截
@app.after_request
def after(response):
    print(response.status)
    return response


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4018)
