#-*-coding: UTF-8-*-
#handlers.py

import re, time, json, logging, hashlib, base64, asyncio, os, functools, datetime

from coroweb import get, post

from utils import check_token, format_time, get_page_index, save_img

from apis import APIValueError, APIResourceNotFoundError

from models import next_id, User, Comment, Blog, Token

from aiohttp import web

_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHAI = re.compile(r'^[0-9a-f]{40}$')


def test(func):
    '''
    测试证明，如果一个装饰器是异步的，必须这样子返回，
    同时在使用装饰器的前面使用@asyncio.coroutine来声明它是一个异步函数
    '''
    @functools.wraps(func)
    def wrapper(*args,**kw):
        yield from kw['request'].json()
        logging.info('---------------------test')
        res = yield from func(*args,**kw)
        return res
    return wrapper

@get('/')
def index(request):
    return {
        '__template__': 'index.html'
    }

@post('/api/register')
def register(*,email, name, psd):
    r = web.Response()
    if not name or not name.strip():
        # raise APIValueError('name')
        result = dict(code=-1,message='名称不能为空')
    elif not email or not _RE_EMAIL.match(email):
        # raise APIValueError('email')
        result = dict(code=-1,message='邮箱不正确')

    elif not psd :
        # raise APIValueError('psd')
        result = dict(code=-1,message='密码不能为空')
    else:
        users =yield from User.findAll('name=?',[name])
        logging.info(len(users))
        if len(users) > 0:
            result = dict(code=-1,message='已经存在用户')
        else:
            uid = next_id()
            shal_psd = '%s:%s' % (uid, psd)
            # logging.info(shal_psd.encode('utf-8'))
            # logging.info(hashlib.sha1(shal_psd.encode('utf-8')))
            user = User(id=uid,name=name,nickname='',email=email,password=hashlib.sha1(shal_psd.encode('utf-8')).hexdigest(),image='')
            
            yield from user.save()
            #创建token
            shal = '%s=%s=%s' % ('Token',uid, time.time())
            shal_uid = hashlib.sha1(shal.encode('utf-8')).hexdigest()

            token = Token(id=next_id(),uid=uid,token_key=shal_uid)
            yield from token.save()
            result =dict(code=1,message='注册成功')

    
    r.content_type='application/json'

    r.body=json.dumps(result,ensure_ascii=False).encode('utf-8')
    return r

@post('/api/login')
def login(*, name, psd):
    r = web.Response()
    if not name or not name.strip():
        result = dict(code=-1,message="名称不能为空")
    elif not psd:
        result = dict(code=-1,message="密码不能为空")
    else:
        users = yield from User.findAll('name=?',[name])
        if len(users) == 0:
            result = dict(code=-1,message="没有此用户")
        else:
            user = users[0]
            shal = '%s:%s' % (user.id, psd)
            shal_psd = hashlib.sha1(shal.encode('utf-8')).hexdigest()
            # shal_psd = hashlib.sha1()
            # shal_psd.update(user.id.encode('utf-8'))
            # shal_psd.update(b':')
            # shal_psd.update(psd.encode('utf-8'))
            if user.password != shal_psd:
                result = dict(code=-1,message="密码不正确")
            else: 
                #修改并返回token
                tokens = yield from Token.findAll('uid=?',[user.id])
                shal = '%s=%s=%s' % ('Token',user.id, time.time())
                shal_uid = hashlib.sha1(shal.encode('utf-8')).hexdigest()

                token = Token(id=tokens[0].id, uid=user.id,token_key=shal_uid,last_time=time.time())
                yield from token.update()
                r.set_cookie('USER_NAME',user.id,max_age=86400,httponly=True)
                logging.info('token: %s' % token['token_key'])
                userDict = dict(id=user.id,name=user.name,token=token['token_key'])
                result = dict(code=1,message="登录成功",list=userDict)
    r.content_type = 'application/json'
    r.body = json.dumps(result, ensure_ascii=False).encode('utf-8')
    return r

@get('/api/logout')
def logout(request):
    r = web.Response()
    r.set_cookie('USER_NAME','-deleted-',max_age=0,httponly=True)
    result = dict(code=1,message="退出登录成功")
    r.content_type='application/json'
    r.body = json.dumps(result, ensure_ascii=False).encode('utf-8')
    return r


@post('/api/addPage')
@asyncio.coroutine
@check_token
@asyncio.coroutine
def addPage(request):
    '''
    添加文章
    '''
    params = yield from request.json()
    kw = dict(**params)
    userId = kw['userId']
    title = kw['title']
    if not userId or not userId.strip():
        result = dict(code=-1,message="请重新登录")
    elif not title or not title.strip():
        result = dict(code=-1, message="标题不能为空")
    else:
        page = Blog(user_id=userId,user_name=kw['userName'],user_image=kw['userImage'],title=title,info=kw['info'],thumb=kw['thumb'],content=kw['content'])
        yield from page.save()
        result = dict(code=1,message="文章添加成功")
    r = web.Response()
    r.content_type='application/json'
    r.body=json.dumps(result,ensure_ascii=False).encode('utf-8')
    return r

