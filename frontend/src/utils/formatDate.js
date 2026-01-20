/**
 * Date Formatting Utilities
 */

/**
 * Format date to readable string
 * @param {string|Date} dateString - ISO date string or Date object
 * @returns {string} Formatted date
 */
export const formatDate = (dateString) => {
  if (! dateString) return 'Unknown'
  
  const date = new Date(dateString)
  
  // Check if date is valid
  if (isNaN(date.getTime())) {
    return 'Invalid date'
  }
  
  // Format:  "Jan 15, 2026 at 10:30 AM"
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    meridiem: 'short'
  }).format(date)
}

/**
 * Format date to time ago (e.g., "2 hours ago")
 * @param {string|Date} dateString - ISO date string or Date object
 * @returns {string} Time ago string
 */
export const formatTimeAgo = (dateString) => {
  if (!dateString) return 'Unknown'
  
  const date = new Date(dateString)
  const now = new Date()
  const secondsDiff = Math.floor((now - date) / 1000)
  
  if (secondsDiff < 60) return 'Just now'
  if (secondsDiff < 3600) return `${Math.floor(secondsDiff / 60)} mins ago`
  if (secondsDiff < 86400) return `${Math.floor(secondsDiff / 3600)} hours ago`
  if (secondsDiff < 604800) return `${Math.floor(secondsDiff / 86400)} days ago`
  
  return formatDate(dateString)
}