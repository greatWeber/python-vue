<template>
    <div class="detail">
        <div class="header clear">
            <h1 class="title fl">{{blog.title}}</h1>
            <span class="time fr">{{blog.create_time}}</span>
        </div>
        <div class="thumb">
            <img :src="imgSrc" alt="" class="img">
        </div>
        <div class="container" v-html="blog.content">
            
        </div>

        <div class="messageBoard">
            <p class="title-line"><span class="text">留言列表</span></p>
            <textarea class="textarea" v-model="message_content"></textarea>
            <a class="send" @click="sendMessage">留言</a>

            <div class="list">
                <div class="list-item">
                    <p class="name">游客</p>
                    <div class="message">
                        <p class="time">2018-06-01</p>
                        <div class="text">发表留言说一下</div>
                    </div>
                </div>
            </div>
        </div>

        <alerts ref="alerts" v-bind:message="message"></alerts>
    </div>
</template>

<script>
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
            }
        },
        created(){
            _this = this;
            _this.id = _this.$route.params.id;
            _this.userId = LocalStorage.getItem('userId');
            _this.userName = LocalStorage.getItem('userName');
            _this.token = LocalStorage.getItem('token');
            _this.getDetail();

        },
        methods: {
            getDetail: ()=>{
                _this.$get('/api/detail',{id:_this.id}).then((res)=>{
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

                _this.$post('/api/addComment',{
                    blogId: _this.id,
                    userId: _this.userId,
                    userName: _this.userName,
                    content: _this.message_content,
                    token: _this.token
                }).then((res)=>{
                    _this.message = res.message;
                    _this.$refs.alerts.show();
                })

            }
        }
    }
</script>

<style scoped lang="scss">
    @import '../css/reset.css';
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
                padding: 5px 15px;
                color: #fff;
                background: #52b983;
            }

            .list {
                width: 100%;
                margin: 20px 0;

                .list-item {
                    padding: 20px 0;
                    border-bottom: 1px solid #52b983;

                    .name {
                        display: inline-block;
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