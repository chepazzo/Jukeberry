import React from 'react';
import type { Song } from '../services/api';
import { formatSeconds } from '../utils/time';

interface SongItemProps {
  song: Song;
  onClick?: (artist: string, title: string) => void;
}

const SongItem: React.FC<SongItemProps> = ({ song, onClick }) => {
  const handleClick = () => {
    if (onClick) {
      onClick(song.artist.join(','), song.title);
    }
  };

  return (
    <div className="song" onClick={handleClick} style={{ cursor: onClick ? 'pointer' : 'default' }}>
      {song.has_art && (
        <div className="album-art">
          <img src={`/api/art/${song.id}`} alt={`${song.album} album art`} />
        </div>
      )}
      <div className="song-info">
        <div>
          <span className="name">{song.title}</span>
          <span className="time">[{formatSeconds(song.secs)}]</span>
        </div>
        <table className="details">
          <tbody>
            <tr>
              <td className="label">Artist(s):</td>
              <td><span className="artist">{song.artist.join(', ')}</span></td>
            </tr>
            <tr>
              <td className="label">Album:</td>
              <td><span className="album">{song.album}</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default SongItem;
