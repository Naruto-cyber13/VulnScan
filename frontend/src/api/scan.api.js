/**
 * Scan API functions
 * All API calls related to scanning functionality
 */

import apiClient from './axios'

/**
 * Scan a website URL
 * @param {string} url - Target URL to scan
 * @param {boolean} premium - Premium tier flag
 * @returns {Promise} Scan result
 */
export const scanUrl = async (url, premium = false) => {
  try {
    const response = await apiClient.post('/v1/scan/url', {
      url,
      premium
    })
    return response.data
  } catch (error) {
    throw error
  }
}

/**
 * Scan log file content
 * @param {string} logContent - Raw log text
 * @param {string} filename - Log file identifier
 * @param {boolean} premium - Premium tier flag
 * @returns {Promise} Scan result
 */
export const scanLog = async ({ logContent, filename, premium }) => {
  try {
    const response = await apiClient.post('/v1/scan/log', {
      filename,
      log_content: logContent,
      premium
    })
    return response.data
  } catch (error) {
    throw error
  }
}

/**
 * Get scan history
 * @param {number} limit - Maximum number of records
 * @returns {Promise} Scan history
 */
export const getScanHistory = async (limit = 50) => {
  try {
    const response = await apiClient.get('/v1/scans/history', {
      params: { limit }
    })
    return response.data
  } catch (error) {
    throw error
  }
}

/**
 * Get available features
 * @returns {Promise} Features information
 */
export const getFeatures = async () => {
  try {
    const response = await apiClient.get('/info/features')
    return response.data
  } catch (error) {
    throw error
  }
}

/**
 * Get tier information
 * @returns {Promise} Tier information
 */
export const getTierInfo = async () => {
  try {
    const response = await apiClient.get('/info/tiers')
    return response.data
  } catch (error) {
    throw error
  }
}