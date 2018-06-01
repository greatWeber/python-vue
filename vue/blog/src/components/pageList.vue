<template>
    <div class="page-list">
        <div class="list-header">
            <p class="header-item-title">文章标题</p>
            <p class="header-item-comment">查看评论</p>
            <p class="header-item-btns">修改</p>
        </div>
        <div class="list-item" v-for="item in list">
            <p class="list-item-title">{{item.title}}</p>
            <p class="list-item-comment">{{item.comment_num}}</p>
            <p class="list-item-btns">
                <router-link class="btn edit" :to="{name: 'editPage',params: {id: item.id}}">修改</router-link>
                <a class="btn delete" @click="delFn(item.id)">删除</a>
            </p>
        </div>
         <confirms ref="confirms" v-bind:message="message"></confirms>
         <alerts ref="alerts" v-bind:message="message"></alerts>
    </div>
   
</template>

<script>
    let _this;
    import {LocalStorage} from '../utils/util.js'
    export default {
        name: 'pageList',
        data(){
            return {
                list: [],
                message: '测试',
                token: ''
            }
        },
        created(){
             _this = this;
             _this.token = LocalStorage.getItem('token');
            _this.getList();
        },
        methods: {
            getList: ()=>{
                _this.$get('/api/getPage').then((res)=>{
                    _this.list = res.blogs;
                    
                });
            },
            delFn: (id)=>{
                _this.message = "确定删除?";
                _this.$refs.confirms.show().then(()=>{
                    console.log('you click sure');
                    _this.delAjax(id);
                },()=>{
                    console.log('you click cancel')
                });
            },
            delAjax: (id)=>{
                _this.$post('/api/delPage',{
                    id: id,
                    token: _this.token
                }).then((res)=>{
                    console.log(res);
                    if(res.code==1){
                        _this.getList();
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
.page-list {
    width: 100%;
    padding: 50px 0;

}

.list-header {
    line-height: 60px;
    font-size: 20px;
    border-bottom: 1px solid #52b983;
    color: #52b983;
    display: flex;
}

.header-item-title {
    flex: 5;
}

.header-item-comment {
    flex: 1;
}

.header-item-btns {
    flex: 2;
}

.list-item {
    line-height: 50px;
    font-size: 16px;
    color: #666;
    border-bottom: 1px solid #ccc;
    display: flex;
    transition: all 0.3s linear;

}

.list-item:hover {
    background: #f5f5f5;
}

.list-item-title {
    text-indent: 10px;
    flex: 5;

}

.list-item-comment {
    flex: 1;
    color: #52b983;
    cursor: pointer;
    
}

.list-item-btns {
    flex: 2;

    .btn {
        display: inline-block;
        height: 20px;
        padding: 5px 10px;
        margin: 15px 10px;
        line-height: 20px;
        border-radius: 3px;
        color: #fff;
    }

    .edit {
        background: #52b983;
    }

    .delete {
        background: #db683b;
    }
    
}



</style>