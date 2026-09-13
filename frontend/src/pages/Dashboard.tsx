import { useQuery } from '@tanstack/react-query'
import { TrendingUp, TrendingDown, Calendar } from 'lucide-react'

function Dashboard() {
  const { data: stats = {} } = useQuery(['dashboardStats'], async () => {
    console.log('Fetching dashboard stats...')
    return { progress: 58, assignmentsDue: 3, certificates: 2, badges: 5 }
  }, { retry: false })

  const { data: activityLog = [] } = useQuery(['activityLog'], async () => {
    console.log('Fetching recent activity...')
    return [
      { action: 'completed_lesson', time: '2 hours ago', icon: '✅' },
      { action: 'submitted_assignment', time: '5 hours ago', icon: '📤' },
      { action: 'earned_badge', time: '1 day ago', icon: '🎖️' },
    ]
  }, { retry: false })

  return (
    <div className="space-y-6">
      {/* Progress Card */}
      <section className="bg-gradient-to-br from-purple-500 to-indigo-600 rounded-lg p-8 text-white mb-8">
        <h2 className="text-2xl font-bold mb-2">Learning Progress</h2>
        <div className="flex items-end gap-4">
          <p className="text-5xl font-bold">{stats.progress}%</p>
          <div className="ml-auto flex flex-col items-end">
            <span className="text-sm opacity-80">Overall Completion</span>
            <span className="text-lg flex items-center gap-1 mt-1">
              {Math.random() > 0.5 ? 
                <TrendingUp className="h-5 w-5" /> : 
                <TrendingDown className="h-5 w-5" />}
            </span>
          </div>
        </div>
      </section>

      {/* Stats Grid */}
      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700 text-center">
          <Calendar className="h-10 w-10 mx-auto mb-3 text-blue-500" />
          <p className="text-3xl font-bold text-gray-900 dark:text-white">{stats.assignmentsDue}</p>
          <p className="text-sm text-gray-500 mt-1">Assignments Due</p>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700 text-center">
          <TrophyIcon className="h-10 w-10 mx-auto mb-3 text-yellow-500" />
          <p className="text-3xl font-bold text-gray-900 dark:text-white">{stats.badges}</p>
          <p className="text-sm text-gray-500 mt-1">Badges Earned</p>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700 text-center">
          <CertIcon className="h-10 w-10 mx-auto mb-3 text-green-500" />
          <p className="text-3xl font-bold text-gray-900 dark:text-white">{stats.certificates}</p>
          <p className="text-sm text-gray-500 mt-1">Certificates</p>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700 text-center">
          <UsersIcon className="h-10 w-10 mx-auto mb-3 text-indigo-500" />
          <p className="text-3xl font-bold text-gray-900 dark:text-white">4</p>
          <p className="text-sm text-gray-500 mt-1">Courses in Progress</p>
        </div>
      </section>

      {/* Recent Activity */}
      <section className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
        <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Recent Activity</h3>
        {activityLog.map((activity: any, idx: number) => (
          <div key={idx} className="flex items-center gap-4 py-3 border-b border-gray-200 dark:border-gray-700 last:border-b-0">
            <span className="text-xl">{activity.icon}</span>
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-900 dark:text-white">{activity.action}</p>
              <p className="text-xs text-gray-500">{activity.time}</p>
            </div>
          </div>
        ))}
        {activityLog.length === 0 && (
          <p className="text-sm text-gray-500 text-center py-4">No recent activity. Start learning!</p>
        )}
      </section>
    </div>
  )
}

// Simple inline icons to avoid external dependencies
function TrophyIcon(props: any) { return <svg {...props}><path d="M12 15c-1.66.54-3.69-1.69-3.69-2.73a2.86 2.86 0 0 1 5.38-.33A2.85 2.85 0 0 1 12 15z"/><path d="M5.5 4c0-2.5 2-4.5 4.5-4.5s4.5 2 4.5 4.5v4a6 6 0 0 1-9 0v-4zM7 13h8l-2-2H7l-2 2z"/></svg>}
function CertIcon(props: any) { return <svg {...props}><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>}
function UsersIcon(props: any) { return <svg {...props}><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>}

export default Dashboard
