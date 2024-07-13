import {PaymentElement,useStripe, useElements} from '@stripe/react-stripe-js';
import Button from '../../Components/Button/Button';
import Validations from '../../Regex';
import { toast } from 'react-toastify';
import TotalServices from '../../TotalServices';
import { useState } from 'react';

const CheckoutFormRenew = ({handleSuccess,amount,inputData}) => {
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
 
    else{
      setLoader(true)
     
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

export default CheckoutFormRenew;