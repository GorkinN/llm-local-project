import { useQuery } from '@tanstack/react-query'
import { BookOpen, Clock, Calendar, ArrowRight } from 'lucide-react'

function Home() {
  const { data: userStats } = useQuery(['userStats'], async () => {
    // Mock API call - replace with actual Axios service
    console.log('Fetching user stats...')
    return { totalCourses: 12, hoursWatched: 34.5, assignmentsDue: 2 }
  }, { retry: false })

  const { data: ongoingCourses = [] } = useQuery(['ongoingCourses'], async () => {
    console.log('Fetching ongoing courses...')
    return [{ 
      title: 'React Fundamentals', 
      progress: 45, 
      instructor: 'John Smith' 
    }, { 
      title: 'Advanced TypeScript', 
      progress: 72, 
      instructor: 'Sarah Jones' 
    }]
  }, { retry: false })

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <section className="bg-gradient-to-r from-blue-500 to-indigo-600 rounded-lg p-8 text-white mb-8">
        <h1 className="text-3xl font-bold mb-2">Welcome back! 👋</h1>
        <p className="opacity-90 max-w-xl">Here are your updates for today. You have {userStats?.assignmentsDue} assignments due soon.</p>
      </section>

      {/* Stats Overview */}
      <section>
        <h2 className="text-xl font-semibold mb-4">Overview</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <BookOpen className="h-8 w-8 text-blue-500" />
              <span className="text-sm text-gray-500">Total Courses</span>
            </div>
            <p className="text-3xl font-bold">{userStats?.totalCourses}</p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <Clock className="h-8 w-8 text-green-500" />
              <span className="text-sm text-gray-500">Hours Watched</span>
            </div>
            <p className="text-3xl font-bold">{userStats?.hoursWatched}</p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <Calendar className="h-8 w-8 text-red-500" />
              <span className="text-sm text-gray-500">Due Today</span>
            </div>
            <p className="text-3xl font-bold text-red-500">{userStats?.assignmentsDue}</p>
          </div>
        </div>
      </section>

      {/* Continue Watching */}
      <section>
        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <Clock className="h-5 w-5" />
          Continue Watching
        </h2>
        {ongoingCourses.map((course: any) => (
          <div key={course.title} className="bg-white dark:bg-gray-800 rounded-lg overflow-hidden shadow-sm border border-gray-200 dark:border-gray-700 mb-4">
            <div className="p-6 flex items-center gap-4">
              <div className="flex-1 min-w-0">
                <h3 className="font-semibold text-gray-900 dark:text-white truncate">{course.title}</h3>
                <p className="text-sm text-gray-500 mt-1">{course.instructor}</p>
                <div className="mt-3 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div 
                    className="bg-blue-500 h-2 rounded-full transition-all" 
                    style={{ width: `${course.progress}%` }}
                  ></div>
                </div>
                <span className="text-xs text-gray-500 mt-1">{course.progress}% complete</span>
              </div>
              <button className="ml-auto flex items-center gap-2 px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors">
                Continue <ArrowRight className="h-4 w-4" />
              </button>
            </div>
          </div>
        ))}
        {ongoingCourses.length === 0 && (
          <p className="text-gray-500 text-center py-8">You have no ongoing courses. Explore our catalog!</p>
        )}
      </section>
    </div>
  )
}

export default Home
