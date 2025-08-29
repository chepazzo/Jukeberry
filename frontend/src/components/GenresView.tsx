import React from 'react';

interface GenresViewProps {
  genres: string[];
  onSelectGenre: (genre: string) => void;
}

const GenresView: React.FC<GenresViewProps> = ({ genres, onSelectGenre }) => {
  return (
    <div>
      <h2>Genres</h2>
      {genres.length === 0 ? (
        <p>Loading genres...</p>
      ) : (
        <div className="grid-container">
          {genres.map((genre) => (
            <div key={genre} className="grid-item" onClick={() => onSelectGenre(genre)}>
              {genre}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default GenresView;
