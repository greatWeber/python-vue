#-*-coding: UTF-8-*-
#utils.py


import re, time, json, logging, hashlib, base64, asyncio, os, functools, datetime

from aiohttp import web

from models import Token

def check_token(func):
    '''
    检查token是否过期
    '''
    @functools.wraps(func)
    def wrapper(*args,**kw):
        err = False
        #获取request里面的参数
        params = yield from kw['request'].json()
        kws = dict(**params)
        key = kws['token']
        if key is None:
            err = True
        else:
            token = yield from Token.findAll('token_key=?',[key])

            if len(token) == 0:
                err = True
            else:
                now = datetime.datetime.now()
                end = now - datetime.timedelta(hours=3) #有效期
                nowNum = time.mktime(now.timetuple())
                endNum = time.mktime(end.timetuple())
                lastTime = token[0]['last_time']

                if lastTime < endNum :
                    #过期
                    err = True
        if err:
            r = web.Response()
            r.content_type = 'application/json'
            Dict = dict(code=-1,message='token失效，请重新登录')
            r.body = json.dumps(Dict,ensure_ascii=False).encode('utf-8')
            return r
        res = yield from func(*args,**kw)
        return res
    return wrapper
                        



@asyncio.coroutine
def createToken(uid):
    '''
    生成token
    '''
    shal = '%s=%s=%s' % ('Token',uid, time.time())
    shal_uid = hashlib.sha1(shal.encode('utf-8')).hexdigest()

    token = Token(id=next_id(),uid=uid,key=shal_uid)
    yield from token.save()
    return token['key']

@asyncio.coroutine
def changeToken(uid):
    '''
    修改token
    '''
    shal = '%s=%s=%s' % ('Token',uid, time.time())
    shal_uid = hashlib.sha1(shal.encode('utf-8')).hexdigest()
    token = Token.findAll('uid=?',[uid])[0]
    yield from token.update(key=shal_uid)
    return token.key


def save_img(suffix, content,path='upload'):
    '''
    保存图片
    '''
    if not os.path.exists(path):
        os.makedirs(path)
    img_name = '%s.%s' % (int(time.time()*1000),suffix)
    img_path = os.path.join(path,img_name)
    with open(img_path,'wb') as f:
        f.write(content)
    return '%s/%s' % (path,img_name)

def del_img(imgpath):
    '''
    删除图片
    '''
    if os.path.isfile(imgpath):
        os.remove(imgpath)
        logging.info('图片已删除')


def get_page_index(str):
    '''
    获取页数
    '''
    p = 1;
    try:
        p = int(str)
    except ValueError as e:
        pass
    if p<1:
        p=1
    return p


def format_time(strtime):
    #格式化时间
    #strtime: 传进来的时间
    localtime = time.localtime(strtime)
    return time.strftime("%Y-%m-%d", localtime)



