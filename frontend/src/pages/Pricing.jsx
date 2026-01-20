/**
 * Pricing Page
 * Information about service tiers (informational only - no payment logic)
 */

import { Link } from 'react-router-dom'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'
import Disclaimer from '../components/Disclaimer'

const Pricing = () => {
  const tiers = [
    {
      name: 'Free',
      price: '$0',
      description: 'Perfect for quick security checks',
      features: [
        'Basic URL security scanning',
        'Standard log analysis',
        'Limited threat details (10 max)',
        'Scan history access',
        'Basic recommendations',
        'Passive checks only'
      ],
      limitations: [
        'Limited threat breakdown',
        'No premium insights',
        'Standard severity assessment'
      ],
      cta: 'Get Started Free',
      highlighted: false
    },
    {
      name: 'Premium',
      price: '$9.99',
      period: '/month',
      description: 'For thorough security analysis',
      features:  [
        'All free tier features',
        'Full threat breakdown',
        'Premium security insights',
        'Detailed threat explanations',
        'Advanced recommendations',
        'Unlimited threat details',
        'Priority support'
      ],
      limitations: [],
      cta: 'Coming Soon',
      highlighted: true
    },
    {
      name: 'Pro',
      price: 'Custom',
      description: 'For organizations & teams',
      features: [
        'All premium features',
        'API access',
        'Custom integrations',
        'Team collaboration',
        'Dedicated support',
        'Advanced reporting',
        'SLA guarantee'
      ],
      limitations:  [],
      cta: 'Contact Sales',
      highlighted: false
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
      <Navbar />
      
      <main className="max-w-7xl mx-auto px-4 py-16">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-white mb-4">Simple, Transparent Pricing</h1>
          <p className="text-xl text-slate-400 mb-8">Choose the perfect plan for your security needs</p>
          <p className="text-sm text-amber-400 bg-amber-950/20 border border-amber-800/30 rounded-lg p-3 inline-block">
            💡 Current Status: Free tier available now.  Premium tier coming soon. 
          </p>
        </div>

        {/* Pricing Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          {tiers.map((tier, idx) => (
            <div
              key={idx}
              className={`glass-card p-8 relative ${
                tier.highlighted ? 'ring-2 ring-indigo-600 md:scale-105' : ''
              }`}
            >
              {/* Highlighted Badge */}
              {tier.highlighted && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <span className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-4 py-1 rounded-full text-sm font-bold">
                    ⭐ Most Popular
                  </span>
                </div>
              )}

              {/* Tier Name */}
              <h2 className="text-3xl font-bold text-white mb-2">{tier.name}</h2>
              <p className="text-slate-400 text-sm mb-6">{tier.description}</p>

              {/* Price */}
              <div className="mb-6">
                <div className="text-4xl font-bold text-white">
                  {tier.price}
                  {tier.period && <span className="text-lg text-slate-400">{tier.period}</span>}
                </div>
              </div>

              {/* CTA Button */}
              <button className={`w-full py-3 rounded-lg font-semibold mb-8 transition-all ${
                tier.highlighted
                  ? 'bg-indigo-600 hover:bg-indigo-700 text-white'
                  :  'border border-slate-700 text-slate-300 hover:border-indigo-600 hover:text-white'
              }`}>
                {tier.cta}
              </button>

              {/* Features */}
              <div className="space-y-3 mb-8">
                <p className="text-slate-400 text-xs font-semibold uppercase">Included: </p>
                {tier.features.map((feature, fidx) => (
                  <div key={fidx} className="flex items-start gap-3">
                    <span className="text-green-400 mt-0.5">✓</span>
                    <span className="text-slate-300 text-sm">{feature}</span>
                  </div>
                ))}
              </div>

              {/* Limitations */}
              {tier.limitations.length > 0 && (
                <div className="space-y-3 border-t border-slate-800 pt-6">
                  <p className="text-slate-400 text-xs font-semibold uppercase">Limitations:</p>
                  {tier.limitations.map((limit, lidx) => (
                    <div key={lidx} className="flex items-start gap-3">
                      <span className="text-slate-500 mt-0.5">✗</span>
                      <span className="text-slate-400 text-sm">{limit}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>

        {/* FAQ Section */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-white mb-8 text-center">Frequently Asked Questions</h2>
          <div className="grid grid-cols-1 md: grid-cols-2 gap-6">
            {[
              {
                q: 'What happens to my data?',
                a:  'Your scan data is stored temporarily for history retrieval.  We never share or sell your scanning data.'
              },
              {
                q: 'Do you perform intrusive testing?',
                a: 'No.  VulnScan Lite performs passive security checks only.  It does not attempt exploitation or aggressive pentesting.'
              },
              {
                q: 'Can I scan someone else\'s website?',
                a: 'Only scan websites you own or have explicit written permission to test. Unauthorized scanning may violate laws.'
              },
              {
                q: 'How often can I scan?',
                a: 'Free tier users can scan as often as they need. Premium tier is coming with unlimited scans.'
              },
              {
                q: 'Is this a replacement for penetration testing?',
                a:  'No. This tool provides quick security insights but is not a substitute for professional security audits.'
              },
              {
                q: 'When will Premium tier be available?',
                a:  'Premium features are currently in development. Sign up to be notified when they launch.'
              }
            ]. map((faq, idx) => (
              <div key={idx} className="glass-card p-6">
                <h3 className="text-white font-semibold mb-2">❓ {faq.q}</h3>
                <p className="text-slate-400 text-sm">{faq.a}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Disclaimer */}
        <div className="mb-8">
          <Disclaimer />
        </div>

        {/* CTA */}
        <div className="glass-card p-12 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">Ready to Scan?</h2>
          <p className="text-slate-400 mb-6 max-w-2xl mx-auto">
            Start with our free tier today.  No credit card required.  Premium features coming soon.
          </p>
          <Link to="/" className="btn-primary inline-block">
            Start Free Security Scan
          </Link>
        </div>
      </main>

      <Footer />
    </div>
  )
}

export default Pricing