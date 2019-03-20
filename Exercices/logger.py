import python
import utime

def log_time(file):
    file.write(str(utime.ticks_ms()) + "\n")