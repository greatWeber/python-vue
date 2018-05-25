import axios from 'axios'

axios.defaults.timeout = 5000
axios.defaults.baseURL = 'http://127.0.0.1:8088'

axios.interceptors.request.use(
    config=> {
        // config.data = config.data
        config.headers = {
            'Content-Type':'application/json'
        }
        // console.log(config)
        return config;
    },
    err => {
        return Promise.reject(err);
    }
)

/**Get 方法
 * @param {地址}
 * @param {参数}
 * @return promise
 */
export function Get(url, params={}){
    return new Promise((resolve,reject)=>{
        axios.get(url, {
            params: params
        }).then(response=>{
            resolve(response.data);
        }).catch(err => {
            reject(err)
        })
    })
}

/**Post 方法
 * @param {地址}
 * @param {参数}
 * @return promise
 */
export function Post(url, params={}){
    console.log(params);
    return new Promise((resolve,reject)=>{
        axios({
          method: 'post',
          url: url,
          data: params
        }).then(response=>{
            resolve(response.data);
        }).catch(err => {
            reject(err)
        });
        // axios.post(url,params).then(response=>{
        //     resolve(response.data);
        // }).catch(err => {
        //     reject(err)
        // })
    })
}