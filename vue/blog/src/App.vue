<template>
<div id="app">
  
 <header class="header clear">
  <div class="header-content">
    <div class="fl">
        <!-- <img class="logo" src="./assets/logo.png"> -->
        <span class="logo icon-vue-blog"></span>
       <ul class="ul">
         <li  v-bind:class="[Index == 1? 'act': '', 'item']" @click="changeIndex( 1)"><router-link :to="{path:'/home'}">首页</router-link></li>
         <li  v-bind:class="[Index == 2? 'act': '', 'item']" @click="changeIndex( 2)"><router-link :to="{path:'/about'}">关于</router-link></li>
         <li v-if="userName" v-bind:class="[Index == 3? 'act': '', 'item']" @click="changeIndex( 3)"><router-link :to="{path:'/pageList'}">列表文章</router-link></li>
         <li v-if="userName" v-bind:class="[Index == 4? 'act': '', 'item']" @click="changeIndex( 4)"><router-link :to="{path:'/addPage'}">添加文章</router-link></li>
         <li v-if="userName" v-bind:class="[Index == 6? 'act': '', 'item']" @click="changeIndex( 6)"><router-link :to="{path:'/recycleBin'}">回收站</router-link></li>


       </ul>
    </div>
    <div class="fr">
       <div class="logout" v-if="userName">
         <span class="name">{{userName}}</span>
        <span class="line">|</span>
        <a class="logout-btn" @click="logout">退出</a>
      </div>
      <div class="login" v-else>
        <a class="login-btn" @click="showLoginFn">登录</a>
        <span class="line">|</span>
        <a class="register" @click="showRegisterFn">注册</a>
      </div>
     
    </div>
  </div>
   
 </header>
 <div class="content">
   <router-view></router-view>
 </div>

<!-- 遮罩 -->
<div class="mask" v-if="showMask"></div>

<!-- 登录框 -->
 <div class="login-box" v-if="showLogin">
   <form class="form">
     <div class="form-item">
       <label class="label">名称:</label>
       <input type="text" name="" v-model="loginName">
     </div>
    <div class="form-item">
       <label class="label">密码:</label>
       <input type="password" name="" v-model="loginPsd">
     </div>
     <div class="form-btn">
      <a class="btn cancel " @click="showLoginFn">取消</a>
      <a class="btn sure " @click="loginFn">确定</a>
     </div>
   </form>
 </div>

 <div class="register-box" v-if="showRegister">
   <form class="form">
     <div class="form-item">
       <label class="label">名称:</label>
       <input type="text" name="" v-model="registerName">
     </div>
     <div class="form-item">
       <label class="label">邮箱:</label>
       <input type="text" name="" v-model="email">
     </div>
    <div class="form-item">
       <label class="label">密码:</label>
       <input type="password" name="" v-model="registerPsd">
     </div>
     <div class="form-btn">
      <a class="btn cancel " @click="showRegisterFn">取消</a>
      <a class="btn sure " @click="registerFn">确定</a>
     </div>
   </form>
 </div>

<alerts ref="alerts" v-bind:message="message"></alerts>
</div>
</template>

