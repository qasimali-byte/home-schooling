import { useEffect, useRef, useState } from "react";
import { FaCloudUploadAlt } from "react-icons/fa";
import { FaFileSignature } from "react-icons/fa";
import { MdOutlineRemoveCircle } from "react-icons/md";
import { toast } from "react-toastify";
import Attachments from "./Attachments";


const FileUpload = ({inputData, setInputData,editData}) => {

    const [editFiles,setEditFiles]=useState([])
    const [editFileIds,setEditFilesIds]=useState([])
  
  
  useEffect(()=>{
   editData && setEditFiles(editData.attached_files_names===null?[]:editData.attached_files_names)
   editData && setEditFilesIds(editData.attached_files_ids===null?[]:editData.attached_files_ids)
  },[editData])
  
  
    const handleGetDOCFile = () =>{
      document.getElementById("docinput").click()
     }
const getFiles=(e)=>{
  let files=[...e.target.files]
 

  let length=inputData.file_names.length+files.length

 if(length>3){
  toast.error("Maximum 3 files are allowed")
}else{
  setInputData({
    ...inputData,
    file_names:[...inputData.file_names,...files]
  })
}

}

const removeFile=(index) =>{
  let data=[...inputData.file_names]
  data.splice(index,1)

  setInputData({
    ...inputData,
    file_names:[...data]
  })
}
const removeEditFile=(index) =>{
  let data=[...editFiles]
  let ids=[...editFileIds]
  
  data.splice(index,1)
  ids.splice(index,1)
  setInputData({
    ...inputData,
    file_ids:[...inputData.file_ids,editFileIds[index]]
  })
  setEditFilesIds(ids)
setEditFiles(data)
}
    return (
  
          <>
      

        <div className=" py-5 bg-white px-2">
   
          <div className=" rounded-lg ">
         
            <div className="md:flex justify-center">
            
              <div className="w-full  grid grid-cols-1 gap-4">
               <Attachments  handleGetDOCFile={handleGetDOCFile} />
             
              
               <div role="button" className="  p-6   flex   items-center cursor-pointer bg-gray-200 h-24"
              
                >
                  <div className=" cursor-pointer">
              
           
                     {
                   
                     inputData.file_names.map((val,index)=>(
                    <div className="flex cursor-text">
                    
                     <span className="  mx-3 items-center">
                   <FaFileSignature/>
                     </span>
      
                       <span className="block  font-normal ">
                 {val.name}
                       </span>
                       <span className=" mx-3 cursor-pointer"
                       onClick={e=>removeFile(index)}
                       >
                       <MdOutlineRemoveCircle />
                       </span>
                      </div>
                       ))
                     
                    }
                     {
                    
                     editFiles?.map((file,index)=>(
                    <div className="flex cursor-text">
                     <span className="  mx-3 items-center">
                   <FaFileSignature/>
                     </span>
              
                       <span className="block  font-normal ">
                 {file}
                       </span>
                       <span className=" mx-3 cursor-pointer"
                       onClick={e=>removeEditFile(index)}
                       >
                       <MdOutlineRemoveCircle />
                       </span>
                      </div>
                       ))
                     
                    }
                    </div>
                  

               
                </div>
           
              </div>
            </div>
          </div>
          <input
                    type="file"
                    id="docinput"
              multiple
                    className="hidden"
                    onChange={getFiles}
                  />
        </div>

        
        </>
      
      );
}
 
export default FileUpload;