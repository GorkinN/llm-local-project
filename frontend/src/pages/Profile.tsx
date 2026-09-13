import { useQuery } from '@tanstack/react-query'
import { Edit2, Upload } from 'lucide-react'

function Profile() {
  const { data: user = {} } = useQuery(['profile'], async () => {
    console.log('Fetching profile...')
    return {
      name: 'Alex Johnson',
      email: 'alex.j@email.com',
      bio: 'Frontend developer passionate about React and TypeScript.',
      avatar: null, // Placeholder for actual image upload logic
      level: 5,
      joined: '2024-01-15'
    }
  }, { retry: false })

  return (
    <div className="space-y-6">
      {/* Profile Header */}
      <section className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden mb-8">
        <div className="h-32 bg-gradient-to-r from-blue-500 to-indigo-600"></div>
        
        <div className="px-6 pb-6 relative">
          {/* Avatar */}
          <div className="absolute -top-16 left-6">
            {user.avatar ? (
              <img src={user.avatar} alt="Avatar" className="w-32 h-32 rounded-full border-4 border-white dark:border-gray-800 object-cover shadow-md" />
            ) : (
              <div className="w-32 h-32 rounded-full bg-indigo-100 dark:bg-indigo-900/50 flex items-center justify-center text-6xl font-bold text-indigo-500">
                {user.name?.split(' ').map(n => n[0]).join('').toUpperCase() || 'U'}
              </div>
            )}
          </div>
          
          <div className="mt-14 max-w-xl ml-auto">
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">{user.name}</h1>
            <p className="text-blue-500 hover:underline cursor-pointer mb-2">{user.email}</p>
            
            <div className="flex items-center gap-4 mb-3">
              <span className="px-3 py-1 bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 rounded-full text-sm font-medium">
                Level {user.level}
              </span>
              <span className="text-sm text-gray-500">Joined {new Date(user.joined).toLocaleDateString()}</span>
            </div>
            
            {/* Edit Button */}
            <button className="px-4 py-2 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg text-sm transition-colors flex items-center gap-2">
              <Edit2 className="h-4 w-4" />
              Edit Profile
            </button>
          </div>
        </div>
      </section>

      {/* Bio Section */}
      <section className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
        <h2 className="text-lg font-semibold mb-3 text-gray-900 dark:text-white">About</h2>
        <p className="text-gray-600 dark:text-gray-400">{user.bio || 'No bio yet.'}</p>
      </section>

      {/* Skills Placeholder */}
      <section className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
        <h2 className="text-lg font-semibold mb-3 text-gray-900 dark:text-white">Skills</h2>
        <div className="flex flex-wrap gap-2">
          {['React', 'TypeScript', 'JavaScript', 'HTML/CSS', 'Git'].map(skill => (
            <span key={skill} className="px-3 py-1 bg-gray-100 dark:bg-gray-700 rounded-full text-sm text-gray-600 dark:text-gray-400">
              {skill}
            </span>
          ))}
        </div>
      </section>

      {/* Avatar Upload Placeholder */}
      {!user.avatar && (
        <section className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6 text-center">
          <h2 className="text-lg font-semibold mb-3 text-gray-900 dark:text-white">Upload Profile Picture</h2>
          <button className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-500 hover:bg-indigo-600 text-white rounded-lg transition-colors">
            <Upload className="h-4 w-4" />
            Upload Photo
          </button>
        </section>
      )}
    </div>
  )
}

export default Profile
