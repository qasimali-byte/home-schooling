import { useEffect, useState } from "react";
import CardInfo from "./CardInfo";
import Package from "./Package";
import UserInfo from "./UserInfo";
import checkoutImg from "../../assets/signup.avif"
import { IoIosArrowBack } from "react-icons/io";
import Signup from "./Signup";
import Payment from "./Payment";
import logo from "../../assets/home-schooling-logo-horizontal.png"
import TotalServices from "../../TotalServices";
import Loader from "../../Components/Loader/Loader";
import Checkout from "./Checkout";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import GetStates from "../../Components/Functions/UtilsFunctions";


const AccountCreation = () => {
    const [signupInfo,setSignupInfo]=useState(false)
    const [loader,setLoader]=useState(false)
    const [plans,setPLans]=useState([])
    const [states,setStates]=useState([])
   

    const [inputData,setInputData]=useState({
        first_name:"",
        last_name:"",
        email:"",
        address:"",
        password:"",
        state_id:"",
        post_code:"",
        confirm_password:"",
        plan_id:"",
        price:""
       
    })
    const navigate=useNavigate()
    const [plan,setPlan]=useState(null)
    const GetData = async () => {
   
        try {
          setLoader(true);
          let response = await TotalServices.getPlans();
          if (response.status === 200) {
            //  console.log(response);
           setPLans(response.data.data)
  setInputData((prev)=>(
   { ...inputData,
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
  
      const handleCheckout =async() =>{
        try {
          setLoader(true);
          let response = await TotalServices.signUp(inputData);
          if (response.status === 200) {
            //  console.log(response);
            toast.success(response.data.message)
          navigate("/thankyou")
      
            setLoader(false);
          }
        } catch (e) {
          console.log(e);
          setLoader(false);
        }
      }
      const GetStatesData=async()=>{
       let data=await GetStates()
     
        setStates(data)
      }
    useEffect(() => {
      GetData();
      GetStatesData();
    }, []);
    useEffect(()=>{
      document.title="Home Schooling - Signup"
            },[])
         
    return ( 
        loader?
        <Loader />
        :
  <div className="bg-cover bg-no-repeat bg-gray-200">
      
{signupInfo &&  <div className="flex justify-center " >
  <img src={logo} alt="" className="w-48 object-contain bg-white rounded-xl  p-3 mt-2"/>
</div>}
        <div className="pt-6 flex flex-col-reverse  min-h-screen lg:flex-row-reverse justify-around  "
       
        >
       

      {signupInfo?
      
        <div className="mx-10  bg-white p-6 h-full rounded-xl w-full">
        <div className="m-2">
                  <span role="button" className="flex items-center " onClick={e=>setSignupInfo(false)}>
          <IoIosArrowBack /> Go back
      </span>
                  </div>
              
                  <div className=" flex flex-col items-center mx-auto  py-4 sm:flex-row ">
                      
      
                     
        <h1  className="text-2xl font-bold text-black">SUMMARY</h1>
       
      </div>
         <div className="flex lg:justify-around lg:flex-row flex-col justify-center items-center">

        
       <div className="px-10">

      
      
      
          <p className=" text-lg font-medium text-white">Account Info</p>
         <UserInfo  inputData={inputData} states={states}/>
         </div>
         <div className="w-full max-w-lg lg:-mt-16">
         {
       plan &&   <div className=" w-full rounded-lg border  px-2 py-4 ">
           
           <Package plan={plan} />
          </div>}
        
         <Checkout plan={plan} amount={inputData.price} handleSuccess={handleCheckout} inputData={inputData} setInputData={setInputData} />
         </div>
        </div>
        </div>
        :
        <Signup setPlan={setPlan} states={states}  setInputData={setInputData} plan={plan} inputData={inputData} setSignupInfo={setSignupInfo} plans={plans} />
}

        </div>

       </div>
       
     );
}
 
export default AccountCreation;