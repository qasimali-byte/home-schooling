import { useContext, useEffect, useState } from "react";
import Button from "../../Components/Button/Button";
import Input from "../../Components/Input/Input";
import { AuthContext } from "../../App";
import TotalServices from "../../TotalServices";
import { toast } from "react-toastify";
import Validations from "../../Regex";
import ButtonLoader from "../../Components/Loader/ButtonLoader";
import SelectInput from "../../Components/Input/SelectInput";
import Utils from "../../Components/Utils/Utils";
import GetStates from "../../Components/Functions/UtilsFunctions";
import Subscription from "./Subscription";
import { MdSubscriptions } from "react-icons/md";

const Profile = () => {
    const [loader,setLoader]=useState(false)
    const [states,setStates]=useState([])
   
    const [inputData,setInputData]=useState({
      first_name:"",
      last_name:"",
   
      address:"",
  
      states_id:"",
      post_code:"",
   
  })
  const getStates=async()=>{
    const data=await GetStates()
    setStates(data)
  }
    const [userData,setUserData]=useState(null)
    const { setUserLogin, userLogin } = useContext(AuthContext);
    const [disable,setDisable]=useState(true)
 
    const [password,setPassword]=useState({
        oldpassword:"",
        newpassword:"",
      confirmPassword:"",
    })
const handleChange=(e) =>{
    setInputData((prev)=>({
...inputData,
[e.target.name]:e.target.value
    }))
}
const handlePassChange=(e) =>{
    setPassword((prev)=>({
...prev,
[e.target.name]:e.target.value
    }))
}
useEffect(()=>{
  document.title="Home Schooling - Manage Profile"
  getStates()
        },[])
const GetData = async () => {
   
    try {
    
      let response = await TotalServices.userData();
      if (response.status === 200) {
        //  console.log(response);
        setInputData(response.data.data)

     
      }
    } catch (e) {
      console.log(e);
      setLoader(false);
    }
  };
  const ChangePassword = async () => {
    console.log(password);
   if(password.newpassword!==password.confirmPassword){
    toast.error("Password doesn't match")
   }
   else if(!Validations.validatePassword(password.newpassword)){
    toast.error("Password must have at least one lowercase letter, one uppercase letter, one digit, and one special character")

   }
   else{
    try {
    setLoader(true)
      let response = await TotalServices.ChangePassword(password);
      if (response.status === 200) {
        //  console.log(response);
   toast.success(response.data.message)
   setLoader(false)
   localStorage.removeItem("UserAuth")
   localStorage.removeItem("UserIsLogin")
 
   setUserLogin(!userLogin)


     
      }
    } catch (e) {
      console.log(e);
      setLoader(false);
    }
   }
  };
  const handleEdit = async () => {
   
    if(Validations.isEmpty(inputData.first_name)||Validations.isEmpty(inputData.last_name)||Validations.isEmpty(inputData.post_code)||Validations.isEmpty(inputData.states_id)||Validations.isEmpty(inputData.address)){
      toast.error("Fields can't be empty")
  }
  else if(inputData.first_name.length>=45){
    toast.error("First Name Character Limit Exceeded")
  }
  else if(inputData.last_name.length>=45){
    toast.error("Last  Name Character Limit Exceeded")
  }
   else{
    try {
 
      let response = await TotalServices.editUserData({...inputData,state:inputData.states_id});
      if (response.status === 200) {
        //  console.log(response);
   toast.success(response.data.message)
  GetData()
setDisable(true)

     
      }
    } catch (e) {
      console.log(e);
 }
   }
  };
  const [activeTab, setActiveTab] = useState(1);

  const handleTabClick = (tabIndex) => {
    setActiveTab(tabIndex);
  };

useEffect(() => {
  GetData();
}, []);
    return ( 
        <div className={`p-4 sm:ml-64 sm:mt-24 bg-gray-200 min-h-[90vh] rounded-tl-xl`}>
           <div className="flex">


<div className="border-b border-gray-200 mb-10">
    <ul className="flex flex-wrap -mb-px text-sm font-medium text-center text-gray-500 ">
        <li className="me-2">
            <button onClick={() => handleTabClick(1)} className={`inline-flex items-center justify-center p-4 border-b-2 border-transparent rounded-t-lg   group ${activeTab===1?"text-primary border-primary":"hover:text-gray-600 hover:border-gray-300"}`}>
                <svg className={`w-4 h-4 me-2  ${activeTab===1?"text-primary border-primary":"text-gray-400 group-hover:text-gray-500 "}`} aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 0a10 10 0 1 0 10 10A10.011 10.011 0 0 0 10 0Zm0 5a3 3 0 1 1 0 6 3 3 0 0 1 0-6Zm0 13a8.949 8.949 0 0 1-4.951-1.488A3.987 3.987 0 0 1 9 13h2a3.987 3.987 0 0 1 3.951 3.512A8.949 8.949 0 0 1 10 18Z"/>
                </svg>Edit Profile
            </button>
        </li>
     
        <li className="me-2">
            <button 
            
             onClick={() => handleTabClick(2)}
             className={`inline-flex items-center justify-center p-4 border-b-2 border-transparent rounded-t-lg   group ${activeTab===2?"text-primary border-primary":"hover:text-gray-600 hover:border-gray-300"}`}>
                <svg  className={`w-4 h-4 me-2  ${activeTab===2?"text-primary border-primary":"text-gray-400 group-hover:text-gray-500 "}`}  aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M5 11.424V1a1 1 0 1 0-2 0v10.424a3.228 3.228 0 0 0 0 6.152V19a1 1 0 1 0 2 0v-1.424a3.228 3.228 0 0 0 0-6.152ZM19.25 14.5A3.243 3.243 0 0 0 17 11.424V1a1 1 0 0 0-2 0v10.424a3.227 3.227 0 0 0 0 6.152V19a1 1 0 1 0 2 0v-1.424a3.243 3.243 0 0 0 2.25-3.076Zm-6-9A3.243 3.243 0 0 0 11 2.424V1a1 1 0 0 0-2 0v1.424a3.228 3.228 0 0 0 0 6.152V19a1 1 0 1 0 2 0V8.576A3.243 3.243 0 0 0 13.25 5.5Z"/>
                </svg>Update Password
            </button>
        </li>
        <li className="me-2">
            <button 
            
             onClick={() => handleTabClick(3)}
             className={`inline-flex items-center justify-center p-4 border-b-2 border-transparent rounded-t-lg   group ${activeTab===3?"text-primary border-primary":"hover:text-gray-600 hover:border-gray-300"}`}>
         <span className={`w-4 h-4 me-2  ${activeTab===3?"text-primary border-primary":"text-gray-400 group-hover:text-gray-500 "}`} >
         <MdSubscriptions />
          </span>   
              
              Manage Subscription
            </button>
        </li>
    
    </ul>
</div>

        
      </div>
    {  activeTab === 1?
        <div className="relative w-full h-full max-w-2xl md:h-auto mx-auto mb-5 shadow-xl">
          <div
            className="relative  rounded-lg shadow text-color-secondary
         "
          >
           
            <div className="space-y-3  p-4 space-x-2">
           
            <form className="grid " 
            // onSubmit={handleSignupInfo}
            >
                 <div className="grid grid-cols-2 gap-2"
                
                 >

                
                        <Input
                       
                        name={"first_name"}
                      
                        placeholder={"First Name"}
                        handleChange={handleChange}
                        value={inputData?.first_name}
                      disabled={disable}
                        type={"text"}

                        />
                        <Input
                       
                        name={"last_name"}
                        
                        placeholder={"Last Name"}
                        handleChange={handleChange}
                        value={inputData?.last_name}
                        disabled={disable}
                        type={"text"}

                        />
                         </div>
                        <Input
                       
                        name={"email"}
                        disabled={true}
                        placeholder={"Email"}
                        handleChange={handleChange}
                        value={inputData?.email}
                      
                        type={"email"}

                        />
                        <Input
                       
                        name={"address"}
                        disabled={disable}
                        placeholder={"Address"}
                        handleChange={handleChange}
                        value={inputData?.address}
                     
                        type={"text"}

                        />
                      
                        <div className="grid grid-cols-2 gap-2">

                     
                        <SelectInput
                         disabled={disable}
                        name={"states_id"}
                      
                        placeholder={"Select State"}
                        handleChange={handleChange}
                        value={inputData?.states_id}
                        data={states}
                      
                        type={"text"}

                        />
                          <Input
                       
                       name={"post_code"}
                       disabled={disable}
                       placeholder={"Postcode"}
                       handleChange={handleChange}
                       value={inputData?.post_code}
               
                       type={"text"}

                       
                       />
                         </div>
                          
                       
                

              

                   
             
                  
                </form>
               {disable?
                <Button text={"Edit"} handleClick={e=>setDisable(false)} />
              :
              <Button text={"Save"} handleClick={handleEdit} color={"bg-green-600"} />
              }
         
              <div className="md:flex justify-end">
           
                {/* {
                  loader?
                  <ButtonLoader />
                  :
                  <Button
                
               text={"Save Profile"}
                //   handleClick={handleAddStore}
                  // disabled={stores.filter(value=>value.name.toLowerCase()===storeInput.name.toLowerCase()).length>0}
                />
  } */}
              
              </div>
            </div>
          </div>
        </div>
        :
        activeTab === 2?

        <div className="relative w-full h-full max-w-2xl md:h-auto mx-auto shadow-xl ">
        <div
            className="relative  rounded-lg shadow text-color-secondary
         "
          >
          
            <div className="space-y-3  p-4 space-x-2">
           
            <form className="grid " 
            // onSubmit={handleSignupInfo}
            >
                

                
                        <Input
                       
                        name={"oldpassword"}
                      
                        placeholder={"Old Password"}
                        handleChange={handlePassChange}
                        value={password.oldpassword}
                
                        type={"password"}

                        />
                         <Input
                       
                       name={"newpassword"}
                     
                       placeholder={"New Password"}
                       handleChange={handlePassChange}
                       value={password.newpassword}
               
                       type={"password"}

                       />
                        <Input
                       
                       name={"confirmPassword"}
                     
                       placeholder={"Confirm Password"}
                       handleChange={handlePassChange}
                       value={password.confirmPassword}
               
                       type={"password"}

                       />
                        
                      
                       
                

              

                   
             
                  
                </form>
             
              <Button text={"Change Password"} handleClick={ChangePassword} />
              
         
              <div className="md:flex justify-end">
           
                
              
              </div>
            </div>
          </div>
        </div>
      :
      <Subscription />  
      }
 </div>
    
     );
}
 
export default Profile;