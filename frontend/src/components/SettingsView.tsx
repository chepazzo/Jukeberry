import React, { useState, useEffect } from 'react';
import type { AlwaysOnConfig, AlwaysOnFilter } from '../services/api';

interface SettingsViewProps {
  config: AlwaysOnConfig | null;
  artists: string[];
  genres: string[];
  onSave: (config: AlwaysOnConfig) => void;
}

const SettingsView: React.FC<SettingsViewProps> = ({ config, artists, genres, onSave }) => {
  const [status, setStatus] = useState(false);
  const [filterType, setFilterType] = useState<'artist' | 'genre'>('artist');
  const [filterValue, setFilterValue] = useState('');

  useEffect(() => {
    if (config) {
      setStatus(config.status);
      if (config.filters.length > 0) {
        setFilterType(config.filters[0].attr);
        setFilterValue(config.filters[0].value);
      }
    }
  }, [config]);

  const handleSave = () => {
    const newFilters: AlwaysOnFilter[] = [];
    if (filterValue) {
      newFilters.push({ attr: filterType, value: filterValue });
    }
    onSave({ status, filters: newFilters });
  };

  if (!config) {
    return <p>Loading settings...</p>;
  }

  return (
    <div>
      <h2>Settings</h2>
      <div>
        <h3>Always On</h3>
        <button onClick={() => setStatus(true)} disabled={status}>Enable</button>
        <button onClick={() => setStatus(false)} disabled={!status}>Disable</button>
      </div>
      <div style={{ marginTop: '20px' }}>
        <h3>Always On Filter</h3>
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
