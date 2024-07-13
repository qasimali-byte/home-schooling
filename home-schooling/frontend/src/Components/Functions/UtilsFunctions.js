import TotalServices from "../../TotalServices";

 const GetStates = async () => {
   
    try {

      let response = await TotalServices.getStates();
      if (response.status === 200) {
        //  console.log(response);
     return response.data.data
      
      }
    } catch (e) {
      console.log(e);

    }
  };
  export const GetLevels = async () => {
   
    try {

      let response = await TotalServices.getLevels();
      if (response.status === 200) {
        //  console.log(response);
     return response.data.data
      
      }
    } catch (e) {
      console.log(e);

    }
  };
  export const GetLearningAreas = async (id) => {
    try {
      let response = await TotalServices.getLearningAreas(id);
      if (response.status === 200) {
        //  console.log(response);
     return response.data.data 
      }
    } catch (e) {
      console.log(e);

    }
  };
  export const GetStrands = async (id) => {
    try {
      let response = await TotalServices.getStrands(id);
      if (response.status === 200) {
        //  console.log(response);
     return response.data.data 
      }
    } catch (e) {
      console.log(e);

    }
  };
  export const GetCodes = async (subject,strand,subStrand) => {
    try {
      let response = await TotalServices.getCodes(subject,strand,subStrand);
      if (response.status === 200) {
        //  console.log(response);
     return response.data.data 
      }
    } catch (e) {
      console.log(e);

    }
  };
  export default GetStates