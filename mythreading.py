# poor man's threading: an implementation of java-style "synchronized"
# taken from http://theorangeduck.com/page/synchronized-python
 
import threading

def synchronized(func):
    func.__lock__ = threading.Lock()
		
    def synced_func(*args, **kws):
        with func.__lock__:
            return func(*args, **kws)

    return synced_func
    
