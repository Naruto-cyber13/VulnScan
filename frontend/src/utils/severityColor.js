/**
 * Severity Color Utilities
 * Maps severity levels to colors and emojis
 */

/**
 * Get color for severity level
 * @param {string} severity - Severity level (LOW, MEDIUM, HIGH)
 * @returns {string} Hex color code
 */
export const getSeverityColor = (severity) => {
  const colors = {
    'LOW': '#10b981',      // Green
    'MEDIUM':  '#f59e0b',   // Amber
    'HIGH': '#ef4444'      // Red
  }
  return colors[severity] || '#64748b'  // Slate if unknown
}

/**
 * Get emoji for severity level
 * @param {string} severity - Severity level (LOW, MEDIUM, HIGH)
 * @returns {string} Emoji character
 */
export const getSeverityEmoji = (severity) => {
  const emojis = {
    'LOW': '✅',
    'MEDIUM':  '⚠️',
    'HIGH': '🚨'
  }
  return emojis[severity] || '❓'
}

/**
 * Get badge class for severity
 * @param {string} severity - Severity level (LOW, MEDIUM, HIGH)
 * @returns {string} Tailwind CSS classes
 */
export const getSeverityBadgeClass = (severity) => {
  const classes = {
    'LOW': 'bg-green-900/30 text-green-300 border-green-800/50',
    'MEDIUM':  'bg-amber-900/30 text-amber-300 border-amber-800/50',
    'HIGH':  'bg-red-900/30 text-red-300 border-red-800/50'
  }
  return classes[severity] || 'bg-slate-800 text-slate-300'
}