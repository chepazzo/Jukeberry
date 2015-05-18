Jukeberry
=========

A simple Jukebox App for my Raspberry Pi. This is meant to act as a self-contained jukebox, not a full-featured media player. As such, it is essentially a 'now playing' queue. A user can browse by artist or genre and select a song to be added to the queue. By default, music is read either from disk or USB stick (if you want, you can mount a shared network drive in /var/media/music, but there is currently no GUI configuration mechanism to accomplish this). Also, while you can control the jukebox from your phone's browser, you explicitly cannot stream content from your phone or mobile device. As the perceived use case is for in a party/business environment, you would want more control over the music played to avoid inappropriate content. If, however, you are using this for a more personal use, then why wouldn't you just use a standard full-featured music player?

Overview
----
This will consist of two parts:  

1. The Controller:
  * Controls the playing of music and catalog, etc.
  * Controlled by ReST API (currently Flask)

2. The Web Interface:
  * Basic web interface using AngularJS and Flask templates
  * Web interface will default to assume controller is local and connect to localhost:5000

Roadmap
----

v1.x:
* Packaging, etc.
* NG-ify code.
* Auto-refresh now-playing and upcoming views.

v2.x:
* Convert to a Single-page application.
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

Previous Versions
-----------------
v0.1:
* Run web server on localhost
* Display currently playing song
* Display current list of songs in queue
* Add to playlist by specifying full path.
* Basic single playlist:
  * Songs added to end.
  * Songs removed when played.
* Music lib is local to controller.

v0.2: 
* Song catalog.
  * Crappy browse by artist --> song
  * Click song to add to queue.
