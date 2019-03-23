Jukeberry
=========

A simple Jukebox App for my Raspberry Pi. This is meant to act as a self-contained jukebox, not a full-featured media player. As such, it is essentially a 'now playing' queue. A user can browse by artist or genre and select a song to be added to the queue. By default, music is read either from disk or USB stick (if you want, you can mount a shared network drive in /var/media/music, but there is currently no GUI configuration mechanism to accomplish this). Also, while you can control the jukebox from your phone's browser, you explicitly cannot stream content from your phone or mobile device. As the perceived use case is for in a party/business environment, you would want more control over the music played to avoid inappropriate content. If, however, you are using this for a more personal use, then why wouldn't you just use a standard full-featured music player?

## Overview
The application consists of two parts:  

1. The Controller:
  * Controls the playing of music and catalog, etc.
  * Controlled by ReST API (currently Flask)

2. The Web Interface:
  * Basic web interface using AngularJS and Flask templates
  * Web interface will default to assume controller is local and connect to localhost:5000

## Installation

### Quick Install

While the application was meant to be installed on a raspberry pi, it's really just a webserver, so it can run anywhere.
Keep in mind, though, that the audio will be played from the device on which it is installed; streaming to a brownser
is not supported.

To install on your local machine:
1. use the python installer:
   ```bash
   sudo python3 setup.py install
   ```

   This will install the python libraries and installs:
   - `/usr/local/bin/start_jukeberry`
   - `/usr/local/bin/juke-loadcatalog`
   - `/etc/jukeberry.ini`

2. Toss some mp3 files into `/var/media/music`
3. Start application
   ```bash
   start_jukeberry
   ```
4. Load your library
   ```bash
   juke-loadcatalog
   ```
5. Enjoy your music:
   http://localhost:5000/

If some of your mp3s aren't recognized as mp3, you can copy the included `install/magic.mime` file
to `/etc/magic.mime`

### Run as a service

If you want to run Jukeberry as a service whenever the device boots:
```bash
sudo cp install/deb/jukeberry.service /lib/systemd/system/jukeberry.service
sudo systemctl enable jukeberry.service
sudo service jukeberry start
juke-loadcatalog
```

### Alternate media player
The default media player is omxplayer which is comes with raspbian. You can, however, change this to use
whichever player you want (e.g. mpg321).

### Ansible install
I have included an Ansible role for installation to make things super easy.

See `install/ansible/README.md` for details

## Config File
See example config file for detailed explanation of options

The config file follows a standard .ini file format.

**DEBUG** Default: False
**AUTOLOAD** Default: False
**THREADED** Default: True
**SSL** Default: False
**PLAYER** Default: omxplayer
**LIB** Default: /var/media/music/

**SSL_CRT** /path/to/crt.crt (only valid when SSL is true)
**SSL_KEY** /path/to/key.key (only valid when SSL is true)

**HOST** Default: 0.0.0.0
**PORT** Default: 5000

Roadmap
----

v2.x:
* Change navigation to be more Jukebox-ish
  * Show only 2 or 4 artists or songs in a view.
  * Include large next/prev buttons.
* Optimize separately for two views:
  1. Raspberry Pi touchscreen/mobile (320x240).
  2. Remote web browser (800x500?).

vY.x:
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

