import React from 'react';

interface ArtistsViewProps {
  artists: string[];
  onSelectArtist: (artist: string) => void;
}

const ArtistsView: React.FC<ArtistsViewProps> = ({ artists, onSelectArtist }) => {
  return (
    <div>
      <h2>Artists</h2>
      {artists.length === 0 ? (
        <p>Loading artists...</p>
      ) : (
        <ul>
          {artists.map((artist) => (
            <li key={artist} onClick={() => onSelectArtist(artist)} style={{ cursor: 'pointer' }}>
              {artist}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ArtistsView;
