import { useEffect, useState } from "react";
import Package from "../Signup/Package";
import SelectInput from "../../Components/Input/SelectInput";
import ButtonLoader from "../../Components/Loader/ButtonLoader";
import Checkout from "../Signup/Checkout";
import TotalServices from "../../TotalServices";

const SubscriptionRenew = ({setShow,email,handleLogin}) => {
    const [plans,setPLans]=useState([])
    const [plan,setPlan]=useState(null)
    const [loader,setLoader]=useState(true)
    
    const GetData = async () => {
   
        try {
          setLoader(true);
          let response = await TotalServices.getPlans();
          if (response.status === 200) {
            //  console.log(response);
           setPLans(response.data.data)
  setInputData((prev)=>(
   { ...inputData,
    email:email,
    plan_id:response.data.data[0].id,
    price:response.data.data[0].price}
  ))
            setLoader(false);
          }
        } catch (e) {
          console.log(e);
          setLoader(false);
        }
      };
      const [inputData,setInputData]=useState({
        plan_id:""
      })
      const handleChange=(e)=>{
setInputData((prev)=>({
...prev,
[e.target.name]:e.target.value
}))
      }
      const handleRenew=async()=>{
        try {
            setLoader(true);
            let response = await TotalServices.SubscriptionRenewal(inputData);
            if (response.status === 200) {
              //  console.log(response);
              setShow(false)
              setLoader(false);
           handleLogin()
   
              setLoader(false);
            }
          } catch (e) {
            console.log(e);
            setLoader(false);
          }
      }
      useEffect(()=>{
        GetData()
      },[])
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
        <div className="fixed top-0 left-0 right-0 z-50  w-full p-4 overflow-x-hidden overflow-y-auto md:inset-0 h-[calc(100%-1rem)] md:h-full bg-[#fffb] ">
        <div className="relative w-full h-full max-w-2xl md:h-auto mx-auto ">
          <div
            className="relative rounded-lg shadow-xl 
         "
          >
            <div className="flex items-start justify-between p-4  -t ">
              <h3 className="text-xl   ">
             Activate Subscription
              </h3>
              <button
                type="button"
                className="  bg-btn-primary text-white -lg text-sm p-1.5 ml-auto inline-flex items-center "
                onClick={(e) => setShow(false)}
              >
                <svg
                  aria-hidden="true"
                  className="w-5 h-5"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    fillRule="evenodd"
                    d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                    clipRule="evenodd"
                  ></path>
                </svg>
                <span className="sr-only">Close modal</span>
              </button>
            </div>
            <div className="mx-auto bg-white px-4 py-6 relative rounded-lg">
          
                <Package plan={plan} />
                <SelectInput
                        name={"plan_id"}
                        data={plans}
                        placeholder={"Select a plan"}
                        handleChange={handleChange}
                        value={inputData.plan_id}
                       
                      
                        type={"text"}
                      />
  
             
 {plan !==null && <Checkout renew={true} plan={plan} amount={inputData.price} handleSuccess={handleRenew} inputData={inputData} setInputData={setInputData} />}
                
  
                
                 
              </div>
          </div>
        </div>
      </div>
     );
}
 
export default SubscriptionRenew;