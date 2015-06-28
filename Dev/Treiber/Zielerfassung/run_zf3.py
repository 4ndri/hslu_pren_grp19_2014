__author__ = 'endru'
import Dev.Treiber.Zielerfassung.zielerfassungv3 as ZF
import time


detector=ZF.Zielerfassung()
time.sleep(2)
while True:
    t = time.time()
    pos = detector.detect()
    print '%s\r' % ' '*20, # clean up row
    dt = time.time() - t
    print 'time: %.1f ms' % (dt*1000) + '\t |\t position: %.5f px' % pos
    ch=raw_input()
    if ch=="s":
        break
print "done"
__author__ = 'endru'
