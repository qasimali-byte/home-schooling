import dayjs from "dayjs"
import customParseFormat from 'dayjs/plugin/customParseFormat'
dayjs.extend(customParseFormat)
  
  export let years=[
    {"name": "Foundation Year", "id": "Foundation Year"},
    {"name": "Year 1", "id": "Year 1"},
    {"name": "Year 2", "id": "Year 2"},
    {"name": "Year 3", "id": "Year 3"},
    {"name": "Year 4", "id": "Year 4"},
    {"name": "Year 5", "id": "Year 5"},
    {"name": "Year 6", "id": "Year 6"},
    {"name": "Year 7", "id": "Year 7"},
    {"name": "Year 8", "id": "Year 8"},
    {"name": "Year 9", "id": "Year 9"},
    {"name": "Year 10", "id": "Year 10"},
   
  ]
 const dateFormat=(date,inputFormat,outPutFormat)=>{
return dayjs(date,inputFormat).format(outPutFormat)
  }
let Utils={
dateFormat
}
export default Utils;