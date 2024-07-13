import { useContext, useEffect, useState } from "react";
import TotalServices from "../../TotalServices";
import Button from "../../Components/Button/Button";
import { AuthContext } from "../../App";
import { FaCheckCircle } from "react-icons/fa";
import Loader from "../../Components/Loader/Loader";
import Confirmation from "../../Components/Confirmation/Confirmation";

const Subscription = () => {
    const [subscription,setSubscription]=useState()
    const { setUserLogin, userLogin } = useContext(AuthContext);
    const [loader,setLoader]=useState(true)
    const [confirmation,setConfirmation]=useState(false)

    const GetData = async () => {
   
        try {
        setLoader(true)
          let response = await TotalServices.GetSubscription();
          if (response.status === 200) {
            //  console.log(response);
            setSubscription(response.data.data[0])
    setLoader(false)
       
          }
        } catch (e) {
          console.log(e);
         
        }
      };
    const handleCancel =async(check)=>{
        if(check){

        
        try {
        
            let response = await TotalServices.CancelSubscription(subscription.id);
            if (response.status === 200) {
              //  console.log(response);
            
              localStorage.removeItem("UserAuth")
              localStorage.removeItem("UserIsLogin")
            
              setUserLogin(!userLogin)
              setConfirmation(false)
           
            }
          } catch (e) {
            console.log(e);
         
          }
        }
        else{
            setConfirmation(false)
        }
    }
      useEffect(()=>{
GetData()
      },[])
    return (<div>
         <div className="relative w-full h-full max-w-2xl md:h-auto mx-auto shadow-xl ">
        <div
            className="relative  rounded-lg bg-white shadow text-color-secondary
         "
          >
           
           
           {loader?
           
           <Loader />
           :
           <div className="space-y-3  p-4 space-x-2">
           
            <h1 className="text-xl">
            Subscription Detail
          </h1>
          <div className="flex justify-between">
          <p>
           { subscription?.plan_name}
          </p>
          <p>
         { subscription?.plan_price}$
          </p>

          </div>
          <div>


{
subscription?.plan_extradata.features?.map(val=>(
  <li className="flex w-64 my-2 justify-start">
<span className="mx-2">
<FaCheckCircle /></span> 
<span>
{  val}
  </span> 
  </li>
))
}
</div>
             <div className="flex justify-end pt-5">
                <div>
                <Button text={"Cancel Subscription"} handleClick={e=>setConfirmation(true)} />
                </div>
          
             </div>
          
              
         
              <div className="md:flex justify-end">
           
                
              
              </div>
            </div>}
          </div>
          {
            confirmation && <Confirmation  message={"Are you sure? You will no longer have access to dashboard"} setShowConfirmation={handleCancel}  />
          }
        </div>
      
      
    </div>  );
}
 
export default Subscription;