<template>
    <div class="page-list">
        <div class="list-header">
            <p class="header-item-title">文章标题</p>
            <p class="header-item-comment">查看留言</p>
            <p class="header-item-btns">修改</p>
        </div>
        <div class="list-item" v-for="(item, index) in list">
            <span v-bind:class="[item.checked == true? 'checked-act': '', 'icon-vue-checked']" @click="changeDel(index)"></span>
            <p class="list-item-title">{{item.title}}</p>
            <p class="list-item-comment" @click="lookComment(item.id)">{{item.comment_num}}</p>
            <p class="list-item-btns">
                <router-link class="btn edit" :to="{name: 'editPage',params: {id: item.id}}">修改</router-link>
                <a class="btn delete" @click="delFn(item.id)">删除</a>
            </p>
        </div>
        <div class="page-check">
            <p class="checkall">
                <span v-bind:class="[allChecked == true? 'checked-act': '', 'icon-vue-checked']"></span>
                <span @click="checkAll">全选</span>
            </p>
            <p class="list-item-btns">
                <a class="btn delete" @click="delsFn">删除</a>
            </p>
        </div>
         <confirms ref="confirms" v-bind:message="message"></confirms>
         <alerts ref="alerts" v-bind:message="message"></alerts>
         <commentList ref="commentList" @blog-reload="reloads"></commentList>
         <load ref="load"></load>
         <paging ref="paging"></paging>
    </div>
   
</template>

<script>
    let _this;
    import {LocalStorage, checkLogin} from '../utils/util.js'
    import commentList from './commentList.vue'
    export default {
        name: 'pageList',
        data(){
            return {
                list: [],
                message: '测试',
                token: '',
                total: 1,
                pageNum: 1,
                pageSize: 10,
                ids: [],
                allChecked: false
            }
        },
        components: {
            commentList
          },
        created(){
             _this = this;
             checkLogin(_this);
             _this.token = LocalStorage.getItem('token');
            
        },
        mounted(){
            _this.getList(_this.initPaging);
            
           
        },
        methods: {
            getList: (cb)=>{

                _this.$get(_this,'/api/getPage',{
                    token : _this.token,
                    pageNum: _this.pageNum,
                    pageSize: _this.pageSize
                }).then((res)=>{
                    let list = res.blogs;
                    for(let i=0;i<list.length;i++){
                        list[i].checked = false;
                    }
                    _this.list = list;
                    _this.total = res.page.total;
                    
                    cb&&cb(); 
                });
            },
            initPaging: ()=>{
                _this.$refs.paging.init(_this.total, function(index){
                    _this.pageNum = index;
                    _this.getList();
                });
            },
            delFn: (id)=>{
                _this.message = "确定删除?";
                _this.$refs.confirms.show().then(()=>{
                    console.log('you click sure');
                    _this.delAjax(id);
                },()=>{
                    console.log('you click cancel');
                });
            },
            delAjax: (id)=>{
                _this.$post(_this,'/api/delPage',{
                    id: id,
                    token: _this.token
                }).then((res)=>{
                    if(res.code==1){
                        _this.getList();
                    }

                    _this.message = res.message;
                    _this.$refs.alerts.show();
                })
            },
            delsFn: ()=>{
                let list = _this.list;
                let ids = [];
                for(let i=0;i<list.length;i++){
                    if(list[i].checked){
                        ids.push(list[i].id);
                    }
                }
                if(ids.length==0){
                    _this.message = "请选择要删除的文章";
                    _this.$refs.alerts.show();
                    return;
                }
                _this.allChecked = false;
                _this.delAjax(ids.join(','));
            },
            lookComment: (id)=>{
                _this.$refs.commentList.show(id);
            },
            reloads: ()=>{
                 _this.getList();
            },
            changeDel: (index)=>{
                _this.list[index].checked = !_this.list[index].checked;
                let list = _this.list;
                let num=0;
                let len = list.length;
                for(let i=0;i<len;i++){
                    if(list[i].checked){
                        num++;
                    }
                }
                if(num == len){
                    _this.allChecked = true;
                }else{
                    _this.allChecked = false;
                }

            },
            checkAll: ()=>{
                let allChecked = _this.allChecked;
                let list = _this.list;
                let len = list.length;
                if(allChecked){
                    for(let i=0;i<len;i++){
                        list[i].checked = false;
                    }
                }else{
                    for(let i=0;i<len;i++){
                        list[i].checked = true;
                    }
                }
                allChecked = !allChecked;
                _this.allChecked = allChecked;
                _this.list = list;
            }
        }
    }
</script>

<style scoped lang="scss">
@import '../css/reset.css';
@import '../css/font-vue.css';
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
    display: inline-block;
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

.icon-vue-checked {
    font-size: 20px;
    color: #ccc;
    vertical-align: middle;
    cursor: pointer; 
}

.checked-act {
    color: #52b983;
}

.page-check {
    width: 100%;
    line-height: 50px;



    

    .checkall {
        cursor: pointer;
        display: inline-block;
    }
}



</style>