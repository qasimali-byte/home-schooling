import { useEffect, useState } from "react";
import Validations from "../../Regex";
import { toast } from "react-toastify";
import ButtonLoader from "../../Components/Loader/ButtonLoader";
import { AiOutlineInfoCircle } from "react-icons/ai";
import Input from "../../Components/Input/Input";
import Button from "../../Components/Button/Button";
import TotalServices from "../../TotalServices";
import dayjs from "dayjs";
import SelectInput from "../../Components/Input/SelectInput";
import Loader from "../../Components/Loader/Loader";
const CreateReport = ({ setShow, editData, GetData, settings }) => {
  const [inputData, setInputData] = useState({
    name: "",

    child_id: "",
    follow_term: false,
  });

  const [loader, setLoader] = useState(false);
  const [childInfo, setChildInfo] = useState([]);
  const [child, setChild] = useState(null);
  const [dataLoader, setDataLoader] = useState(true);
  //   useEffect(() => {
  // editData &&console.log(dayjs(editData.start_date).format('YYYY-MM-DD'));

  //     editData && setinputData({...editData,
  //     start_date:dayjs(editData.start_date).format('YYYY-MM-DD')})
  //   }, []);
  const handleAdd = async (e) => {
    e.preventDefault();

    if (
      Validations.isEmpty(inputData.name) ||
      Validations.isEmpty(inputData.child_id)
    ) {
      toast.error("Fields can't be empty");
    } else {
      try {
        setLoader(true);
        let response = editData
          ? await TotalServices.EditChild(editData.id, inputData)
          : await TotalServices.AddReport(inputData);

        console.log(response);

        if (response.status === 200) {
          // console.log(response);
          toast.success(response.data.message);
          setLoader(false);
          GetData();
          setShow(false);
        }
      } catch (e) {
        console.log(e);
        setLoader(false);
      }
    }
  };
  const handleChangeCard = (e) => {
    if (e.target.value === "") {
      setChild(null);
    } else {
      setChild(childInfo.filter((val) => val.id == e.target.value)[0]);
    }

    handleChange(e);
  };
  const handleChange = (e) => {
    setInputData(() => ({
      ...inputData,
      [e.target.name]: e.target.value,
    }));
  };
  const handleCheckbox = (e) => {
    setInputData((prev) => ({
      ...prev,
      [e.target.name]: e.target.checked,
    }));
  };
  const GetChildData = async () => {
    try {
      setDataLoader(true);
      let response = await TotalServices.ListChild(1000, 0, "");
      if (response.status === 200) {
        //  console.log(response);
        setChildInfo(
          response?.data.data.map((val) => ({
            ...val,
            name: val.first_name + " " + val.last_name,
            state: val.name,
          }))
        );
        setDataLoader(false);
      }
    } catch (e) {
      console.log(e);
      setDataLoader(false);
    }
  };
  useEffect(() => {
    GetChildData();
  }, []);
  let states = [
    { name: "New South Wales", id: "New South Wales" },
    { name: "Queensland", id: "Queensland" },
    { name: "South Australia", id: "South Australia" },
    { name: "Tasmania", id: "Tasmania" },
    { name: "Victoria", id: "Victoria" },
    { name: "Western Australia", id: "Western Australia" },
  ];
  let years = [
    { name: "Foundation Year", id: "Foundation Year", states },
    { name: "Year 1", id: "Year 1" },
    { name: "Year 2", id: "Year 2" },
  ];

  return (
    <div className="fixed top-0 left-0 right-0 z-50  w-full p-4 overflow-x-hidden overflow-y-auto md:inset-0 h-[calc(100%-1rem)] md:h-full bg-[#fffb] ">
      <div className="relative w-full h-full max-w-xl mx-auto bg-white rounded-xl md:h-auto ">
        <div className="relative shadow-xl -lg text-color-secondary rounded-xl ">
          <div className="flex items-start justify-between p-4 border-b -t ">
            <h3 className="text-xl ">New Report</h3>
            <button
              type="button"
              className="  bg-btn-primary text-white -lg text-sm p-1.5 ml-auto inline-flex items-center "
              onClick={(e) => setShow(false)}
            >
              <svg
                aria-hidden="true"
                className="w-5 h-5"
                fill="currentColor"
                viewBox="0 0 20 20"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  fillRule="evenodd"
                  d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                  clipRule="evenodd"
                ></path>
              </svg>
              <span className="sr-only">Close modal</span>
            </button>
          </div>
          <div className="relative px-4 py-6 mx-auto">
            {dataLoader ? (
              <div>
                <Loader />
              </div>
            ) : (
              <div className={` rounded-tl-xl p-4`}>
                <div>
                  <div className="flex items-center">
                    <label htmlFor="">
                      Please check the box if you follow School term dates
                    </label>
                    <input
                      name="follow_term"
                      onChange={handleCheckbox}
                      className="mx-3"
                      type="checkbox"
                    />
                  </div>
                  <Input
                    name={"name"}
                    placeholder={"Report Name"}
                    handleChange={handleChange}
                    value={inputData?.name}
                  />
                  <SelectInput
                    name={"child_id"}
                    data={childInfo}
                    placeholder={"Select Child"}
                    handleChange={handleChangeCard}
                    value={child !== null ? child?.id : ""}
                  />
                </div>

                <div className="flex justify-end mt-5">
                  <div className="">
                    {loader ? (
                      <ButtonLoader />
                    ) : (
                      <Button
                        text={"Generate Report"}
                        handleClick={handleAdd}
                      />
                    )}
                  </div>
                </div>
                {/* <div>
        <GenerateReport inputData={inputData} childData={child} />
      </div> */}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CreateReport;
