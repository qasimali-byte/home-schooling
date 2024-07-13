import React, { useState, useEffect, useContext } from "react";
import { AuthContext } from "../App";
import Dashboard from "../Pages/Dashboard/Dashboard";
import Login from "../Pages/Login/Login";


const ProtectedRoutes = () => {
  const {userLogin}=useContext(AuthContext)
  const [UserIsLogin, setUserIsLogin] = useState(
    localStorage.getItem("UserIsLogin")
  );

  useEffect(() => {
console.log("e");
setUserIsLogin(localStorage.getItem("UserIsLogin"))
  }, [userLogin]);
  return UserIsLogin === "true" ? <Dashboard />: <Login />;
};

export default ProtectedRoutes;
