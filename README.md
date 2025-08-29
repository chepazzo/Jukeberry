# Jukeberry

A simple, self-contained Jukebox application, originally designed for the Raspberry Pi. The backend is powered by Python and Flask, with a modern, decoupled frontend built with React and TypeScript.

## Overview

The application consists of two main parts:

1.  **Backend (Flask):** A Python-based ReST API that manages the song catalog, controls music playback, and handles the playlist queue.
2.  **Frontend (React):** A modern, single-page application (SPA) built with React, TypeScript, and Vite. It communicates with the Flask backend via the API.

## Installation

Follow these steps to set up the backend and frontend.

### Backend Setup

1.  **Create and activate a Python virtual environment:**
    ```bash
    python3 -m venv jukeberry-venv
    source jukeberry-venv/bin/activate
    ```

2.  **Install Python dependencies:**
    ```bash
    pip install -e .
    ```
    This installs the necessary libraries and makes the `start_jukeberry` and `juke-loadcatalog` commands available.

3.  **Configure the application:**
    Copy the example configuration file:
    ```bash
    cp config/jukeberry.example.ini jukeberry.conf
    ```
    Then, edit `jukeberry.conf` to specify your music library path and other settings.

### Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```

## Running the Application

### Development

For development, you'll need to run the Flask backend and the Vite frontend dev server in separate terminals.

1.  **Start the Backend:**
    In the project root, with your Python virtual environment activated, run:
    ```bash
    start_jukeberry
    ```

2.  **Start the Frontend:**
    In the `frontend` directory, run the Vite development server:
    ```bash
    npm run dev
    ```
    The React frontend will be available at `http://localhost:5173`. The Vite server is configured to proxy API requests to the Flask backend, so everything should work seamlessly.

3.  **Load Your Music Catalog:**
    In a third terminal (with the Python venv activated), run:
    ```bash
    juke-loadcatalog
    ```

### Production

For a production deployment, you first need to build the React frontend.

1.  **Build the Frontend:**
    In the `frontend` directory, run:
    ```bash
    npm run build
    ```
    This will create an optimized, static build of the application in the `frontend/dist` directory.

2.  **Run the Production Server:**
    Start the Flask server as you would for development. It is automatically configured to serve the built frontend from the `frontend/dist` directory.
    ```bash
    start_jukeberry
    ```

3.  **Access the Application:**
    The application will be available at `http://localhost:5000`.

## Raspberry Pi Setup

For running on a Raspberry Pi in kiosk mode, you can configure the system to launch the browser on startup.

1.  Open `/home/pi/.config/lxsession/LXDE-pi/autostart` for editing.
2.  Add the following line to the end:
    ```
    @chromium-browser --kiosk http://localhost:5000/
    ```

