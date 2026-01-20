/**
 * Scan Result Page
 * Displays detailed scan results and findings
 */

import { useEffect, useState } from 'react'
import { useParams, useLocation, Link } from 'react-router-dom'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'
import ScanResultCard from '../components/ScanResultCard'
import VulnerabilityItem from '../components/VulnerabilityItem'
import Disclaimer from '../components/Disclaimer'
import { getSeverityColor, getSeverityEmoji } from '../utils/severityColor'
import { formatDate } from '../utils/formatDate'

const ScanResult = () => {
  const { scanId } = useParams()
  const location = useLocation()
  const [result, setResult] = useState(location.state?.scanResult || null)
  const [loading, setLoading] = useState(! result)
  const [activeTab, setActiveTab] = useState('overview')

  useEffect(() => {
    // Try to get result from location state, or sessionStorage
    if (! result) {
      const stored = sessionStorage.getItem('scanResult')
      if (stored) {
        setResult(JSON.parse(stored))
      }
      setLoading(false)
    }
  }, [result])

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
        <Navbar />
        <div className="flex items-center justify-center min-h-[60vh]">
          <p className="text-slate-400">Loading scan results...</p>
        </div>
      </div>
    )
  }

  if (!result) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
        <Navbar />
        <main className="max-w-4xl mx-auto px-4 py-16">
          <div className="glass-card p-8 text-center">
            <h2 className="text-2xl font-bold text-white mb-2">No Results Found</h2>
            <p className="text-slate-400 mb-6">The scan results could not be loaded. </p>
            <Link to="/" className="btn-primary">Start New Scan</Link>
          </div>
        </main>
      </div>
    )
  }

  const severityColor = getSeverityColor(result.severity)
  const severityEmoji = getSeverityEmoji(result.severity)
  const threatCount = result.threat_count || 0

  // Determine if this is URL or Log scan
  const isUrlScan = !!result.target_url
  const isLogScan = !!result.filename

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
      <Navbar />
      
      <main className="max-w-6xl mx-auto px-4 py-12">
        {/* Header Card */}
        <div className="glass-card p-8 mb-8 border-b-2" style={{ borderBottomColor: severityColor + '40' }}>
          <div className="flex items-start justify-between mb-6">
            <div>
              <h1 className="text-4xl font-bold text-white mb-2 flex items-center gap-3">
                <span>{severityEmoji}</span> 
                Security Scan Report
              </h1>
              <p className="text-slate-400">
                Scan ID: <code className="bg-slate-800 px-2 py-1 rounded text-slate-200 font-mono text-sm">{result.scan_id}</code>
              </p>
            </div>
            <div className="text-right">
              <div 
                className="px-6 py-3 rounded-lg font-bold text-lg mb-2 inline-block"
                style={{ backgroundColor: severityColor + '20', color: severityColor }}
              >
                {result.severity} RISK
              </div>
              <p className="text-slate-400 text-sm">Score: {result.severity_score?. toFixed(1) || 'N/A'}/10</p>
            </div>
          </div>

          {/* Target Info */}
          <div className="grid grid-cols-1 md: grid-cols-3 gap-6 bg-slate-900/50 rounded-lg p-6 border border-slate-800">
            <div>
              <p className="text-slate-500 text-xs font-semibold uppercase mb-1">Target</p>
              <p className="text-white font-mono text-sm break-all">
                {isUrlScan ? result.target_url : result.filename}
              </p>
            </div>
            <div>
              <p className="text-slate-500 text-xs font-semibold uppercase mb-1">Scanned</p>
              <p className="text-white">{formatDate(result.scanned_at)}</p>
            </div>
            <div>
              <p className="text-slate-500 text-xs font-semibold uppercase mb-1">Threats Found</p>
              <p className="text-white text-2xl font-bold">{threatCount}</p>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-6 border-b border-slate-800 overflow-x-auto">
          <button
            onClick={() => setActiveTab('overview')}
            className={`px-4 py-3 font-semibold transition-colors whitespace-nowrap ${
              activeTab === 'overview'
                ? 'text-indigo-400 border-b-2 border-indigo-600'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            Overview
          </button>
          {isUrlScan && (
            <button
              onClick={() => setActiveTab('headers')}
              className={`px-4 py-3 font-semibold transition-colors whitespace-nowrap ${
                activeTab === 'headers'
                  ? 'text-indigo-400 border-b-2 border-indigo-600'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Security Headers
            </button>
          )}
          {isLogScan && (
            <button
              onClick={() => setActiveTab('threats')}
              className={`px-4 py-3 font-semibold transition-colors whitespace-nowrap ${
                activeTab === 'threats'
                  ? 'text-indigo-400 border-b-2 border-indigo-600'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Threats ({threatCount})
            </button>
          )}
          <button
            onClick={() => setActiveTab('recommendations')}
            className={`px-4 py-3 font-semibold transition-colors whitespace-nowrap ${
              activeTab === 'recommendations'
                ? 'text-indigo-400 border-b-2 border-indigo-600'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            Recommendations
          </button>
        </div>

        {/* Tab Content */}
        <div className="space-y-6">
          {/* Overview Tab */}
          {activeTab === 'overview' && (
            <div className="space-y-6">
              {isUrlScan && result.security_headers && (
                <div>
                  <h2 className="text-2xl font-bold text-white mb-4">🔒 Security Headers</h2>
                  <div className="grid grid-cols-1 gap-3">
                    {result.security_headers.map((header, idx) => (
                      <div key={idx} className="glass-card p-4 flex items-center justify-between">
                        <div>
                          <h4 className="text-white font-semibold">{header.header_name}</h4>
                          {header.present ?  (
                            <p className="text-green-400 text-sm">✓ Present</p>
                          ) : (
                            <p className="text-amber-400 text-sm">⚠️ Missing</p>
                          )}
                        </div>
                        <span className={`px-3 py-1 rounded text-sm font-semibold ${
                          header. present 
                            ? 'bg-green-900/30 text-green-300' 
                            : 'bg-amber-900/30 text-amber-300'
                        }`}>
                          {header.present ? 'Found' : 'Missing'}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {isUrlScan && (
                <div>
                  <h2 className="text-2xl font-bold text-white mb-4">📊 Connection Info</h2>
                  <div className="glass-card p-6 space-y-4">
                    <div className="flex justify-between items-center">
                      <span className="text-slate-400">HTTPS Enabled: </span>
                      <span className={`font-semibold ${result.https_enabled ? 'text-green-400' : 'text-red-400'}`}>
                        {result.https_enabled ? '✓ Yes' : '✗ No'}
                      </span>
                    </div>
                    <div className="flex justify-between items-center border-t border-slate-800 pt-4">
                      <span className="text-slate-400">HTTP Status: </span>
                      <span className="text-white font-mono">{result.status_code}</span>
                    </div>
                    {result.server_info && (
                      <div className="flex justify-between items-center border-t border-slate-800 pt-4">
                        <span className="text-slate-400">Server:</span>
                        <span className="text-white font-mono text-sm">{result.server_info}</span>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {isLogScan && result.threat_breakdown && (
                <div>
                  <h2 className="text-2xl font-bold text-white mb-4">📊 Threat Breakdown</h2>
                  <div className="grid grid-cols-1 md: grid-cols-2 gap-4">
                    {Object.entries(result.threat_breakdown).map(([type, count]) => (
                      <div key={type} className="glass-card p-4">
                        <p className="text-slate-400 text-sm capitalize">{type. replace('_', ' ')}</p>
                        <p className="text-3xl font-bold text-indigo-400 mt-2">{count}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Findings */}
              {result.findings && result.findings.length > 0 && (
                <div>
                  <h2 className="text-2xl font-bold text-white mb-4">📋 Key Findings</h2>
                  <div className="space-y-3">
                    {result.findings.map((finding, idx) => (
                      <div key={idx} className="glass-card p-4 flex items-start gap-3">
                        <span className="text-lg">•</span>
                        <p className="text-slate-300">{finding}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Security Headers Tab (URL only) */}
          {activeTab === 'headers' && isUrlScan && result.security_headers && (
            <div className="space-y-4">
              <h2 className="text-2xl font-bold text-white mb-6">🔐 Detailed Header Analysis</h2>
              {result.security_headers.map((header, idx) => (
                <ScanResultCard
                  key={idx}
                  title={header.header_name}
                  severity={header.present ? 'LOW' : 'MEDIUM'}
                  description={header.present ? 'Security header is configured' : 'Security header is missing'}
                  details={header.value || header.recommended}
                  remediation={header. recommended}
                />
              ))}
            </div>
          )}

          {/* Threats Tab (Log only) */}
          {activeTab === 'threats' && isLogScan && result.threats_detected && (
            <div className="space-y-4">
              <h2 className="text-2xl font-bold text-white mb-6">🚨 Detected Threats</h2>
              {result.threats_detected.length === 0 ? (
                <div className="glass-card p-8 text-center">
                  <p className="text-green-400 text-lg font-semibold">✓ No threats detected! </p>
                </div>
              ) : (
                result.threats_detected.map((threat, idx) => (
                  <VulnerabilityItem key={idx} threat={threat} index={idx} />
                ))
              )}
            </div>
          )}

          {/* Recommendations Tab */}
          {activeTab === 'recommendations' && (
            <div className="space-y-4">
              <h2 className="text-2xl font-bold text-white mb-6">✓ Security Recommendations</h2>
              {(result.recommendations || result.findings || []).length === 0 ? (
                <div className="glass-card p-8 text-center">
                  <p className="text-slate-400">No specific recommendations at this time.</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {(result.recommendations || result.findings || []).map((rec, idx) => (
                    <div key={idx} className="glass-card bg-green-950/20 border-green-800/30 p-4 flex items-start gap-3">
                      <span className="text-xl">✓</span>
                      <p className="text-green-100">{rec}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Premium Insights */}
          {result.premium_insights && result.premium_insights.length > 0 && (
            <div className="glass-card bg-purple-950/20 border-purple-800/30 p-6">
              <h3 className="text-lg font-bold text-purple-200 mb-4 flex items-center gap-2">
                <span>✨</span> Premium Insights
              </h3>
              <ul className="space-y-2">
                {result.premium_insights.map((insight, idx) => (
                  <li key={idx} className="text-purple-100 text-sm flex items-start gap-2">
                    <span className="text-purple-400 flex-shrink-0">→</span>
                    {insight}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {/* Disclaimer */}
        <div className="mt-12">
          <Disclaimer />
        </div>

        {/* Action Buttons */}
        <div className="flex gap-4 mt-8">
          <Link to="/" className="btn-primary flex-1 text-center">
            New Scan
          </Link>
          <Link to="/scan-history" className="btn-secondary flex-1 text-center">
            View History
          </Link>
        </div>
      </main>

      <Footer />
    </div>
  )
}

export default ScanResult