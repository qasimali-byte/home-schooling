
import TermActivities from "./TermActivities";

const TermReportData = ({tableData,subjectData,GetData,termData,report_id,followTerm,termId}) => {
 

    return (
      <>
     {tableData.map(subject=>(
        <div>
<TermActivities subject={subject} termId={termId} subjectData={subjectData} GetData={GetData}  termData={termData} report_id={report_id} />
</div>
      
    ))}
       
      
        </>
    )
}
 
export default TermReportData;