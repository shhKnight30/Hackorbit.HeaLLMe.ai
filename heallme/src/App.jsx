// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
// import './App.css'

// import LandingPage from "./components/landingpage/LandingPage"
// import Chat from "./components/chat/Chat"
import { Outlet } from "react-router-dom"
import Header from "./components/Header/Header"
import Footer from "./components/footer/Footer"
import LandingPage from "./components/landingpage/LandingPage"
function App() {

  return (
   
    <>
    <Header/>
    <Outlet/>
    {/* <LandingPage/> */}
    <Footer/>
    </>
  )
}

export default App
