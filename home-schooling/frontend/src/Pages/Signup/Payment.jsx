
import checkoutImg from "../../assets/checkout.jpg"

import TotalServices from "../../TotalServices";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { useState } from "react";
import Checkout from "./Checkout"
import { IoIosArrowBack } from "react-icons/io";

const Payment = ({setSignupInfo,inputData,plan}) => {
  const navigate=useNavigate()
  const [loader,setLoader]=useState(false)
  const [checkout,setCheckout]=useState(false)
 
    return (
        <div>
          
          <div className="flex justify-center min-h-screen">
<div className="hidden lg:flex w-full justify-center items-center " >
                <img src={checkoutImg} alt="" className="h-full object-cover"/>
            </div>
          
  <div className="flex-col w-full max-w-xl m-12 p-6 flex justify-center">
  <div className="m-2">
                  <span role="button" className="flex items-center" onClick={e=>setSignupInfo(false)}>
          <IoIosArrowBack /> Go back
      </span>
                  </div>
 
</div>


 
</div>

        </div>
      );
}
 
export default Payment;