// ThankYou.js
import React, { useEffect } from 'react';
import Thanks from "../../assets/logo.png"
import Button from '../../Components/Button/Button';
import { useNavigate } from 'react-router-dom';

const ThankYou = () => {
    const navigate=useNavigate()
    useEffect(()=>{
      document.title="Home Schooling - Thank You"
            },[])
  return (
    <div className="max-w-2xl mx-auto flex items-center justify-center min-h-screen">
       
    <div className="w-full p-2 bg-white rounded shadow-md border-2 border-gray-200">
    <div className="text-center">
        <img
          src={Thanks}
          alt="Checkmark Icon"
          className="mx-auto w-28"
        />
      </div>
      <div className='p-3'>

  
      <h2 className="text-6xl text-center text-green-600 mb-4 font-bold">Thank You!</h2>
      <p className="text-gray-700 mb-6">
        Your signup and payment were successful. We appreciate your business!
      </p>
    
  
      <p className="text-gray-700 mt-6">
        If you have any questions, feel free to contact us.
      </p>
  
      <div className="mt-8 flex justify-center">
        <div>
        <Button text={"Login"} handleClick={e=>navigate("/")}/>
        </div>
       
       
        </div>
     
       
      </div>
    </div>
  </div>
  
  );
};

export default ThankYou;
