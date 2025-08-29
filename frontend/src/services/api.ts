export interface Song {
  title: string;
  artist: string[];
  album: string;
  secs: number;
  genre?: string; // Genre is not in the original model, but good to have
}

export interface AlwaysOnFilter {
  attr: 'artist' | 'genre';
  value: string;
}

export interface AutoPlayConfig {
  status: boolean;
  filters: Record<string, string>;
}

// The API response seems to be wrapped in a 'data' object.
interface ApiResponse<T> {
  status: 'success' | 'fail';
  data: T;
  message?: string;
}

const API_BASE_URL = '/api';

const fetchApi = async <T>(url: string, options?: RequestInit): Promise<T> => {
  const response = await fetch(`${API_BASE_URL}${url}`, options);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  const result: ApiResponse<T> = await response.json();
  if (result.status === 'fail') {
    throw new Error(result.message || 'API request failed');
  }
  return result.data;
};

export const getSongs = (): Promise<Song[]> => fetchApi('/get/songs');

export const getPlaylist = (): Promise<Song[]> => fetchApi('/get/playlist');

export const getCurrentSong = (): Promise<Song | null> => fetchApi('/get/currsong');

export const loadCatalog = (): Promise<Song[]> => fetchApi('/loadcatalog');

export const addSongToPlaylist = (song: Partial<Song>): Promise<void> => 
  fetchApi('/add', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(song),
  });

export const addRandomSong = (filters: Record<string, string>): Promise<void> => 
  fetchApi('/add_random', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(filters),
  });

export const removeSongFromPlaylist = (id: number): Promise<void> => 
  fetchApi('/rm', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id }),
  });

export const play = (): Promise<void> => fetchApi('/play', { method: 'POST' });

export const pause = (): Promise<void> => fetchApi('/pause', { method: 'POST' });

export const skip = (): Promise<void> => fetchApi('/skip', { method: 'POST' });

export const setVolume = (level: number): Promise<void> => 
  fetchApi('/volume', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ level }),
  });

export const getAutoPlay = (): Promise<AutoPlayConfig> => fetchApi('/get/autoplay');

export const setAutoPlay = (settings: AutoPlayConfig): Promise<void> => 
  fetchApi('/set/autoplay', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(settings),
  });
