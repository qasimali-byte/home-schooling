const  Input = ({placeholder,name,handleChange,value,type,disabled,handleFocus,handleBlur,classes,label,icon,labelColor}) => {
   
    return ( 
   <div className="my-1">

 {label && <label className={`font-semibold text-sm ${labelColor?labelColor: "text-white"}`} >{label}</label>}

<div className={`flex bg-white border rounded-lg justify-between items-center mt-2  px-5 py-3` } >


        <input
     className="border-0 outline-none w-full disabled:text-gray-400"
        placeholder={placeholder} 
        type={type}
        name={name}
   onFocus={handleFocus}
   onBlur={handleBlur}
        value={value}
        disabled={disabled}
        onChange={handleChange}
        />
          {icon &&<span>
    {icon}
   </span>}
        </div>
        <p className="text-red-500 text-sm break-norma max-w-sm" id={name}></p>
      
  
 
           </div>
  
     );
}
 
export default  Input;