@post('/api/editPage')
@asyncio.coroutine
@check_token
@asyncio.coroutine
def editPage(request):
    '''
    修改文章
    '''
    params = yield from request.json()
    kw = dict(**params)
    title = kw['title']
    pid= kw['id']
    userId= kw['userId']
    if not userId or not userId.strip():
        result = dict(code=-1,message="请重新登录")
    if not pid or not pid.strip():
        result = dict(code=-1, message="参数有误")
    elif not title or not title.strip():
        result = dict(code=-1, message="标题不能为空")
    else:
        # page = Blog(id=pid,user_id=userId,title=title,info=kw['info'],thumb=kw['thumb'],content=kw['content'])
        yield from Blog.update2(id=pid,user_id=userId,title=title,info=kw['info'],thumb=kw['thumb'],content=kw['content'])
        result = dict(code=1,message="文章修改成功")
    # r = web.Response()
    # r.content_type='application/json'
    # r.body=json.dumps(result,ensure_ascii=False).encode('utf-8')
    return result


@get('/api/getPage')
def getPage(request,*,pageNum=1,pageSize=10):
    '''
    获取文章列表
    '''
    index = get_page_index(pageNum)
    size = get_page_index(pageSize)
    num = yield from Blog.findNumber('count(id)')
    p = Page(num,index,size)
    logging.info('page:%s' % p)
    if num == 0:
        return dict(page=p,blogs=())
    blogs = yield from Blog.findAll(where='is_del=0',orderBy='created_time desc',limit=(p['offset'],p['size']))
    for blog in blogs:
        blog['created_time'] = format_time(blog['created_time'])

    return dict(page=p,blogs=blogs)

@post('/api/delPage')
@asyncio.coroutine
@check_token
@asyncio.coroutine
def delPage(request):
    '''
    删除文章
    '''
    params = yield from request.json()
    kw = dict(**params)
    pid = kw['id']
    if not pid or not pid.strip():
        result = dict(code=-1,message="id不能为空")
    yield from Blog.update2(id=pid,is_del=True)
    result = dict(code=1,message="删除成功")
    return result;
    

@get('/api/detail')
@asyncio.coroutine
def detail(request,*,id):
    '''
    获取文章详情
    '''

    # params = yield from request.json()
    # kw = dict(**params)
    # id = kw['id']
    if not id or not id.strip():
        result = dict(code=-1,message="文章id不能为空")
    page = yield from Blog.find(id)
    if len(page) < 0:
        result = dict(code=-1,message="文章不存在")
    else:
        if page['is_del'] == 1:
            result = dict(code=-1,message="该文章已经被删除，请到回收站还原")
        else:
            page['created_time'] = format_time(page['created_time'])
            result = dict(code=1,blog=page)

    return result


@post('/api/addComment')
@asyncio.coroutine
@check_token
@asyncio.coroutine
def addComment(request):
    '''
    添加文章
    '''
    params = yield from request.json()
    kw = dict(**params)
    userId = kw['userId']
    blogId = kw['blogId']

    content = kw['content']
    if not userId or not userId.strip():
        result = dict(code=-1,message="请重新登录")
    elif not blogId or not blogId.strip():
        result = dict(code=-1, message="blogId不能为空")
    elif not content or not content.strip():
        result = dict(code=-1, message="留言不能为空")
    else:
        comment = Comment(user_id=userId,blog_id=blogId,user_name=kw['userName'],content=content)
        yield from comment.save()
        result = dict(code=1,message="留言成功")
    # r = web.Response()
    # r.content_type='application/json'
    # r.body=json.dumps(result,ensure_ascii=False).encode('utf-8')
    return result






@post('/api/upload')
@asyncio.coroutine
def upload(request):

    params = yield from request.post()
    kw = dict(**params)
    img = kw['image']
    content = img.file.read()
    suffix = str(img.content_type.split('/')[1])
    img_path = save_img(suffix,content)
    
    Dict = dict(path=img_path,suffix=suffix)
    result = dict(code=1,message="图片上传成功",list=Dict)
    r = web.Response()
    r.content_type='application/json'
    r.body = json.dumps(result,ensure_ascii=False).encode('utf-8')
    return r


def Page(num,index,size):
    # 分页
    offset = (index-1)*size
    if index*size < num:
        pageSize = size
    else:
        pageSize = num - offset
    return dict(offset=offset,size=pageSize)





