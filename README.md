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

## Hardware

### Current Tested Components

This is what I am currently using:

1. $35 - Raspberry Pi B (Discontinued)
2. $35 - [PiTFT Mini Kit - 320x240 2.8" TFT+Touchscreen for Raspberry Pi](https://www.adafruit.com/product/1601) (req solder assembly)
3. $10 - [Adafruit PiTFT Enclosure for Raspberry Pi Model B](https://www.amazon.com/gp/product/B00MBWMIGO)
4. $ 6 - [Adafruit Tactile Switch Buttons (6mm slim)](https://www.amazon.com/gp/product/B00KAE2I7E/)

### Newer Components

I **think** these will work together, but I haven't actually tried to assemble them.

1. $50 - [Raspberry Pi 3 B+](https://www.amazon.com/gp/product/B07BC6WH7V) (incl power, heat sinks)
2. $45 - [Adafruit (PID 2423) PiTFT Plus 320x240 2.8" TFT + Capacitive Touchscreen](https://www.amazon.com/gp/product/B01HN0LL2A) (pre-assembled)
3. $ 9 - [Pi Model B+ / Pi 2 / Pi 3 - Case Base and Faceplate Pack - Clear - for 2.8" PiTFT](https://www.adafruit.com/product/3062)

I also want to try some larger screens and cases. Like the [SmartiPi Touch case for The Official Raspberry Pi 7" Touchscreen Display - Adjustable Angle](https://www.amazon.com/SmartiPi-Official-Raspberry-Touchscreen-Display/dp/B01HV97F64/).

## Wish List

* Add wifi and other setup options to "Settings" view.
* Add volume up/down control
  * These commands only work with `mpg321`, not with `omxplayer`:
    - inc 5%: `amixer set PCM -- $[$(amixer get PCM|grep -o [0-9]*%|sed 's/%//')+5]%`
    - dec 5%: `amixer set PCM -- $[$(amixer get PCM|grep -o [0-9]*%|sed 's/%//')5]%`
* Update "Settings" view.
* Add support for newer touchscreens
* Add Functionality for the 4 buttons on PiTFT displays
  * e.g. volume control, play random, re-load music catalog, &c
* Change navigation to be more Jukebox-ish
  * Show only 2 or 4 artists or songs in a view.
  * Include large next/prev buttons.
* Optimize separately for two views:
  1. Raspberry Pi touchscreen/mobile (320x240).
  2. Remote web browser (800x500?).
* Web-ify setup on Raspberry Pi (wifi, etc).
* Web admin interface list Jukeboxes and allow user to specify which to control.
  * Will function similar to multi-DVR or media-center GUI.  Select from list and act as remote.
  * Allows server to run anywhere (even on localhost)
* Music Lib can be remote.
  * Needs web admin interface to add remote lib
  * Not sure how to implement the admin perms.  nfs might be bad.  want to avoid smb.
* Sync to playlists on local mobile devices.
  * Requires client app on phone.
  * Allows for consolidated playlists if named the same.
  * *Note*: I'm not sure how I file about this as it wouldn't really be a "Jukebox".
