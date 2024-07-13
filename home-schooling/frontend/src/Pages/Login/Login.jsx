import { useContext, useEffect, useState } from "react";
import Input from "../../Components/Input/Input";
// import logo from "../../assets/logo.png"
import login from "../../assets/signup.avif"
import Button from "../../Components/Button/Button";
import logo from "../../assets/home-schooling-logo-horizontal.png"
import TotalServices from "../../TotalServices";
import { AuthContext } from "../../App";
import Validations from "../../Regex";
import { Link, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import SubscriptionRenew from "./SubscriptionRenew";
const Login = () => {
    const navigate=useNavigate()
    const [subscription,setSubscription]=useState(false)
    const [inputData,setInputData]=useState({
      
        email:"",
     
        password:"",
      
    })
    const [loader,setLoader]=useState(false)
    const {userLogin, setUserLogin}=useContext(AuthContext)
    const handleChange=(e) =>{
setInputData((...prev)=>({
    ...inputData,
    [e.target.name]:e.target.value
}))
    }
    const handleLogin =async(e) =>{
        e?.preventDefault();
        if(Validations.isEmpty(inputData.email)||Validations.isEmpty(inputData.password)){
            toast.error("Fields can't be empty")
        }
        else{
        try {
          setLoader(true);
          let response = await TotalServices.login(inputData);
          if (response.status === 200) {
            if(response.data.status===406){
              setSubscription(true)
              toast.error(response.data.message)
            }
            else{
              let items = {
                access_token: response.data.access_token,
                refresh_token: response.data.refresh_token,
              };
              localStorage.setItem("UserAuth", JSON.stringify(items));
            localStorage.setItem("UserIsLogin","true")
     
          navigate("/")
    setUserLogin(!userLogin)
            }
            //  console.log(response);
          
            setLoader(false);
          }
        } catch (e) {
          console.log(e);
          setLoader(false);
        }
    }
      }
      useEffect(()=>{
document.title="Home Schooling - Login"
      },[])
    return ( 
        <section 
        className="  w-full min-h-screen bg-cover flex flex-col justify-around bg-gray-200"
   
        
        >
           
   
         
          
           
            <div className="w-full  h-full backdrop-blur-sm flex justify-center items-center relative">
              <div className="w-full">

            
          
          
                <div className="mx-auto bg-white  max-w-xl px-4 pb-16 relative sm:w-2/3 w-full rounded-xl ">
                <div className="flex justify-center  " >
                <img src={logo} alt="" className="w-48 object-contain bg-white p-3 rounded-xl "/>
            </div>
                    <h1 className="text-lg text-black font-bold tracking-wider text-center top-0 pb-10 pt-4">
                 Login
                    </h1>
    
               
    
                  
    
                    <form className="grid w-full max-w-lg mx-auto"
                    onSubmit={handleLogin}
                    >
                    
                            <Input
                           
                            name={"email"}
                         
                            placeholder={"Email"}
                            handleChange={handleChange}
                            value={inputData.email}
                          
                            type={"email"}
    
                            />
                          
                         
                              <Input
                           
                           name={"password"}
                         
                           placeholder={"Password"}
                           handleChange={handleChange}
                           value={inputData.password}
                         
                           type={"password"}
    
                           />
                             
                           
                    
    <div className="w-full flex mt-3">
        <Button text={"Log in"}  />
    </div>
                  <div>
                    <p className="text-black mt-3">
                        Doesn't have an account? <Link className="text-btn-primary" to={"/signup"} >SignUp</Link>
                    </p>
                  </div>
    
                       
                 
                      
                    </form>
                </div>
            </div>
            </div>
            {
              subscription && <SubscriptionRenew email={inputData.email} setShow={setSubscription} handleLogin={handleLogin} />
            }
    </section>
     );
}
 
export default Login;