<script>
import {LocalStorage} from './utils/util.js';
export default {
  name: 'App',
  data() {
    return {
      userName:'',
      Index: 1,
      showLogin: false,
      showRegister: false,
      showMask: false,
      loginPsd: '',
      loginName: '',
      registerPsd: '',
      registerName: '',
      email: '',
      message: ''
    }
  },
  created() {
    // this.userName = window.localStorage.getItem('userName') 
    this.userName = LocalStorage.getItem('userName') 
    var path = this.$route.path;
    if(path == '/home'){
      this.Index =1;
    }else if(path == '/about'){
      this.Index =2;
    }else if(path == '/pageList'){
      this.Index =3;
    }else if(path == '/addPage'){
      this.Index =4;
    }else if(path == '/detail'){
      this.Index =5;
    }else if(path == '/recycleBin'){
      this.Index =6;
    }
  },
  computed: {
    ShowMsg: function(){
      return this.showMsg;
    }
  },
  methods: {
    changeIndex: function( index){
      this.Index = index
    },
    showLoginFn: function(){
      this.showLogin = !this.showLogin;
      this.showMask = !this.showMask;
    },
    showRegisterFn: function(){
      this.showRegister = !this.showRegister;
      this.showMask = !this.showMask;
    },
    loginFn: function(){
      var _this = this;
      _this.$post('/api/login',{
        name: _this.loginName,
        psd: _this.loginPsd
      }).then(res=>{
        console.log(res)
         // 显示提示
          _this.message = res.message;
          _this.$refs.alerts.show();
         if(res.code == 1){
             
              _this.userName = res.list.name;
              // 保存用户信息
              LocalStorage.setItem('userName',res.list.name,3);
              LocalStorage.setItem('userId',res.list.id,3);
              LocalStorage.setItem('token',res.list.token,3);

              
              setTimeout(function(){
                _this.showLogin = !_this.showLogin;
                _this.showMask = !_this.showMask;
                window.location.reload();
              },1000)
          }

      })
    },
     registerFn: function(){
      var _this = this;
      this.$post('/api/register',{
        name: this.registerName,
        psd: this.registerPsd,
        email: this.email
      }).then(res=>{
        if(res.code == 1){
            _this.showMsg = !_this.showMsg;
            _this.message = res.message;
            // 清空输入框
            
            setTimeout(function(){
              _this.showMsg = false;
              _this.showRegister = !_this.showRegister;
              _this.showMask = !_this.showMask;
            },1000)
        }else{
            _this.showMsg = !_this.showMsg;
            _this.message = res.message;
            setTimeout(function(){
              _this.showMsg = false;
            },1000)
        }
      })
    },
    logout: function(){
      var _this = this;
      _this.$get('/api/logout').then(res=>{
          if(res.code == 1){
              _this.showMsg = !_this.showMsg;
              _this.message = res.message;
              
              setTimeout(function(){
                _this.showMsg = false;
                window.localStorage.setItem('userName','')
                window.localStorage.setItem('userId','')
                _this.userName = ''
              },1000)
          }else{
              _this.showMsg = !_this.showMsg;
              _this.message = res.message;
              setTimeout(function(){
                _this.showMsg = false;
              },1000)
          }
      })
    }
  }
}
</script>

<style>
@import './css/reset.css';
@import './css/font-vue.css';
#app {
  width: 100%;
 
}
.content {
    width: 1000px;
    margin: 0 auto;
    height: auto;
}

.header {
  width: 100%;
  height: 50px;
  line-height: 50px;
  background: #eee;
  margin-bottom: 20px;

}
.header-content {
    width: 1000px;
    margin: 0 auto;
}
.header .logo {
  width: 50px;
  height: 50px;
  font-size: 30px;
  display: inline-block;
  color: #52b983;
}

.header .logout .name {
  color: #52b983;
}

.header .ul {
  display: inline-block;
  vertical-align: top;
}

.header .ul .item {
  display: inline-block;
  vertical-align: top;
  font-size: 16px;
  padding: 0 20px;
  cursor: pointer;
}

.header .ul .item a{
  color: #333;
}

.header .ul .act a{
  color: #52b983;
}

.form {
  padding: 20px;
}

.form .form-item {
  margin: 10px 0;
  height: 50px;
  line-height: 50px;
}

.form .form-item .label {
  display: inline-block;
  width: 60px;
  text-align: left;
}

.form .form-item input {
  width: 200px;
  border: none;
  border-bottom: 1px solid #333;
}

.form .form-btn {
   margin: 10px 0;
  height: 50px;
  line-height: 50px;
  text-align: center;
}

.form .form-btn .btn {
  padding: 5px 10px;
  margin: 0 10px;
  cursor: pointer;
  color: #fff;
  border-radius: 5px;

}

.form .form-btn .sure {
  background: #52b983;
}

.form .form-btn .cancel {
  background: #db683b;
}

.login-box, .register-box {
  position: fixed;
  left: 50%;
  margin-left: -150px;
  top: 50%;
  margin-top: -150px;
  border: 1px solid #333;
  border-radius: 10px;
  z-index: 999;
}

.mask {
  position: fixed;
  top:0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255,255,255,0.8)
}

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

.showModel {
  display: block;
  opacity: 1;
  transition: all 0.3s linear;
}

</style>

