<template>
    <div class="alert">

        <transition name="fade">
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
  border: 1px solid #ccc;
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
  color: #666;
  z-index: 9999;
}

</style>

<script>
    export default {
        name: 'alert',
        data(){
            return {
                message: '这是弹窗'
            }
        }
    }
</script>