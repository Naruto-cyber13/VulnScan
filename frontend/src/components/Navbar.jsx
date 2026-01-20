/**
 * Navigation Bar Component
 * Displays branding and navigation links
 */

import { Link } from 'react-router-dom'

const Navbar = () => {
  return (
    <nav className="sticky top-0 z-50 bg-slate-950 border-b border-slate-800 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm: px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo/Brand */}
          <Link to="/" className="flex items-center gap-3 group">
            <div className="w-8 h-8 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">V</span>
            </div>
            <span className="text-xl font-bold text-white group-hover:text-indigo-400 transition-colors">
              VulnScan Lite
            </span>
          </Link>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center gap-8">
            <Link 
              to="/" 
              className="text-slate-400 hover:text-white transition-colors font-medium"
            >
              Home
            </Link>
            <Link 
              to="/scan-history" 
              className="text-slate-400 hover:text-white transition-colors font-medium"
            >
              History
            </Link>
            <Link 
              to="/pricing" 
              className="text-slate-400 hover:text-white transition-colors font-medium"
            >
              Pricing
            </Link>
          </div>

          {/* CTA Button */}
          <Link 
            to="/" 
            className="btn-primary"
          >
            Start Scan
          </Link>
        </div>
      </div>
    </nav>
  )
}

export default Navbar