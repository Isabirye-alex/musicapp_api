import React, { useState, useEffect } from 'react';
import { MoreVertical, Edit2, Trash2 } from 'lucide-react';
import { fetchUsers } from '../api/client';

const Users = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      const data = await fetchUsers();
      if (data && data.length > 0) {
        setUsers(data);
      } else {
        // Fallback mock data if API fails or is empty
        setUsers([
          { id: '1', first_name: 'John', last_name: 'Doe', email: 'john@example.com', role: 'admin', is_active: true },
          { id: '2', first_name: 'Jane', last_name: 'Smith', email: 'jane@example.com', role: 'user', is_active: true },
          { id: '3', first_name: 'Mike', last_name: 'Johnson', email: 'mike@example.com', role: 'user', is_active: false },
          { id: '4', first_name: 'Sarah', last_name: 'Williams', email: 'sarah@example.com', role: 'user', is_active: true },
        ]);
      }
      setLoading(false);
    };
    loadData();
  }, []);

  return (
    <div className="users-page">
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 className="h2 text-gradient">Users Management</h1>
          <p className="text-muted">View and manage platform users.</p>
        </div>
        <button className="btn btn-primary">Add User</button>
      </div>

      <div className="table-container glass-card" style={{ padding: 0, overflow: 'hidden' }}>
        <table className="data-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Role</th>
              <th>Status</th>
              <th style={{ textAlign: 'right' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan="5" style={{ textAlign: 'center', padding: '3rem' }}>Loading users...</td>
              </tr>
            ) : (
              users.map(user => (
                <tr key={user.id}>
                  <td>
                    <div style={{ fontWeight: 500 }}>{user.first_name} {user.last_name}</div>
                  </td>
                  <td className="text-muted">{user.email}</td>
                  <td>
                    <span className={`badge ${user.role === 'admin' ? 'badge-primary' : 'badge-warning'}`}>
                      {user.role}
                    </span>
                  </td>
                  <td>
                    <span className={`badge ${user.is_active ? 'badge-success' : 'badge-danger'}`}>
                      {user.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td style={{ textAlign: 'right' }}>
                    <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.5rem' }}>
                      <button className="btn-icon"><Edit2 size={16} /></button>
                      <button className="btn-icon" style={{ color: 'var(--danger)' }}><Trash2 size={16} /></button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Users;
