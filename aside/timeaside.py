#! /usr/bin/env python
import time
import datetime
#print time.gmtime().tm_sec 
time1 = time.time() #datetime.time() #time.gmtime()
print "%E" % time1 
time.sleep(5)
time2 = time.time() #datetime.time() #time.gmtime()
print "%E" % time2
print "%E" % (time2 - time1) 
