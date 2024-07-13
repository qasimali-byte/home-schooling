import { useState } from "react";
import ActionButtons from "../../Components/Actions/ActionButtons";
import ImageViewer from "./ImageViewer";
import Validations from "../../Regex";
import Utils from "../../Components/Utils/Utils";

const Accordion = ({ val, handleDelete, handleEdit }) => {
  const [toggle, setToggle] = useState(false);
  return (
    <div className="mb-2 border rounded">
      <div
        className="flex items-center justify-between p-4 cursor-pointer"
        onClick={() => setToggle(!toggle)}
      >
        <div className="flex justify-between w-full mr-4">
          {val.term_id && (
            <p className="font-semibold text-gray-800">Term {val.term_id}</p>
          )}
          <p className="font-semibold text-gray-800">
            Activity Start Date{" "}
            <span className="ml-1 text-gray-500">
              {Utils.dateFormat(
                val.act_start_date,
                "DD-MM-YYYY",
                "DD MMMM YYYY"
              )}
            </span>
            {val.act_end_date !== null ? (
              <>
                {" "}
                - Activity End Date{" "}
                <span className="ml-1 text-gray-500">
                  {Utils.dateFormat(
                    val.act_end_date,
                    "DD-MM-YYYY",
                    "DD MMMM YYYY"
                  )}
                </span>{" "}
              </>
            ) : (
              ""
            )}
          </p>
        </div>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className={`h-6 w-6 ${toggle ? "transform rotate-180" : ""}`}
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </div>
      {toggle && (
        <div className="p-4 bg-gray-200 rounded-lg shadow-lg">
          <div className="flex justify-between">
            {val.inserted_date === val.last_updated_date
              ? val.inserted_date !== null && (
                  <p className="text-green-500">
                    <span className="mx-2 font-semibold">Created at:</span>
                    <span className="italic">
                      {val.inserted_date.substring(0, 16)}
                    </span>
                  </p>
                )
              : val.last_updated_date !== null && (
                  <p className="text-blue-500">
                    <span className="mx-2 font-semibold">Last updated:</span>
                    <span className="italic">
                      {val.last_updated_date.substring(0, 16)}
                    </span>
                  </p>
                )}
          </div>

          <div className="mt-4">
            <p className="text-lg font-bold text-gray-700">Description</p>
            <p className="p-4 mt-2 text-gray-800 bg-gray-100 rounded-lg">
              {val.json_subject_data.ContentDesc}
            </p>
          </div>

          {val.json_subject_data.Elaboration && (
            <div className="mt-4">
              <p className="text-lg font-bold text-gray-700">Elaboration</p>
              <p className="p-4 mt-2 text-gray-800 bg-gray-100 rounded-lg">
                {val.json_subject_data.Elaboration}
              </p>
            </div>
          )}

          <div>
            {val?.json_subject_data?.GCC && (
              <div className="mt-4">
                <p className="text-lg font-bold text-gray-700">
                  {" "}
                  General Capabilities
                </p>

                <p className="p-4 mt-2 text-gray-800 bg-gray-100 rounded-lg ">
                  General Capabilities are {val.json_subject_data.GCC}{" "}
                  {val.json_subject_data.Element &&
                    ", " + val.json_subject_data.Element}{" "}
                  {val?.json_subject_data.SubElement &&
                    " and " + val.json_subject_data.SubElement}
                  .
                </p>
              </div>
            )}
          </div>

          <div className="flex justify-between mt-4">
            {val.created_date !== null && (
              <p className="text-yellow-500">
                <span className="mx-2 font-semibold">Activity Done:</span>
                <span className="italic">
                  {val.created_date.substring(0, 16)}
                </span>
              </p>
            )}
          </div>

          <div className="mt-4">
            <p className="text-lg font-bold text-gray-700">Activity</p>
            <div className="flex items-start justify-between mb-3">
              <p className="w-full p-4 text-gray-800 whitespace-pre-wrap bg-gray-100 rounded-lg">
                {val.activity_description}
              </p>
              <div className="flex items-center">
                <ActionButtons
                  handleDeleteClick={(e) => handleDelete(val.activity_id)}
                  handleEditClick={(e) => handleEdit(val)}
                  editMessage={"Edit Activity"}
                  deleteMessage={"Delete Activity"}
                />
              </div>
              {val.attached_files_names !== null &&
                val.attached_files_names.filter((val, index) =>
                  Validations.isImage(val)
                ).length >= 1 && (
                  <div className="flex items-center">
                    <ImageViewer
                      fileNames={val.attached_files_names}
                      fileUrls={val?.attached_files_urls}
                    />
                  </div>
                )}
            </div>

            {val.attached_files_names !== null && (
              <div className="mt-4">
                <p className="text-lg font-bold text-gray-700">Files</p>
                <div className="p-4 text-gray-800 bg-gray-100 rounded-lg">
                  {val.attached_files_names.map((file, index) => (
                    <a
                      key={index}
                      className="block mt-2 hover:text-blue-500 hover:underline"
                      target="_blank"
                      href={val?.attached_files_urls[index]}
                    >
                      {file}
                    </a>
                  ))}
                </div>
              </div>
            )}

            {val.attached_links !== null && val.attached_links !== "" && (
              <div className="mt-4">
                <p className="text-lg font-bold text-gray-700">Urls</p>
                <div className="p-4 text-gray-800 bg-gray-100 rounded-lg">
                  {val.attached_links.split(",").map((link, index) => (
                    <a
                      key={index}
                      className="block mt-2 break-words  hover:text-blue-500 hover:underline"
                      target="_blank"
                      href={link}
                    >
                      {link}
                    </a>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default Accordion;
