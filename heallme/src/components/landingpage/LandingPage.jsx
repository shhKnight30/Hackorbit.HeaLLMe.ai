import { HeartPulse } from 'lucide-react';
import { Link } from 'react-router-dom';
import {Typewriter} from 'react-simple-typewriter'
const LandingPage = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-white via-blue-300 to-white   text-gray-800">
   

      <section className="flex flex-col-reverse md:flex-row items-center justify-between px-10 py-20 max-w-7xl mx-auto">
        <div className="md:w-1/2 text-center md:text-left">
          {/* <h2 className="text-4xl font-bold mb-4 text-blue-700">Your AI Health Companion</h2> */}
          <h1 className='text-5xl'>
            <Typewriter
                words={['HeaLLMe.ai']}
                loop={true}
                cursor
                cursorStyle="..."
                typeSpeed={150}
                deleteSpeed={150}
                delaySpeed={1500}
                />

          </h1>
        <div className='mt-[30px]'>
  
            <p className="text-lg mb-6">'Your personalized ai agent for medical assistence ... Talk to an intelligent medical assistant that listens, assesses, and gives you smart health insights — instantly and securely.</p>
            <a href="#start" className="bg-blue-600 text-white px-6 py-3 rounded-full hover:bg-blue-700 transition">Get Started</a>
        </div>
          
        </div>
        <div className="md:w-1/2 flex justify-center mb-10 md:mb-0">
          <img src="https://cdn-icons-png.flaticon.com/512/4703/4703117.png" alt="AI Doctor" className="w-64" />
        </div>
      </section>

      <section id="features" className="bg-gradient-to-br from-blue-300 via-white to-blue-300 py-16 px-6">
        <div className="max-w-5xl mx-auto text-center">
          <h3 className="text-3xl font-bold mb-10 text-blue-700">Features</h3>
          <div className="grid md:grid-cols-3 gap-8 text-left">
            <div className="bg-blue-50 p-6 rounded-xl shadow-sm">
              <HeartPulse className="w-10 h-10 text-blue-600 mb-4" />
              <h4 className="text-xl font-semibold mb-2">Symptom Analysis</h4>
              <p>Enter your symptoms in natural language and get personalized health insights instantly.</p>
            </div>
            <div className="bg-blue-50 p-6 rounded-xl shadow-sm">
              <HeartPulse className="w-10 h-10 text-blue-600 mb-4" />
              <h4 className="text-xl font-semibold mb-2">Risk Assessment</h4>
              <p>Real-time risk scoring and triage suggestions to help you take the next right step.</p>
            </div>
            <div className="bg-blue-50 p-6 rounded-xl shadow-sm">
              <HeartPulse className="w-10 h-10 text-blue-600 mb-4" />
              <h4 className="text-xl font-semibold mb-2">Smart Recommendations</h4>
              <p>Self-care tips, urgency warnings, and prevention insights — powered by AI.</p>
            </div>
          </div>
        </div>
      </section>

      <section id="how" className="bg-gradient-to-br from-white via-blue-200 to-white  py-16 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <h3 className="text-3xl font-bold mb-10 text-blue-700">How It Works</h3>
          <ol className="text-left space-y-6 text-lg">
            <li><span className="font-semibold">1. Start a chat</span> – Describe your symptoms naturally.</li>
            <li><span className="font-semibold">2. AI processes input</span> – Medical AI analyzes your health situation.</li>
            <li><span className="font-semibold">3. Receive insights</span> – Get real-time risk scores and next steps.</li>
          </ol>
        </div>
      </section>

      <section id="start" className="bg-blue-600 text-white py-16 px-6 text-center">
        <h3 className="text-3xl font-bold mb-4">Ready to check your health?</h3>
        <p className="mb-6">Start your AI-powered health chat in seconds.</p>
        <Link to="/chat" className="bg-white text-blue-600 font-semibold px-6 py-3 rounded-full hover:bg-gray-100">Launch HeaLLMe.ai</Link>
      </section>

    </div>
  )
}

export default LandingPage