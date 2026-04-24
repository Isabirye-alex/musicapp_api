import React from 'react';
import { Bell, Search, User } from 'lucide-react';
import './Topbar.css';

const Topbar = () => {
  return (
    <header className="topbar glass">
      <div className="search-bar">
        <Search size={18} className="search-icon" />
        <input type="text" placeholder="Search users, songs..." />
      </div>
      
      <div className="topbar-actions">
        <button className="btn-icon relative">
          <Bell size={20} />
          <span className="notification-dot"></span>
        </button>
        <div className="user-profile">
          <div className="avatar">
            <User size={18} />
          </div>
          <div className="user-info">
            <span className="user-name">Admin User</span>
            <span className="user-role text-muted">Superadmin</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Topbar;
