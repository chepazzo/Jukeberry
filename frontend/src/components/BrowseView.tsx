import React from 'react';
import type { Song } from '../services/api';
import SongListView from './SongListView';

interface BrowseViewProps {
  songs: Song[];
  onAddSong: (artist: string, title: string) => void;
}

const BrowseView: React.FC<BrowseViewProps> = ({ songs, onAddSong }) => {
  return (
    <div>
      <h2>Browse All Songs</h2>
      {songs.length === 0 ? (
        <p>Loading songs...</p>
      ) : (
        <SongListView songs={songs} onAddSong={onAddSong} />
      )}
    </div>
  );
};

export default BrowseView;
