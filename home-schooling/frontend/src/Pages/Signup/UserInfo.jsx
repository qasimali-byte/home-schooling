import { FaUser } from "react-icons/fa";
import { MdEmail } from "react-icons/md";
import { IoLocation } from "react-icons/io5";
import { MdFolderZip } from "react-icons/md";
import { FaCity } from "react-icons/fa6";
import { useEffect, useState } from "react";
const UserInfo = ({inputData,states}) => {
    const [state,setState]=useState("")
useEffect(()=>{
   
setState(states.find(val=>val.id=inputData.state_id)?.["name"])
},[])
    return ( <div className="mx-auto text-black">

        <div className="p-4  border-b flex  items-center border-b-black">
<span className="mr-3">
    <FaUser />
</span>
<h4>
    {inputData?.first_name+ " "+ inputData?.last_name}
</h4>
        </div>
        <div className="p-4 flex  items-center border-b border-b-black">
<span className="mr-3">
    <MdEmail />
</span>
<h4>
    {inputData?.email}
</h4>
        </div>
        <div className="p-4 flex  items-center border-b-black border-b">
<span className="mr-3">
    <IoLocation />
</span>
<h4>
    {inputData?.address}
</h4>
        </div>
        <div className="p-4 flex  items-center border-b border-b-black">
<span className="mr-3">
    <MdFolderZip />
</span>
<h4>
    {inputData?.post_code}
</h4>
        </div>
        <div className="p-4 flex  items-center border-b border-b-black">
<span className="mr-3">
    <FaCity />
</span>
<h4>
    {state}
</h4>
        </div>
    </div> );
}
 
export default UserInfo;