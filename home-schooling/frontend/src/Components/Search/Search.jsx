import { useEffect, useState } from "react";
import { AiOutlineSearch } from "react-icons/ai";

const Search = ({setSearchQuery,searchQuery,currentPage,setCurrentPage,GetData,placeholder,newClass,type}) => {
  const [focus,setFocus]=useState(false)
useEffect(()=>{
  searchQuery==="" && focus && GetData() ;
},[searchQuery])
    return ( 
      
         <form   onSubmit={(e) => {
          e.preventDefault()
        
      currentPage!==1?setCurrentPage(1):GetData()
          }}>
        <div className="flex items-center justify-between bg-gray-100 border-gray-100 border   sm:text-md md:mx-2 ">
       
        <input className="2xl:w-96 lg:w-96 w-full text-black  outline-none border-none p-3   mx-2 "  
        placeholder={placeholder?placeholder:"Search"} 
        type={"search"}
        onFocus={e=>setFocus(true)}
        value={searchQuery}
        onChange={(e) => {
          setSearchQuery(e.target.value);
        }}
        />
        <button
    className=" -full px-4 text-color-secondary   py-2    focus:outline-none    "
   role="button"
  >
  
<AiOutlineSearch size={25} />

  </button>
        </div>
        </form>      
 
     );
}
 
export default Search;