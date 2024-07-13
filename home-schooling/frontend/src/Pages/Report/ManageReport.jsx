import { useContext, useEffect, useState } from "react";
import Search from "../../Components/Search/Search"
import Loader from "../../Components/Loader/Loader";
import ChildTable from "./ReportTable";
import PaginationButtons from "../../Components/Pagination/PaginationButtons"
import NoDataFound from "../../Components/NoDataFound/NoDataFound"
import TotalServices from "../../TotalServices";
import Button from "../../Components/Button/Button";
import CreateReport from "./CreateReport";
import ReportTable from "./ReportTable";


const ManageReport = () => {
    const [totalRecords, setTotalRecords] = useState("");
  const [record, setRecord] = useState(0);
  const [NumberOfRecordsPerPage] = useState(5);
  const [currentPage, setCurrentPage] = useState(1);
  const [goto, setGoto] = useState("");
  const [totalPages, setTotalPages] = useState(1);
    const [searchQuery, setSearchQuery] = useState("");
    const [tableData,setTableData]=useState([])
    const [loader,setLoader]=useState(false)
    const [show,setShow]=useState(false)

  
    const GetData = async () => {
   
      try {
        setLoader(true);
        let response = await TotalServices.ListReport(
          NumberOfRecordsPerPage,
          (currentPage - 1) * NumberOfRecordsPerPage,
          searchQuery
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
    };
  useEffect(()=>{
    document.title="Home Schooling - Manage Report"
  },[])
  useEffect(() => {
    GetData();
 
  }, [currentPage]);

  return (
    <div className={`p-4 sm:ml-64 sm:mt-24 bg-gray-200 rounded-tl-xl min-h-screen`}>
 <div className="lg:flex justify-between my-2">
  <div className="flex my-2">
  <Button text={"Create Report"} handleClick={e=>setShow(true)} />
  </div>
     
    
        <Search   setSearchQuery={setSearchQuery} searchQuery={searchQuery} currentPage={currentPage} setCurrentPage={setCurrentPage} GetData={GetData} placeholder="Search Report" />
      </div>
   
     
      {
     loader?
    <Loader />
   :
   tableData.length>=1?
     <div>
      <ReportTable tableData={tableData}  GetData={GetData}  />
    {totalRecords> NumberOfRecordsPerPage && <PaginationButtons
                    totalRecords={totalRecords}
                    setRecord={setRecord}
                    record={record}
                    NumberOfRecordsPerPage={NumberOfRecordsPerPage}
                    setCurrentPage={setCurrentPage}
                    currentPage={currentPage}
                    setGoto={setGoto}
                    goto={goto}
                    totalPages={totalPages}
                />}
                </div>
                :
                <NoDataFound  text={"No Report found"}/>

                }
            {show && <CreateReport setShow={setShow}  GetData={GetData}/>}    
    </div>

  );
};

export default ManageReport;
