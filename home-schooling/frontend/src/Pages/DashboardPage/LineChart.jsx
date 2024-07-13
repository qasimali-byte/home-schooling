import { Bar,Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    ArcElement,
    PointElement,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    LineElement,
    Tooltip,
    Legend,
  } from 'chart.js';
  ChartJS.register(
    ArcElement,
    LineElement,
    PointElement,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
  );
  

const LineChart = () => {
    const getLast7Days = () => {
        const today = new Date();
        const last7Days = [];
    
        for (let i = 6; i >= 0; i--) {
          const day = new Date(today);
          day.setDate(today.getDate() - i);
          last7Days.push(day.toDateString());
        }
    
        return last7Days;
      };
let labels=getLast7Days()    
    const data = {
        labels,
        datasets: [
          {
            label: 'Activities',
            data: [5,4,2,3,2,4,1],
            backgroundColor: "#02af9d",
          },
         
        ],
      };
      let options= {
        responsive: true,
      
        
              barThickness : 40,
        
    
        plugins: {
          legend: {
            position: 'bottom',
          },
          title: {
            display: true,
            text: 'Daily Activities'
          }
        }
      }
    return ( 
        <div className="w-full lg:flex">
        <div className="w-full">
        <Bar 
        data={data}
        options={options}
        />
        </div>
        <div className="w-full">
        <Line 
        data={data}
        options={options}
        />
        </div>
     
 

        </div>
     );
}
 
export default LineChart;