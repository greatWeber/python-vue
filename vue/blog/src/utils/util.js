
let LocalStorage = {
    setItem: (key,value,time='',now = new Date().getTime())=>{
       console.log(key);
        if(!key){
            throw Error('参数错误','key值不能为空')
        }
        let params = {key:key,value:value,time:time,now: now};
        let json = JSON.stringify(params);
        window.localStorage.setItem(key,json);

    },

    getItem: (key)=>{
        if(!key){
            throw Error('参数错误','key值不能为空')
        }

        let data = window.localStorage.getItem(key);
        console.log(data);
        if(!data){
            return null;
        }
        let params = JSON.parse(data);
        
        if(params.time){
            let range = params.time * 3600* 1000;
            let time = new Date().getTime();
            if(parseInt(params.now) + range < time){
                window.localStorage.setItem(key,'');
                return null;
            }else{
                return params.value;
            }
        }
    }
};

let checkLogin = (_this)=>{
    let userName = LocalStorage.getItem('userName');
    if(!userName){
         _this.$router.push({path:'home'});
    }
}

export {LocalStorage, checkLogin};