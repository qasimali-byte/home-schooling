import planimage from "../../assets/package.png"
const Package = ({plan}) => {
    return (  <div className="flex flex-col rounded-lg bg-[#173175] sm:flex-row text-white">
   
    <div className="flex w-full flex-col px-4 py-4">
      <span className="font-semibold uppercase ">{plan?.name}</span>
      <span className="float-right text-right">{plan?.duration} Days</span>
      <div>
      <ul className="text-right">
       
        {
          plan!==null && plan.extra_data.features?.map(val=>(
            <li>
            {  val}
            </li>
          ))
        }
      </ul>
      </div>
      <div className="flex justify-end">
      <p className="mt-auto text-lg font-bold">${plan?.price}</p>
     
      </div>
     
    </div>
  </div> );
}
 
export default Package;