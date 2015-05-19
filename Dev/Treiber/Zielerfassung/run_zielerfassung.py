__author__ = 'endru'
import Dev.Treiber.Zielerfassung.zielerfassung as ZF
import time


detector=ZF.Zielerfassung()

while True:
    t = time.time()
    pos = detector.detect
    print '%s\r' % ' '*20, # clean up row
    dt = time.time() - t
    print 'time: %.1f ms' % (dt*1000) + '\t |\t position: %.5f px' % pos
    ch=raw_input()
    if ch=="s":
        break
print "done"
