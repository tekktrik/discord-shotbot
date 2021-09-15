import time

class CommandTimer:
    
    def __init__(self, single_lockout=10, fill_lockout=60):
    
        self._single_lockout_min = single_lockout
        self._fill_lockout_min = fill_lockout
        self._single_unlock_time = time.time()
        self._fill_unlock_time = time.time()
        self._in_progress_lock = False
        self._user_lock = False
        
    def isSingleTimerReady(self):
        return True if (time.time() >= self._single_unlock_time) else False
        
    def isFillTimerReady(self):
        return True if (time.time() >= self._fill_unlock_time) else False
        
    def resetTimers(self):
        self._single_unlock_time = time.time() + self._single_lockout_min*60
        self._fill_unlock_time = time.time() + self._fill_lockout_min*60
        
    def getTimerTimeRemaining(self):
        single_time_remain = self._single_unlock_time - time.time()
        fill_time_remain = self._fill_unlock_time - time.time()
        return single_time_remain/60, fill_time_remain/60
        
    def setInProgress(self):
        self._in_progress_lock = True
        
    def markProgressComplete(self):
        self._in_progress_lock = False
        
    def isInProgress(self):
        return self._in_progress_lock
        
    def setUserLockOn(self):
        self._user_lock = True
        
    def setUserLockOff(self):
        self._user_lock = False
        
    def isUserLockSet(self):
        return self._user_lock