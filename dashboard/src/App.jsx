import { useState } from 'react'
import progressData from './data/progress.json'

function App() {
  // Convert object to array for easier mapping
  const days = Object.values(progressData).sort((a, b) => a.day - b.day)

  const [selectedDay, setSelectedDay] = useState(null)

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
              onClick={() => setSelectedDay(dayData)}
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

      {/* Task Detail Modal */}
      {selectedDay && (
        <div className="fixed inset-0 bg-black/80 flex items-center justify-center p-4 z-50" onClick={() => setSelectedDay(null)}>
          <div className="bg-[#0f0f23] rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto border border-[#333340] shadow-2xl" onClick={e => e.stopPropagation()}>
            <div className="p-8">
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h2 className="text-3xl font-bold text-[#00cc00] mb-2" style={{ textShadow: '0 0 2px #00cc00' }}>
                    {selectedDay.title || `Day ${selectedDay.day}`}
                  </h2>
                  <div className="flex items-center gap-2">
                    <span className={`px-3 py-1 rounded-full text-sm font-medium
                      ${selectedDay.status === 'not_started' ? 'bg-slate-700 text-slate-300' : ''}
                      ${selectedDay.status === 'in_progress' ? 'bg-yellow-500/20 text-yellow-500' : ''}
                      ${selectedDay.status === 'completed' ? 'bg-green-500/20 text-green-500' : ''}
                    `}>
                      {selectedDay.status.replace('_', ' ').toUpperCase()}
                    </span>
                  </div>
                </div>
                <button
                  onClick={() => setSelectedDay(null)}
                  className="p-2 hover:bg-[#333340] rounded-lg transition-colors text-slate-400 hover:text-white"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                </button>
              </div>

              {selectedDay.html ? (
                <div className="day-desc">
                  <div dangerouslySetInnerHTML={{ __html: selectedDay.html }} />
                </div>
              ) : (
                <div className="text-center py-12 text-slate-500">
                  <p className="text-xl">No task description available.</p>
                  <p className="mt-2 text-sm">Run the update script to fetch task details.</p>
                </div>
              )}

              <div className="mt-8 pt-6 border-t border-[#333340] flex justify-end">
                <a
                  href={`https://adventofcode.com/2025/day/${selectedDay.day}`}
                  target="_blank"
                  rel="noreferrer"
                  className="flex items-center gap-2 text-[#009900] hover:text-[#99ff99] transition-colors"
                >
                  [View on AdventOfCode.com]
                </a>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default App
