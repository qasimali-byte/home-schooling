import { useContext, useEffect, useState } from "react";
import Search from "../../Components/Search/Search"
import Loader from "../../Components/Loader/Loader";
import ChildTable from "./ChildTable";
import PaginationButtons from "../../Components/Pagination/PaginationButtons"
import NoDataFound from "../../Components/NoDataFound/NoDataFound"
import TotalServices from "../../TotalServices";
import Button from "../../Components/Button/Button";
import CreateChild from "./CreateChild";
import GetStates,{GetLevels} from "../../Components/Functions/UtilsFunctions";


const ManageChild = () => {
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
    const [states,setStates]=useState([])
    const [levels,setLevels]=useState([])

  
    const GetData = async () => {
   
      try {
        setLoader(true);
        let response = await TotalServices.ListChild(
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
    const GetStatesData=async()=>{
      let data=await GetStates()
    
       setStates(data)
     }
     const GetLevelData=async()=>{
      let data=await GetLevels()
       setLevels(data.map(val=>({name:val.label,id:val.value})))
     }
  useEffect(() => {
    GetData();
 
  }, [currentPage]);
  useEffect(()=>{
    GetLevelData()
  },[])
  useEffect(()=>{
    GetStatesData()
    document.title="Home Schooling - Manage Child"
  
          },[])
  return (
    <div className={`p-4 sm:ml-64 sm:mt-24 bg-gray-200 h-dvh rounded-tl-3xl min-h-[90vh]`}>
 <div className="lg:flex justify-between my-2">
  <div className="flex">
  <Button text={"Add Child"} handleClick={e=>setShow(true)} />
  </div>
     
    
        <Search   setSearchQuery={setSearchQuery} searchQuery={searchQuery} currentPage={currentPage} setCurrentPage={setCurrentPage} GetData={GetData} placeholder="Search Children" />
      </div>
   
     
      {
     loader?
     
    <Loader />
   :
   tableData.length>=1?
     <div>
      <ChildTable tableData={tableData}  GetData={GetData} states={states} levels={levels}  />
    {totalRecords>NumberOfRecordsPerPage&&   <PaginationButtons
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
                <NoDataFound  text={"No Child found"}/>

                }
                {show && <CreateChild setShow={setShow} GetData={GetData} states={states} levels={levels} />}
    </div>
  );
};

export default ManageChild;
