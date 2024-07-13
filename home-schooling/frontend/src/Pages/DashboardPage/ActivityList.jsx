// StudyActivities.js

import React from 'react';

const StudyActivities = ({ activities ,date}) => {
  return (
    <div className="container mx-auto p-4">
      <h2 className="text-2xl font-semibold mb-4">Study Activities for {date.getDate()+"/"+(date.getMonth()+1)+"/"+date.getFullYear()}</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {activities.map((activity, index) => (
          <div key={index} className="bg-white p-4 shadow-md rounded-md">
            <h3 className="text-lg font-semibold mb-2">{activity.name}</h3>
            <p className="text-gray-600">{activity.description}</p>
            <div className="mt-4">
              <p className="text-gray-500 font-semibold">Strand: {activity.strand}</p>
              <p className="text-gray-500 font-semibold">Substrand: {activity.substrand}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default StudyActivities;
