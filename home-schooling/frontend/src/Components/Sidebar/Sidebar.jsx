import { useContext, useEffect, useRef, useState } from "react";
import { MdDashboard } from "react-icons/md";
import { HiDocumentReport } from "react-icons/hi";
import { Link, NavLink, useNavigate } from "react-router-dom";
import { FaChild } from "react-icons/fa";
import dashboard from "../../assets/dashboard.png"
import logo from "../../assets/home-schooling-logo-horizontal.png"
import SideBarButton from "./SideBarButton";
import { AuthContext } from "../../App";
import TopBar from "./Topbar";
import Button from "../Button/Button";
const Sidebar = () => {

  const [classes, setClasses] = useState(true);

  const {userLogin,setUserLogin } = useContext(AuthContext);


  
  const [loader,setLoader]=useState(false)
 
  const changeIconMenu=() =>{
    SetIconMenu(!iconMenu)
      }
    

     
  
  const handleChange = () => {
    setClasses(!classes);
  };
const handleLogout =() =>{
  localStorage.removeItem("UserAuth")
  localStorage.removeItem("UserIsLogin")
  setUserLogin(!userLogin)
}

  let navLinks=[
    {
      name:"Dashboard",
      links:"/",
    
      icons:<MdDashboard />
    },
    {
      name:"Manage Children",
      links:"/manage-children",
    
      icons:<FaChild />
    }, 
    {
      name:"Manage Report",
      links:"/manage-report",
    
      icons:<HiDocumentReport />
    }, 
   
   
   

  ]
  return (
    <>
      <SideBarButton handleChange={handleChange}></SideBarButton>
      <TopBar  />
      <aside
        id="default-sidebar"
        className={`fixed top-0 left-0 z-40 w-60 h-screen   ${
          classes
            ? "transition-transform -translate-x-full sm:translate-x-0"
            : ""
        }`}
        aria-label="Sidebar"
      >
   
      <div className="px-3 py-4 h-full flex flex-col justify-between  bg-white   lg:pb-0 sm:pt-32">
     
          <ul className="space-y-2 font-medium">
          <li>
          <Link
              
              to={"/"}
                className="flex justify-center pb-2 text-sm font-bold  sm:hidden  border-b border-b-color-secondary   "
              >
      
                <img className="w-15 font-bold" src={logo} />
              </Link>
              </li>
           
        
     
   
        {/* permissions.includes(val.permission) && */}
   
           {navLinks.map((val,index)=>(  <li>
              <NavLink
              key={index}
              to={val.links}
              onClick={handleChange}
              className={({isActive})=>(`p-2 justify-start flex  items-center   w-full rounded-lg ${isActive?" font-bold":"text-primary font-normal"} `)}
              >
          <span>
            {val.icons}
          </span>
             {  <span className="mx-2">{val.name}</span>}
              </NavLink>
            </li>))}

          
          </ul>
         <div className="mb-3">

       
          <Button text={"Log out"} handleClick={handleLogout} />
          </div>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
