import React, { useState } from "react";
import { GoDotFill } from "react-icons/go";
import { GrAddCircle } from "react-icons/gr";
import { MdOutlineCancel } from "react-icons/md";

const Button = ({ text, handleClick, classes, disabled, color, canHover }) => {
  const [hover, setHover] = useState(false);

  return (
    <button
      className={`w-full  text-white font-bold py-3 px-4  rounded-full  disabled:opacity-70   ${
        color ? color : "bg-btn-primary"
      } `}
      onClick={handleClick}
      disabled={disabled}
    >
      {text}
    </button>
  );
};

export default Button;
