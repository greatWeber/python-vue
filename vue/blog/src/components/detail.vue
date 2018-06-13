<template>
    <div class="detail">
        <div class="header clear">
            <h1 class="title fl">{{blog.title}}</h1>
            <span class="time fr">{{blog.create_time}}</span>
        </div>
        <div class="thumb">
            <img :src="imgSrc" alt="" class="img">
        </div>
        <div class="container markdown-body" v-html="blog.content">
            
        </div>

        <div class="messageBoard">
            <p class="title-line"><span class="text">留言列表</span></p>
            <quill-editor class="editor-example bubble textarea"
                      ref="myTextEditor"
                      :content="message_content"
                      :options="editorOption"
                      @change="onEditorChange($event)">
            </quill-editor>
            <!-- <textarea class="textarea" v-model="message_content"></textarea> -->
            <a class="send" @click="sendMessage">留言</a>
            <div class="emoticon">
                <a class="em-btn icon-vue-em" @click="em_show = !em_show"></a>
                <div class="em-box" v-show="em_show">
                    <div class="em-imgs" >
                        <img v-for="img in em_imgs" class="img" :src="HOST+''+img" @click="choiceImg"></img>
                    </div>
                    <ul class="em-ul" >
                        <li v-for="(em, index) in em_ul" v-bind:class="[em_index == index? 'act': '', 'em-ul-item']" @click="choiceUl(index)">{{em}}</li>
                    </ul>
                </div>
            </div>

            <div class="list">
                <div class="list-item" v-for="item in list">
                    <p class="name">{{item.user_name}}</p>
                    <div class="message">
                        <p class="time">{{item.created_time}}</p>
                        <div class="text" v-html="item.content"></div>
                    </div>
                </div>
            </div>
        </div>

        <alerts ref="alerts" v-bind:message="message"></alerts>
        <load ref="load"></load>
    </div>
</template>

<script>
import 'mavon-editor/dist/css/index.css'

