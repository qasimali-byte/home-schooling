import { useEffect, useState } from "react";
import Button from "../../Components/Button/Button";
import CreateActivity from "./CreateActivity";
import TotalServices from "../../TotalServices";
import { useLocation, useNavigate } from "react-router-dom";
import Loader from "../../Components/Loader/Loader";
import PaginationButtons from "../../Components/Pagination/PaginationButtons";
import NoDataFound from "../../Components/NoDataFound/NoDataFound";
import ActivitySelect from "../../Components/Input/ActivitySelect";
import ButtonLoader from "../../Components/Loader/ButtonLoader";
import NoTermReportData from "./NonTermReportData/NoTermReportData";
import TermReportData from "./TermReportData/TermReportData";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import { GetLearningAreas } from "../../Components/Functions/UtilsFunctions";

const GenerateReport = () => {
  const [show, setShow] = useState(false);
  const [loader, setLoader] = useState(true);
  const [totalRecords, setTotalRecords] = useState("");
  const [record, setRecord] = useState(0);
  const [NumberOfRecordsPerPage] = useState(5);
  const [currentPage, setCurrentPage] = useState(1);
  const [goto, setGoto] = useState("");
  const [totalPages, setTotalPages] = useState(1);
  const [searchQuery, setSearchQuery] = useState("");
  const [tableData, setTableData] = useState([]);
  const [termData, setTermData] = useState([]);
  const [termId, setTermId] = useState(null);
  const { state } = useLocation();
  const [activeTab, setActiveTab] = useState("");
  const [downloadLoader, setDownloadLoader] = useState(false);
  const [subjectList, setSubjectList] = useState([]);
  const [learningAreas, setLearningAreas] = useState([]);
  const navigate = useNavigate();
  const GetLearningAreasData = async () => {
    let data = await GetLearningAreas(state.data.level_id);
    setLearningAreas(data);
  };

  const GetTermReportData = async () => {
    if (state.id) {
      try {
        setLoader(true);
        let response = await TotalServices.ListTermSubjects(
          NumberOfRecordsPerPage,
          (currentPage - 1) * NumberOfRecordsPerPage,
          state.id,
          termId === null ? "" : termId
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

  const GetTermData = async () => {
    try {
      let response = await TotalServices.getTermData({ report_id: state.id });
      if (response.status === 200) {
        //  console.log(response);
        setTermData(response.data.data.date_ranges);
      }
    } catch (e) {
      console.log(e);
    }
  };
  const handleDownload = async () => {
    try {
      setDownloadLoader(true);
      let response = await TotalServices.DownloadActivity(
        state.id,
        state.data.follow_term
      );
      if (response.status === 200) {
        setDownloadLoader(false);

        window.open(response.data.report_url);
      }
    } catch (e) {
      console.log(e);
      setDownloadLoader(false);
    }
  };
  useEffect(() => {
    // state.data.follow_term!==0?  GetReportData():null
    GetTermData();
  }, []);
  const GetReportSubjects = async () => {
    if (state.id) {
      try {
        setLoader(true);
        let response = await TotalServices.ListSubjects(state.id);
        if (response.status === 200) {
          // console.log(object);
          setSubjectList(response?.data.data);
          activeTab?.subject_name
            ? GetStrandData()
            : setActiveTab(response?.data?.data[0]);

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
  const GetStrandData = async () => {
    try {
      setLoader(true);
      let response = await TotalServices.ListStrands(
        NumberOfRecordsPerPage,
        (currentPage - 1) * NumberOfRecordsPerPage,
        state.id,
        activeTab.subject_id,
        termId === null ? "" : termId,
        state.data.follow_term
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
  useEffect(() => {
    state.data.follow_term === 0 && GetReportSubjects();
  }, []);
  useEffect(() => {
    state?.id !== undefined
      ? state.data.follow_term === 1
        ? GetTermReportData()
        : activeTab && activeTab !== "" && GetStrandData()
      : navigate("/manage-report");
  }, [currentPage]);
  useEffect(() => {
    currentPage !== 1
      ? setCurrentPage(1)
      : termId !== null
      ? GetTermReportData()
      : activeTab && activeTab !== "" && GetStrandData();
  }, [termId, activeTab]);

  useEffect(() => {
    GetLearningAreasData();
  }, []);
  var settings = {
    rows: 1,
    slidesToShow: 9,
    speed: 500,
    infinite: false,
    initialSlide: 0,
    slidesToScroll: 1,
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 6,
          slidesToScroll: 1,
          infinite: true,
        },
      },
      {
        breakpoint: 600,
        settings: {
          slidesToShow: 4,
          slidesToScroll: 1,
          initialSlide: 0,
        },
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 3,
          slidesToScroll: 1,
        },
      },
    ],
  };
  return (
    <div className="min-h-screen p-4 bg-gray-200 sm:ml-64 sm:mt-24 rounded-tl-xl">
      <div className="flex justify-between">
        <h1 className="mb-3 text-3xl text-primary">{state?.data.name}</h1>
        <div className="flex items-center">
          {state.data.follow_term !== 0 && (
            <div className="flex items-center justify-between mx-3">
              <label className="mx-3" htmlFor="">
                Filter by term:
              </label>
              <ActivitySelect
                name={"states_has_terms_id"}
                data={termData}
                optionLabel={"term_name"}
                valueLabel={"term_id"}
                placeholder={"All Terms"}
                handleChange={(e) => setTermId(e.target.value)}
                value={termId}
              />
            </div>
          )}

          <div>
            <Button text={"Add Activity"} handleClick={(e) => setShow(true)} />
          </div>
          <div className="mx-3">
            {downloadLoader ? (
              <ButtonLoader />
            ) : (
              <Button text={"Export Report"} handleClick={handleDownload} />
            )}
          </div>
        </div>
      </div>
      <div className="pb-2 border-b border-black">
        <h1 className="text-4xl font-bold text-gray-800">
          {state?.data.child_name}
        </h1>

        <div className="flex mt-2 text-gray-700">
          <p className="text-sm italic">
            <span> {state?.data.state_name}</span>,{" "}
            <span>{state?.data.school_year}</span>
          </p>
        </div>
      </div>
      {/* <div className="flex justify-center mb-10 border-b border-gray-200">
    <ul className="flex flex-wrap -mb-px text-sm font-medium text-center text-gray-500 "> */}
      <div className="justify-center ">
        {subjectList.length >= 1 && (
          <div className="px-10 m-auto ">
            <Slider className="mx-auto" {...settings}>
              {subjectList.map((val) => (
                <div className="flex justify-center w-96">
                  <div className="flex justify-center ">
                    <button
                      onClick={() => setActiveTab(val)}
                      className={` items-center justify-center p-4  rounded-t-lg   group ${
                        activeTab?.subject_name === val.subject_name
                          ? "text-primary border-b-2  border-primary"
                          : "border-b-2  hover:text-gray-600 hover:border-gray-300"
                      }`}
                    >
                      {val.subject_name}
                    </button>
                  </div>
                </div>
              ))}
            </Slider>
          </div>
        )}
      </div>
      {loader ? (
        <Loader />
      ) : tableData.length >= 1 ? (
        <div>
          <NoTermReportData
            followTerm={state.data.follow_term}
            tableData={tableData}
            GetData={
              state.data.follow_term === 0
                ? GetReportSubjects
                : GetTermReportData
            }
            termData={termData}
            termId={termId}
            report_id={state.id}
            subId={activeTab.subject_id}
            learningAreas={learningAreas}
          />
          {/* </>
     :
     <TermReportData tableData={tableData} termId={termId} followTerm={state.data.follow_term}  termData={termData} report_id={state.id}/>
     }  */}
          {totalPages > NumberOfRecordsPerPage && (
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
          )}
        </div>
      ) : (
        <NoDataFound text={"No Activity found"} />
      )}
      {show && (
        <CreateActivity
          followTerm={state.data.follow_term}
          termData={termData}
          setShow={setShow}
          GetData={
            state?.data.follow_term === 0
              ? GetReportSubjects
              : GetTermReportData
          }
          report_id={state.id}
          learningAreas={learningAreas}
        />
      )}
    </div>
  );
};

export default GenerateReport;
