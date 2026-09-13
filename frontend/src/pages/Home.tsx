import React from 'react'
import { Card } from '../components/Card'
import { Button } from '../components/Button'
import Badge from '../components/Badge'

export function Home() {
  return (
    <div className="max-w-7xl mx-auto space-y-8">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary-50 via-white to-secondary-50 rounded-2xl p-8 md:p-12 text-center">
        <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary-600 via-neutral-800 to-secondary-600 mb-4">
          Welcome to LMS Dashboard
        </h1>
        <p className="text-lg text-neutral-600 max-w-2xl mx-auto mb-8">
          Track your courses, assignments, and progress all in one place. 
          Designed for students who want a modern learning experience.
        </p>
        <div className="flex justify-center gap-4 flex-wrap">
          <Button size="lg" onClick={(e) => e.preventDefault()}>
            View My Courses
          </Button>
          <Button variant="outline" size="lg" onClick={(e) => e.preventDefault()}>
            Create Assignment
          </Button>
        </div>
      </section>

      {/* Stats Section */}
      <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card href="#courses" title="Active Courses" description="Currently enrolled">
          <div className="text-3xl font-bold text-primary-600">5</div>
        </Card>

        <Card href="#assignments" title="Upcoming Assignments" description="Due this week">
          <div className="text-3xl font-bold text-warning-600">8</div>
        </Card>

        <Card href="#dashboard" title="Completed Projects" description="This semester">
          <div className="text-3xl font-bold text-success-600">23</div>
        </Card>

        <Card title="GPA">
          <div className="text-4xl font-bold text-neutral-800 mb-1">3.8<span className="text-sm text-neutral-500 ml-1">/4.0</span></div>
          <Badge variant="success" size="sm" className="mt-2 inline-block self-end">Dean&apos;s List</Badge>
        </Card>
      </section>

      {/* Quick Actions */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card href="#courses" title="Browse Courses">
          <Button variant="outline" size="sm" onClick={() => window.location.hash = '/courses'}>
            📚 View Course Catalog
          </Button>
        </Card>

        <Card title="My Assignments">
          <div className="text-sm text-neutral-600 mb-3">You have 8 assignments due this week.</div>
          <Button variant="outline" size="sm" onClick={() => window.location.hash = '/assignments'}>
            Check Deadlines
          </Button>
        </Card>

        <Card title="Study Groups">
          <div className="text-sm text-neutral-600 mb-3">Join or create study groups for your courses.</div>
          <Button variant="secondary" size="sm" onClick={() => window.location.hash = '/profile'}>
            Find Peers
          </Button>
        </Card>
      </section>

      {/* Recent Activity */}
      <section>
        <h2 className="text-2xl font-semibold mb-4 text-neutral-800">Recent Activity</h2>
        <div className="bg-white rounded-xl border border-neutral-200 divide-y divide-neutral-100 max-w-md">
          <div className="p-4 hover:bg-neutral-50 transition-colors cursor-pointer" onClick={() => window.location.hash = '/courses'}>
            <div className="flex items-start gap-3">
              <span className="text-xl">🎓</span>
              <div className="flex-1">
                <p className="font-medium text-neutral-800">Started Course Enrollment</p>
                <p className="text-sm text-neutral-500 mt-0.5">Advanced React Patterns • 2 hours ago</p>
              </div>
            </div>
          </div>

          <div className="p-4 hover:bg-neutral-50 transition-colors cursor-pointer" onClick={() => window.location.hash = '/assignments'}>
            <div className="flex items-start gap-3">
              <span className="text-xl">📝</span>
              <div className="flex-1">
                <p className="font-medium text-neutral-800">Assignment Submitted</p>
                <p className="text-sm text-neutral-500 mt-0.5">Data Structures Quiz (Score: 85%) • Today, 4:32 PM</p>
              </div>
            </div>
          </div>

          <div className="p-4 hover:bg-neutral-50 transition-colors cursor-pointer" onClick={() => window.location.hash = '/dashboard'}>
            <div className="flex items-start gap-3">
              <span className="text-xl">⭐</span>
              <div className="flex-1">
                <p className="font-medium text-neutral-800">Course Rating Updated</p>
                <p className="text-sm text-neutral-500 mt-0.5">Advanced React Patterns now has 4.7★ (1,234 reviews) • Yesterday</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

export default Home
