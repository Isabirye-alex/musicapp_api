import React, { useState, useEffect } from 'react';
import { Play, MoreVertical, Trash2 } from 'lucide-react';
import { fetchSongs } from '../api/client';

const Songs = () => {
  const [songs, setSongs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      const data = await fetchSongs();
      if (data && data.length > 0) {
        setSongs(data);
      } else {
        // Fallback mock data if API fails or is empty
        setSongs([
          { id: '1', song_name: 'Blinding Lights', artist_name: 'The Weeknd', thumbnail_url: 'https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?auto=format&fit=crop&q=80&w=100&h=100', hex_code: '#eab308' },
          { id: '2', song_name: 'Shape of You', artist_name: 'Ed Sheeran', thumbnail_url: 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&q=80&w=100&h=100', hex_code: '#3b82f6' },
          { id: '3', song_name: 'Levitating', artist_name: 'Dua Lipa', thumbnail_url: 'https://images.unsplash.com/photo-1493225457124-a1a2a5956093?auto=format&fit=crop&q=80&w=100&h=100', hex_code: '#ec4899' },
          { id: '4', song_name: 'Stay', artist_name: 'The Kid LAROI, Justin Bieber', thumbnail_url: 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&q=80&w=100&h=100', hex_code: '#8b5cf6' },
        ]);
      }
      setLoading(false);
    };
    loadData();
  }, []);

  return (
    <div className="songs-page">
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 className="h2 text-gradient">Songs Library</h1>
          <p className="text-muted">Manage all uploaded songs on the platform.</p>
        </div>
      </div>

      <div className="table-container glass-card" style={{ padding: 0, overflow: 'hidden' }}>
        <table className="data-table">
          <thead>
            <tr>
              <th>Track</th>
              <th>Artist</th>
              <th>Color Accent</th>
              <th style={{ textAlign: 'right' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan="4" style={{ textAlign: 'center', padding: '3rem' }}>Loading songs...</td>
              </tr>
            ) : (
              songs.map(song => (
                <tr key={song.id}>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                      <div style={{ width: '40px', height: '40px', borderRadius: 'var(--radius-sm)', overflow: 'hidden', position: 'relative' }}>
                        {song.thumbnail_url ? (
                           <img src={song.thumbnail_url} alt="thumbnail" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                        ) : (
                           <div style={{ width: '100%', height: '100%', background: 'var(--bg-card-hover)' }}></div>
                        )}
                        <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', background: 'rgba(0,0,0,0.4)', display: 'flex', alignItems: 'center', justifyContent: 'center', opacity: 0, transition: 'opacity var(--transition-fast)', cursor: 'pointer' }}
                             onMouseEnter={(e) => e.currentTarget.style.opacity = 1}
                             onMouseLeave={(e) => e.currentTarget.style.opacity = 0}
                        >
                          <Play size={16} fill="white" />
                        </div>
                      </div>
                      <div style={{ fontWeight: 500 }}>{song.song_name}</div>
                    </div>
                  </td>
                  <td className="text-muted">{song.artist_name}</td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <div style={{ width: '16px', height: '16px', borderRadius: '50%', background: song.hex_code || 'var(--accent-primary)' }}></div>
                      <span className="text-muted" style={{ fontSize: '0.875rem' }}>{song.hex_code || '#000000'}</span>
                    </div>
                  </td>
                  <td style={{ textAlign: 'right' }}>
                    <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.5rem' }}>
                      <button className="btn-icon" style={{ color: 'var(--danger)' }}><Trash2 size={16} /></button>
                      <button className="btn-icon"><MoreVertical size={16} /></button>
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

export default Songs;
