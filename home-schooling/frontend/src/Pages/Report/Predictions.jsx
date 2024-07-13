import Button from "../../Components/Button/Button";
import Loader from "../../Components/Loader/Loader";

const Predictions = ({ predictions, handlePredict, loader }) => {
  return loader ? (
    <Loader />
  ) : (
    <div className="my-3  p-2">
      {predictions.length >= 1 ? (
        <div className=" p-3 shadow-sm">
          <h1 className="font-bold my-2">
            Please select one of the subject elaboration
          </h1>
          {predictions.map((val, index) => (
            <div
              key={index}
              className="p-4 my-2 bg-white shadow-md rounded-lg hover:bg-gray-100 cursor-pointer transition-all"
            >
              <p onClick={(e) => handlePredict(val)} className="text-blue-600">
                {val}
              </p>
            </div>
          ))}
        </div>
      ) : (
        <div className="p-4 my-2 bg-red-50 border-l-4 border-red-500">
          <p className="text-red-500">
            Please add your activity description to predict the subject data
            (minimum 75 characters)
          </p>
        </div>
      )}
      <p className="text-center font-bold text-xl">or</p>
      <div className="flex justify-center">
        <div>
          <Button text={"Fill Manually"} handleClick={(e) => handlePredict()} />
        </div>
      </div>
    </div>
  );
};

export default Predictions;
