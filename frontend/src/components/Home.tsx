import { BookOpen, Clock, Calendar } from 'lucide-react'

function Home() {
  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <section className="bg-gradient-to-r from-blue-500 to-indigo-600 rounded-lg p-8 text-white dashboard-cards">
        <h1 className="text-3xl font-bold mb-2">Welcome back! 👋</h1>
        <p className="opacity-90">Here are your updates for today...</p>
      </section>

      {/* Stats Overview */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <BookOpen className="h-8 w-8 text-blue-500" />
            <span className="text-sm text-gray-500">Total Courses</span>
          </div>
          <p className="text-3xl font-bold">12</p>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <Clock className="h-8 w-8 text-green-500" />
            <span className="text-sm text-gray-500">Hours Watched</span>
          </div>
          <p className="text-3xl font-bold">34.5</p>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <Calendar className="h-8 w-8 text-purple-500" />
            <span className="text-sm text-gray-500">Due Today</span>
          </div>
          <p className="text-3xl font-bold text-red-500">2</p>
        </div>
      </section>

      {/* Continue Watching */}
      <section>
        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <BookOpen className="h-5 w-5" />
          Continue Watching
        </h2>
        <div className="bg-white dark:bg-gray-800 rounded-lg overflow-hidden shadow-sm border border-gray-200 dark:border-gray-700"></div>
      </section>
    </div>
  )
}

export default Home
