import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import './App.css'
import Signup from "./Pages/Signup/Signup";
import AccountCreation from "./Pages/Signup/AccountCreation";
import Login from "./Pages/Login/Login";
import ProtectedRoutes from "./Routes/ProtectedRoutes";
import { createContext, useState } from "react";
import DashboardPage from "./Pages/DashboardPage/DashboardPage";
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import ManageChild from "./Pages/Child/ManageChild";
import ManageReport from "./Pages/Report/ManageReport";
import ThankYou from "./Pages/Thankyou/ThankYou";
import Profile from "./Pages/Profile/Profile"
import EmailVerification from "./Pages/EmailVerification/EmailVerification";
import GenerateReport from "./Pages/Report/GenerateReport";
import NotFound from "./Pages/NoPage/404Page";
export const AuthContext = createContext();

function App() {

  const [userLogin, setUserLogin] = useState(false);
  const [iconMenu,SetIconMenu]=useState(false)
  return (
    <>
    <ToastContainer />
       <AuthContext.Provider
        value={{ userLogin, setUserLogin,iconMenu,SetIconMenu}}
      >
      <Router>
   
          <Routes>
         
              {/* ADMIN  */}
             
             
              <Route path="/signup" element={ <AccountCreation/>} />  
              <Route path="*" element={ <NotFound />} />  
              <Route path="/thankyou" element={ <ThankYou/>} />  
              <Route path="/email-verification" element={<EmailVerification />} />
              <Route path="/" element={ <ProtectedRoutes/>} >
              <Route path="" element={ <DashboardPage/>} />  
              <Route path="manage-children" element={ <ManageChild/>} />  
              <Route path="manage-report" element={ <ManageReport/>} /> 
              
              <Route path="profile" element={ <Profile/>} />  
              <Route path="report" element={ <GenerateReport/>} />  
         
            
              </Route>
         
            

              </Routes>
            
              </Router>
   

              </AuthContext.Provider>
   
    </>
  )
}

export default App
