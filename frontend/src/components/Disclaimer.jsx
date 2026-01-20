/**
 * Disclaimer Component
 * Legal notice about tool limitations and usage restrictions
 */

const Disclaimer = () => {
  return (
    <div className="glass-card bg-amber-950/20 border-amber-800/50 p-4 rounded-lg">
      <div className="flex gap-3">
        <div className="flex-shrink-0">
          <svg className="h-5 w-5 text-amber-400 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M8. 257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-. 213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
        </div>
        <div>
          <h3 className="text-sm font-semibold text-amber-200">⚠️ Disclaimer</h3>
          <p className="text-xs text-amber-100/90 mt-1 leading-relaxed">
            <strong>Passive Security Analysis Only: </strong> VulnScan Lite performs passive, non-intrusive security checks only. It is <strong>NOT</strong> a substitute for professional penetration testing or comprehensive security audits.
          </p>
          <p className="text-xs text-amber-100/90 mt-2 leading-relaxed">
            <strong>Usage Rights:</strong> Only scan websites that you own or have explicit written permission to test.  Unauthorized scanning may violate laws. 
          </p>
        </div>
      </div>
    </div>
  )
}

export default Disclaimer