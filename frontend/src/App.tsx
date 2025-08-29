import { useState, useEffect } from 'react';
import './App.css';
import CurrentView from './components/CurrentView';
import ArtistsView from './components/ArtistsView';
import GenresView from './components/GenresView';
import BrowseView from './components/BrowseView';
import SettingsView from './components/SettingsView';
import SongListView from './components/SongListView';
import { getSongs, getCurrentSong, getPlaylist, addSongToPlaylist, addRandomSong, getAutoPlay, setAutoPlay, skip, loadCatalog } from './services/api';
import type { Song, AutoPlayConfig } from './services/api';

type View = 'current' | 'artists' | 'genres' | 'browse' | 'songlist' | 'settings';

function App() {
  const [currentView, setCurrentView] = useState<View>('current');
  const [songs, setSongs] = useState<Song[]>([]);
  const [artists, setArtists] = useState<string[]>([]);
  const [genres, setGenres] = useState<string[]>([]);
  const [filter, setFilter] = useState<{ type: 'artist' | 'genre'; value: string } | null>(null);
  const [currentSong, setCurrentSong] = useState<Song | null>(null);
  const [playlist, setPlaylist] = useState<Song[]>([]);
  const [autoPlay, setAutoPlayState] = useState<AutoPlayConfig | null>(null);

  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const [fetchedSongs, autoPlayConfig] = await Promise.all([
          getSongs(),
          getAutoPlay(),
        ]);
        setSongs(fetchedSongs);
        setAutoPlayState(autoPlayConfig);

        // Derive unique, sorted lists for artists and genres
        const uniqueArtists = [...new Set(fetchedSongs.flatMap((song: Song) => song.artist))].sort();
        const uniqueGenres = [...new Set(fetchedSongs.flatMap((song: Song) => song.genre || []))].sort();

        setArtists(uniqueArtists);
        setGenres(uniqueGenres);

      } catch (error) {
        console.error('Error fetching songs:', error);
      }
    };

    fetchInitialData();
  }, []);

  useEffect(() => {
    const refreshPlaylist = async () => {
      try {
        const [curr, pList] = await Promise.all([getCurrentSong(), getPlaylist()]);
        setCurrentSong(curr);
        setPlaylist(pList);
      } catch (error) {
        console.error('Error refreshing playlist:', error);
      }
    };

    refreshPlaylist(); // Initial fetch
    const intervalId = setInterval(refreshPlaylist, 10000); // Poll every 10 seconds

    return () => clearInterval(intervalId); // Cleanup on unmount
  }, []);

  const handleFilterSelect = (type: 'artist' | 'genre', value: string) => {
    setFilter({ type, value });
    setCurrentView('songlist');
  };

  const handleAddSong = async (artist: string, title: string) => {
    try {
      await addSongToPlaylist({ artist: [artist], title });
      // Refresh playlist and current song immediately after adding a song
      const [newCurrentSong, newPlaylist] = await Promise.all([getCurrentSong(), getPlaylist()]);
      setCurrentSong(newCurrentSong);
      setPlaylist(newPlaylist);
    } catch (error) {
      console.error('Error adding song:', error);
    }
  };

  const handleRandomSong = async () => {
    try {
      await addRandomSong(filter || {});
      // Refresh playlist and current song immediately after adding a song
      const [newCurrentSong, newPlaylist] = await Promise.all([getCurrentSong(), getPlaylist()]);
      setCurrentSong(newCurrentSong);
      setPlaylist(newPlaylist);
    } catch (error) {
      console.error('Error adding random song:', error);
    }
  };

  const handleSkipSong = async () => {
    try {
      await skip();
      // After skipping, we should refetch the current song and playlist
      const [newCurrentSong, newPlaylist] = await Promise.all([getCurrentSong(), getPlaylist()]);
      setCurrentSong(newCurrentSong);
      setPlaylist(newPlaylist);
    } catch (error) {
      console.error('Error skipping song:', error);
    }
  };

  const handleSetAutoPlay = async (config: AutoPlayConfig) => {
    try {
      await setAutoPlay(config);
      setAutoPlayState(config);
    } catch (error) {
      console.error('Error setting auto play config:', error);
    }
  };

  const handleReloadCatalog = async () => {
    try {
      const fetchedSongs = await loadCatalog();
      setSongs(fetchedSongs);
      const uniqueArtists = [...new Set(fetchedSongs.flatMap((song: Song) => song.artist))].sort();
      const uniqueGenres = [...new Set(fetchedSongs.flatMap((song: Song) => song.genre || []))].sort();
      setArtists(uniqueArtists);
      setGenres(uniqueGenres);
      alert('Catalog reloaded successfully!');
    } catch (error) {
      console.error('Error reloading catalog:', error);
      alert('Failed to reload catalog.');
    }
  };

  const renderView = () => {
    switch (currentView) {
      case 'current':
        return <CurrentView currentSong={currentSong} playlist={playlist} autoPlay={autoPlay} onSkip={handleSkipSong} />;
      case 'artists':
        return <ArtistsView artists={artists} onSelectArtist={(artist: string) => handleFilterSelect('artist', artist)} />;
      case 'genres':
        return <GenresView genres={genres} onSelectGenre={(genre: string) => handleFilterSelect('genre', genre)} />;
      case 'songlist': {
        if (!filter) return <p>No filter selected.</p>;
        const filteredSongs = songs.filter((song: Song) => {
          if (filter.type === 'artist') {
            return song.artist.includes(filter.value);
          }
          if (filter.type === 'genre') {
            return song.genre && song.genre.includes(filter.value);
          }
          return false;
        });
        return <SongListView songs={filteredSongs} onAddSong={handleAddSong} />;
      }
      case 'browse':
        return <BrowseView songs={songs} onAddSong={handleAddSong} />;
      case 'settings':
        return <SettingsView config={autoPlay} artists={artists} genres={genres} onSave={handleSetAutoPlay} onReloadCatalog={handleReloadCatalog} />;
      default:
        return <CurrentView currentSong={currentSong} playlist={playlist} autoPlay={autoPlay} onSkip={handleSkipSong} />;
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Jukeberry</h1>
      </header>
      <nav className="app-nav">
        <button onClick={() => setCurrentView('current')}>Now Playing</button>
        <button onClick={() => setCurrentView('artists')}>Artists</button>
        <button onClick={() => setCurrentView('genres')}>Genres</button>
        <button onClick={() => setCurrentView('browse')}>Browse</button>
        <button onClick={handleRandomSong}>Random</button>
        <button onClick={() => setCurrentView('settings')}>Settings</button>
      </nav>
      <main className="app-main">
        {renderView()}
      </main>
    </div>
  );
}

export default App;
