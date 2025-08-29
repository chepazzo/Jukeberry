import React from 'react';
import type { Song } from '../services/api';
import { formatSeconds } from '../utils/time';

interface SongListViewProps {
  songs: Song[];
  onAddSong: (artist: string, title: string) => void;
}

const SongListView: React.FC<SongListViewProps> = ({ songs, onAddSong }) => {
  if (songs.length === 0) {
    return <p>No songs found.</p>;
  }

  return (
    <ul>
      {songs.map((song, index) => (
        <li key={index} onClick={() => onAddSong(song.artist.join(','), song.title)} style={{ cursor: 'pointer' }}>
          <strong>{song.title}</strong> ({formatSeconds(song.secs)}) by {song.artist.join(', ')} - <em>{song.album}</em>
        </li>
      ))}
    </ul>
  );
};

export default SongListView;
