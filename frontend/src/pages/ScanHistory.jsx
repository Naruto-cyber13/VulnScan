/**
 * Scan History Page
 * Displays list of previous scans
 */

import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'
import { getScanHistory } from '../api/scan.api'
import { getSeverityColor, getSeverityEmoji } from '../utils/severityColor'
import { formatDate } from '../utils/formatDate'
import Disclaimer from '../components/Disclaimer'

const ScanHistory = () => {
  const [scans, setScans] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const data = await getScanHistory(100)
        setScans(data. scans || [])
      } catch (err) {
        setError('Failed to load scan history')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    fetchHistory()
  }, [])

  const handleScanClick = (scan) => {
    navigate(`/scan-result/${scan.scan_id}`, { 
      state: { scanResult: scan } 
    })
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
      <Navbar />
      
      <main className="max-w-6xl mx-auto px-4 py-12">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">Scan History</h1>
          <p className="text-slate-400">View and revisit your previous security scans</p>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="glass-card p-12 text-center">
            <div className="inline-block mb-4">
              <svg className="animate-spin h-8 w-8 text-indigo-600" viewBox="0 0 24 24" fill="none">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
            </div>
            <p className="text-slate-400">Loading your scans...</p>
          </div>
        )}

        {/* Error State */}
        {error && ! loading && (
          <div className="glass-card bg-red-950/20 border-red-800/30 p-6 text-center">
            <p className="text-red-200 mb-4">❌ {error}</p>
            <Link to="/" className="btn-primary">Start New Scan</Link>
          </div>
        )}

        {/* Empty State */}
        {!loading && !error && scans.length === 0 && (
          <div className="glass-card p-12 text-center">
            <p className="text-4xl mb-4">📊</p>
            <h2 className="text-2xl font-bold text-white mb-2">No Scans Yet</h2>
            <p className="text-slate-400 mb-6">You haven't performed any security scans yet.</p>
            <Link to="/" className="btn-primary">Start Your First Scan</Link>
          </div>
        )}

        {/* Scans Grid */}
        {! loading && !error && scans. length > 0 && (
          <div className="grid grid-cols-1 md: grid-cols-2 lg: grid-cols-3 gap-4">
            {scans.map((scan, idx) => {
              const severityColor = getSeverityColor(scan.severity)
              const emoji = getSeverityEmoji(scan.severity)

              return (
                <button
                  key={idx}
                  onClick={() => handleScanClick(scan)}
                  className="glass-card p-6 text-left hover:border-indigo-600/50 transition-all hover:shadow-lg cursor-pointer group"
                >
                  {/* Header */}
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <p className="text-slate-500 text-xs font-semibold uppercase mb-2">
                        {scan.scan_type === 'URL' ? '🌐 Website Scan' : '📋 Log Analysis'}
                      </p>
                      <h3 className="text-white font-semibold truncate group-hover:text-indigo-400 transition-colors">
                        {scan.target}
                      </h3>
                    </div>
                  </div>

                  {/* Severity Badge */}
                  <div className="flex items-center justify-between mb-4">
                    <span 
                      className="px-3 py-1 rounded-full text-white text-xs font-semibold"
                      style={{ backgroundColor: severityColor + '30', color: severityColor }}
                    >
                      {emoji} {scan.severity}
                    </span>
                    <span className="text-slate-400 text-sm">
                      {scan.threat_count} threat{scan.threat_count !== 1 ? 's' : ''}
                    </span>
                  </div>

                  {/* Date */}
                  <p className="text-slate-500 text-xs">
                    {formatDate(scan.scanned_at)}
                  </p>

                  {/* Premium Badge */}
                  {scan. premium && (
                    <div className="mt-4 pt-4 border-t border-slate-800">
                      <span className="text-xs bg-purple-900/30 text-purple-300 px-2 py-1 rounded">
                        ✨ Premium
                      </span>
                    </div>
                  )}
                </button>
              )
            })}
          </div>
        )}

        {/* Actions */}
        <div className="mt-12">
          <Link to="/" className="btn-primary">
            Perform New Scan
          </Link>
        </div>
        {/* Disclaimer (MANDATORY) */}
        <Disclaimer />
      </main>
      

      <Footer />
    </div>
  )
}

export default ScanHistory