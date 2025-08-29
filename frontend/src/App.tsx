import { useState, useEffect } from 'react';
import './App.css';
import CurrentView from './components/CurrentView';
import ArtistsView from './components/ArtistsView';
import GenresView from './components/GenresView';
import BrowseView from './components/BrowseView';
import SettingsView from './components/SettingsView';
import SongListView from './components/SongListView';
import { getSongs, getCurrentSong, getPlaylist, addSongToPlaylist, addRandomSongToPlaylist, getAlwaysOn, setAlwaysOn } from './services/api';
import type { Song, AlwaysOnConfig } from './services/api';

type View = 'current' | 'artists' | 'genres' | 'browse' | 'songlist' | 'settings';

function App() {
  const [currentView, setCurrentView] = useState<View>('current');
  const [songs, setSongs] = useState<Song[]>([]);
  const [artists, setArtists] = useState<string[]>([]);
  const [genres, setGenres] = useState<string[]>([]);
  const [filter, setFilter] = useState<{ type: 'artist' | 'genre'; value: string } | null>(null);
  const [currentSong, setCurrentSong] = useState<Song | null>(null);
  const [playlist, setPlaylist] = useState<Song[]>([]);
  const [alwaysOn, setAlwaysOnState] = useState<AlwaysOnConfig | null>(null);

  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const [fetchedSongs, alwaysOnConfig] = await Promise.all([
          getSongs(),
          getAlwaysOn(),
        ]);
        setSongs(fetchedSongs);
        setAlwaysOnState(alwaysOnConfig);

        // Derive unique, sorted lists for artists and genres
        const uniqueArtists = [...new Set(fetchedSongs.flatMap(song => song.artist))].sort();
        // Assuming 'album' can be used as a proxy for genre for now, based on original app structure.
        const uniqueGenres = [...new Set(fetchedSongs.map(song => song.album))].sort();

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
      await addSongToPlaylist(artist, title);
      // Refresh playlist immediately after adding a song
      const pList = await getPlaylist();
      setPlaylist(pList);
    } catch (error) {
      console.error('Error adding song:', error);
    }
  };

  const handleRandomSong = async () => {
    try {
      await addRandomSongToPlaylist(filter || undefined);
      const pList = await getPlaylist();
      setPlaylist(pList);
    } catch (error) {
      console.error('Error adding random song:', error);
    }
  };

  const handleSetAlwaysOn = async (config: AlwaysOnConfig) => {
    try {
      await setAlwaysOn(config);
      setAlwaysOnState(config);
    } catch (error) {
      console.error('Error setting always on config:', error);
    }
  };

  const renderView = () => {
    switch (currentView) {
      case 'current':
        return <CurrentView currentSong={currentSong} playlist={playlist} alwaysOn={alwaysOn} />;
      case 'artists':
        return <ArtistsView artists={artists} onSelectArtist={(artist: string) => handleFilterSelect('artist', artist)} />;
      case 'genres':
        return <GenresView genres={genres} onSelectGenre={(genre: string) => handleFilterSelect('genre', genre)} />;
      case 'songlist': {
        if (!filter) return <p>No filter selected.</p>;
        const filteredSongs = songs.filter(song => {
          if (filter.type === 'artist') {
            return song.artist.includes(filter.value);
          }
          if (filter.type === 'genre') {
            // Using album as genre proxy
            return song.album === filter.value;
          }
          return false;
        });
        return <SongListView songs={filteredSongs} onAddSong={handleAddSong} />;
      }
      case 'browse':
        return <BrowseView songs={songs} onAddSong={handleAddSong} />;
      case 'settings':
        return <SettingsView config={alwaysOn} artists={artists} genres={genres} onSave={handleSetAlwaysOn} />;
      default:
        return <CurrentView currentSong={currentSong} playlist={playlist} alwaysOn={alwaysOn} />;
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Jukeberry</h1>
      </header>
      <nav className="app-nav">
        <button onClick={() => setCurrentView('current')}>Top</button>
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
