import { useEffect, useState } from "react";
import Validations from "../../Regex";
import { toast } from "react-toastify";
import ButtonLoader from "../../Components/Loader/ButtonLoader";
import { AiOutlineInfoCircle } from "react-icons/ai";
import Input from "../../Components/Input/Input";
import Button from "../../Components/Button/Button";
import TotalServices from "../../TotalServices";
import dayjs from "dayjs"
import SelectInput from "../../Components/Input/SelectInput";
import {years} from "../../Components/Utils/Utils";
const CreateChild = ({ setShow, editData, GetData ,states,levels}) => {
  const [inputData, setinputData] = useState({
    first_name:"",
    last_name:"",
    address:"",
    age:"",
    state_id:"",
    post_code:"",
    start_date:"",
    school_year:"",
    level_id:""
 
   
   
  });
  const [selected,setSelected]=useState(null)
  const [loader, setLoader] = useState(false);
  useEffect(() => {


    editData && setinputData({...editData,
    start_date:dayjs(editData.start_date).format('YYYY-MM-DD')})
  }, []);
  const handleAdd = async (e) => {
  
    
    if(Validations.isEmpty(inputData.first_name)||Validations.isEmpty(inputData.last_name)||Validations.isEmpty(inputData.post_code)||Validations.isEmpty(inputData.state)||Validations.isEmpty(inputData.address)||Validations.isEmpty(inputData.age)||Validations.isEmpty(inputData.start_date)||Validations.isEmpty(inputData.level_id)){
      toast.error("Fields can't be empty")
  }
  
    else {
      try {
        setLoader(true);
        let response =   editData?
        await  TotalServices.EditChild(editData.id,inputData)
         :
         await TotalServices.AddChild(inputData)

         


        if (response.status === 200) {
          // console.log(response);
          toast.success(response.data.message);
          setLoader(false);
          GetData();
          setShow(false);
        }
      } catch (e) {
        console.log(e);
        setLoader(false);
      }
    }
  };
  const handleChange= (e) =>{
setinputData((prev)=>(
  {
    ...prev,
   [e.target.name]:e.target.value
  }
))
  }
  return (
    <div className="fixed top-0 left-0 right-0 z-50  w-full p-4 overflow-x-hidden overflow-y-auto md:inset-0 h-[calc(100%-1rem)] md:h-full bg-[#fffb] ">
      <div className="relative w-full h-full max-w-2xl md:h-auto mx-auto ">
        <div
          className="relative rounded-lg shadow-xl 
       "
        >
          <div className="flex items-start justify-between p-4  -t ">
            <h3 className="text-xl   ">
              {editData ? "Edit Child" : "Add Child"}
            </h3>
            <button
              type="button"
              className="  bg-btn-primary text-white -lg text-sm p-1.5 ml-auto inline-flex items-center "
              onClick={(e) => setShow(false)}
            >
              <svg
                aria-hidden="true"
                className="w-5 h-5"
                fill="currentColor"
                viewBox="0 0 20 20"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  fillRule="evenodd"
                  d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                  clipRule="evenodd"
                ></path>
              </svg>
              <span className="sr-only">Close modal</span>
            </button>
          </div>
          <div className="mx-auto bg-white px-4 py-6 relative rounded-lg">
        
              

           

              

                <form className="grid "
              
                >
                 <div className="grid grid-cols-2 gap-2"
                
                 >

                
                        <Input
                       
                        name={"first_name"}
                      
                        placeholder={"First Name"}
                        handleChange={handleChange}
                        value={inputData.first_name}
                      
                        type={"text"}

                        />
                        <Input
                       
                        name={"last_name"}
                        
                        placeholder={"Last Name"}
                        handleChange={handleChange}
                        value={inputData.last_name}
                      
                        type={"text"}

                        />
                 
                        <Input
                       
                        name={"age"}
                     
                        placeholder={"Age"}
                        handleChange={handleChange}
                        value={inputData.age}
                      
                        type={"number"}

                        />
                       
                         <SelectInput
                       
                       name={"level_id"}
                     
                       placeholder={"School Year"}
                       handleChange={handleChange}
                       value={inputData.level_id}
                       data={levels}
                     
                       type={"text"}

                       />
                    

                     
                        <SelectInput
                       
                       name={"state_id"}
                     
                       placeholder={"Select State"}
                       handleChange={handleChange}
                       value={inputData.state_id}
                       data={states}
                     
                       type={"text"}

                       />
                       
                          <Input
                       
                       name={"post_code"}
                     
                       placeholder={"Postcode"}
                       handleChange={handleChange}
                       value={inputData.post_code}
               
                       type={"text"}

                       
                       />
                         </div>
               
                         <Input
                       
                        name={"address"}
                      
                        placeholder={"Address"}
                        handleChange={handleChange}
                        value={inputData.address}
                      
                        type={"text"}

                        />
                       <Input
                       labelColor={"text-black"}
                       label={"Select Start Date"}
                       name={"start_date"}
                     
                       placeholder={"Start Date"}
                       handleChange={handleChange}
                       value={inputData.start_date}
                     
                       type={"date"}

                       />
              

              

                   
             
                  
                </form>
                <div className="flex justify-end">

               
                <div className=" mt-3 flex">
  <div>


  {loader?
  <ButtonLoader />:
  <Button text={editData ? "Save Child" : "Add Child"} handleClick={handleAdd} color={"bg-green-500"} />}
    </div>
</div>

</div>
            </div>
        </div>
      </div>
    </div>
  );
};

export default CreateChild;
