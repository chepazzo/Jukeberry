import React from 'react';
import type { Song } from '../services/api';
import SongItem from './SongItem';

interface SongListViewProps {
  songs: Song[];
  onAddSong: (artist: string, title: string) => void;
}

const SongListView: React.FC<SongListViewProps> = ({ songs, onAddSong }) => {
  if (songs.length === 0) {
    return <p>No songs found.</p>;
  }

  return (
    <div className="song-list-container">
      {songs.map((song, index) => (
        <SongItem key={index} song={song} onClick={onAddSong} />
      ))}
    </div>
  );
};

export default SongListView;
