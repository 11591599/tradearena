import { Routes, Route, Navigate } from 'react-router-dom'
import Trade from './pages/Trade'
import Arena from './pages/Arena'
import Leaderboard from './pages/Leaderboard'
import Profile from './pages/Profile'
import Nav from './components/Nav'

function App() {
  return (
    <div className="app">
      <Routes>
        <Route path="/" element={<Trade />} />
        <Route path="/arena" element={<Arena />} />
        <Route path="/leaderboard" element={<Leaderboard />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
      <Nav />
    </div>
  )
}

export default App