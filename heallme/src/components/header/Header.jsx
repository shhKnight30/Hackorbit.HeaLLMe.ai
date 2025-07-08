import React from 'react'
import { Link } from 'react-router-dom'
const Header = () => {
  return (
    
    <header className="w-full px-6 py-4 bg-white shadow-md flex justify-between items-center">
      <h1 className="text-2xl font-bold text-blue-600"><Link to='/'> HeaLLMe.ai</Link></h1>
      <nav>
        <a href="#features" className="mx-4 text-gray-600 hover:text-blue-600">Features</a>
        <a href="#how" className="mx-4 text-gray-600 hover:text-blue-600">How It Works</a>
        <a href="#start" className="mx-4 text-white bg-blue-600 px-4 py-2 rounded-full hover:bg-blue-700">Try Now</a>
      </nav>
    </header>
  )
}

export default Header