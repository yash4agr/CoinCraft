/**
 * Date utility functions for CoinCraft application
 * Uses browser's built-in timezone handling for accurate local time display
 */

/**
 * Format a date string to show relative time in user's local timezone
 * @param dateString - ISO date string or date object
 * @param options - Formatting options
 * @returns Formatted date string
 */
export const formatDateIST = (
  dateString: string | Date,
  options: {
    showTime?: boolean
    showYear?: boolean
    format?: 'relative' | 'absolute' | 'both'
  } = {}
): string => {
  if (!dateString) return 'Recently'
  
  try {
    const date = new Date(dateString)
    const now = new Date()
    
    // Convert UTC transaction time to IST (UTC+5:30)
    const istOffset = 5.5 * 60 * 60 * 1000 // 5 hours 30 minutes in milliseconds
    const istDate = new Date(date.getTime() + istOffset)
    
    // Calculate time difference: current local time vs IST transaction time
    const diffInMs = now.getTime() - istDate.getTime()
    const diffInMinutes = Math.floor(diffInMs / (1000 * 60))
    const diffInHours = Math.floor(diffInMs / (1000 * 60 * 60))
    const diffInDays = Math.floor(diffInMs / (1000 * 60 * 60 * 24))
    
    // Relative time formatting
    let relativeTime = ''
    if (diffInMinutes < 1) {
      relativeTime = 'Just now'
    } else if (diffInMinutes < 60) {
      relativeTime = `${diffInMinutes} minutes ago`
    } else if (diffInHours < 24) {
      relativeTime = `${diffInHours} hours ago`
    } else if (diffInDays === 1) {
      relativeTime = 'Yesterday'
    } else if (diffInDays < 7) {
      relativeTime = `${diffInDays} days ago`
    } else {
      relativeTime = `${diffInDays} days ago`
    }
    
    // Absolute time formatting - use IST timezone
    const absoluteTime = istDate.toLocaleDateString('en-IN', {
      year: options.showYear !== false ? 'numeric' : undefined,
      month: 'short',
      day: 'numeric',
      hour: options.showTime !== false ? '2-digit' : undefined,
      minute: options.showTime !== false ? '2-digit' : undefined,
      timeZone: 'Asia/Kolkata'
    })
    
    // Return based on format option
    switch (options.format) {
      case 'absolute':
        return absoluteTime
      case 'both':
        return diffInDays < 7 ? relativeTime : absoluteTime
      case 'relative':
      default:
        return relativeTime
    }
  } catch (error) {
    console.error('Error formatting date:', error)
    return 'Recently'
  }
}

/**
 * Get current time in IST
 * @returns Current time in IST as string
 */
export const getCurrentTimeIST = (): string => {
  const now = new Date()
  return now.toLocaleTimeString('en-IN', {
    timeZone: 'Asia/Kolkata',
    hour12: true,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

/**
 * Check if a date is today in IST
 * @param dateString - ISO date string or date object
 * @returns boolean
 */
export const isTodayIST = (dateString: string | Date): boolean => {
  try {
    const date = new Date(dateString)
    const now = new Date()
    
    // Convert transaction date to IST for comparison
    const istOffset = 5.5 * 60 * 60 * 1000
    const istDate = new Date(date.getTime() + istOffset)
    
    // Compare IST transaction date with current local date
    return istDate.toDateString() === now.toDateString()
  } catch (error) {
    return false
  }
}

/**
 * Format date for display in transaction lists
 * @param dateString - ISO date string or date object
 * @returns Formatted date string
 */
export const formatTransactionDate = (dateString: string | Date): string => {
  return formatDateIST(dateString, { format: 'both' })
}

/**
 * Test function to verify timezone conversion
 * @param testDateString - ISO date string to test
 * @returns Debug information
 */
export const testTimezoneConversion = (testDateString: string) => {
  const testDate = new Date(testDateString)
  const now = new Date()
  
  console.log('🧪 [TIMEZONE TEST] Test date string:', testDateString)
  console.log('🧪 [TIMEZONE TEST] Test date object:', testDate)
  console.log('🧪 [TIMEZONE TEST] Current time:', now)
  console.log('🧪 [TIMEZONE TEST] Test date in local timezone:', testDate.toLocaleString())
  console.log('🧪 [TIMEZONE TEST] Current in local timezone:', now.toLocaleString())
  console.log('🧪 [TIMEZONE TEST] Time difference (ms):', now.getTime() - testDate.getTime())
  console.log('🧪 [TIMEZONE TEST] Time difference (minutes):', Math.floor((now.getTime() - testDate.getTime()) / (1000 * 60)))
  console.log('🧪 [TIMEZONE TEST] Time difference (hours):', Math.floor((now.getTime() - testDate.getTime()) / (1000 * 60 * 60)))
  
  return formatDateIST(testDateString)
}
