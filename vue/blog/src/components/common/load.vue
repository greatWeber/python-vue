<template>
    <div v-show="isShow">
        <transition name="fade" >
            <div class="loading-mark">
                <span class="loading"></span>
            </div>
        </transition>
    </div>
    
    
</template>

<script>
    let _this;
    export default {
        name: 'load',
        data(){
            return {
                isShow: false
            }
        },
        created(){
            _this = this;
        },
        methods: {
            show: ()=>{
                _this.isShow = true;
            },
            hide: ()=>{
                setTimeout(()=>{
                    _this.isShow = false;
                },500)
                
            }
        }
    }
</script>

<style>
@import '../../css/reset.css';
@import '../../css/font-vue.css';

.loading-mark { 
    position: fixed;
    top: 0;
    left: 0;
    z-index: 998;
    width: 100%;
    height: 100%;
    text-align: center;
    background: rgba(255,255,255,0.8);

    
}
.loading {
    margin-top: 200px;
    width: 100px;
    height: 100px;
    background: url(../../assets/loading.png) center center no-repeat;
    color: #52b983;
    display: inline-block;
    animation: loadings 1s infinite ;
    animation-timing-function: linear;
}


@keyframes loadings
{
    0% {
        transform: rotate(0deg);
        transform-origin: center center;
    }
    100% {
        transform-origin: center center;
        transform: rotate(360deg);
    }
}

@-webkit-keyframes loadings
{
    0% {
        transform-origin: center center;
        transform: rotateX(0deg);
    }
    100% {
        transform-origin: center center;
        transform: rotateX(360deg);
    }
}
</style>