import React, { useState } from "react";
import "./paginationButton.css";
import "react-confirm-alert/src/react-confirm-alert.css";

const SelectView = ({ filterSelected, setFilterSelected }) => {
  return (
    <>
      <div className="">
        <select
          className="form-select form-select mt-2 mr-3"
          style={{
            padding: "5px",
            border: "2px solid rgb(117 4 30)",
            borderRadius: "8px",
          }}
          aria-label=".form-select-lg example"
          value={filterSelected}
          onChange={(e) => {
            setFilterSelected(e.target.value);
          }}
        >
          {/* <option value={"Select View"}>Select</option> */}
          <option value={5}>5</option>
          <option value={25}>25</option>
          <option value={50}>50</option>
          <option value={100}>100</option>
        </select>
      </div>
    </>
  );
};
export default SelectView;
