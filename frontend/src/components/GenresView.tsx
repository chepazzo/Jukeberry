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
        <ul>
          {genres.map((genre) => (
            <li key={genre} onClick={() => onSelectGenre(genre)} style={{ cursor: 'pointer' }}>
              {genre}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default GenresView;
