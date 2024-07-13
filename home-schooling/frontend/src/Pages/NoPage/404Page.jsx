import React, { useEffect } from 'react';
import Button from '../../Components/Button/Button';
import { useNavigate } from 'react-router-dom';

const NotFound = () => {
    useEffect(()=>{
        document.title="Home Schooling - 404"
              },[])
    const navigate=useNavigate()
  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
    <div className="text-center p-20 rounded-lg shadow-lg bg-white ">
      <h1 className="text-5xl font-bold text-gray-800 mb-4">404 Not Found</h1>
      <p className="text-xl text-gray-600 mb-6">
        It seems like you've taken a wrong turn!
      </p>
      <div className='flex justify-center'>

    
      <div>
      <Button
        text="Home Page"
        handleClick={(e) => navigate("/")}
        className="bg-blue-500 text-white px-6 py-3 rounded-full hover:bg-blue-600 transition duration-300"
      />
      </div>
      </div>
   
      <p className="text-sm text-gray-500 mt-4">
        If you think this is a mistake, please contact support.
      </p>
    </div>
  </div>
  
  );
};

export default NotFound;
