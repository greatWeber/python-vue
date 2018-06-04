<template>
    <div class="commentList" v-show="isShow">
        <transition name="fade" >
            <div>
                <span class="closeBtn icon-vue-x" @click="close"></span>
                <div class="list-head">
                    <p class="head-item-name">名称</p>
                    <p class="head-item-title">留言</p>
                    <p class="head-item-del">删除</p>
                </div>
                <div class="list-content">
                    <div class="list-item" v-for="item in list">
                        <p class="item-item-name">{{item.user_name}}</p>
                        <p class="item-item-title">{{item.content}}</p>
                        <p class="item-item-del">
                            <a class="delBtn" @click="delFn(item.id)">删除 </a>
                        </p>
                    </div>
                </div>
                
            </div>

        </transition>
        <alerts ref="alerts" v-bind:message="message"></alerts>
    </div>
</template>

<script>
    let _this;
    import {LocalStorage} from '../utils/util.js'
    export default {
        name: 'commentList',
        data(){
            return {
                isShow: false,
                list: {},
                message: '',
                token: '',
                blogId: ''
            }
        },
        created(){
            _this = this;
            _this.token = LocalStorage.getItem('token');
        },
        methods: {
            show: (blogId)=>{
                _this.blogId = blogId;
                _this.isShow = true;
                _this.getComment(blogId);
            },
            close: ()=>{
                _this.$emit('blog-reload');
                _this.isShow = false;
            },
            getComment: (blogId)=>{
                _this.$get('/api/getComment',{
                    blogId: blogId,
                    pageNum: 0,
                    pageSize: 10
                }).then((res)=>{
                    if(res.code==1){
                        _this.list = res.comments;
                    }else{
                        _this.message = res.message;
                        _this.$refs.alerts.show();
                    }
                })
            },
            delFn: (id)=>{
                _this.$post('/api/delComment',{
                    id: id,
                    blogId: _this.blogId,
                    token: _this.token
                }).then((res)=>{
                    if(res.code == 1){
                        setTimeout(()=>{
                            _this.getComment(_this.blogId);
                        },500)
                        
                    }
                    _this.message = res.message;
                    _this.$refs.alerts.show();
                })
            }
        }
    }
</script>

<style scoped lang="scss">
    @import '../css/reset.css';
    @import '../css/font-vue.css';
    
    .commentList {
        position: fixed;
        top: 50%;
        left: 50%;
        margin-left: -410px;
        margin-top: -310px;
        width: 800px;
        height: 600px;
        padding: 20px;
        border: 1px solid #52b983;
        border-radius: 5px;
        background: #fff;
        box-shadow: 0 0 10px #52b983;

        .closeBtn {
            font-size: 30px;
            position: absolute;
            top: 20px;
            right: 20px;
            color: #52b983;
             cursor: pointer;

        }

        .list-head {
            height: 80px;
            line-height: 80px;
            width: 100%;
            display: flex;
            font-size: 18px;
            color: #52b983;
            border-bottom: 1px solid #52b983;

            .head-item-name, .head-item-del {
                flex: 1;

            }

            .head-item-title {
                flex: 3;
            }
        }

        .list-content {
            width: 100%;
            height: 450px;
            overflow-y: scroll;

            .list-item {
                height: 50px;
                line-height: 50px;
                font-size: 14px;
                color: #666;
                border-bottom: 1px solid #ccc;
                display: flex;
                transition: all 0.3s linear;

                &:hover {
                    background: #f5f5f5;

                }

                .item-item-name, .item-item-del {
                    flex: 1;

                }

                .item-item-title {
                    flex: 3;

                }

                .delBtn {
                   
                    color: #fff;
                    padding: 5px 10px;
                    background: #db683b;
                    border-radius: 3px;
                }
            }
        }
    }

</style>