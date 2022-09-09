from libs import stats


def check(data):
    if data is 'success':
        return stats.JsonResp(0, data).res()
    else:
        return stats.err[data], 403
