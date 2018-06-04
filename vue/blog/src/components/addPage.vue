<template>
    <div class="addPage">
        <form class="pageForm">
            <div class="form-item">
                <label for="tilte" class="label">标题</label>
                <input type="text" id="tilte" name="title" v-model="title">
            </div>
            <div class="form-item">
                <label for="" class="label">缩略图</label>
                <input type="file" id="file" name="file" @change="upload">
                <label class="thumb" for="file"></label>
                <img class="img" :src="imgsrc" alt="">
            </div>
            <div class="form-item">
                <label for="info" class="label">简介</label>
                <input type="text" id="info" name="info" v-model="info">
            </div>
            <quillEditor v-model="content"></quillEditor>
            <div class="form-btn">
                <span class="btn btn-sure" @click="addPageFn">添加</span>
                <span class="btn btn-cancel">重置</span>
            </div>
        </form>

        <alerts ref="alerts" v-bind:message="message"></alerts>

        <load ref="load"></load>
    </div>
   

</template>

<script>
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'

import {LocalStorage} from '../utils/util.js'
import { quillEditor } from 'vue-quill-editor'
let _this;
    export default {
        name: 'addPage',
        data(){
            return {
                imgsrc: '',
                title: '',
                info: '',
                userId: '',
                userName: '',
                userImage: '',
                content: '',
                thumb: '',
                token: '',
                message: ''
            }
        },
        created: function(){
            this.userId = LocalStorage.getItem('userId');
            this.userName = LocalStorage.getItem('userName');
            this.token = LocalStorage.getItem('token');
        },
        mounted(){
            _this = this;
        },
        components: {
            quillEditor
      },
        methods: {
            upload: function(e){
                var _this = this;
                console.log(e)
                console.log(e.target.files[0])
                var file = e.target.files[0];
                var formData = new FormData();
                formData.append('image',file);
                _this.$refs.load.show();
               _this.$ajax({
                    method: 'POST',
                    url: '/api/upload',
                    data: formData,
                    headers: {'Content-Type':'multipart/form-data'}
               }).then(res=>{
                _this.$refs.load.hide();
                var data = res.data;
                _this.imgsrc = _this.HOST+data.list.path;
                _this.thumb = data.list.path;
               })
            },
            addPageFn: function(){
                _this.$refs.load.show();
                var _this = this;
                _this.$post('/api/addPage',{
                    userId: _this.userId,
                    userName: _this.userName,
                    userImage: _this.userImage,
                    title: _this.title,
                    thumb: _this.thumb,
                    info: _this.info,
                    content: _this.content,
                    token: _this.token
                }).then(res=>{
                    _this.$refs.load.hide();
                    if(res.code == 1){
                        setTimeout(()=>{
                            _this.$router.push({path:'pageList'});
                        },1000)
                        
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

.addPage {
    width: 800px;
    overflow: hidden; 

    .pageForm {
        width: 100%; 

        .form-item {
            width: 100%;
            margin: 20px 0;
            line-height: 50px;
            vertical-align: middle;

            .label {
                display: inline-block;
                width: 20%;
                text-align: left;
            }

            input[type='text'] {
                width: 75%;
                border: none;
                border-bottom: 1px solid #666;
            }

            input[type='file'] {
                display: none;
            }

            #file {
                display: none;
            }

            .thumb {
                display: inline-block;
                width: 100px;
                height: 100px;
                border: 1px solid #666;
                background: url(../assets/add.png) center center no-repeat;
            }

            .img {
                width: 100px;
                height: 100px;
            }

        }

        .form-btn {
            .btn {
                display: inline-block;
                padding: 5px 10px;
                color: #fff;
                margin: 10px;
                cursor: pointer;
                border-radius: 5px;
            }
            .btn-sure {
                background: #52b983;
            }

            .btn-cancel {
                background: #db683b;
            }
        }

    }
}

</style>