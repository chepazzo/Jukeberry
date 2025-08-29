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
        <div className="grid-container">
          {artists.map((artist) => (
            <div key={artist} className="grid-item" onClick={() => onSelectArtist(artist)}>
              {artist}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ArtistsView;
