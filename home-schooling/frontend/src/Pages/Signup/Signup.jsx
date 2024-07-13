import { useEffect, useState } from "react";
import Input from "../../Components/Input/Input";
import signup from "../../assets/signup.avif"
import { FaCheckCircle } from "react-icons/fa";
import Button from "../../Components/Button/Button";
import SelectInput from "../../Components/Input/SelectInput";
import Validations from "../../Regex"
import { toast } from "react-toastify";
import TotalServices from "../../TotalServices";
import { Link } from "react-router-dom";
import logo from "../../assets/home-schooling-logo-horizontal.png"
const Signup = ({setSignupInfo,setInputData,inputData,plans,setPlan,plan,states}) => {
   
    const handleChange=(e) =>{
setInputData((...prev)=>({
    ...inputData,
    [e.target.name]:e.target.value
}))
    }

    const handleSignupInfo=async(e) =>{
        e.preventDefault()
        if(Validations.isEmpty(inputData.first_name)||Validations.isEmpty(inputData.last_name)||Validations.isEmpty(inputData.post_code)||Validations.isEmpty(inputData.state)||Validations.isEmpty(inputData.address)||Validations.isEmpty(inputData.email)||Validations.isEmpty(inputData.plan_id)){
            toast.error("Fields can't be empty")
        }
        else if(!Validations.isEmail(inputData.email)){
            toast.error("Invalid Email")
        }
        else if(inputData.password!==inputData.confirm_password){
            toast.error("Passwords doesn't match")
        }
        else if(!Validations.validatePassword(inputData.password)){
            toast.error("Password must have at least one lowercase letter, one uppercase letter, one digit, and one special character")
        }
        else {
            let response = await TotalServices.checkMail({email:inputData.email});
            if (response.status === 200) {
              //  console.log(response);
            
         
              setSignupInfo(true)
              setLoader(false);
            }
          } 
          
        
       
    }
    useEffect(()=>{
      
       if(document.activeElement.name!=='email'){
        inputData.email !=="" &&  checkMail()
       }

    },[inputData.email])
    const checkMail =async(e) =>{
        if(!Validations.isEmail(inputData.email)){
           document.getElementById("email").innerText="Invalid Email"
        }
        else{

            let response = await TotalServices.checkMail({email:inputData.email});
            if (response.data.status === 200) {
            
                document.getElementById("email").innerText=""
           
             
              }
              else{
                document.getElementById("email").innerText=response.data.message
              }
        }
    }
    const checkPassword =async(e) =>{
        if(!Validations.validatePassword(inputData.password)){
           document.getElementById([e.target.name]).innerText="Password must have at least one lowercase letter, one uppercase letter, one digit, and one special character"
        }
        else{
         
            
                document.getElementById([e.target.name]).innerText=""
           
             
              
            
        }
    }
useEffect(()=>{
 let temp_plan=plans.filter(val=>val.id==inputData.plan_id)[0]
 temp_plan && setPlan({...temp_plan,
    extra_data:JSON.parse(temp_plan?.extra_data)})
    setInputData(()=>({
        ...inputData,
        price:temp_plan?.price
    }))
       
     },[inputData.plan_id]
)
    return ( 
        <section className="mx-auto  ">

      

        <div className="flex items-center  justify-center ">
            <div className="fixed min-h-screen bg-primary top-0 left-0 text-white w-72 flex flex-col ">
                <div>
                <div className="flex justify-center " >
  <img src={logo} alt="" className="w-48 object-contain bg-white rounded-xl  p-3 mt-2"/>
</div>
                </div>
                <div className="my-auto flex justify-center">

               
                <div className="h-full">
                    <h1 className="text-xl font-bold my-3">
                  {  plan?.name}
                    </h1>
                <ul className="">
                <li className="flex w-48 my-2 justify-start">
          <span className="mx-2">
          <FaCheckCircle /></span> 
          <span>
         $ {  plan?.price}
            </span> 
            </li>
            <li className="flex w-64 my-2 justify-start">
          <span className="mx-2">
          <FaCheckCircle /></span> 
          <span>
          {  plan?.duration} Days
            </span> 
            </li>
       
        {
          plan && plan.extra_data.features?.map(val=>(
            <li className="flex w-64 my-2 justify-start">
          <span className="mx-2">
          <FaCheckCircle /></span> 
          <span>
          {  val}
            </span> 
            </li>
          ))
        }
        
       
      </ul>
      </div>
                </div>

            </div>
            <div className="mx-auto bg-white p-6 relative rounded-xl h-full">
        
                <h1 className=" text-2xl py-4 text-black font-bold  ">
  Sign Up
                </h1>

           

              

                <form className="grid  pb-3" onSubmit={handleSignupInfo}>
                 
                        
                    
                
                        <Input
                       
                        name={"first_name"}
                      
                        placeholder={"First Name"}
                        handleChange={handleChange}
                        value={inputData.first_name}
                      
                        type={"text"}

                        />
                       
                        <Input
                       
                        name={"last_name"}
                        
                        placeholder={"Last Name"}
                        handleChange={handleChange}
                        value={inputData.last_name}
                      
                        type={"text"}

                        />
                         
                        
                        <Input
                       
                        name={"email"}
                     
                        placeholder={"Email"}
                        handleChange={handleChange}
                        handleBlur={checkMail}
                        value={inputData.email}
                        
                        type={"email"}
                      

                        />
                    

                     
                        <Input
                       
                        name={"address"}
                      
                        placeholder={"Address"}
                        handleChange={handleChange}
                        value={inputData.address}
                     
                        type={"text"}

                        />
                      
                         <SelectInput
                        name={"plan_id"}
                        data={plans}
                        placeholder={"Select a plan"}
                        handleChange={handleChange}
                        value={inputData.plan_id}
                       
                      
                        type={"text"}
                      />
                     
                        <div className="grid grid-cols-2 gap-2">

                     
                        <SelectInput
                       
                        name={"state_id"}
                      
                        placeholder={"Select State"}
                        handleChange={handleChange}
                        value={inputData.state_id}
                        data={states}
                      
                        type={"text"}

                        />
                       
                          <Input
                       
                       name={"post_code"}
                     
                       placeholder={"Postcode"}
                       handleChange={handleChange}
                       value={inputData.post_code}
               
                       type={"text"}

                       
                       />
                      
                         </div>
                          <Input
                       
                       name={"password"}
                     
                       placeholder={"Password"}
                       handleChange={handleChange}
                       value={inputData.password}
                     handleBlur={checkPassword}
                       type={"password"}

                       />
                 
                     
                          <Input
                       
                       name={"confirm_password"}
                      
                       placeholder={"Confirm Password"}
                       handleChange={handleChange}
                       value={inputData.confirm_password}
                     
                       type={"password"}

                       />
                       <div className="mt-2">

                      
                     <Button text={"Continue to payment"} />
                     </div>
                     <div>
                    <p className="text-black mt-3">
                        Already have an account? <Link className="text-btn-primary" to={"/"} >Sign in</Link>
                    </p>
                  </div>
     
                </form>
            </div>
        </div>
 
</section>
     );
}
 
export default Signup;