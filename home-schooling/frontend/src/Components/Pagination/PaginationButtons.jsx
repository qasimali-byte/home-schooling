import React, { useState } from "react";
import "./paginationButton.css";
// import { confirmAlert } from "react-confirm-alert";
import {
  FaAngleRight,
  FaAngleLeft,
  FaAngleDoubleLeft,
  FaAngleDoubleRight,
} from "react-icons/fa";
const PaginationButtons = (props) => {
  const DarkMode = false;

  var numbers = 0;
  var page = -props.NumberOfRecordsPerPage;
  var onlyNumbers = /^\d+$/;
  var ValidatedString = props.goto.match(onlyNumbers);

  const maxNo = () => {
    var num = 0;
    for (var i = 1; i <= 5; i++) {
      if ((props.totalRecords - i) % 5 === 0) num = props.totalRecords - i;
    }

    props.setCurrentPage(props.totalPages);
    props.setRecord((props.totalPages - 1) * props.NumberOfRecordsPerPage);
  };

  return (
    <>
      <div className="main-pagination">
        <button
          className="p-3 mx-1 text-white btn-hover3 -md bg-primary"
          disabled={props.record - props.NumberOfRecordsPerPage < 0}
          onClick={() => {
            props.setRecord(0);
            props.setCurrentPage(1);
          }}
        >
          <FaAngleDoubleLeft />
        </button>
        <button
          className="p-3 mx-1 text-white btn-hover3 -md bg-primary"
          disabled={props.record - props.NumberOfRecordsPerPage < 0}
          onClick={() => {
            props.setRecord(props.record - props.NumberOfRecordsPerPage);
            props.setCurrentPage(props.currentPage - 1);
          }}
        >
          <FaAngleLeft />
        </button>

        {[...Array(props.totalPages)].map(
          (i) => (
            (page = page + props.NumberOfRecordsPerPage),
            (numbers = numbers + 1),
            numbers === props.currentPage ? (
              <>
                {numbers === props.totalPages && props.totalPages > 2 ? (
                  <button
                    className="p-3 mx-1 text-white btn-hover3 -md bg-primary"
                    value={page - props.NumberOfRecordsPerPage * 2}
                    onClick={(e) => {
                      props.setRecord(parseInt(e.target.value));
                      props.setCurrentPage(parseInt(e.target.innerText));
                    }}
                  >
                    {numbers - 2}
                  </button>
                ) : null}

                {numbers !== 1 ? (
                  <button
                    className="p-3 mx-1 text-white btn-hover3 -md bg-primary"
                    value={page - props.NumberOfRecordsPerPage}
                    onClick={(e) => {
                      props.setRecord(parseInt(e.target.value));
                      props.setCurrentPage(parseInt(e.target.innerText));
                    }}
                  >
                    {numbers - 1}
                  </button>
                ) : null}

                <button
                  className="p-3 mx-1 text-white btn-hover3 -md bg-primary"
                  disabled={props.currentPage === numbers ? true : false}
                  value={page}
                  onClick={(e) => {
                    props.setRecord(parseInt(e.target.value));
                    props.setCurrentPage(parseInt(e.target.innerText));
                  }}
                >
                  {numbers}
                </button>

                {numbers < props.totalPages ? (
                  <button
                    className="p-3 mx-1 text-white btn-hover3 -md bg-primary"
                    disabled={
                      props.record + props.NumberOfRecordsPerPage >
                      props.totalRecords
                    }
                    value={page + props.NumberOfRecordsPerPage}
                    onClick={(e) => {
                      props.setRecord(parseInt(e.target.value));
                      props.setCurrentPage(parseInt(e.target.innerText));
                    }}
                  >
                    {numbers + 1}
                  </button>
                ) : null}

                {numbers === 1 && props.totalPages > 2 ? (
                  <button
                    className="p-3 mx-1 text-white btn-hover3 -md bg-primary"
                    value={page + props.NumberOfRecordsPerPage * 2}
                    onClick={(e) => {
                      props.setRecord(parseInt(e.target.value));
                      props.setCurrentPage(parseInt(e.target.innerText));
                    }}
                  >
                    {numbers + 2}
                  </button>
                ) : null}

                {props.totalPages > 2 &&
                props.currentPage + 2 < props.totalPages ? (
                  <button
                    className="p-3 mx-1 text-white btn-hover3 -md bg-primary"
                    value={page + props.NumberOfRecordsPerPage * 3}
                    onClick={(e) => {
                      props.setRecord(parseInt(e.target.value));
                      props.setCurrentPage(props.currentPage + 3);
                    }}
                  >
                    ...
                  </button>
                ) : null}
              </>
            ) : null
          )
        )}

        <button
          className="p-3 mx-1 text-white btn-hover3 -md bg-primary"
          disabled={
            props.record + props.NumberOfRecordsPerPage >= props.totalRecords
          }
          onClick={() => {
            props.setRecord(props.record + props.NumberOfRecordsPerPage);
            props.setCurrentPage(props.currentPage + 1);
          }}
        >
          <FaAngleRight />
        </button>

        <button
          className="p-3 mx-1 text-white btn-hover3 -md bg-primary"
          disabled={
            props.record + props.NumberOfRecordsPerPage >= props.totalRecords
          }
          onClick={() => {
            maxNo();
          }}
        >
          <FaAngleDoubleRight />
        </button>

        <div className="items-center hidden ml-2 md:flex md:ml-4 ">
          <p className="mb-0 mr-1 text-color-secondary">Go to: </p>
          <form
            onSubmit={(e) => {
              if (!ValidatedString) {
                // confirmAlert({
                //   customUI: ({ onClose }) => {
                //     return (
                //       <div
                //         style={{
                //           borderRadius: "25px",
                //         }}
                //         className="p-5 text-center bg-white shadow "
                //       >
                //         <h1>Oops! Only numbers are allowed.</h1>
                //         <p>Please enter valid page number.</p>
                //         <button
                //           style={
                //             DarkMode === true
                //               ? {
                //                   backgroundColor: "var(--bg-fill5)",
                //                   color: "var(--txtColor2)",
                //                 }
                //               : {
                //                   backgroundColor: "var(--bg-fill6)",
                //                 }
                //           }
                //           className="px-5 py-3 my-3 btn-hover3 -md"
                //           onClick={onClose}
                //         >
                //           Go Back
                //         </button>
                //       </div>
                //     );
                //   },
                // });
              } else if (props.goto === "") {
                // confirmAlert({
                //   customUI: ({ onClose }) => {
                //     return (
                //       <div
                //         style={{
                //           borderRadius: "25px",
                //         }}
                //         className="p-5 text-center bg-white shadow-lg "
                //       >
                //         <h1>Oops! Page Doesn't Exist.</h1>
                //         <p>Please enter valid page number.</p>
                //         <button
                //           style={
                //             DarkMode === true
                //               ? {
                //                   backgroundColor: "var(--bg-fill5)",
                //                   color: "var(--txtColor2)",
                //                 }
                //               : {
                //                   backgroundColor: "var(--bg-fill6)",
                //                 }
                //           }
                //           className="px-5 py-3 my-3 btn-hover3 -md"
                //           onClick={onClose}
                //         >
                //           Go Back
                //         </button>
                //       </div>
                //     );
                //   },
                // });
              } else if (props.goto > props.totalPages || props.goto <= 0) {
                // confirmAlert({
                //   customUI: ({ onClose }) => {
                //     return (
                //       <div
                //         style={{
                //           borderRadius: "25px",
                //         }}
                //         className="p-5 text-center bg-white shadow "
                //       >
                //         <h1>Oops! Page Doesn't Exist.</h1>
                //         <p>Please enter valid page number.</p>
                //         <button
                //           style={
                //             DarkMode === true
                //               ? {
                //                   backgroundColor: "var(--bg-fill5)",
                //                   color: "var(--txtColor2)",
                //                 }
                //               : {
                //                   backgroundColor: "var(--bg-fill6)",
                //                 }
                //           }
                //           className="px-5 py-3 my-3 btn-hover3 -md"
                //           onClick={onClose}
                //         >
                //           Go Back
                //         </button>
                //       </div>
                //     );
                //   },
                // });
              } else if (props.totalPages !== 1) {
                if (parseInt(props.goto) === props.totalPages) {
                  maxNo();
                } else {
                  props.setRecord(
                    props.NumberOfRecordsPerPage * parseInt(props.goto) -
                      props.NumberOfRecordsPerPage
                  );
                  props.setCurrentPage(parseInt(props.goto));
                }
              }

              e.preventDefault();
            }}
          >
            <input
              className="ml-1 mr-1 border shadow-sm"
              style={{
                width: "30pt",
                textAlign: "center",
              }}
              value={props.goto}
              onChange={(e) => props.setGoto(e.target.value)}
            />
          </form>

          <small className="ms-2">
            {props.currentPage} / {props.totalPages}
          </small>
        </div>
      </div>
    </>
  );
};
export default PaginationButtons;
