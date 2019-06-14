#-*- coding:utf8 -*-

import time
import datetime
import sys
#if __name__ == '__main__':

print ("Start : %s" % time.ctime())
time.sleep(5)
print ("End : %s" % time.ctime())

while 1:
    sys.stdout.flush()
    print ("Start : %s" % time.ctime())
    time.sleep(5)
    print("End : %s" % time.ctime())
    sys.stdout.flush()
    #nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #print(nowTime)
    #time.sleep(2)