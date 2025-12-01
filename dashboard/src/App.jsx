import { useState } from 'react'
import progressData from './data/progress.json'

function App() {
  // Convert object to array for easier mapping
  const days = Object.values(progressData).sort((a, b) => a.day - b.day)

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8">
      <header className="mb-12 text-center">
        <h1 className="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-emerald-600 mb-4">
          Advent of Code 2025
        </h1>
        <p className="text-slate-400 text-xl">Progress Dashboard</p>
      </header>

      <main className="max-w-6xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {days.map((dayData) => (
            <div
              key={dayData.day}
              className={`rounded-xl p-6 border transition-all duration-300 group cursor-pointer relative overflow-hidden
                ${dayData.status === 'not_started' ? 'bg-slate-800 border-slate-700 hover:border-slate-500' : ''}
                ${dayData.status === 'in_progress' ? 'bg-slate-800 border-yellow-500/50 hover:border-yellow-400' : ''}
                ${dayData.status === 'completed' ? 'bg-slate-800 border-green-500/50 hover:border-green-400' : ''}
              `}
            >
              <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                <span className="text-6xl font-bold">
                  {dayData.day}
                </span>
              </div>

              <h2 className="text-2xl font-bold mb-2 text-slate-200">Day {dayData.day}</h2>
              <div className="flex items-center gap-2 mb-4">
                <span className={`w-3 h-3 rounded-full 
                  ${dayData.status === 'not_started' ? 'bg-slate-600' : ''}
                  ${dayData.status === 'in_progress' ? 'bg-yellow-500' : ''}
                  ${dayData.status === 'completed' ? 'bg-green-500' : ''}
                `}></span>
                <span className="text-sm text-slate-400 capitalize">{dayData.status.replace('_', ' ')}</span>
              </div>

              <div className="flex gap-2 mt-4 flex-wrap">
                {dayData.languages.map(lang => (
                  <span key={lang} className="text-xs px-2 py-1 rounded bg-slate-700 text-slate-300 border border-slate-600">
                    {lang}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  )
}

export default App
