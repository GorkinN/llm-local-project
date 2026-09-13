import { useQuery } from '@tanstack/react-query'
import { BookOpen, Star, Clock } from 'lucide-react'

function Courses() {
  const { data: courses = [] } = useQuery(['courses'], async () => {
    console.log('Fetching courses...')
    return [
      { id: 1, title: 'React Fundamentals', instructor: 'John Smith', duration: '8h', rating: 4.8, enrolled: 1204, status: 'in-progress' },
      { id: 2, title: 'Advanced TypeScript', instructor: 'Sarah Jones', duration: '6h', rating: 4.9, enrolled: 892, status: 'not-started' },
      { id: 3, title: 'Full React Stack', instructor: 'Mike Wilson', duration: '12h', rating: 4.7, enrolled: 756, status: 'completed' },
    ]
  }, { retry: false })

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">My Courses</h1>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {courses.map((course: any) => (
          <div key={course.id} className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden hover:shadow-md transition-shadow">
            <div className="p-6">
              <div className="flex items-start justify-between mb-4">
                <BookOpen className="h-10 w-10 text-blue-500" />
                {course.status === 'in-progress' && (
                  <span className="px-2 py-1 bg-green-100 dark:bg-green-900/30 text-green-700 text-xs rounded-full">In Progress</span>
                )}
              </div>
              
              <h3 className="font-semibold text-lg mb-1 text-gray-900 dark:text-white">{course.title}</h3>
              <p className="text-sm text-gray-500 mb-2">{course.instructor}</p>
              
              <div className="flex items-center gap-4 text-sm text-gray-500 mb-4">
                <span className="flex items-center gap-1"><Clock className="h-4 w-4" /> {course.duration}</span>
                <span className="flex items-center gap-1"><Star className="h-4 w-4 fill-yellow-400" /> {course.rating}</span>
              </div>
              
              <button className={`w-full py-2 rounded-lg text-white transition-colors ${
                course.status === 'in-progress' 
                  ? 'bg-green-500 hover:bg-green-600' 
                  : 'bg-blue-500 hover:bg-blue-600'
              }`}>
                {course.status === 'completed' ? 'Completed ✓' : 'Continue'}
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Courses
