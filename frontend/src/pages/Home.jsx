/**
 * Home Page
 * Landing page with scanner form
 */

import Navbar from '../components/Navbar'
import Footer from '../components/Footer'
import ScanForm from '../components/ScanForm'
import Disclaimer from '../components/Disclaimer'

const Home = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
      <Navbar />
      
      
      <main className="max-w-4xl mx-auto px-4 py-16 space-y-6">
        <ScanForm />
        <Disclaimer />
      </main>


      <Footer />
    </div>
  )
}

export default Home