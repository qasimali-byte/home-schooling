import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate, useParams } from "react-router-dom";
import { toast } from "react-toastify";
import Loader from "../../Components/Loader/Loader";
import TotalServices from "../../TotalServices";
import Button from "../../Components/Button/Button";
import signup from "../../assets/signup.avif";
const EmailVerification = () => {
  // let { token, username } = useParams();
  const [loader, setLoader] = useState(true);
  const [message, setMessage] = useState("");
  const [expired, setExpired] = useState(true);
  const [resendLink, setResendLink] = useState("");

  let navigate = useNavigate();

  let location = useLocation();

  const queryParams = new URLSearchParams(location.search);
  const token = queryParams.get("token");
  const email = queryParams.get("email");

  const handleVerification = async () => {
    try {
      setLoader(true);

      const response = await TotalServices.EmailVerification(token);
      // console.log(response, "res");

      if (response.status === 200) {
        if (response.data.status === 401) {
          setExpired(true);
          setLoader(false);
          setResendLink(response.data.resend_url);
        } else {
          setLoader(false);
          setExpired(false);
        }
      }
    } catch (error) {
      console.log("error ", error);
      setLoader(false);
    }
  };
  const handleResendEmail = async () => {
    try {
      const response = await TotalServices.ResendEmailVerification(email);
      // console.log(response, "res");

      if (response.status === 200) {
        toast.success(response.data.message);
      }
    } catch (error) {
      console.log("error ", error);
      setLoader(false);
    }
  };
  useEffect(() => {
    document.title = "Home Schooling - Email Verification";
  }, []);
  useEffect(() => {
    handleVerification();
  }, []);
  return (
    <div
      className="flex items-center justify-center w-full h-screen bg-cover "
      style={{ backgroundImage: `url(${signup})` }}
    >
      <div className="block rounded-lg bg-white p-6 shadow-[0_2px_15px_-3px_rgba(0,0,0,0.07),0_10px_20px_-2px_rgba(0,0,0,0.04)] ">
        <h1 className="mb-4 text-base text-neutral-600 ">
          <b>Checking Verification!</b>
        </h1>
        {loader ? (
          <div className="p-4 ">
            <div className="flex justify-center mb-5">
              <Loader />
            </div>

            <p className="mb-0 text-center text-secondary">
              Please wait, while we are checking your Verification
            </p>
          </div>
        ) : !expired ? (
          <div>
            <p className="mb-5 text-center">
              Your email, is verified now, you can go to login page.
            </p>
            <div className="flex justify-end">
              <div>
                <Button text={"Login"} handleClick={(e) => navigate("/")} />
              </div>
            </div>
          </div>
        ) : (
          <div>
            <p className="mb-5 text-center">
              Your email, is Expired or Damaged, Please Contact Administrator or
              Resend Verification Link.
            </p>
            <div className="flex justify-end">
              <div>
                <Button text={"Resend Link"} handleClick={handleResendEmail} />
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default EmailVerification;
