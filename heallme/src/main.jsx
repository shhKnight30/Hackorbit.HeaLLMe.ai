import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { createBrowserRouter, RouterProvider} from 'react-router-dom'
import LandingPage from './components/landingpage/LandingPage.jsx'
import Chat from './components/chat/Chat.jsx'

const router = createBrowserRouter([
  {
    path:'/',
    element:<App/>,
    children:[
          {
        // index:true,
        path:"",
        element: <LandingPage/>
      },{
        path:'chat',
        element:<Chat/>
      }
    ]
  }
])
createRoot(document.getElementById('root')).render(
  <StrictMode>
 <RouterProvider router={router} />
  </StrictMode>,
)
