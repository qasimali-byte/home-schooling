import { useState } from "react";
import ActionButtons from "../../../Components/Actions/ActionButtons";

const EditChild = ({val,handleEdit}) => {
    const [hover,setHover]=useState(false)
    return ( 
        <div
        onMouseEnter={e=>handleEdit(val)}
        >

      
        <ActionButtons 
                  on
        editMessage={"Edit Child"}
     />
        </div>
     );
}
 
export default EditChild;