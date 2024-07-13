// CardComponent.js
import React from 'react';

const CardComponent = ({ subject, strands }) => {
  return (
    <div className="max-w-sm rounded overflow-hidden shadow-lg bg-white rounded-xl">
      <div className="px-6 py-4">
        <div className="font-bold text-xl mb-2">{subject}</div>
        {strands.map((strand, index) => (
          <div key={index}>
            <p className="text-gray-700 text-base">
              <strong>Strand:</strong> {strand.name}
            </p>
            {strand.substrands && strand.substrands.length > 0 && (
              <div className="ml-4">
                <p className="text-gray-700 text-base">
                  <strong>Substrands:</strong>
                </p>
                <ul className="list-disc">
                  {strand.substrands.map((substrand, subIndex) => (
                    <li key={subIndex} className="text-gray-700 text-base ml-4">
                      {substrand.name} - {substrand.activityCount} activities
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default CardComponent;
