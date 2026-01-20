/**
 * Scan Progress Component
 * Shows loading state during scanning
 */

const ScanProgress = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-64 gap-6">
      {/* Animated Scanner */}
      <div className="relative w-24 h-24">
        <div className="absolute inset-0 bg-indigo-600/20 rounded-full animate-pulse" />
        <div className="absolute inset-2 border-4 border-transparent border-t-indigo-600 border-r-indigo-600 rounded-full animate-spin" />
        <div className="absolute inset-6 flex items-center justify-center">
          <span className="text-2xl">🔍</span>
        </div>
      </div>

      {/* Status Text */}
      <div className="text-center">
        <h3 className="text-xl font-bold text-white mb-2">Scanning Website...</h3>
        <p className="text-slate-400">Analyzing security posture.  This may take a few seconds.</p>
      </div>

      {/* Progress Bar */}
      <div className="w-full max-w-xs">
        <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
          <div className="h-full bg-gradient-to-r from-indigo-600 to-purple-600 animate-pulse rounded-full" style={{
            animation: 'slideProgress 2s ease-in-out infinite'
          }} />
        </div>
      </div>

      <style>{`
        @keyframes slideProgress {
          0% { width: 0%; }
          50% { width: 100%; }
          100% { width: 100%; }
        }
      `}</style>
    </div>
  )
}

export default ScanProgress