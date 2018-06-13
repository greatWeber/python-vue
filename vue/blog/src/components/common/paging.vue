<template>
    <div style="text-align: center;" v-if="show">
         <div class="paging" ref="paging">
            <span class=" paging-prev icon-vue-prev"></span>
            <span v-bind:class="[item == current? 'act': '', 'paging-item']" v-for="item in pageList" v-bind:data-index="item">{{item}}</span>
            <span class=" paging-next icon-vue-next"></span>
        </div>
    </div>
   
</template>

<script>
    let _this;
    export default {
        name: 'paging',
        created(){
            _this = this;
           
        },
        data(){
            return {
                total: 1, //传进来的总数
                max: 5, //最大显示数量
                current: 1, //当前页数
                half: 3, //中心点
                pageList: [1],
                paging: null,
                show: true
            }
        },
        mounted(){
            _this.paging = _this.$refs.paging;
             // _this.init(10);
        },
        methods: {
            init: (num,cb)=>{
                let pageList = [];
                _this.total = num;
                if(num==0){
                    _this.show = false;
                    return;
                }else{
                    _this.show = true;
                }
                for(let i=1;i<=num;i++){
                    if(pageList.length<5){
                        pageList.push(i);
                    }
                    
                }
                _this.pageList = pageList;
               _this.paging.addEventListener('click', function(e){
                    let classNames = e.target.className.split(' ');
                    if(classNames.indexOf('paging-item')!=-1){
                        let target = e.target;
                        let index = target.dataset.index;
                        console.log(index);
                        _this.current = index;
                        _this.changeList(index);
                        cb(index);

                    }
               }, false);

            },
            changeList: (index)=>{
                 
                let pageList = [];
                if(index>_this.half&&_this.total>5){
                   let range = index - _this.half;
                    for(let i=range+1;i<=_this.total;i++){
                        if(pageList.length<5){
                            pageList.push(i);
                        }
                    }
                    
                }else{
                    for(let i=1;i<=_this.total;i++){
                        if(pageList.length<5){
                            pageList.push(i);
                        }
                        
                    }
                }

                _this.pageList = pageList;
            }
        }
    }
</script>

<style scoped lang="scss">
@import '../../css/reset.css';
@import '../../css/font-vue.css';
    .paging {
        display: inline-block;
        text-align: center;
        width: auto;
        height: 50px;
        line-height: 50px;
        margin: 50px auto;
        border: 1px solid #52b983;
        font-size: 0;
        box-sizing: border-box;
        overflow: hidden;

        .act {
            background: #52b983;
            color: #fff !important;
        }

        .paging-item {
            width: 50px;
            text-align: center;
            display: inline-block;
            vertical-align: top;
            border-right: 1px solid #52b983;
            font-size: 16px;
            color: #52b983;
            cursor: pointer;
        }
        .paging-prev, .paging-next {
            width: 50px;
            text-align: center;
            display: inline-block;
            vertical-align: top;
            border-right: 1px solid #52b983;
            font-size: 16px;
            color: #52b983;
            cursor: pointer;
        }
        .paging-next {
            border-right: none;
        }
    }
</style>