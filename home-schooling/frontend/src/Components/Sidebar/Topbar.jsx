import { Link } from "react-router-dom";
import logo from "../../assets/home-schooling-logo-horizontal.png"
import {CiMenuBurger} from "react-icons/ci"
import menu from "../../assets/menu-bar.png"
import UserInfo from "./UserInfo";
import { GoDotFill } from "react-icons/go";
import { useEffect, useState } from "react";
import TotalServices from "../../TotalServices";
const TopBar = ({handleChange}) => {
  const [inputData,setInputData]=useState(null)
  const GetData = async () => {
   
    try {
    
      let response = await TotalServices.userData();
      if (response.status === 200) {
        //  console.log(response);
        setInputData(response.data?.data)

     
      }
    } catch (e) {
      console.log(e);
      setLoader(false);
    }
  };
  useEffect(() => {
    GetData();
  
  }, []);
    return ( 
      <div className="hidden sm:block w-screen z-50 fixed top-0 bg-white p-2 mb-2 pt-4  ">
        <div className="flex justify-between items-center mx-3">
        <Link      
              to={"/"}
              className="flex justify-center items-center  border-b-color-secondary p-2 rounded-xl text-primary   "
              >
               
                <img className="w-48 object-contain  font-bold" src={logo} />

              </Link>
              <div className="flex justify-center items-center ">
              {/* <div className="rounded-full bg-gray-200 mr-2 px-4 py-2 text-xl relative">
                  N
                  <span className="absolute -right-1 -top-1">
                  <GoDotFill color="red" />
                  </span>
                </div> */}
            
              <div className="flex p-3 bg-gray-200 rounded-full">
            
              {inputData &&  <UserInfo inputData={inputData} />}
               
              </div>
            
              </div>
              {/* <NotificationHandler /> */}
        </div>
       
              
      </div>
         );
}
 
export default TopBar;