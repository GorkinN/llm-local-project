import { useQuery } from '@tanstack/react-query'
import { FileText, Clock, CheckCircle, AlertCircle } from 'lucide-react'

function Assignments() {
  const { data: assignments = [] } = useQuery(['assignments'], async () => {
    console.log('Fetching assignments...')
    return [
      { id: 1, courseId: 1, title: 'Build a Todo App', dueDate: '2024-09-15', status: 'submitted', points: 100 },
      { id: 2, courseId: 1, title: 'Create an API Service', dueDate: '2024-09-16', status: 'in-progress', points: 80 },
    ]
  }, { retry: false })

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Assignments</h1>
      
      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50 dark:bg-gray-900 sticky top-0 z-10">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Assignment</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Course</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Due Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Points</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 dark:divide-gray-800">
            {assignments.map((assignment: any) => (
              <tr key={assignment.id} className="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center gap-3">
                    <FileText className="h-5 w-5 text-blue-500" />
                    <span className="font-medium text-gray-900 dark:text-white">{assignment.title}</span>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  React Fundamentals
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {new Date(assignment.dueDate).toLocaleDateString()}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {assignment.status === 'submitted' ? (
                    <span className="flex items-center gap-1 text-green-600"><CheckCircle className="h-4 w-4" /> Submitted</span>
                  ) : (
                    <span className="flex items-center gap-1 text-blue-600"><AlertCircle className="h-4 w-4" /> In Progress</span>
                  )}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {assignment.points} pts
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Assignments
