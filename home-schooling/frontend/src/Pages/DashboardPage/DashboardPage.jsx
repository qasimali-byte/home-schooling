import { useContext, useEffect, useState } from "react";
import { AuthContext } from "../../App";
import CardComponent from "./CardComponet";
import LineChart from "./LineChart";
import MyCalender from "./Calendar";
import ActivityList from "./ActivityList";
import StudyActivities from "./ActivityList";

const DashboardPage = () => {
    const { iconMenu } = useContext(AuthContext);
    const [value, onChange] = useState(new Date());
    const subjects = [
      {
        subject: 'Mathematics',
        strands: [
          {
            name: 'Algebra',
            substrands: [
              { name: 'Linear Equations', activityCount: 10 },
              { name: 'Quadratic Equations', activityCount: 5 },
            ],
          },
          {
            name: 'Geometry',
            substrands: [
              { name: 'Triangles', activityCount: 8 },
              { name: 'Circles', activityCount: 7 },
            ],
          },
        ],
      },
      {
        subject: 'English',
        strands: [
          {
            name: 'Grammar',
            substrands: [
              { name: 'Parts of Speech', activityCount: 12 },
              { name: 'Punctuation', activityCount: 6 },
            ],
          },
          {
            name: 'Literature',
            substrands: [
              { name: 'Poetry', activityCount: 8 },
              { name: 'Prose', activityCount: 10 },
            ],
          },
        ],
      },
      {
        subject: 'Geography',
        strands: [
          {
            name: 'Physical Geography',
            substrands: [
              { name: 'Landforms', activityCount: 9 },
              { name: 'Climate', activityCount: 7 },
            ],
          },
          {
            name: 'Human Geography',
            substrands: [
              { name: 'Population', activityCount: 8 },
              { name: 'Cultural Regions', activityCount: 6 },
            ],
          },
        ],
      },
      {
        subject: 'Science',
        strands: [
          {
            name: 'Biology',
            substrands: [
              { name: 'Cell Biology', activityCount: 10 },
              { name: 'Genetics', activityCount: 8 },
            ],
          },
          {
            name: 'Physics',
            substrands: [
              { name: 'Mechanics', activityCount: 12 },
              { name: 'Thermodynamics', activityCount: 7 },
            ],
          },
        ],
      },
      {
        subject: 'Humanities and Social Sciences',
        strands: [
          {
            name: 'History',
            substrands: [
              { name: 'Ancient Civilizations', activityCount: 9 },
              { name: 'Modern History', activityCount: 8 },
            ],
          },
          {
            name: 'Social Sciences',
            substrands: [
              { name: 'Sociology', activityCount: 7 },
              { name: 'Psychology', activityCount: 6 },
            ],
          },
        ],
      },
      {
        subject: 'The Arts',
        strands: [
          {
            name: 'Visual Arts',
            substrands: [
              { name: 'Drawing', activityCount: 10 },
              { name: 'Painting', activityCount: 8 },
            ],
          },
          {
            name: 'Performing Arts',
            substrands: [
              { name: 'Drama', activityCount: 7 },
              { name: 'Music', activityCount: 9 },
            ],
          },
        ],
      },
    ];
    const studyActivities = [
      {
        name: 'Mathematics',
        description: 'Solved math problems for 1 hour.',
        strand: 'Algebra',
        substrand: 'Linear Equations',
      },
      {
        name: 'Reading',
        description: 'Read a book for 30 minutes.',
        strand: 'Language Arts',
        substrand: 'Comprehension',
      },
      {
        name: 'Science',
        description: 'Conducted a simple science experiment.',
        strand: 'Physics',
        substrand: 'Motion and Forces',
      },
      // Add more activities as needed
    ];
    useEffect(()=>{
      document.title="Home Schooling - Dashboard"
            },[])

   
    return (
        <div className={`p-3  h-full sm:ml-60 sm:mt-24 pt-30 rounded-tl-3xl   border-t border-r bg-gray-100`}>
                <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {/* Total Students Card */}
          {subjects.map((subject, index) => (
        <CardComponent key={index} {...subject} />
      ))}

         
        </section>

        {/* Recent Activities Section */}
        <section className="mt-8">
         <LineChart />
        </section>
        <section className="mt-8 flex justify-between p-3">
        <StudyActivities activities={studyActivities} date={value} />
          <MyCalender onChange={onChange} value={value} />
        </section>
        </div>

      );
}
 
export default DashboardPage;