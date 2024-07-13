import { useState } from "react";
import ActionButtons from "../../../Components/Actions/ActionButtons";
import ImageViewer from "../ImageViewer";
import Validations from "../../../Regex";
import Utils from "../../../Components/Utils/Utils";

const TermAccordion = ({val,handleDelete,handleEdit}) => {
    const [toggle,setToggle]=useState(false)
    return (
     
          <div  className="border rounded mb-2">
            <div
              className="flex justify-between items-center p-4 cursor-pointer"
              onClick={() => setToggle(!toggle)}
            >
              <div className="flex justify-between w-full mr-4">

             
              <p className="font-semibold text-gray-800">
  Term {val.term_id}
</p>
<p className="font-semibold text-gray-800">
             Activity Start Date   <span className="ml-1 text-gray-500">{Utils.dateFormat(val.start_date,"DD-MM-YYYY","DD MMMM YYYY")}</span>{val.end_date !== null ?<> - Activity End Date <span className="ml-1 text-gray-500">{Utils.dateFormat(val.end_date,"DD-MM-YYYY","DD MMMM YYYY")}</span> </>: ""}
</p></div>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className={`h-6 w-6 ${toggle ? 'transform rotate-180' : ''}`}
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </div>
            {toggle && (
             <div className="p-4">

             <div className="flex justify-between">

          
        




{val.inserted_date===val.last_updated_date?
       val.inserted_date  !==null &&    <p>
         
         <span className="mx-2">
          Created at:
         </span>  
       <span>
         {val.inserted_date.substring(0,16)}
       </span>
         </p>
         :
         val.last_updated_date  !==null&&      <p>
         
         <span className="mx-2">
           Last updated:
         </span>  
       <span>
         {val.last_updated_date.substring(0,16)}
       </span>
         </p>
}
</div>
         <div className="flex justify-between">

         
           { val.created_date  !==null &&   <p>
         
         <span className="mx-2">
           Activity Done:
         </span>  
       <span>
         {val.created_date.substring(0,16)}
       </span>
         </p>}
           </div>
          
     
       <div className="mt-4">
           <div className="flex justify-between items-start mb-3 ">
               {/* <p className="text-gray-800 text-lg font-bold">Activity</p> */}
               <p className="bg-gray-100 rounded-lg p-4 text-gray-700 w-full h-full max-h-max whitespace-pre-wrap mx-3">
           {val.activity_description}
           </p>
              
<div>
<ActionButtons 
           handleDeleteClick={e=>handleDelete(val.activity_id)}
           handleEditClick={e=>handleEdit(val)}
   editMessage={"Edit Activity"}
   deleteMessage={"Delete Activity"}
/>   
</div>
         
             
  { val.attached_files_names !==null &&  val.attached_files_names.filter((val,index)=> Validations.isImage(val)).length>=1 && <div className="flex">
               <ImageViewer fileNames={val.attached_files_names}  fileUrls={val?.attached_files_urls}/>
        
               </div>}
           </div>
          
      { val.attached_files_names!==null &&     <div className="">
          <p className="text-gray-800 text-lg font-bold my-3">
           Files
          </p>
          <div className="bg-gray-100 rounded-lg p-4 text-gray-700 w-full h-full flex justify-between ">

        <div className="w-1/2">

       
          { val.attached_files_names!==null &&val.attached_files_names.map((file,index)=> (
          <a className="block hover:text-blue-500 hover:underline" target="_blank" href={val?.attached_files_urls[index]}>{file}</a>
          ))}
           </div>
    
            </div>
          
           </div>}
      
          {val.attached_links!==null && val.attached_links!==""&&     <div className="">
          <p className="text-gray-800 text-lg font-bold my-3">
           Urls
          </p>
          <div className="bg-gray-100 rounded-lg p-4 text-gray-700 w-full h-ful">

        
          {val.attached_links!==null &&val.attached_links.split(",").map((link,index)=> (
          <a className="block hover:text-blue-500 hover:underline" target="_blank" href={link}>{link}</a>
          ))}
            </div>
           </div>}
     </div>  
     </div>
            )}
          </div>
      
      );
}
 
export default TermAccordion;