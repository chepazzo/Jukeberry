Jukeberry
=========

Attempt at a simple Jukebox App for my Raspberry Pi.

Overview
----
This will consist of two parts:  

1. The Controller:
  * Controls the playing of music and catalog, etc.
  * Controlled by ReST API (currently Flask)

2. The Web Interface:
  * Basic web interface using AngularJS and Flask templates
  * Web interface will default to assume controller is local and connect to localhost:5000

ToDo
----

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

v1.0:
* Web admin interface list Jukeboxes and allow user to specify which to control.
  * Will function similar to multi-DVR or media-center GUI.  Select from list and act as remote.
  * Allows server to run anywhere (even on localhost)
* Music Lib can be remote.
  * Needs web admin interface to add remote lib
  * Not sure how to implement the admin perms.  nfs might be bad.  want to avoid smb.
