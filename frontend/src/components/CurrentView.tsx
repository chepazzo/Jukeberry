import React from 'react';
import type { Song, AlwaysOnConfig } from '../services/api';
import { formatSeconds } from '../utils/time';

interface CurrentViewProps {
  currentSong: Song | null;
  playlist: Song[];
  alwaysOn: AlwaysOnConfig | null;
}

const CurrentView: React.FC<CurrentViewProps> = ({ currentSong, playlist, alwaysOn }) => {
  const totalPlaylistSecs = playlist.reduce((acc, song) => acc + song.secs, 0);
  return (
    <div>
      <div>
        <h2>Currently Playing</h2>
        {currentSong ? (
          <div>
            <strong>{currentSong.title}</strong> ({formatSeconds(currentSong.secs)}) by {currentSong.artist.join(', ')}
            <br />
            <em>{currentSong.album}</em>
          </div>
        ) : (
          <p>Nothing is currently playing.</p>
        )}
      </div>

      <div style={{ marginTop: '20px' }}>
        <h2>Next Up ({formatSeconds(totalPlaylistSecs)})</h2>
        {playlist.length > 0 ? (
          <ol>
            {playlist.map((song, index) => (
              <li key={index}>
                <strong>{song.title}</strong> by {song.artist.join(', ')}
              </li>
            ))}
          </ol>
        ) : (
          <p>The playlist is empty.</p>
        )}
        {alwaysOn?.status && (
          <p style={{ marginTop: '10px', fontStyle: 'italic' }}>
            Always On is active.
            {alwaysOn.filters.length > 0 &&
              ` Filtering by: ${alwaysOn.filters[0].attr}: ${alwaysOn.filters[0].value}`}
          </p>
        )}
      </div>
    </div>
  );
};

export default CurrentView;
