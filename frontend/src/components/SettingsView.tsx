import React, { useState, useEffect } from 'react';
import type { AutoPlayConfig } from '../services/api';

interface SettingsViewProps {
  config: AutoPlayConfig | null;
  artists: string[];
  genres: string[];
  onSave: (config: AutoPlayConfig) => void;
}

const SettingsView: React.FC<SettingsViewProps> = ({ config, artists, genres, onSave }) => {
  const [status, setStatus] = useState(false);
  const [filterType, setFilterType] = useState('artist');
  const [filterValue, setFilterValue] = useState('');

  useEffect(() => {
    if (config) {
      setStatus(config.status);
      const filterKeys = Object.keys(config.filters);
      if (filterKeys.length > 0) {
        const key = filterKeys[0];
        setFilterType(key);
        setFilterValue(config.filters[key]);
      }
    }
  }, [config]);

  const handleSave = () => {
    const newFilters = filterValue ? { [filterType]: filterValue } : {};
    onSave({ status, filters: newFilters });
  };

  if (!config) {
    return <p>Loading settings...</p>;
  }

  return (
    <div>
      <h2>Settings</h2>
      <div>
        <h3>Auto Play</h3>
        <label>
          <input type="checkbox" checked={status} onChange={(e) => setStatus(e.target.checked)} />
          Enable Auto Play
        </label>
      </div>
      <div style={{ marginTop: '20px' }}>
        <h3>Auto Play Filter</h3>
        <select value={filterType} onChange={(e) => setFilterType(e.target.value as 'artist' | 'genre')}>
          <option value="artist">Artist</option>
          <option value="genre">Genre (by Album)</option>
        </select>
        <select value={filterValue} onChange={(e) => setFilterValue(e.target.value)}>
          <option value="">-- Select --</option>
          {(filterType === 'artist' ? artists : genres).map(item => (
            <option key={item} value={item}>{item}</option>
          ))}
        </select>
      </div>
      <button onClick={handleSave} style={{ marginTop: '20px' }}>Save Settings</button>
    </div>
  );
};

export default SettingsView;
