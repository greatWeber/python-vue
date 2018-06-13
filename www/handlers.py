#-*-coding: UTF-8-*-
#handlers.py

import re, time, json, logging, hashlib, base64, asyncio, os, functools, datetime, math

from coroweb import get, post

from utils import check_token, format_time, get_page_index, save_img, del_img

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
        page = Blog(user_id=userId,user_name=kw['userName'],user_image=kw['userImage'],title=title,info=kw['info'],thumb=kw['thumb'],content=kw['content'],imgs=kw['imgs'],md=kw['md'])
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
        yield from Blog.update2(id=pid,user_id=userId,title=title,info=kw['info'],thumb=kw['thumb'],content=kw['content'],imgs=kw['imgs'],md=kw['md'])
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
    where = 'is_del=0'
    num = yield from Blog.findNumber('count(*)', where=where)
    p = Page(num,index,size)
    logging.info('page:%s' % p)
    if num == 0:
        return dict(page=p,blogs=())
    blogs = yield from Blog.findAll(where=where,orderBy='created_time desc',limit=(p['offset'],p['size']))
    for blog in blogs:
        blog['created_time'] = format_time(blog['created_time'])

    return dict(page=p,blogs=blogs)

@get('/api/getDelPage')
def getDelPage(request,*,pageNum=1,pageSize=10):
    '''
    获取已删除的文章列表
    '''
    index = get_page_index(pageNum)
    size = get_page_index(pageSize)
    where = 'is_del=1'
    num = yield from Blog.findNumber('count(*)', where=where)
    p = Page(num,index,size)
    logging.info('page:%s' % p)
    if num == 0:
        return dict(page=p,blogs=())
    blogs = yield from Blog.findAll(where=where,orderBy='created_time desc',limit=(p['offset'],p['size']))
    for blog in blogs:
        blog['created_time'] = format_time(blog['created_time'])

    return dict(page=p,blogs=blogs)


@post('/api/reduction')
@asyncio.coroutine
@check_token
@asyncio.coroutine
def reduction(request):
    '''
    还原已删除的文章
    '''
    params = yield from request.json()
    kw = dict(**params)
    id = kw['id']
    if not id or not id.strip():
        return dict(code=-1,message="文章id不能为空")
    yield from Blog.update2(id=id,is_del=0)
    return dict(code=1,message="文章还原成功")


@post('/api/delPageRealy')
@asyncio.coroutine
@check_token
@asyncio.coroutine
def delPageRealy(request):
    '''
    彻底删除文章
    '''
    params = yield from request.json()
    kw = dict(**params)
    id = kw['id']
    if not id or not id.strip():
        return dict(code=-1,message="文章id不能为空")
    page = yield from Blog.find(id)
    imgpath = page['thumb']
    yield from page.remove()
    del_img(imgpath)
    comments = yield from Comment.findAll('blog_id=?',[id])
    ids = []
    for comment in comments:
        ids.append(comment['id'])
    if len(ids) >0:
        yield from Comment.remove2(id=ids)
    
    return dict(code=1,message="文章已彻底删除")



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
    添加留言
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
        page = yield from Blog.find(blogId)
        num = page['comment_num']
        num = num +1
        yield from Blog.update2(id=blogId,comment_num=num)

        result = dict(code=1,message="留言成功")
    return result

@get('/api/getComment')
@asyncio.coroutine
def getComment(request, *, blogId, pageNum, pageSize):
    '''
    获取留言列表
    '''
    index = get_page_index(pageNum)
    size = get_page_index(pageSize)
    if not blogId or not blogId.strip():
        return dict(code=-1,message="文章id不能为空")
    where = "is_del=0 AND blog_id='%s'" % blogId
    num = yield from Comment.findNumber('count(*)',where=where)
    p = Page(num,index,size)
    logging.info('page:%s' % p)
    if num == 0:
        return dict(code=1,page=p,comments=())
    comments = yield from Comment.findAll(where=where,orderBy='created_time desc',limit=(p['offset'],p['size']))
    for comment in comments:
        comment['created_time'] = format_time(comment['created_time'])

    return dict(code=1,page=p,comments=comments)


@post('/api/delComment')
@asyncio.coroutine
@check_token
@asyncio.coroutine
def delComment(request):
    '''
    删除评论
    '''
    params = yield from request.json()
    kw = dict(**params)
    if not kw['id'] or not kw['id'].strip():
        return dict(code=-1,message="id不能为空")
    elif not kw['blogId'] or not kw['blogId'].strip():
        return dict(code=-1,message="文章id不能为空")
    comment = Comment(id=kw['id'])
    yield from comment.remove()
    page = yield from Blog.find(kw['blogId'])
    num = page['comment_num']
    num = num-1
    yield from Blog.update2(id=kw['blogId'],comment_num=num)
    return dict(code=1,message="留言删除成功")


@post('/api/clearImgs')
@asyncio.coroutine
def clearImgs(request):
    '''
    清理图片
    '''
    pages = yield from Blog.findAll();
    imgs = []
    for page in pages:
        imgs.append(page['thumb'])
        img = page['imgs'].split(',')
        for i in img:
            imgs.append(i)
    currentpath = os.path.abspath('.')
    upload = os.path.join(currentpath,'upload')
    #列出当前目录下的所有文件
    dirs = ['upload/'+x for x in os.listdir(upload) if os.path.splitext(x)]
    for img in dirs:
        if img not in imgs:
            os.remove(img)

    return dict()


@get('/api/emoticon')
@asyncio.coroutine
def emoticon(request):
    currentpath = os.path.abspath('.')
    emoticon = os.path.join(currentpath,'emoticon')
    dirs = [x for x in os.listdir(emoticon)]
    logging.info(dirs)
    emoticons = [];
    for Dir in dirs:
        imgDir = os.path.join(emoticon,Dir)
        imgs = ['emoticon/'+Dir+'/'+x for x in os.listdir(imgDir)]
        imgDict = dict(path=imgs,dir=Dir)
        emoticons.append(imgDict)
        logging.info(emoticons)
    return dict(code=1,message="表情包获取成功",emoticons=emoticons,dirs=dirs)









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
    total = math.ceil(num/size)
    offset = (index-1)*size
    if index*size < num:
        pageSize = size
    else:
        pageSize = num - offset
    return dict(offset=offset,size=pageSize,total=total)





