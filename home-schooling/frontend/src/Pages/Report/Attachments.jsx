import { useState } from "react";
import { FaCloudUploadAlt } from "react-icons/fa";

const Attachments = ({handleGetDOCFile}) => {
    const [hover,setHover]=useState(false)
    return (
        <div role="button" className="relative   h-20 rounded-lg  border-2 border-blue-700 bg-[#2563eb] flex justify-center items-center cursor-pointer"
        onMouseEnter={e=>setHover(true)}
        onMouseLeave={e=>setHover(false )}
        onClick={handleGetDOCFile}
        >
          <div className="absolute cursor-pointer">
      
              <i className="fa fa-folder-open fa-4x text-blue-700"></i>
            
             
            
              <div className="flex flex-col items-center  cursor-pointer">
             {hover? <span className="block text-white font-normal uppercase">
             Add Attachments
              </span>
              :
              <span className="flex flex-col justify-center items-center text-white font-normal uppercase">
          <FaCloudUploadAlt size={50} />
          Upload up to 3 files only.
              </span>
}
             </div>
            
            </div>
          

       
        </div>
      );
}
 
export default Attachments;