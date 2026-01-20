/**
 * Footer Component
 * Displays footer information and links
 */

const Footer = () => {
  return (
    <footer className="bg-slate-950 border-t border-slate-800 mt-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand */}
          <div>
            <h3 className="text-white font-bold text-lg mb-4">VulnScan Lite</h3>
            <p className="text-slate-400 text-sm">
              Lightweight security analysis platform for on-demand scanning
            </p>
          </div>

          {/* Product */}
          <div>
            <h4 className="text-white font-semibold mb-4">Product</h4>
            <ul className="space-y-2">
              <li><a href="#features" className="text-slate-400 hover:text-white transition-colors text-sm">Features</a></li>
              <li><a href="#pricing" className="text-slate-400 hover:text-white transition-colors text-sm">Pricing</a></li>
              <li><a href="#docs" className="text-slate-400 hover:text-white transition-colors text-sm">Documentation</a></li>
            </ul>
          </div>

          {/* Company */}
          <div>
            <h4 className="text-white font-semibold mb-4">Company</h4>
            <ul className="space-y-2">
              <li><a href="#about" className="text-slate-400 hover:text-white transition-colors text-sm">About</a></li>
              <li><a href="#privacy" className="text-slate-400 hover:text-white transition-colors text-sm">Privacy</a></li>
              <li><a href="#terms" className="text-slate-400 hover:text-white transition-colors text-sm">Terms</a></li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="text-white font-semibold mb-4">Contact</h4>
            <ul className="space-y-2">
              <li><a href="mailto:support@vulnscan.com" className="text-slate-400 hover:text-white transition-colors text-sm">support@vulnscan.com</a></li>
              <li><a href="https://github.com" className="text-slate-400 hover:text-white transition-colors text-sm">GitHub</a></li>
              <li><a href="https://twitter.com" className="text-slate-400 hover:text-white transition-colors text-sm">Twitter</a></li>
            </ul>
          </div>
        </div>

        <div className="border-t border-slate-800 pt-8">
          <p className="text-slate-500 text-sm text-center">
            © 2026 VulnScan Lite. All rights reserved.  | Made with security in mind
          </p>
        </div>
      </div>
    </footer>
  )
}

export default Footer