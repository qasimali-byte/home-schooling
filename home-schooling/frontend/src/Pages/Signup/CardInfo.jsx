import Input from "../../Components/Input/Input";
import { FaUser } from "react-icons/fa";
import { MdEmail } from "react-icons/md";
import { IoLocation } from "react-icons/io5";
import { MdFolderZip } from "react-icons/md";
import { RiLockPasswordFill } from "react-icons/ri";
import { FaCity } from "react-icons/fa";
import { BsCreditCard2FrontFill } from "react-icons/bs";
import Button from "../../Components/Button/Button";
import { useState } from "react";
const CardInfo = () => {
    const [inputData,setInputData]=useState({
        first_name:"",
        last_name:"",
        email:"",
        address:"",
        password:"",
        state:"",
        zip:"",
        confirm_password:""
    })
    const handleChange=(e) =>{
setInputData((...prev)=>({
    ...prev,
    [e.target.name]:e.target.value
}))
    }
    return ( 
        <form className="grid  ">
                 
        <Input
       
        name={inputData.first_name}
        label={"Cardholder Name"}
        placeholder={"Enter cardholder name"}
        handleChange={handleChange}
        value={inputData.last_name}
        icon={<FaUser />}
        type={"text"}

        />
        <Input
       
        name={inputData.first_name}
        label={"Card Number"}
        placeholder={"Enter your card number"}
        handleChange={handleChange}
        value={inputData.last_name}
        icon={<BsCreditCard2FrontFill />}
        type={"number"}

        />
        <div className="grid grid-cols-2 ">

      
        <Input
       
        name={inputData.first_name}
        label={"Expiration Date"}
        placeholder={"Enter your email address"}
        handleChange={handleChange}
        value={inputData.last_name}
       
        type={"month"}

        />
        <Input
       
        name={inputData.first_name}
        label={"CVV"}
        placeholder={"Enter your cvv"}
        handleChange={handleChange}
        value={inputData.last_name}
       
        type={"number"}

        />
         </div>
       
         <div class="mt-6 flex items-center justify-between">
        <p class="text-sm font-medium text-gray-900">Total</p>
        <p class="text-2xl font-semibold text-gray-900">$238.99</p>
        </div>


<div className="w-full flex pt-5">
<Button text={"Buy Plan"} handleClick={e=>setSignupInfo(true)} />
</div>


   

  
</form>
     );
}
 
export default CardInfo;