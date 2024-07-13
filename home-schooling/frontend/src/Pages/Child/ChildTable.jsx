import { AiFillDelete, AiFillEdit } from "react-icons/ai";
import { useNavigate } from "react-router-dom/dist";
import Confirmation from "../../Components/Confirmation/Confirmation"
import { useContext, useState } from "react";
import TotalServices from "../../TotalServices";
import { toast } from "react-toastify";
import CreateChild from "./CreateChild";
import ActionButtons from "../../Components/Actions/ActionButtons"

const ChildTable = ({tableData,levels,GetData,settings,states}) => {
  const [showDelete,setShowDelete]=useState(false)
  const [deleteId,setDeleteId]=useState(null)
  const [showEdit,setShowEdit]=useState(false)
  const [editData,setEditData]=useState(null)
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

      const response = await TotalServices.DeleteChild(deleteId);
     

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
 
    return ( 
        <div className="overflow-x-auto mx-2">
        <table className="min-w-full divide-y divide-gray-200 overflow-x-auto ">
          <thead >
            <tr className="text-gray-700 bg-btn border-b border-b-black ">
              <th
                scope="col"
                className="px-6 py-3 text-left  font-medium uppercase tracking-wider -tl-xl"
              >
         First Name
              </th>
              <th
                scope="col"
                className="px-6 py-3   font-medium uppercase tracking-wider text-left"
              >
   Last Name
              </th>
            
          
              <th
                scope="col"
                className="px-6 py-3 text-left  font-medium uppercase tracking-wider -tr-xl"
              >
     Age
              </th>
              <th
                scope="col"
                className="px-6 py-3 text-left  font-medium uppercase tracking-wider -tr-xl"
              >
School Year
              </th>
              <th
                scope="col"
                className="px-6 py-3 text-left  font-medium uppercase tracking-wider -tr-xl"
              >
Start Date
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
                   {val.first_name}
                    </div>
                   
            </td>
         
            <td className="px-6 py-4 whitespace-nowrap">
             
           
             <div className=" font-medium capitalize">
            {val.last_name}
             </div>
            
     </td>
     <td className="px-6 py-4 whitespace-nowrap">
             
           
             <div className=" font-medium capitalize">
            {val.age}
             </div>
            
     </td>
     <td className="px-6 py-4 whitespace-nowrap">
             
           
             <div className=" font-medium capitalize">
            {val.level_name}
             </div>
            
     </td>
     <td className="px-6 py-4 whitespace-nowrap">
             
           
             <div className=" font-medium capitalize">
            {val.start_date.substring(0,16)}
             </div>
            
     </td>
          
           
     <td className="px-6 py-4 whitespace-nowrap">
             
             
        <ActionButtons 
                handleDeleteClick={e=>handleDelete(val.id)}
                handleEditClick={e=>handleEdit(val)}
        editMessage={"Edit Child"}
        deleteMessage={"Delete Child"}
     />
            
            
     </td>
            
             
            
            </tr>)) }
        
      
          </tbody>
        </table>
       
        {showEdit && <CreateChild levels={levels} editData={editData}  setShow={setShowEdit} GetData={GetData} settings={settings} states={states}/>}
        {showDelete && <Confirmation  setShowConfirmation={DeleteData} message="Are you sure you want to delete this Child?"/>}
      </div>
     );
}
 
export default ChildTable;