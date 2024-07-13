const  SelectInput = ({placeholder,name,handleChange,value,type,disabled,label,data}) => {

    return ( 
   <div className="my-1">

 {label && <label className="font-semibold text-sm" >{label}</label>}
<div className={`flex bg-white justify-between items-center mt-2  border rounded-lg px-5 py-3` } >


        <select
     className="border-0 outline-none w-full"
        placeholder={placeholder} 
        type={type}
        name={name}
        value={value}
        disabled={disabled}
        onChange={handleChange}
        >
 <option value="">{placeholder}</option>
{data?.map(val=>(<option value={val.id}>{val.name}</option>))
}
        </select>
         
        </div>
 
           </div>
  
     );
}
 
export default  SelectInput;