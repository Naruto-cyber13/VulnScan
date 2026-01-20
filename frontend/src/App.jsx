/**
 * Main App Component
 * Sets up routing for all pages
 */

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import ScanResult from './pages/ScanResult'
import ScanHistory from './pages/ScanHistory'
import Pricing from './pages/Pricing'
import NotFound from './pages/NotFound'

function App() {
  return (
    <Router>
      <Routes>
        {/* Home / Scanner Page */}
        <Route path="/" element={<Home />} />
        
        {/* Scan Result Page */}
        <Route path="/scan-result/:scanId" element={<ScanResult />} />
        
        {/* Scan History Page */}
        <Route path="/scan-history" element={<ScanHistory />} />
        
        {/* Pricing Page */}
        <Route path="/pricing" element={<Pricing />} />
        
        {/* 404 Not Found */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  )
}

export default App