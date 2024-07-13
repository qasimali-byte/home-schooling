import Slider from "react-slick";
import Validations from "../../Regex";

const ImageViewer = ({fileNames,fileUrls}) => {
  var settings = {
      
    rows:1,
    slidesToShow:1,
    speed: 500,

    infinite: false,
    initialSlide: 0,
    slidesToScroll: 1,
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 6,
          slidesToScroll: 1,
          infinite: true,
         
        }
      },
      {
        breakpoint: 600,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 1,
          initialSlide: 0,
        }
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow:1,
          slidesToScroll: 1
        }
      }
    ]
   
  };
    return (
        <div className="w-48 mx-6">
            <Slider className=""
        {...settings}
       > 
      {fileNames !== null &&fileNames.map((val,index)=> Validations.isImage(val) &&( 
        <div
        key={index}
        className=" flex justify-center max-w-48">

      <div className=" mx-2  flex flex-col items-center">
         
          <img className=""
          src={fileUrls[index]}
            />
            <p className="">
              {val}
            </p>
          
        </div>
        </div>
      
        ))
     }
        </Slider> 
        </div>
      );
}
 
export default ImageViewer;