import { useEffect, useState } from "react";
import SelectInput from "../../Components/Input/SelectInput";
import Input from "../../Components/Input/Input";
import Button from "../../Components/Button/Button";
import TextArea from "../../Components/Input/TextArea";
import ActivitySelect from "../../Components/Input/ActivitySelect";
import TotalServices from "../../TotalServices";
import { toast } from "react-toastify";
import Validations from "../../Regex";
import ButtonLoader from "../../Components/Loader/ButtonLoader";
import dayjs from "dayjs";
import FileUpload from "./FileUplaod";
import axios from "axios";
import Select from "react-select";
import {
  GetCodes,
  GetStrands,
} from "../../Components/Functions/UtilsFunctions";
import Loader from "../../Components/Loader/Loader";
import Tooltip from "../../Components/ToolTip/Tooltip";
import { useLocation } from "react-router-dom";
import Predictions from "./Predictions";

const CreateActivity = ({
  setShow,
  subjectData,
  GetData,
  editData,
  report_id,
  termData,
  dateData,
  followTerm,
  learningAreas,
}) => {
  const [inputData, setInputData] = useState({
    description: "",
    start_date: "",
    end_date: null,
    states_has_terms_id: null,
    urls: "",
    file_names: [],
    file_ids: [],
  });
  const [loader, setLoader] = useState(false);
  const [dataLoader, setDataLoader] = useState(false);
  const [strandsOptions, setStrandsOptions] = useState([]);
  const [subStrandsOptions, setSubStrandsOptions] = useState([]);
  const [subStrand, setSubStrand] = useState(null);
  const [codesOptions, setCodesOptions] = useState([]);
  const [code, setCode] = useState(null);
  const [term, setTerm] = useState(null);
  const [codeLoader, setCodeLoader] = useState(false);
  const [learningArea, setLearningArea] = useState(null);
  const [subjectOption, setSubjectOptions] = useState([]);
  const [subject, setSubject] = useState(null);
  const [elaboration, setElaboration] = useState(null);
  const [elaborationOptions, setElaborationOptions] = useState([]);
  const [GCCOptions, setGCCOptions] = useState([]);
  const [GCC, setGCC] = useState(null);
  const [element, setElement] = useState(null);
  const [elementOptions, setElementOptions] = useState([]);
  const [subElement, setSubElement] = useState(null);
  const [subElementOptions, setSubElementOptions] = useState([]);
  const [strand, setStrand] = useState(null);
  const [predict, setPredict] = useState(false);
  const [predictions, setPredictions] = useState([]);
  const [predictionLoader, setPredictionsLoader] = useState(false);
  const [showPredictions, setShowPredictions] = useState(false);
  const [elabLoader, setElabLoader] = useState(false);
  const { state } = useLocation();
  let styles = {
    control: (baseStyles, state) => ({
      ...baseStyles,
      paddingLeft: 10,
      paddingRight: 10,
      paddingTop: 5,
      paddingBottom: 5,
      borderRadius: 8,
    }),
  };
  const handleTermChange = (e) => {
    if (e.target.value === "") {
      setTerm(null);
      handleActivityChange(e);
    } else {
      let tempTerm = termData.filter(
        (val) => val.state_terms_id == e.target.value
      )[0];
      setTerm(tempTerm);
      setInputData((prev) => ({
        ...inputData,
        [e.target.name]: e.target.value,
        start_date: dayjs(tempTerm.term_start_date).format("YYYY-MM-DD"),
        end_date: dayjs(tempTerm.term_end_date).format("YYYY-MM-DD"),
      }));
    }
  };
  const handleActivityChange = (e) => {
    setInputData(() => ({
      ...inputData,
      [e.target.name]: e.target.value,
    }));
  };
  const handleLearningArea = (value) => {
    setPredict(false);
    setLearningArea(value);
    setSubjectOptions(value.subjects);
    setSubject(value.subjects[0]);

    setStrand(null);
    setSubStrand(null);
    setCode(null);
    setElaboration(null);
  };
  const handleSubject = (value) => {
    setSubject(value);
    setStrand(null);
    setSubStrand(null);
    setCode(null);
    setElaboration(null);
  };

  const handleAdd = async (e) => {
    e.preventDefault();

    if (
      Validations.isEmpty(inputData.description) ||
      Validations.isEmpty(inputData.start_date) ||
      code === null
    ) {
      toast.error("Fields can't be empty");
    } else if (
      followTerm !== 0 &&
      new Date(inputData.start_date) < new Date(term.term_start_date)
    ) {
      toast.error("Start date should be greater than Term Start Date");
    } else if (
      followTerm !== 0 &&
      new Date(inputData.start_date) > new Date(term.term_end_date)
    ) {
      toast.error("Start date should be less than Term End Date");
    } else if (
      followTerm !== 0 &&
      inputData.end_date !== null &&
      new Date(inputData.end_date) > new Date(term.term_end_date)
    ) {
      // console.log(new Date(inputData.end_date)>=new Date(term.term_end_date),inputData.end_date,new Date(term.term_end_date));
      toast.error("End date should be less than Term End Date");
    }
    // else if(inputData.end_date!==null &&new Date(inputData.start_date)>=new Date(inputData.end_date)){
    //   toast.error("End date should be Greater than Start Date")
    // }
    else if (
      !Validations.isEmpty(inputData.urls) &&
      inputData.urls.split(",").length > 3
    ) {
      toast.error("Max 3 links are allowed with each activity");
    } else {
      if (!Validations.isEmpty(inputData.urls)) {
        let urls = inputData.urls.split(",");
        for (let i = 0; i < urls.length; i++) {
          if (!Validations.isValidUrl(urls[i])) {
            toast.error("Url:" + urls[i] + " is not valid");
            return;
          }
        }
      }
      if (inputData.file_names.length > 0) {
        for (let i = 0; i < inputData.file_names.length; i++) {
          if (Validations.specialCharacters(inputData.file_names[i].name)) {
            toast.error(
              "Special Characters like (-,) not allowed in file names"
            );
            return;
          }
        }
        try {
          let stampedFiles = inputData.file_names.map((val) => {
            let date = new Date();
            let tempName = val.name.replaceAll(" ", "_");
            let name = tempName.split(".");
            name.splice(name.length - 1, 1);
            let newName = name.join(" ");

            return (
              newName +
              "_" +
              date.getMilliseconds() +
              "." +
              val.name.split(".")[val.name.split(".").length - 1]
            );
          });
          setLoader(true);
          const res = await TotalServices.GetSignedUrls({
            file_names: stampedFiles,
          });
          if (res.status === 200) {
            UplaodAll(res.data.urls, stampedFiles);
          }
        } catch (e) {
          console.log(e);
          setLoader(false);
        }
      } else {
        SendDataToBackend([]);
      }
    }
  };
  const UplaodAll = async (urls, stampedFiles) => {
    setLoader(true);

    try {
      for (let i = 0; i < urls.length; i++) {
        let formFile = new FormData();
        formFile.append("file", inputData.file_names[i]);

        const response = await axios.put(urls[i], inputData.file_names[i], {
          headers: {
            "Content-Type": inputData.file_names[i].type,
          },
        });

        if (response.status !== 200) {
          throw new Error("Request failed");
        }
      }
      SendDataToBackend(stampedFiles);
    } catch (error) {
      console.error("Error uploading files:", error);
      toast.error("Error uploading file please try again");
      setLoader(false);
    }
  };
  const SendDataToBackend = async (stampedFiles) => {
    try {
      let body = {
        ...inputData,

        file_names: stampedFiles,
        report_id: report_id,
        subject_id: subject.value,
        end_date:
          inputData.end_date === inputData.start_date
            ? null
            : inputData.end_date,
        json_data: {
          CdCode: code?.value,
          Strand: strand?.value,
          Substrand: subStrand?.value,
          ContentDesc: code?.description,
          Elaboration: elaboration?.value,
          GCC: GCC?.value,
          Element: element?.value,
          SubElement: subElement?.value,
        },
      };
      setLoader(true);
      let response = editData
        ? await TotalServices.EditActivities(body, editData.activity_id)
        : await TotalServices.AddActivities(body);

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
  };
  const GetStrandsData = async () => {
    setDataLoader(true);
    let data = await GetStrands(subject.value);
    setStrandsOptions(
      data.map((val) => ({ ...val, label: val.Strand, value: val.Strand }))
    );
    setDataLoader(false);
  };
  const ElaborationPrediction = async () => {
    try {
      setPredict(true);

      setPredictionsLoader(true);
      let body = {
        description: inputData.description,
        level_id: state.data.level_id,
      };
      let response = await TotalServices.PredictElaboration(body);
      if (response.status === 200) {
        // console.log(response);

        setPredictions(response.data.data);
        setPredictionsLoader(false);
        setShowPredictions(false);
        setGCCOptions([]);
        setLearningArea(null);
        setSubject(null);
        setStrand(null);
        setSubStrand(null);
        setCode(null);
        setElaboration(null);
        setGCC(null);
        setElement(null);
        setSubElement(null);
        setElaborationOptions([]);
        setElementOptions([]);
        setSubElementOptions([]);
        setSubStrandsOptions([]);
        setStrandsOptions([]);
        setCodesOptions([]);
      }
    } catch (e) {
      console.log(e);
      setPredictionsLoader(false);
    }
  };
  const ElaborationData = async (val) => {
    try {
      setElabLoader(true);
      let body = {
        elaboration: val,
      };
      let response = await TotalServices.PredictionData(body);
      let data = response.data.data;
      if (response.status === 200) {
        data.ContentDesc &&
          setCode({
            label: data.ContentDesc,
            value: data.CdCode,
            description: data.ContentDesc,
          });
        data.Substrand &&
          setSubStrand({ label: data.Substrand, value: data.Substrand });
        data.Strand && setStrand({ label: data.Strand, value: data.Strand });
        data.subject_name &&
          setSubject({ label: data.subject_name, value: data.subject_id });
        data.learning_area &&
          setLearningArea({
            label: data.learning_area,
            value: data.learning_area,
          });
        setShowPredictions(true);
        data.GC && setGCC({ label: data.GC, value: data.GC });
        data.Element &&
          setElement({ label: data.Element, value: data.Element });
        data.Subelement &&
          setSubElement({ label: data.Subelement, value: data.Subelement });
        setElaboration({ label: val, value: val });
        setElabLoader(false);
      }
    } catch (e) {
      setElabLoader(false);
      console.log(e);
    }
  };
  const GetCodesData = async () => {
    setCodeLoader(true);
    let data = await GetCodes(subject.value, strand.value, subStrand.value);
    setCodesOptions(
      data.map((val) => ({ ...val, label: val.description, value: val.code }))
    );
    setCodeLoader(false);
  };
  const handleStrand = (val) => {
    setStrand(val);
    setSubStrand(null);
    setCode(null);
    setElaboration(null);
    setSubStrandsOptions(
      val?.Sub_strands.map((item) => ({ value: item, label: item }))
    );
  };
  const handleSubStrand = (val) => {
    setCode(null);
    setElaboration(null);
    setSubStrand(val);
  };
  const handleCode = (val) => {
    setCode(val);
    setElaboration(null);
    setElaborationOptions(
      val.elaborations.map((item) => ({ value: item, label: item }))
    );
    setGCCOptions(
      val.gcc.map((item) => ({ ...item, label: item.GC, value: item.GC }))
    );
  };
  const handleElab = (val) => {
    setElaboration(val);
  };
  const handleGCC = (val) => {
    setGCC(val);
    setElement(null);
    setSubElement(null);
    setElementOptions(
      val?.elements.map((item) => ({
        ...item,
        value: item.Element,
        label: item.Element,
      }))
    );
  };
  const handleElement = (val) => {
    setElement(val);

    setSubElement(null);
    setSubElementOptions(
      val.sub_elements.map((item) => ({
        ...item,
        value: item.Subelement,
        label: item.Subelement,
      }))
    );
  };
  const handleSubElement = (val) => {
    setSubElement(val);
  };
  const handlePredict = (elab) => {
    if (elab) {
      ElaborationData(elab);
    } else {
      setShowPredictions(true);
    }
  };
  useEffect(() => {
    if (editData) {
      //  console.log(editData,termData,termData.filter(val=>val.state_terms_id===editData.states_has_terms_id)[0]);
      let {
        subject_name,
        learning_name,
        subject_id,
        strand_name,
        sub_strand_name,
        CdCode,
      } = editData;
      let { Elaboration, SubElement, Element, GCC, ContentDesc } =
        editData.json_subject_data;
      setSubject({ label: subject_name, value: subject_id });
      setLearningArea({ label: learning_name, value: learning_name });
      setStrand({ label: strand_name, value: strand_name });
      setSubStrand({ label: sub_strand_name, value: sub_strand_name });
      setCode({ label: ContentDesc, value: CdCode, description: ContentDesc });
      GCC && setGCC({ label: GCC, value: GCC });
      Element && setElement({ label: Element, value: Element });
      SubElement && setSubElement({ label: SubElement, value: SubElement });
      Elaboration && setElaboration({ label: Elaboration, value: Elaboration });
      followTerm === 1 &&
        setTerm(
          termData?.filter(
            (val) => val.state_terms_id === editData.states_has_terms_id
          )[0]
        );

      setInputData((prev) => ({
        ...inputData,
        start_date: dayjs(editData.act_start_date, "DD-MM-YYYY").format(
          "YYYY-MM-DD"
        ),
        end_date: dayjs(editData.act_end_date, "DD-MM-YYYY").format(
          "YYYY-MM-DD"
        ),
        description: editData.activity_description,

        states_has_terms_id: editData.states_has_terms_id,

        report_id: "",
        urls: editData?.attached_links !== null ? editData?.attached_links : "",
      }));
      setShowPredictions(true);
    }
  }, []);
  useEffect(() => {
    if (dateData !== null) {
      dateData &&
        setTerm(
          termData.filter(
            (val) => val.state_terms_id === dateData.state_terms_id
          )[0]
        );
      dateData &&
        setInputData({
          ...inputData,
          start_date: dayjs(dateData.act_start_date).format("YYYY-MM-DD"),
          end_date: dayjs(dateData.act_end_date).format("YYYY-MM-DD"),
          states_has_terms_id: dateData.state_terms_id,
        });
    }
  }, [dateData]);

  useEffect(() => {
    subject !== null && !predict && GetStrandsData();
  }, [subject]);
  useEffect(() => {
    subStrand !== null && !predict && GetCodesData();
  }, [subStrand]);

  return (
    <div className="fixed top-0 left-0 right-0 z-50  w-full p-4 overflow-x-hidden overflow-y-auto md:inset-0 h-[calc(100%-1rem)] md:h-full bg-[#fffb] ">
      <div className="relative w-full h-full mx-auto bg-white rounded-xl md:h-auto ">
        <div className="relative shadow-xl -lg text-color-secondary ">
          <div className="flex items-start justify-between p-4 border-b -t ">
            <h3 className="text-xl ">ACTIVITY</h3>
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
            <div className={` rounded-tl-xl p-4`}>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  {followTerm !== 0 && (
                    <ActivitySelect
                      name={"states_has_terms_id"}
                      data={termData}
                      optionLabel={"term_name"}
                      valueLabel={"state_terms_id"}
                      placeholder={"Select Term"}
                      handleChange={handleTermChange}
                      value={inputData.states_has_terms_id}
                    />
                  )}
                  <div className="grid grid-cols-2 gap-4">
                    <Input
                      name={"start_date"}
                      labelColor={"text-black"}
                      type={"date"}
                      label={
                        term !== null
                          ? `Select Start Date - Term Start(${term?.term_start_date.substring(
                              0,
                              16
                            )})`
                          : "Select Start Date"
                      }
                      placeholder={"Select Subject"}
                      handleChange={handleActivityChange}
                      value={inputData.start_date}
                      disabled={editData}
                    />

                    <Input
                      name={"end_date"}
                      type={"date"}
                      labelColor={"text-black"}
                      label={
                        term !== null
                          ? `Select End Date - Term End(${term?.term_end_date.substring(
                              0,
                              16
                            )})`
                          : "Select End Date"
                      }
                      placeholder={"Select Subject"}
                      handleChange={handleActivityChange}
                      value={inputData.end_date}
                      disabled={editData}
                    />
                  </div>
                  {elabLoader ? (
                    <Loader />
                  ) : showPredictions ? (
                    <div className="grid grid-cols-2 gap-4">
                      <Tooltip text={"Select Learning Area for the activity"}>
                        <Select
                          styles={styles}
                          placeholder="Select Learning Area"
                          options={learningAreas}
                          isSearchable={true}
                          value={learningArea}
                          onChange={handleLearningArea}
                        />
                      </Tooltip>
                      {(subjectOption.length > 1 ||
                        subject?.label !== learningArea?.label) && (
                        <Tooltip text={"Select Subject for the activity"}>
                          {" "}
                          <Select
                            styles={styles}
                            placeholder="Select Subject"
                            options={subjectOption}
                            value={subject}
                            isSearchable={true}
                            onChange={handleSubject}
                          />
                        </Tooltip>
                      )}
                      {dataLoader ? (
                        <Loader />
                      ) : (
                        <>
                          {(strandsOptions.length >= 1 || strand !== null) && (
                            <Tooltip text={"Select Category for the activity"}>
                              <Select
                                styles={styles}
                                placeholder="Select Category"
                                options={strandsOptions}
                                value={strand}
                                isSearchable={true}
                                onChange={handleStrand}
                              />
                            </Tooltip>
                          )}
                          {(subStrandsOptions.length >= 1 ||
                            subStrand !== null) && (
                            <Tooltip
                              text={"Select  Sub-Category for the activity"}
                            >
                              <Select
                                styles={styles}
                                placeholder="Select Sub-Category"
                                options={subStrandsOptions}
                                value={subStrand}
                                isSearchable={true}
                                onChange={handleSubStrand}
                              />
                            </Tooltip>
                          )}
                        </>
                      )}
                      {codeLoader ? (
                        <Loader />
                      ) : (
                        <>
                          {(codesOptions.length >= 1 || code !== null) && (
                            <Tooltip
                              text={"Select  Code for the activity"}
                              classes={"col-span-2"}
                            >
                              <Select
                                styles={styles}
                                placeholder="Select Description"
                                options={codesOptions}
                                value={code}
                                isSearchable={true}
                                onChange={handleCode}
                              />
                            </Tooltip>
                          )}
                          {(elaborationOptions.length >= 1 ||
                            elaboration !== null) && (
                            <Tooltip
                              text={"Select Elaboration for the activity "}
                              classes="col-span-2"
                            >
                              <Select
                                styles={styles}
                                className="col-span-2"
                                placeholder="Select Elaboration"
                                options={elaborationOptions}
                                value={elaboration}
                                isSearchable={true}
                                onChange={handleElab}
                              />
                            </Tooltip>
                          )}

                          {(GCCOptions.length >= 1 || GCC !== null) && (
                            <div className="col-span-2">
                              <p className="font-bold text-gray-800">
                                General Capabilities:
                              </p>
                            </div>
                          )}
                          {(GCCOptions.length >= 1 || GCC !== null) && (
                            <Tooltip
                              text={
                                "Select General Capability for the activity"
                              }
                            >
                              {" "}
                              <Select
                                styles={styles}
                                placeholder="General Capabilities"
                                options={GCCOptions}
                                value={GCC}
                                isSearchable={true}
                                onChange={handleGCC}
                              />
                            </Tooltip>
                          )}
                          {(elementOptions.length >= 1 || element !== null) && (
                            <Tooltip text={"Select  Element for the activity"}>
                              <Select
                                styles={styles}
                                placeholder="Select Element"
                                options={elementOptions}
                                value={element}
                                isSearchable={true}
                                onChange={handleElement}
                              />
                            </Tooltip>
                          )}
                          {(subElementOptions.length >= 1 ||
                            subElement !== null) && (
                            <Tooltip
                              text={"Select  Sub-element for the activity"}
                            >
                              {" "}
                              <Select
                                styles={styles}
                                placeholder="Select Sub-element"
                                options={subElementOptions}
                                value={subElement}
                                isSearchable={true}
                                onChange={handleSubElement}
                              />
                            </Tooltip>
                          )}
                        </>
                      )}
                    </div>
                  ) : (
                    <Predictions
                      predictions={predictions}
                      predict={predict}
                      loader={elabLoader}
                      handlePredict={handlePredict}
                    />
                  )}

                  <Input
                    name={"urls"}
                    type={"text"}
                    labelColor={"text-black"}
                    placeholder={
                      "Add links separated by comma( , )(max 3 links)"
                    }
                    handleChange={handleActivityChange}
                    value={inputData.urls}
                  />
                  <FileUpload
                    inputData={inputData}
                    setInputData={setInputData}
                    editData={editData}
                  />
                </div>
                <div className="relative h-full">
                  <TextArea
                    name={"description"}
                    classes={"h-36"}
                    placeholder={"Activity"}
                    handleChange={handleActivityChange}
                    value={inputData.description}
                  />
                  <div className="absolute bottom-0 right-0 flex mx-2">
                    <div>
                      {predictionLoader ? (
                        <ButtonLoader
                          text={"Fetching Ai driven results..."}
                          color={"bg-blue-500"}
                        />
                      ) : (
                        <Button
                          handleClick={ElaborationPrediction}
                          disabled={inputData.description.length < 75}
                          color={"bg-blue-500"}
                          text={"Predict"}
                        />
                      )}
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex justify-end mt-5">
                <div className="">
                  {loader ? (
                    <ButtonLoader />
                  ) : (
                    <Button
                      text={editData ? "Save Activity" : "Add Activity"}
                      handleClick={handleAdd}
                    />
                  )}
                </div>
              </div>
              {/* <div>
          <GenerateReport inputData={inputData} childData={child} />
        </div> */}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CreateActivity;
