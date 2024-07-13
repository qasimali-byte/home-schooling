import React, { useEffect, useRef, useState } from 'react';

const Tooltip = ({ text, children,classes }) => {
  const [showTooltip, setShowTooltip] = useState(false);
  const tooltipRef = useRef(null);
  const toggleTooltipIn = () => {
    setShowTooltip(true);
  };
  const toggleTooltipOut = () => {
    setShowTooltip(false);
  };
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (tooltipRef.current && !tooltipRef.current.contains(event.target)) {
        setShowTooltip(false);
      }
    };

    document.addEventListener('click', handleClickOutside);

    return () => {
      document.removeEventListener('click', handleClickOutside);
    };
  }, []);
  return (
    <div className={`relative inline-block ${classes?classes:""}`} ref={tooltipRef}>
      <div onMouseEnter={toggleTooltipIn} 
      onMouseLeave={toggleTooltipOut}
      >
        {children}
      </div>
      {showTooltip && (
        <div className="absolute left-0 bottom-full z-10 mb-3">
        <div className="bg-gray-800 text-white p-2 rounded ">
          {text}
        </div>
        <div className="absolute w-4 h-4 bg-gray-800 transform rotate-45 bottom-0 left-1/2 -translate-x-2 -mb-1"></div>
      </div>
        
      )}
      
    </div>
  );
};

export default Tooltip;