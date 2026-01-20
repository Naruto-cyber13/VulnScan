/**
 * Scan Result Card Component
 * Displays individual security finding
 */

import { getSeverityColor } from '../utils/severityColor'

const ScanResultCard = ({ title, severity, description, details, remediation, reference }) => {
  const severityColor = getSeverityColor(severity)

  return (
    <div className="glass-card p-5 border-l-4" style={{ borderLeftColor: severityColor }}>
      <div className="flex items-start justify-between mb-3">
        <div>
          <h4 className="text-white font-semibold text-lg">{title}</h4>
          {reference && (
            <a href={reference} target="_blank" rel="noopener noreferrer" className="text-indigo-400 hover:text-indigo-300 text-xs mt-1 inline-flex items-center gap-1">
              📚 Learn more <span>↗</span>
            </a>
          )}
        </div>
        <span 
          className="px-3 py-1 rounded-full text-white text-xs font-semibold"
          style={{ backgroundColor: severityColor + '40', color: severityColor }}
        >
          {severity}
        </span>
      </div>

      {description && (
        <p className="text-slate-300 text-sm mb-3">{description}</p>
      )}

      {details && (
        <div className="bg-slate-950 rounded p-3 mb-3 border border-slate-800">
          <p className="text-slate-400 text-xs font-mono">{details}</p>
        </div>
      )}

      {remediation && (
        <div className="bg-green-950/20 border border-green-800/30 rounded p-3">
          <p className="text-green-200 text-sm">
            <strong>✓ Recommendation:</strong> {remediation}
          </p>
        </div>
      )}
    </div>
  )
}

export default ScanResultCard