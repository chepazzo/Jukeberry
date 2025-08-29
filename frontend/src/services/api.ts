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

export interface AlwaysOnConfig {
  status: boolean;
  filters: AlwaysOnFilter[];
}

// The API response seems to be wrapped in a 'data' object.
interface ApiResponse<T> {
  data: T;
}

const API_BASE_URL = '/api';

export const getSongs = async (): Promise<Song[]> => {
  const response = await fetch(`${API_BASE_URL}/get_songs`);
  if (!response.ok) {
    throw new Error('Failed to fetch songs');
  }
  const result: ApiResponse<Song[]> = await response.json();
  return result.data;
};

export const getCurrentSong = async (): Promise<Song | null> => {
  const response = await fetch(`${API_BASE_URL}/get_currsong`);
  if (!response.ok) {
    throw new Error('Failed to fetch current song');
  }
  const result: ApiResponse<Song | null> = await response.json();
  return result.data;
};

export const getPlaylist = async (): Promise<Song[]> => {
  const response = await fetch(`${API_BASE_URL}/get_playlist`);
  if (!response.ok) {
    throw new Error('Failed to fetch playlist');
  }
  const result: ApiResponse<Song[]> = await response.json();
  return result.data;
};

export const addSongToPlaylist = async (artist: string, title: string): Promise<void> => {
  const response = await fetch(`${API_BASE_URL}/add`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ artist, title }),
    });

  if (!response.ok) {
    throw new Error('Failed to add song to playlist');
  }
};

export const addRandomSongToPlaylist = async (filter?: { type: 'artist' | 'genre'; value: string }): Promise<void> => {
  const response = await fetch(`${API_BASE_URL}/add_random`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: filter ? JSON.stringify({ [filter.type]: filter.value }) : JSON.stringify({}),
    });

  if (!response.ok) {
    throw new Error('Failed to add random song');
  }
};

export const getAlwaysOn = async (): Promise<AlwaysOnConfig> => {
  const response = await fetch(`${API_BASE_URL}/get_alwayson`);
  if (!response.ok) {
    throw new Error('Failed to fetch always on config');
  }
  const result: ApiResponse<AlwaysOnConfig> = await response.json();
  return result.data;
};

export const setAlwaysOn = async (config: AlwaysOnConfig): Promise<void> => {
  const response = await fetch(`${API_BASE_URL}/set_alwayson`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(config),
  });

  if (!response.ok) {
    throw new Error('Failed to set always on config');
  }
};
