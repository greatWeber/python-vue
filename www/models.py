#-*-coding: UTF-8-*-
#models.py

from orm import Model, StringField, BooleanField, IntergerField, FloatField, TextField

import uuid ,time

def next_id():
	return '%015d%s000' % (time.time()*1000, uuid.uuid4())


class User(Model):
    #用户表
    __table__ = 'users'

    id = StringField(primary_key=True,default=next_id,ddl='varchar(60)')
    name = StringField(ddl='varchar(50)')
    nickname = StringField(ddl='varchar(50)')
    password = StringField(ddl='varchar(50)')
    email = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(500)')
    created_time = FloatField(default=time.time())
    is_del = BooleanField()
    is_admin = BooleanField()


class Blog(Model):
    #博客表
    __table__ = 'blogs'

    id = StringField(primary_key=True,default=next_id,ddl='varchar(60)')
    user_id = StringField(ddl='varchar(60)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    title = StringField(ddl='varchar(50)')
    thumb = StringField(ddl='varchar(500)')
    info = StringField(ddl='varchar(200)')
    content = TextField()
    is_del = BooleanField()
    created_time = FloatField(default=time.time())

class Comment(Model):
    #评论
    __table__ = 'comments'
    id = StringField(primary_key=True,default=next_id,ddl='varchar(60)')
    blog_id = StringField(ddl='varchar(60)')
    user_id = StringField(ddl='varchar(60)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    content = TextField()
    is_del = BooleanField()
    created_time = FloatField(default=time.time())


class Token(Model):
    #token表
    __table__ = 'tokens'

    id = StringField(primary_key=True,default=next_id,ddl='varchar(60)')
    uid = StringField(ddl='varchar(60)')
    token_key = StringField(ddl='varchar(100)')
    last_time = FloatField(default=time.time())



