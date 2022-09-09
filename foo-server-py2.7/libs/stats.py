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
# 2：机器人连接异常；3：py3.6服务器异常；4：会话异常
err = dict(
    ErrFailToConnect=ErrorStat(20001, '机器人连接失败').res(),
    ErrAlreadyConnect=ErrorStat(20002, '机器人已经连接').res(),
    ErrIpNotFound=ErrorStat(20003, 'ip未找到').res(),
    ErrParametersNotAllowed=ErrorStat(20004, '参数不符合要求').res(),
    ErrPy36ServerError=ErrorStat(30001, 'python3.6服务器异常').res(),
    ErrSessionNotFound=ErrorStat(40001, '会话不存在').res()
)
