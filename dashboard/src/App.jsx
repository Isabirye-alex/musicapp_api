import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Overview from './pages/Overview';
import Users from './pages/Users';
import Songs from './pages/Songs';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Overview />} />
          <Route path="users" element={<Users />} />
          <Route path="songs" element={<Songs />} />
          <Route path="settings" element={<div style={{ padding: '2rem' }}>Settings (Coming Soon)</div>} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
