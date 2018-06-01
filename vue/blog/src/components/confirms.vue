<template>
    <div class="confirms" v-show="isShow">

        <transition name="fade" >
            <div  class="model">
                <p>{{message}}</p>
                <div class="btns-box">
                  <span class="sure" ref="sureBtn">是</span>
                  <span class="cancel" ref="cancelBtn">否</span>
                </div>
            </div>
        </transition>
    </div>
    
</template>

<style scoped lang="scss">

.confirms {
  .model {
    width: 250px;
    height: 200px; 
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

  .btns-box {
    width: 100%;
    height: 100px;
    font-size: 0;
  }

  .btns-box .sure {
    display: inline-block;
    font-size: 16px;
    line-height: 30px;
    height: 30px;
    width: 60px;
    border-radius: 3px;
    text-align: center;
    color: #fff;
    background: #52b983;
    margin: 25px;
    cursor: pointer;
  }

  .btns-box .cancel {
    display: inline-block;
    font-size: 16px;
    line-height: 30px;
    height: 30px;
    width: 60px;
    border-radius: 3px;
    text-align: center;
    color: #fff;
    background: #db683b;
    margin: 25px;
    cursor: pointer;
  }

}


</style>

<script>
    export default {
        name: 'confirms',
        props: ['message'],
        data(){
            return {
                isShow: false
            }
        },
        complated: {

        },
        methods: {
            show: function(){
                var _this = this;
                _this.isShow = true;
                let sureBtn = _this.$refs.sureBtn;
                let cancelBtn = _this.$refs.cancelBtn;

                return new Promise((resolve,reject)=>{
                  sureBtn.addEventListener('click', function(e){
                    _this.isShow = false;
                    resolve();
                  }, false);

                  cancelBtn.addEventListener('click', function(e){
                    _this.isShow = false;
                    reject();
                  }, false);
                })
                
            }
        }
    }
</script>