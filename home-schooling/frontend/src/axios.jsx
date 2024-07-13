import axios from "axios";
import { toast } from "react-toastify";
import ApiURL from "./config/config";
import Services from "./ServicesRoutes";


const API = axios.create({
  baseURL: ApiURL,
  headers: {
    "Content-type": "application/json",
  },
});

// request interceptor for settting the two headers refresh & access tokens
API.interceptors.request.use(
  (config) => {
   
    const token = JSON.parse(localStorage.getItem("UserAuth"));
    if (
      config.url==="/User" && config.method==="get" 

    ) {
    
      config.headers["Authorization"] = "Bearer " + token.refresh_token;
    }
  
   else if (
      token &&
      
      config.url!=="/User"
   
  ) {
      config.headers["Authorization"] = "Bearer " + token.access_token;
    } 
  
  //   if (config.url.includes("/Demo") && config.method==="post"){
    
  //     config.headers["Content-Type"] = 'multipart/form-data'
  // }

// if (config.url.includes(Services.DownloadActivity) && config.method==="get"){
// console.log(config.url);
//     config.maxContentLength= Infinity;
//     config.maxBodyLength=Infinity;
//     config.responseType= 'blob';
// }
 
    // Optional
    // config.headers["Content-Type"] = "application/json";
    // console.log(config);
    return config;
  },
  (error) => {
    Promise.reject(error);
  }
);

// response interceptor, when the backend throws error 403 for token expire it call the refresh token API and updates the token
API.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    const originalRequest = error.config;
    // console.log(error, " Original Request");

    if(error.response===undefined){
      toast.error("There is an error. Please try again");
    }
   else if (error.response.status === 500) {
      toast.error("There is an error. Please try again");
    }
    else if (error.response.status !== 403) {
    if(error.response.config.responseType==='blob'){
      error.response.data.text().then(res=>JSON.parse(res)).then(result=>{
        toast.error(result.message);
      })
    }else{
      toast.error(error.response.data.message);
    }
     
      
    }
   
   else if (error.response.status === 403) {
    localStorage.removeItem("UserAuth")
    localStorage.removeItem("UserIsLogin")
    window.location.reload(false)
    }
    Promise.reject(error);
  }
);

export default API;
