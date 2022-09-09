# coding=utf-8

# 返回data的类
class JsonResp(object):

    # python中可选参数是一个元组
    def __init__(self, code=0, *data):
        self.code = code
        if len(data):
            self.data = data[0]

    def res(self):
        return dict(data=self.data, code=self.code)


# 异常的类
class ErrorStat(JsonResp):
    def __init__(self, code, message, *data):
        super(ErrorStat, self).__init__(code, *data)
        self.message = message

    def res(self):
        return dict(code=self.code, message=self.message)


# 异常实例
err = dict(

)
