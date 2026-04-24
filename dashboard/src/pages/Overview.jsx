import React from 'react';
import { Users, Music, Headphones, Activity } from 'lucide-react';
import MetricCard from '../components/ui/MetricCard';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import './Overview.css';

const data = [
  { name: 'Jan', users: 400, songs: 240 },
  { name: 'Feb', users: 300, songs: 139 },
  { name: 'Mar', users: 200, songs: 980 },
  { name: 'Apr', users: 278, songs: 390 },
  { name: 'May', users: 189, songs: 480 },
  { name: 'Jun', users: 239, songs: 380 },
  { name: 'Jul', users: 349, songs: 430 },
];

const Overview = () => {
  return (
    <div className="overview-page">
      <div className="page-header">
        <h1 className="h2 text-gradient">Dashboard Overview</h1>
        <p className="text-muted">Welcome back to the MusicAdmin platform.</p>
      </div>

      <div className="grid-cards mb-8">
        <MetricCard 
          title="Total Users" 
          value="1,248" 
          icon={<Users size={24} />} 
          trend="up" 
          trendValue="+12%" 
        />
        <MetricCard 
          title="Total Songs" 
          value="8,594" 
          icon={<Music size={24} />} 
          trend="up" 
          trendValue="+5%" 
        />
        <MetricCard 
          title="Active Listeners" 
          value="892" 
          icon={<Headphones size={24} />} 
          trend="up" 
          trendValue="+18%" 
        />
        <MetricCard 
          title="Platform Activity" 
          value="98%" 
          icon={<Activity size={24} />} 
          trend="down" 
          trendValue="-1%" 
        />
      </div>

      <div className="chart-section glass-card">
        <h3 className="h4 mb-4">Growth Analytics</h3>
        <div className="chart-container">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <defs>
                <linearGradient id="colorUsers" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6366f1" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="colorSongs" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
              <XAxis dataKey="name" stroke="#9ca3af" axisLine={false} tickLine={false} />
              <YAxis stroke="#9ca3af" axisLine={false} tickLine={false} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#181b21', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '0.5rem' }}
                itemStyle={{ color: '#f8f9fa' }}
              />
              <Area type="monotone" dataKey="users" stroke="#6366f1" fillOpacity={1} fill="url(#colorUsers)" />
              <Area type="monotone" dataKey="songs" stroke="#8b5cf6" fillOpacity={1} fill="url(#colorSongs)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default Overview;
