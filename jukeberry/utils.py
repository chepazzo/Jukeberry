# -*- coding: utf-8 -*-
'''
Utility functions.
'''
import subprocess
import threading
import time

from pprint import pprint as pp

def find_player(name=None):
    '''
    Finds the full path to the player app on the system.

    Args:
      name (str): The name of the music player to run.

    Returns:
      str: The fully qualified path to the music player on the system.
    '''
    ## Find mpg123 executable
    if name is None:
        return None
    p=subprocess.Popen(["which", name],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    return p.stdout.read().replace("\n", "")

def _popenAndCall(onExit, popenArgs):
    """
    Runs a program on the external system asynchronously.

    Args:
      onExit (obj): This should be the callback function to call (asynchronously) when
        the external program is run.

      popenArgs (list): A list/tuple of args to pass to subprocess.Popen.
        Usually, this is going to be : ``[<filename> <args>]``.

    Returns:
      threading.Thread: Thread object created that contains the running program.
    """
    def runInThread(onExit, popenArgs):
        proc = subprocess.Popen(*popenArgs)
        proc.wait()
        onExit()
        return
    thread = threading.Thread(target=runInThread, args=(onExit, popenArgs))
    thread.start()
    #pp(dir(thread))
    # returns immediately after the thread starts
    return thread

def secs2ms(secs):
    '''
    Converts seconds to ``mm:ss`` format.

    Args:
      secs (int): Number of seconds to convert.

    Returns:
      str: A ``mm:ss`` formatted string.
    '''
    (h,m,s) = _secs2hms(secs)
    ms = "{: 2}:{:02}".format(m,s)
    return ms

def _secs2hms(secs):
    '''
    Converts seconds to ``(h,m:s)``.

    Args:
      secs (int): Number of seconds to convert.

    Returns:
      tuple: A tuple of ints representing ``(h,m:s)``.
    '''
    t = time.gmtime(secs)
    return (t.tm_hour,t.tm_min,t.tm_sec)
