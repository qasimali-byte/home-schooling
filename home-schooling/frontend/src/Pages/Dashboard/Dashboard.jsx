import { Outlet } from "react-router-dom";
import Sidebar from "../../Components/Sidebar/Sidebar";



const Dashboard = () => {
  
    return ( 
        <>
        <Sidebar />
        <Outlet />
        </>
     );
}
 
export default Dashboard;