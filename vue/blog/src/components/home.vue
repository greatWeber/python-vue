<template>
    <div class="home">
        <div class="page-list">
            <div class="list-item" v-for="item in pageList">
                <router-link :to="{name: 'detail',params: {id: item.id}}">
                    <h2 class="title">{{item.title}}</h2>
                    <div class="img-box">
                        <img :src="imgsrc(item.thumb)" alt="" class="img">
                    </div>
                    
                    <div class="bottom">
                        <span class="time">{{item.created_time}}</span>
                    </div>
                </router-link>
            </div>
        </div>
        <paging ref="paging"></paging>
        <load ref="load"></load>
    </div>
</template>

<script>
let _this;
    export default {
        name: 'home',
        data(){
            return {
                pageList: [],
                pageNum:1,
                pageSize: 10,
                total: 1,
                host: this.HOST,
            }
        },
        created(){
            _this = this;
            
        },
        mounted(){
            _this.getList();
            _this.$refs.paging.init(_this.total, function(index){
                _this.pageNum = index;
                _this.getList();
            });
        },
        methods: {
           imgsrc: function(img){
            return this.host+img
           },
           getList: ()=>{
            _this.$refs.load.show();
            _this.$get('/api/getPage',{pageNum:_this.pageNum,pageSize:_this.pageSize}).then(res=>{
                _this.$refs.load.hide();
                 
                _this.pageList = res.blogs;
                _this.total = res.page.total;
            })
           }
        }
    }
</script>

<style scoped lang="scss">
@import '../css/reset.css';
.home {
    width: 100%;
    margin: 0 auto;

    .page-list {
        width: 100%;

        .list-item {
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
            margin: 20px 0;
            &:hover {
                box-shadow: 0 0 15px #ccc;
                transition: all 0.3s linear;
            }

            .title {
                color: #555; 
                line-height: 2;
            }

            .img-box {
                width: 100%;
                height: 250px;
                overflow: hidden;

                .img {
                    width: 100%;
                }
            }

            .time {
                color: #666;
                line-height: 2;
            }
        }
    }
}
    
</style>