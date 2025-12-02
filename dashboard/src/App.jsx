import { useState } from 'react'
import progressData from './data/progress.json'
import SolutionViewer from './components/SolutionViewer'

function App() {
  const [selectedDay, setSelectedDay] = useState(null)
  const [selectedLang, setSelectedLang] = useState(null)
  const [activeTab, setActiveTab] = useState('task') // 'task' or 'solution'

  // Convert object to array for easier mapping
  const days = Object.values(progressData).sort((a, b) => a.day - b.day)

  const handleDayClick = (dayData) => {
    setSelectedDay(dayData)
    // Default to solution if available, otherwise task
    if (dayData.solutions && Object.keys(dayData.solutions).length > 0) {
      setActiveTab('solution')
      setSelectedLang(Object.keys(dayData.solutions)[0])
    } else {
      setActiveTab('task')
    }
  }

  const closeSolution = () => {
    setSelectedDay(null)
    setSelectedLang(null)
    setActiveTab('task')
  }

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
              onClick={() => handleDayClick(dayData)}
              className={`rounded-xl p-6 border transition-all duration-300 group relative overflow-hidden
                ${dayData.status === 'not_started' ? 'bg-slate-800 border-slate-700 hover:border-slate-500 cursor-default' : ''}
                ${dayData.status === 'in_progress' ? 'bg-slate-800 border-yellow-500/50 hover:border-yellow-400 cursor-pointer' : ''}
                ${dayData.status === 'completed' ? 'bg-slate-800 border-green-500/50 hover:border-green-400 cursor-pointer' : ''}
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

      {/* Modal */}
      {selectedDay && (
        <div className="fixed inset-0 bg-black/80 flex items-center justify-center p-4 z-50" onClick={closeSolution}>
          <div className="bg-slate-800 rounded-xl w-full max-w-5xl max-h-[90vh] flex flex-col shadow-2xl border border-slate-700" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between p-6 border-b border-slate-700">
              <div className="flex items-center gap-4">
                <h2 className="text-2xl font-bold text-white">Day {selectedDay.day}</h2>
                <div className="flex bg-slate-900 rounded-lg p-1">
                  <button
                    onClick={() => setActiveTab('task')}
                    className={`px-4 py-1.5 rounded-md text-sm font-medium transition-all ${activeTab === 'task'
                        ? 'bg-slate-700 text-white shadow-sm'
                        : 'text-slate-400 hover:text-slate-200'
                      }`}
                  >
                    Task
                  </button>
                  <button
                    onClick={() => setActiveTab('solution')}
                    disabled={!selectedDay.solutions || Object.keys(selectedDay.solutions).length === 0}
                    className={`px-4 py-1.5 rounded-md text-sm font-medium transition-all ${activeTab === 'solution'
                        ? 'bg-slate-700 text-white shadow-sm'
                        : 'text-slate-400 hover:text-slate-200 disabled:opacity-50 disabled:cursor-not-allowed'
                      }`}
                  >
                    Solution
                  </button>
                </div>
              </div>
              <button onClick={closeSolution} className="text-slate-400 hover:text-white transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {activeTab === 'solution' && (
              <div className="flex border-b border-slate-700 px-6 bg-slate-900/50">
                {Object.keys(selectedDay.solutions).map(lang => (
                  <button
                    key={lang}
                    onClick={() => setSelectedLang(lang)}
                    className={`px-4 py-3 text-sm font-medium transition-colors border-b-2 ${selectedLang === lang
                        ? 'border-green-500 text-green-400'
                        : 'border-transparent text-slate-400 hover:text-slate-200'
                      }`}
                  >
                    {lang.toUpperCase()}
                  </button>
                ))}
              </div>
            )}

            <div className="flex-1 overflow-auto p-6 bg-[#1e1e1e]">
              {activeTab === 'task' ? (
                selectedDay.html ? (
                  <div className="prose prose-invert max-w-none" dangerouslySetInnerHTML={{ __html: selectedDay.html }} />
                ) : (
                  <div className="text-center py-12 text-slate-500">
                    <p className="text-xl">No task description available.</p>
                    <p className="mt-2 text-sm">Run the update script to fetch task details.</p>
                  </div>
                )
              ) : (
                selectedLang && selectedDay.solutions[selectedLang] && (
                  <SolutionViewer
                    code={selectedDay.solutions[selectedLang].content}
                    language={selectedLang === 'cpp' ? 'cpp' : selectedLang}
                    highlightRanges={selectedDay.solutions[selectedLang].highlight_ranges}
                  />
                )
              )}
            </div>

            {activeTab === 'task' && (
              <div className="p-4 border-t border-slate-700 bg-slate-800 flex justify-end">
                <a
                  href={`https://adventofcode.com/2025/day/${selectedDay.day}`}
                  target="_blank"
                  rel="noreferrer"
                  className="flex items-center gap-2 text-green-500 hover:text-green-400 transition-colors text-sm font-medium"
                >
                  View on AdventOfCode.com &rarr;
                </a>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default App
