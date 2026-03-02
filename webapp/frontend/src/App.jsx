import { Routes, Route } from 'react-router-dom'
import ChatPage from './pages/ChatPage'
import './App.module.css'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<ChatPage />} />
      <Route path="/chat/:conversationId" element={<ChatPage />} />
    </Routes>
  )
}
