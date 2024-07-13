const Confirmation = ({setShowConfirmation,message,warning}) => {
    return (

        <>
            <div className="justify-center items-center flex overflow-x-hidden overflow-y-auto fixed inset-0 z-50 outline-none focus:outline-none m-0 p-0">
                <div className="relative w-full h-full max-w-md md:h-auto">
                    <div className="relative  -lg shadow bg-white">
                        <button
                         onClick={() => setShowConfirmation(false)}
                        type="button" className="absolute top-3 right-2.5 bg-transparent   -lg text-sm p-1.5 ml-auto inline-flex items-center hover:bg-gray-800 hover:text-white" data-modal-hide="popup-modal">
                           
                            <svg aria-hidden="true" className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                            <span  className="sr-only">Close modal</span>
                        </button>
                        <div className="p-6 text-center">
                            <svg aria-hidden="true" className="mx-auto mb-4 w-14 h-14 text-gray-200" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                            <h3 className="mb-3 text-lg font-normal  text-color-secondary">
                                
                              {message}
                                
                                </h3>
                                <p className="text-red-500 mb-4">
                                    {warning}
                                </p>
                            <button  type="button" className="text-secondary bg-primary focus:outline-none font-medium -lg text-sm inline-flex items-center px-5 py-2.5 text-center mr-2 my-4"
                            onClick={() => setShowConfirmation(true)}>
                                Yes, I'm sure
                            </button>
                            <button 
                            onClick={() => setShowConfirmation(false)}
                            data-modal-hide="popup-modal" type="button" className="  focus:outline-none  -lg border  text-sm font-medium px-5 py-2.5  focus:z-10 bg-primary  text-secondary">No, cancel</button>
                        </div>
                    </div>
                </div>
            </div>
        </>




    );
}
export default Confirmation;