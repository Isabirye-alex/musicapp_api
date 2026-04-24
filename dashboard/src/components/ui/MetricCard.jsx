import React from 'react';
import './MetricCard.css';

const MetricCard = ({ title, value, icon, trend, trendValue }) => {
  return (
    <div className="metric-card glass-card">
      <div className="metric-header">
        <h3 className="metric-title text-muted">{title}</h3>
        <div className="metric-icon">{icon}</div>
      </div>
      <div className="metric-content">
        <div className="metric-value h2">{value}</div>
        {trend && (
          <div className={`metric-trend ${trend === 'up' ? 'text-success' : 'text-danger'}`}>
            <span>{trend === 'up' ? '↑' : '↓'}</span>
            <span>{trendValue}</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default MetricCard;
