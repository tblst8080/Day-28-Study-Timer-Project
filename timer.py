import time


class Timer:
    def __init__(self):
        # default timer values
        self.t_reference = None
        self.is_paused = False

        self.lapse = 0
        self.paused_lapse = 0
        # switch for automatic time-check
        self.is_timing = False

        # tracks the activity progress
        self.progress = 0

    def start(self):
        """Starts timer"""
        # for new session
        if not self.is_timing and not self.is_paused:
            self.reset_time()  #
            self.is_timing = True  # turns on time check and update
            self.paused_lapse = 0


        # for pausing
        elif self.is_timing:
            self.is_timing = False
            self.paused_lapse = self.lapse
            self.is_paused = True


        # for un-pausing
        elif not self.is_timing and self.is_paused:
            self.is_timing = True
            self.reset_time()
            self.is_paused = False

    def keep_time(self):
        """Finds time passed since timer start or last reset"""
        self.lapse = time.time() - self.t_reference + self.paused_lapse

    def reset_time(self):
        """Reset timer to 0"""
        self.t_reference = time.time()

    def reset_clock(self):
        """Reset timer to 0, stop the timer, and reset progress"""
        self.progress = 0
        self.is_timing = False
        self.is_paused = False
