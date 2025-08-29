import React from 'react';
import type { Song, AutoPlayConfig } from '../services/api';
import { formatSeconds } from '../utils/time';
import SongItem from './SongItem';

interface CurrentViewProps {
  currentSong: Song | null;
  playlist: Song[];
  autoPlay: AutoPlayConfig | null;
}

const CurrentView: React.FC<CurrentViewProps> = ({ currentSong, playlist, autoPlay }) => {
  const totalPlaylistSecs = playlist.reduce((acc, song) => acc + song.secs, 0);
  return (
    <div>
      <div>
        <h2>Currently Playing</h2>
        {currentSong ? (
          <SongItem song={currentSong} />
        ) : (
          <p>Nothing is currently playing.</p>
        )}
      </div>

      <div style={{ marginTop: '20px' }}>
        <h2>Next Up ({formatSeconds(totalPlaylistSecs)})</h2>
        {playlist.length > 0 ? (
          <div className="song-list-container">
            {playlist.map((song, index) => (
              <SongItem key={index} song={song} />
            ))}
          </div>
        ) : (
          <p>The playlist is empty.</p>
        )}
        {autoPlay?.status && (
          <p style={{ marginTop: '10px', fontStyle: 'italic' }}>
            Auto Play is active.
            {Object.keys(autoPlay.filters).length > 0 &&
              ` Filtering by: ${Object.keys(autoPlay.filters)[0]}: ${Object.values(autoPlay.filters)[0]}`}
          </p>
        )}
      </div>
    </div>
  );
};

export default CurrentView;
