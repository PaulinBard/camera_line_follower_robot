import time


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""

class Timer:
    elapsed_time = 0
    def __init__(self):
        self._start_time = None

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        self.elapsed_time = time.perf_counter() - self._start_time
        print(f"Elapsed time: {elapsed_time:0.4f} seconds")
        self._start_time = None

    def sleep(self, seconds):
        time.sleep(seconds)

    def reset(self): ###call after stop
        self.elapsed_time = 0

