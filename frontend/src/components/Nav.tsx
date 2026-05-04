import { NavLink } from 'react-router-dom'
import { TrendingUp, Swords, Trophy, User } from 'lucide-react'

export default function Nav() {
  const items = [
    { to: '/', icon: TrendingUp, label: 'Trade' },
    { to: '/arena', icon: Swords, label: 'Arena' },
    { to: '/leaderboard', icon: Trophy, label: 'Top' },
    { to: '/profile', icon: User, label: 'Profile' },
  ]

  return (
    <nav className="nav">
      {items.map(({ to, icon: Icon, label }) => (
        <NavLink key={to} to={to} className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
          <Icon />
          {label}
        </NavLink>
      ))}
    </nav>
  )
}