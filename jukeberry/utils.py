import subprocess
import threading
import time

from pprint import pprint as pp

def find_player(name=None):
    ## Find mpg123 executable
    if name is None:
        return None
    p=subprocess.Popen(["which", name],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    return p.stdout.read().replace("\n", "")

def _popenAndCall(onExit, popenArgs):
    """
    Runs the given args in a subprocess.Popen, and then calls the function
    onExit when the subprocess completes.
    onExit is a callable object, and popenArgs is a list/tuple of args that 
    would give to subprocess.Popen.
    """
    def runInThread(onExit, popenArgs):
        proc = subprocess.Popen(*popenArgs)
        proc.wait()
        onExit()
        return
    thread = threading.Thread(target=runInThread, args=(onExit, popenArgs))
    thread.start()
    pp(dir(thread))
    # returns immediately after the thread starts
    return thread

def secs2ms(secs):
    (h,m,s) = _secs2hms(secs)
    ms = "{: 2}:{:02}".format(m,s)
    return ms

def _secs2hms(secs):
    t = time.gmtime(secs)
    return (t.tm_hour,t.tm_min,t.tm_sec)