import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'
import { quillEditor } from 'vue-quill-editor'


    let _this = this;
    import {LocalStorage} from '../utils/util.js'
    export default {
        name: 'detail',
        data(){
            return {
                id: '',
                blog: {},
                message: '',
                imgSrc: '',
                message_content: '',
                userId: '',
                userName: '',
                token: '',
                list: '',
                em_show: false,
                em_imgs: [],
                em_ul: [],
                em_data: [],
                em_index: 0,
                 editorOption: {
                    theme: 'bubble',
                    placeholder: "输入任何留言",
                    modules: {
                    toolbar: [
                      ['bold', 'italic', 'underline', 'strike'],
                      [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                      [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
                      [{ 'color': [] }, { 'background': [] }],
                      [{ 'font': [] }],
                      [{ 'align': [] }],
                      ['link', 'image'],
                      ['clean']
                    ]
                  }
                }
            }
        },
        components: {
            quillEditor
        },
        created(){
            _this = this;
            _this.id = _this.$route.params.id;
            _this.userId = LocalStorage.getItem('userId');
            _this.userName = LocalStorage.getItem('userName');
            _this.token = LocalStorage.getItem('token');
            

        },
        mounted(){
             _this.getDetail();

            _this.getComment();

            _this.getEmoticon();
        },
        methods: {
            getDetail: ()=>{
                _this.$get(_this,'/api/detail',{id:_this.id}).then((res)=>{
                    if(res.code == 1){
                        _this.blog = res.blog;
                        _this.imgSrc = _this.HOST+res.blog.thumb;
                    }else{
                        _this.message = res.messagee;
                        _this.$refs.alerts.show();

                    }
                })
            },
            sendMessage: ()=>{
                if(!_this.message_content){
                    _this.message = "留言内容不能为空";
                    _this.$refs.alerts.show();
                    return;
                }

                _this.$post(_this,'/api/addComment',{
                    blogId: _this.id,
                    userId: _this.userId,
                    userName: _this.userName,
                    content: _this.message_content,
                    token: _this.token
                }).then((res)=>{
                    _this.message = res.message;
                    _this.$refs.alerts.show();
                    if(res.code == 1){
                        _this.message_content = '';
                        _this.getComment();
                    }
                })

            },

            getComment: ()=>{
                _this.$get(_this,'/api/getComment',{
                    blogId: _this.id,
                    pageNum: 0,
                    pageSize: 10
                }).then((res)=>{
                    if(res.code == 1){
                        _this.list = res.comments;
                        
                    }else{
                        _this.message = res.message;
                        _this.$refs.alerts.show();
                    }
                })
            },

            getEmoticon: ()=>{
                _this.$get(_this,'/api/emoticon').then((res)=>{
                    console.log(res);
                    _this.em_data = res.emoticons;
                    _this.em_ul = res.dirs;
                    _this.em_imgs = res.emoticons[0].path;
                })
            },

            choiceImg: (e)=>{
                let src = e.target.src;
                console.log(src);
                let imgstr = `<img src="${src}"/>`;
                console.log(imgstr);
                _this.message_content += imgstr;
                _this.em_show = ! _this.em_show;
            },
            choiceUl: (index)=>{
                _this.em_index = index;
                _this.em_imgs = _this.em_data[index].path;
                

            },

            onEditorChange: (e)=>{
                console.log(e);
                _this.message_content = e.html;
            }
        }
    }
</script>

<style scoped lang="scss">
    @import '../css/reset.css';
    @import '../css/font-vue.css';
    .detail {

        .header {
            // padding: 0 20px;
            height: 100px;
            line-height: 100px;
            background: #fff;
            border-bottom: 1px solid #52b983;

            .title {
                margin-left: 20px;
                font-size: 25px;
                color: #666;

            }

            .time {
                margin-right: 20px;
                color: #999;
                font-size: 13px;
            }
        }

        .thumb {
            width: 100%;
            height: 350px;
            margin: 20px 0;
            overflow: hidden;

            .img {
                width: 100%;
            }
        }

        .container {
            font-size: 15px;
            color: #666;
            line-height: 1.5;
        }

        .messageBoard {
            box-sizing: border-box;
            margin-top: 30px;

            .title-line {
                border-bottom: 1px solid #52b983;
                height: 25px;
                // overflow: hidden;
                font-size: 16px;
                color: #fff;

                .text {
                    padding: 5px 10px;
                    background: #52b983;
                }
            }

            .textarea {
                box-sizing: border-box;
                margin: 20px 0;
                width: 100%;
                height: 150px;
                font-size: 14px;
                line-height: 2;
                color: #666;
                border: 1px solid #ccc;
                outline-color: #52b983;
            }

            .send {
                display: inline-block;
                padding: 5px 15px;
                color: #fff;
                background: #52b983;
            }

            .emoticon {
                display: inline-block;
                position: relative;

                .em-btn {
                    font-size: 30px;
                    vertical-align: middle;
                    margin-left: 10px;
                }

                .em-box {
                    position: absolute;
                    top:-310px;
                    left:0;
                    width: 600px;
                    height: 300px;
                    background: #fff;
                    border: 1px solid #eee;
                }

                .em-imgs {
                    width: 100%;
                    height: 250px;
                    overflow-y: auto;
                    overflow-x: hidden;

                    .img {
                        width: 100px;
                        height: 100px;
                        margin: 5px;
                        cursor: pointer;
                    }

                }

                .em-ul {
                    width: 100%;
                    height: 50px;
                    background: #ccc;
                    overflow-x: auto;
                    overflow-y: hidden;
                    display: flex;
                }

                .em-ul-item {
                    cursor: pointer;
                    height: 100%;
                    line-height: 50px;
                    text-align: center;
                    color: #666;
                    flex: 1;
                }

                .act {
                    background: #eee;
                }
            }

            .list {
                width: 100%;
                margin: 20px 0;

                .list-item {
                    padding: 20px 0;
                    border-bottom: 1px solid #52b983;

                    .name {
                        display: inline-block;
                        vertical-align: top;
                        height: 50px;
                        width: 50px;
                        line-height: 50px;
                        text-align: center;
                        border-radius: 50%;
                        overflow: hidden;
                        color: #fff;
                        background: #52b983;
                        margin-right: 30px;
                    }

                    .message {
                        display: inline-block;
                        font-size: 14px;
                        color: #666;
                        
                        .time {
                            line-height: 2;
                        }

                    }

                }
            }
        }
    }

</style>