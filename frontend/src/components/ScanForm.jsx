/**
 * Scan Form Component
 * Supports both Website URL scans and Log scans
 */

import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { scanUrl, scanLog } from '../api/scan.api'
import Disclaimer from './Disclaimer'

const ScanForm = () => {
  const [scanType, setScanType] = useState('url') // 'url' | 'log'
  const [url, setUrl] = useState('')
  const [logData, setLogData] = useState('')
  const [premium, setPremium] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [logFilename, setLogFilename] = useState('pasted_log.txt')


  const navigate = useNavigate()

  // Validate URL format
  const isValidUrl = (string) => {
    try {
      new URL(string)
      return true
    } catch {
      return false
    }
  }

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    try {
      let result
      

      /* ===========================
         URL SCAN
      =========================== */
      if (scanType === 'url') {
        if (!url.trim()) {
          setError('Please enter a website URL')
          return
        }

        let urlToScan = url.trim()
        if (!urlToScan.startsWith('http://') && !urlToScan.startsWith('https://')) {
          urlToScan = 'https://' + urlToScan
        }

        if (!isValidUrl(urlToScan)) {
          setError('Please enter a valid URL (e.g., https://example.com)')
          return
        }

        setLoading(true)
        result = await scanUrl(urlToScan, premium)
      }

      /* ===========================
         LOG SCAN
      =========================== */
      if (scanType === 'log') {
        if (!logData.trim()) {
          setError('Please paste log data to scan')
          return
        }

        setLoading(true)
        result = await scanLog({
          logContent: logData,
          filename: logFilename,
          premium
      })
      }

      // Store scan result for result page
      if (!result || !result.scan_id) {
        throw new Error('Invalid scan response from server')
      }

      sessionStorage.setItem('scanResult', JSON.stringify(result))

      navigate(`/scan-result/${result.scan_id}`, {
        state: { scanResult: result }
      })

    } catch (err) {
  console.error(err)

  if (err.response?.data?.detail) {
    setError(
      Array.isArray(err.response.data.detail)
        ? err.response.data.detail[0].msg
        : err.response.data.detail
    )
  } else {
    setError('Scan failed. Please check backend logs.')
  }

  return   // ⬅️ THIS LINE IS MANDATORY
} finally {
  setLoading(false)
}

  }

  return (
    <div className="space-y-6">
      <form onSubmit={handleSubmit} className="glass-card p-8 space-y-6">

        {/* Scan Type Toggle */}
        
<div className="flex gap-4">
  <button
    type="button"
    onClick={() => {
      setScanType('url')
      setLogData('')
    }}
    className={`px-4 py-2 rounded-lg font-medium transition-all ${
      scanType === 'url'
        ? 'bg-indigo-600 text-white'
        : 'bg-slate-800 text-slate-400'
    }`}
  >
    🌐 Website Scan
  </button>

  <button
    type="button"
    onClick={() => {
      setScanType('log')
      setUrl('')
      setPremium(false)
    }}
    className={`px-4 py-2 rounded-lg font-medium transition-all ${
      scanType === 'log'
        ? 'bg-indigo-600 text-white'
        : 'bg-slate-800 text-slate-400'
    }`}
  >
    📄 Log Scan
  </button>
</div>


        {/* Header */}
        <div>
          <h2 className="text-3xl font-bold text-white mb-2">
            {scanType === 'url'
              ? 'Website Security Scanner'
              : 'Log Security Scanner'}
          </h2>
          <p className="text-slate-400">
            {scanType === 'url'
              ? 'Get instant security insights about any website'
              : 'Analyze security events from application or server logs'}
          </p>
        </div>

        {/* URL Input */}
        {scanType === 'url' && (
          <div>
            <label className="block text-sm font-semibold text-slate-300 mb-2">
              Website URL
            </label>
            <div className="relative">
              <input
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="e.g., example.com or https://example.com"
                disabled={loading}
                className="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-600"
              />
              <span className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500">
                🔗
              </span>
            </div>
          </div>
        )}

        {/* Log Input */}
        {scanType === 'log' && (
      <>
      <div>
      <label className="block text-sm font-semibold text-slate-300 mb-2">
        Log File Name
      </label>
      <input
        type="text"
        value={logFilename}
        onChange={(e) => setLogFilename(e.target.value)}
        placeholder="e.g., access.log"
        disabled={loading}
        className="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-600"
      />
      </div>

      <div>
      <label className="block text-sm font-semibold text-slate-300 mb-2">
        Log Data
      </label>
      <textarea
        rows={8}
        value={logData}
        onChange={(e) => setLogData(e.target.value)}
        placeholder="Paste your log content here..."
        disabled={loading}
        className="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white resize-none focus:outline-none focus:ring-2 focus:ring-indigo-600"
      />
      </div>
      </>
      )}

        {/* Premium Toggle (URL scan only) */}
        {(scanType === 'url' || scanType === 'log') && (
          <div className="flex items-center gap-3">
            <input
              id="premium"
              type="checkbox"
              checked={premium}
              onChange={(e) => setPremium(e.target.checked)}
              disabled={loading}
              className="w-4 h-4 rounded bg-slate-800 border-slate-700 text-indigo-600 focus:ring-indigo-600"
            />
            <label htmlFor="premium" className="text-sm text-slate-400">
              Enable premium analysis (full threat breakdown & insights)
            </label>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="bg-red-950/50 border border-red-800/50 rounded-lg p-3">
            <p className="text-red-200 text-sm flex items-center gap-2">
              <span>❌</span> {error}
            </p>
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          disabled={loading}
          className="w-full btn-primary py-3 font-semibold disabled:opacity-50 flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24" fill="none">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              Scanning...
            </>
          ) : (
            <>
              <span>🔍</span>
              Start Security Scan
            </>
          )}
        </button>
      </form>

      {/* Disclaimer */}
      <Disclaimer />

      {/* Info Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="glass-card p-4">
          <h3 className="text-white font-semibold mb-2 flex items-center gap-2">
            🔒 HTTPS Check
          </h3>
          <p className="text-slate-400 text-sm">Verify SSL/TLS encryption status</p>
        </div>
        <div className="glass-card p-4">
          <h3 className="text-white font-semibold mb-2 flex items-center gap-2">
            🛡️ Headers Analysis
          </h3>
          <p className="text-slate-400 text-sm">Detect missing security headers</p>
        </div>
        <div className="glass-card p-4">
          <h3 className="text-white font-semibold mb-2 flex items-center gap-2">
            📊 Risk Score
          </h3>
          <p className="text-slate-400 text-sm">Get instant security assessment</p>
        </div>
      </div>
    </div>
  )
}

export default ScanForm
