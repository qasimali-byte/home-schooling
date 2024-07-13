import Services from "./ServicesRoutes";
import http from "./axios";

//user
const login = (data) => {
  return http.post(Services.login, data);
};
const signUp = (data) => {
  return http.patch(Services.login, data);
};

const Logout = () => {
  return http.put(Services.login);
};
const EmailVerification = (token) => {
  return http.post(Services.UserAccount + "?token=" + token);
};
//get subscription plans
const userData = () => {
  return http.get(Services.UserAccount);
};
const editUserData = (data) => {
  return http.patch(Services.UserAccount, data);
};
const ChangePassword = (data) => {
  return http.put(Services.UserAccount, data);
};
const getPlans = () => {
  return http.get(Services.plans);
};
const getStates = () => {
  return http.get(Services.States);
};
const getLevels = () => {
  return http.get(Services.Levels);
};
const getTermData = (data) => {
  return http.post(Services.States, data);
};
const getLearningAreas = (id) => {
  return http.patch(Services.SubjectData + "?level_id=" + id);
};
const getStrands = (id) => {
  return http.put(Services.SubjectData + "?subject_id=" + id);
};
const getCodes = (sub_id, strand, subStrand) => {
  return http.get(
    Services.SubjectData +
      "?subject_id=" +
      sub_id +
      "&strand_name=" +
      strand +
      "&substrand_name=" +
      subStrand
  );
};
//DowloadActivity
const DownloadActivity = (id, followTerm) => {
  return http.get(
    Services.DownloadActivity +
      "?report_id=" +
      id +
      "&follow_term=" +
      followTerm
  );
};
const getPaymentIntent = (data) => {
  return http.post(Services.plans, data);
};
const checkMail = (data) => {
  return http.patch(Services.plans, data);
};
const GetSubscription = (data) => {
  return http.put(Services.plans, data);
};
const CancelSubscription = (id) => {
  return http.delete(Services.plans + "?subscription_id=" + id);
};
//children apis
const ListChild = (limit, offset, query) => {
  //+"?page_size=" + limit + "&page_number=" + offset+"&search="+query
  return http.get(
    Services.Childs +
      "?page_size=" +
      limit +
      "&page_number=" +
      offset +
      "&search=" +
      query
  );
};
const DeleteChild = (id) => {
  return http.delete(Services.Childs + "?child_id=" + id);
};
const EditChild = (id, data) => {
  return http.patch(Services.Childs + "?child_id=" + id, data);
};
const AddChild = (data) => {
  return http.post(Services.Childs, data);
};
//Reports
const ListReport = (limit, offset, query) => {
  //+"?page_size=" + limit + "&page_number=" + offset+"&search="+query
  return http.get(
    Services.Reports +
      "?page_size=" +
      limit +
      "&page_number=" +
      offset +
      "&search=" +
      query
  );
};
const DeleteReport = (id) => {
  return http.delete(Services.Reports + "?report_id=" + id);
};
const EditReport = (id, data) => {
  return http.patch(Services.Reports + "?report_id=" + id, data);
};
const AddReport = (data) => {
  return http.post(Services.Reports, data);
};
const SubjectDetails = () => {
  return http.put(Services.Reports);
};
//Activities
const ListActivities = (
  limit,
  offset,
  code,
  id,
  term_id,
  followTerm,
  subId
) => {
  //+"?page_size=" + limit + "&page_number=" + offset+"&search="+query
  return http.get(
    Services.Activity +
      "?page_size=" +
      limit +
      "&page_number=" +
      offset +
      "&CdCode=" +
      code +
      "&report_id=" +
      id +
      "&term_id=" +
      term_id +
      "&follow_term=" +
      followTerm +
      "&subject_id=" +
      subId
  );
};
//Get starnds data for a subject
const ListStrands = (limit, offset, id, subjectId, termId, followTerm) => {
  //+"?page_size=" + limit + "&page_number=" + offset+"&search="+query

  return http.post(
    Services.Levels +
      "?report_id=" +
      id +
      "&subject_id=" +
      subjectId +
      "&term_id=" +
      termId +
      "&page_size=" +
      limit +
      "&page_number=" +
      offset +
      "&follow_term=" +
      followTerm
  );
};
const ListSubjects = (id) => {
  return http.post(Services.SubjectData + "?report_id=" + id);
};
const ListTermSubjects = (limit, offset, id, term_id) => {
  return http.put(
    Services.Levels +
      "?page_size=" +
      limit +
      "&page_number=" +
      offset +
      "&report_id=" +
      id +
      "&term_id=" +
      term_id
  );
};
const ListSubjectCodes = (id, subjectId, limit, offset) => {
  //+"?page_size=" + limit + "&page_number=" + offset+"&search="+query
  return http.post(
    Services.Levels +
      "?page_size=" +
      limit +
      "&page_number=" +
      offset +
      "&report_id=" +
      id +
      "&subject_id=" +
      subjectId
  );
};
const DeleteActivities = (id) => {
  return http.delete(Services.Activity + "?activity_id=" + id);
};
const EditActivities = (data, id) => {
  return http.patch(Services.Activity + "?activity_id=" + id, data);
};
const AddActivities = (data) => {
  return http.post(Services.Activity, data);
};
const GetSignedUrls = (data) => {
  return http.put(Services.Activity, data);
};
const SubscriptionRenewal = (data) => {
  return http.post(Services.Subscriber, data);
};
const PredictElaboration = (data) => {
  return http.post(Services.AIActivity, data);
};
const PredictionData = (data) => {
  return http.patch(Services.AIActivity, data);
};
const TotalServices = {
  login,
  signUp,
  Logout,
  getPlans, //get subscription plans
  ListChild,
  DeleteChild,
  EditChild,
  AddChild,
  getPaymentIntent,
  checkMail,
  userData,
  editUserData,
  ChangePassword,
  EmailVerification,
  ListReport,
  DeleteReport,
  EditReport,
  AddReport,
  SubjectDetails,
  ListActivities,
  EditActivities,
  DeleteActivities,
  AddActivities,
  getStates,
  getTermData,
  DownloadActivity,
  GetSignedUrls,
  ListSubjects,
  ListStrands,
  getLevels,
  getLearningAreas,
  getStrands,
  getCodes,
  ListSubjectCodes,
  ListTermSubjects,
  GetSubscription,
  CancelSubscription,
  SubscriptionRenewal,
  PredictElaboration,
  PredictionData,
};

export default TotalServices;
