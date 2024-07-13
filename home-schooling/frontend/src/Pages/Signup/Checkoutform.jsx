import {PaymentElement,useStripe, useElements} from '@stripe/react-stripe-js';
import Button from '../../Components/Button/Button';
import Validations from '../../Regex';
import { toast } from 'react-toastify';
import TotalServices from '../../TotalServices';
import { useState } from 'react';

const CheckoutForm = ({handleSuccess,amount,inputData}) => {
    const stripe = useStripe();
    const elements = useElements();
  const [loader,setLoader]=useState(false)
    const handleSubmit = async (event) => {
      // We don't want to let default form submission happen here,
      // which would refresh the page.
      event.preventDefault();
  
      if (!stripe || !elements) {
        // Stripe.js hasn't yet loaded.
        // Make sure to disable form submission until Stripe.js has loaded.
        return;
      }
      if(Validations.isEmpty(inputData.first_name)||Validations.isEmpty(inputData.last_name)||Validations.isEmpty(inputData.post_code)||Validations.isEmpty(inputData.state)||Validations.isEmpty(inputData.address)||Validations.isEmpty(inputData.email)||Validations.isEmpty(inputData.plan_id)){
        toast.error("Fields can't be empty")
    }
    else if(!Validations.isEmail(inputData.email)){
        toast.error("Invalid Email")
    }
    else if(inputData.password!==inputData.confirm_password){
        toast.error("Passwords doesn't match")
    }
    else if(!Validations.validatePassword(inputData.password)){
        toast.error("Password must have at least one lowercase letter, one uppercase letter, one digit, and one special character")
    }
  
    else{
      setLoader(true)
      let response = await TotalServices.checkMail({email:inputData.email});
      if (response.data.status !== 200) {
      
        toast.error(response.data.message)
     
        setLoader(false)
        }
        else{
      const result = await stripe.confirmPayment({
        //`Elements` instance that was used to create the Payment Element
        elements,
        confirmParams: {
          return_url: "http://34.195.110.86:7034",
        },
        redirect: "if_required",
      });
  
  
      if (result.error) {
        // Show error to your customer (for example, payment details incomplete)
        console.log(result.error.message);
        setLoader(false)
        toast.error("Error while transaction")
      }
      else if (result.paymentIntent && result.paymentIntent.status === "succeeded") {
        setLoader(false)
        console.log("Payment succeeded");
        handleSuccess();
      } else {
        setLoader(false)
        // Your customer will be redirected to your `return_url`. For some payment
        // methods like iDEAL, your customer will be redirected to an intermediate
        // site first to authorize the payment, then redirected to the `return_url`.
      }
    }
    }
    };
  return (
    <form className='w-full mx-auto mt-10' onSubmit={handleSubmit}>
     
      <PaymentElement />
      <div className='mt-3'>
      <Button text={"Pay $"+amount} disabled={!stripe || loader}/>
      </div>
    
    </form>
  );
};

export default CheckoutForm;