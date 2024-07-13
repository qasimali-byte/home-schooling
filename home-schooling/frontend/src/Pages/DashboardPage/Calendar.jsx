import { useState } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';



export default function MyCalender({onChange,value}) {


  return (
    <div className='p-6'>
        <h1>
            
        </h1>
      <Calendar onChange={onChange} value={value} />
    </div>
  );
}