import React from 'react';
import { NavLink } from 'react-router-dom';
import { Home, Users, Music, Settings, LogOut } from 'lucide-react';
import './Sidebar.css';

const Sidebar = () => {
  const navItems = [
    { name: 'Overview', path: '/', icon: <Home size={20} /> },
    { name: 'Users', path: '/users', icon: <Users size={20} /> },
    { name: 'Songs', path: '/songs', icon: <Music size={20} /> },
    { name: 'Settings', path: '/settings', icon: <Settings size={20} /> },
  ];

  return (
    <aside className="sidebar glass">
      <div className="sidebar-header">
        <div className="logo">
          <div className="logo-icon bg-gradient">M</div>
          <span className="logo-text h4 text-gradient">MusicAdmin</span>
        </div>
      </div>
      
      <nav className="sidebar-nav">
        <ul>
          {navItems.map((item) => (
            <li key={item.name}>
              <NavLink 
                to={item.path} 
                className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}
              >
                {item.icon}
                <span>{item.name}</span>
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
      
      <div className="sidebar-footer">
        <button className="nav-link logout-btn">
          <LogOut size={20} />
          <span>Logout</span>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
