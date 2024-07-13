import NonTermActivities from "./NonTermActivities";

const NoTermReportData = ({
  followTerm,
  tableData,
  termId,
  termData,
  report_id,
  GetData,
  subId,
  learningAreas,
}) => {
  return (
    <>
      <div
        className="flex items-center justify-center my-5"
        //  onClick={e=>handleSendDates(item)}
      >
        {/* <p className="px-4 py-2 text-xl text-white bg-blue-500 rounded-full">
             {item?.subject_name}
            </p> */}
      </div>
      {tableData?.map((subject) => (
        <NonTermActivities
          subject={subject}
          termId={termId}
          followTerm={followTerm}
          termData={termData}
          GetData={GetData}
          subId={followTerm === 0 ? subId : subject.subject_id}
          report_id={report_id}
          learningAreas={learningAreas}
        />
      ))}
    </>
  );
};

export default NoTermReportData;
