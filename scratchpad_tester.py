import time as time

ts = time.time() + 864000

time.strftime("%Y%m%d%H:%M", time.localtime(ts))
