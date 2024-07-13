import { useEffect, useState } from "react";
import TotalServices from "../../../TotalServices";
import { useLocation } from "react-router-dom";
import Accordion from "../Accordion";
import Loader from "../../../Components/Loader/Loader";
import PaginationButtons from "../../../Components/Pagination/PaginationButtons";
import NoDataFound from "../../../Components/NoDataFound/NoDataFound";
import TermAccordion from "./TermAccordion";
import CreateActivity from "../CreateActivity";
import Confirmation from "../../../Components/Confirmation/Confirmation";
import { toast } from "react-toastify";

const TermActivities = ({
  subject,
  termId,
  subjectData,
  termData,
  report_id,
}) => {
  const { state } = useLocation();
  const [searchQuery, setSearchQuery] = useState("");
  const [loader, setLoader] = useState(true);
  const [totalRecords, setTotalRecords] = useState("");
  const [record, setRecord] = useState(0);
  const [NumberOfRecordsPerPage] = useState(5);
  const [currentPage, setCurrentPage] = useState(1);
  const [goto, setGoto] = useState("");
  const [totalPages, setTotalPages] = useState(1);
  const [tableData, setTableData] = useState([]);
  const [show, setShow] = useState(false);
  const [editData, setEditData] = useState(null);
  const [showDelete, setShowDelete] = useState(false);
  const [deleteId, setDeleteId] = useState(null);
  const [dateData, setDateData] = useState(null);
  const handleEdit = (val) => {
    setDateData(null);
    setEditData({ ...val, ...subject });
    setShow(true);
  };
  const handleDelete = (id) => {
    setDeleteId(id);
    setShowDelete(true);
  };
  const DeleteData = async (check) => {
    if (!check) {
      setShowDelete(false);
    } else {
      try {
        // setLoader(true)

        const response = await TotalServices.DeleteActivities(deleteId);

        if (response.status === 200) {
          // console.log(response)
          toast.success(response.data.message);
          // setLoader(false)
          setShowDelete(false);
          GetData();
        }
      } catch (error) {
        console.log("error ", error);
        setShowDelete(false);
        // setLoader(false)
      }
    }
  };
  const handleSendDates = (item) => {
    setEditData(null);
    setDateData(item.subjects[0].activities[0]);
    setShow(true);
  };
  const GetReportData = async () => {
    if (state.id) {
      try {
        setLoader(true);
        let response = await TotalServices.ListActivities(
          NumberOfRecordsPerPage,
          (currentPage - 1) * NumberOfRecordsPerPage,
          searchQuery,
          state.id,
          termId === null ? "" : termId,
          state.data.follow_term,
          subject.sub_strand_code_id
        );
        if (response.status === 200) {
          //  console.log(response);
          setTableData(response?.data.data);
          setTotalPages(response?.data?.pages);
          setTotalRecords(response?.data?.total_records);
          setRecord((currentPage - 1) * NumberOfRecordsPerPage);
          setGoto("");

          setLoader(false);
        }
      } catch (e) {
        console.log(e);
        setLoader(false);
      }
    } else {
      navigate("/manage-report");
    }
  };
  useEffect(() => {
    GetReportData();
  }, [currentPage]);
  return (
    <div className="p-6 my-2 bg-white rounded-lg shadow-md">
      <div className="">
        <p className="text-xl font-bold text-gray-600">{subject.name}</p>

        <p className="font-bold text-gray-600 text-md">
          <span className="mr-3">{subject.strand_name}</span>
          <span className="mr-3">|</span>
          <span>{subject.sub_strand_name}</span>
        </p>
        <p className="text-sm text-gray-600">{subject.code}</p>
        <p className="text-gray-700">{subject.description}</p>
        {loader ? (
          <Loader />
        ) : tableData.length >= 1 ? (
          <>
            {tableData?.map((val) => (
              <TermAccordion
                val={val}
                handleEdit={handleEdit}
                handleDelete={handleDelete}
              />
            ))}
            {totalPages > 1 && (
              <div className="flex justify-end">
                {" "}
                <PaginationButtons
                  totalRecords={totalRecords}
                  setRecord={setRecord}
                  record={record}
                  NumberOfRecordsPerPage={NumberOfRecordsPerPage}
                  setCurrentPage={setCurrentPage}
                  currentPage={currentPage}
                  setGoto={setGoto}
                  goto={goto}
                  totalPages={totalPages}
                />
              </div>
            )}
          </>
        ) : (
          <NoDataFound text={"No Activity found"} />
        )}
      </div>
      {show && (
        <CreateActivity
          dateData={dateData}
          report_id={report_id}
          termData={termData}
          subjectData={subjectData}
          editData={editData}
          setShow={setShow}
          GetData={GetReportData}
        />
      )}
      {showDelete && (
        <Confirmation
          setShowConfirmation={DeleteData}
          message="Are you sure you want to delete this Activity?"
        />
      )}
    </div>
  );
};

export default TermActivities;
