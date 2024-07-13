import { AiFillDelete, AiFillEdit } from "react-icons/ai";
import { useNavigate } from "react-router-dom/dist";
import Confirmation from "../../Components/Confirmation/Confirmation"
import { useContext, useState } from "react";
import TotalServices from "../../TotalServices";
import { toast } from "react-toastify";
import CreateChild from "./CreateReport";
import ActionButtons from "../../Components/Actions/ActionButtons"
import Button from "../../Components/Button/Button";

const ReportTable = ({tableData,setLoader,GetData,settings}) => {
  const navigate=useNavigate()
  const [showDelete,setShowDelete]=useState(false)
  const [deleteId,setDeleteId]=useState(null)
  const [supplerId,setSupplierId]=useState(null)

  const [show,setShow]=useState(false)
  const [showEdit,setShowEdit]=useState(false)
  const [showData,setShowData]=useState(null)
  const [editData,setEditData]=useState(null)
  const [showFiles,setShowFiles]=useState(false)
  const handleEdit =(val)=>{
    setShowEdit(true)
    setEditData(val)
  }
  const handleDelete=(id)=>{
    setDeleteId(id)
    setShowDelete(true)
  }
  const DeleteData= async (check) => {
    if(!check ){
      setShowDelete(false)
    }
    else{
    try {
     
   
      // setLoader(true)

      const response = await TotalServices.DeleteReport(deleteId);
     

      if (response.status === 200) {
    // console.log(response)
      toast.success(response.data.message)
      // setLoader(false)
      setShowDelete(false)
      GetData()
    
      }
    } catch (error) {
      console.log("error ", error);
      setShowDelete(false)
      // setLoader(false)
    }
  }

  };
  const handleCopyToClipboard = (key) => {
    navigator.clipboard.writeText(key.replace("pbkdf2:sha256:",""))
      .then(() => {
       toast.success("Copied to Clipboard")
      })
      .catch((error) => {
        toast.error('Copy to clipboard failed:', error);
      });
  };
    return ( 
        <div className="overflow-x-auto mx-2">
        <table className="min-w-full divide-y divide-gray-200 overflow-x-auto ">
          <thead >
            <tr className="text-gray-700 bg-btn border-b border-b-black ">
         
              <th
                scope="col"
                className="px-6 py-3   font-medium uppercase tracking-wider text-left whitespace-nowrap"
              >
Report Name
              </th>
            
          
            
              <th
                scope="col"
                className="px-6 py-3 text-left  font-medium uppercase tracking-wider -tr-xl whitespace-nowrap"
              >
Year
              </th>
              <th
                scope="col"
                className="px-6 py-3 text-left  font-medium uppercase tracking-wider -tr-xl whitespace-nowrap"
              >
Child
              </th>
              <th
                scope="col"
                className="px-6 py-3 text-left  font-medium uppercase tracking-wider -tr-xl whitespace-nowrap"
              >
Date Created
              </th>
              <th
                scope="col"
                className="px-6 py-3 text-left  font-medium uppercase tracking-wider -tr-xl whitespace-nowrap"
              >
Last Updated
              </th>
              <th
                scope="col"
                className="px-6 py-3 text-left  font-medium uppercase tracking-wider -tr-xl whitespace-nowrap"
              >
Report
              </th>
              <th
                scope="col"
                className="px-6 py-3 text-left  font-medium uppercase tracking-wider -tr-xl"
              >
Actions
              </th>
            </tr>
          </thead>
          <tbody className=" divide-y divide-gray-200 text-color-secondary">
          {tableData?.map(val=>( <tr>
              <td className="px-6 py-4 whitespace-nowrap">
             
           
                    <div className=" font-medium capitalize">
                   {val.name}
                    </div>
                   
            </td>
         
          
     <td className="px-6 py-4 whitespace-nowrap">
             
           
             <div className=" font-medium capitalize">
            {val.level_name}
             </div>
            
     </td>
     <td className="px-6 py-4 whitespace-nowrap">
             
           
             <div className=" font-medium capitalize">
            {val.child_name}
             </div>
            
     </td>
     <td className="px-6 py-4 whitespace-nowrap">
             
           
             <div className=" font-medium capitalize">
            {val.create_date.substring(0,16)}
             </div>
            
     </td>
     <td className="px-6 py-4 whitespace-nowrap">
             
           
             <div className=" font-medium capitalize">
            {val.last_edited?.substring(0,16)}
             </div>
            
     </td>
     <td className="px-6 py-4 whitespace-nowrap">
             
           
           <Button text={"View"} handleClick={e=>navigate("/report",{state:{id:val.id,data:val}})} />
     </td>
           
     <td className="px-6 py-4 whitespace-nowrap">
             
             
        <ActionButtons 
                handleDeleteClick={e=>handleDelete(val.id)}
                handleEditClick={e=>handleEdit(val)}
       
        deleteMessage={"Delete Report"}
     />
            
            
     </td>
            
             
            
            </tr>)) }
        
      
          </tbody>
       

        </table>
       
        {showEdit && <CreateChild editData={editData}   setShow={setShowEdit} GetData={GetData} settings={settings}/>}
        {showDelete && <Confirmation  setShowConfirmation={DeleteData} message="Are you sure you want to delete this Report?"/>}
      </div>
     );
}
 
export default ReportTable;