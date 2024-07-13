import { Elements } from "@stripe/react-stripe-js";
import { loadStripe } from "@stripe/stripe-js";
import TotalServices from "../../TotalServices";
import { useEffect, useState } from "react";
import Loader from "../../Components/Loader/Loader";
import CheckoutForm from "./Checkoutform";
import CheckoutFormRenew from "../Login/CheckoutformRenew";

// Make sure to call `loadStripe` outside of a component’s render to avoid
// recreating the `Stripe` object on every render.

export default function Checkout({
  renew,
  amount,
  handleSuccess,
  inputData,
  plan,
  setInputData,
}) {
  const [paymentIntent, setPaymentIntent] = useState("");
  const stripePromise = loadStripe(
    "pk_test_51P2U2WLdwoqQPCJekPlFwnc1rLEIcTicjON3I9DUivwfp5wAoRVNEcddXzZbalfs3595Nycdi4UoNCE7Btv7YbVm00ObzinX3B"
  );
  const [loader, setLoader] = useState(true);

  const GetData = async () => {
    try {
      setLoader(true);
      let response = await TotalServices.getPaymentIntent({
        amount: amount,
        email: inputData.email,
        price_id: plan.stripe_id,
      });
      if (response.status === 200) {
        setPaymentIntent(response.data.clientSecret);
        setInputData((prev) => ({
          ...prev,
          stripe_subscription_id: response.data.subscriptionId,
          user_stripe_id: response.data.customer_id,
        }));

        setLoader(false);
      }
    } catch (e) {
      console.log(e);
      setLoader(false);
    }
  };

  useEffect(() => {
    amount !== "" && GetData();
  }, [amount]);
  const options = {
    // passing the client secret obtained from the server

    clientSecret: paymentIntent,
  };

  return loader ? (
    <Loader />
  ) : (
    stripePromise !== "" && (
      <Elements stripe={stripePromise} options={options}>
        {renew ? (
          <CheckoutFormRenew
            handleSuccess={handleSuccess}
            amount={amount}
            inputData={inputData}
          />
        ) : (
          <CheckoutForm
            handleSuccess={handleSuccess}
            amount={amount}
            inputData={inputData}
          />
        )}
      </Elements>
    )
  );
}
