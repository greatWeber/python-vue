<template>
    <div class="alert" v-show="isShow">

        <transition name="fade" >
            <div  class="model">
                <p>{{message}}</p>
            </div>
        </transition>
    </div>
    
</template>

<style type="text/css">
.model {
  width: 250px;
  height: 100px;
  border: 1px solid #52b983;
  border-radius: 10px;
  background: #f9f9f9;
  text-align: center;
  line-height: 100px;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  margin: auto;
  color: #52b983;
  z-index: 9999;
}

</style>

<script>
    export default {
        name: 'alerts',
        props: ['message'],
        data(){
            return {
                isShow: false
            }
        },
        complated: {

        },
        methods: {
            show: function(time){
                let timeout = time || 0;

                let _this = this;
                setTimeout(()=>{
                  _this.isShow = true;
                setTimeout(function(){
                    _this.isShow = false;
                },1000)
                }, timeout)
                
            }
        }
    }
</script>