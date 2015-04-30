__author__ = 'endru'
# import Dev.Hardware.Stepper.Stepper as Stp
import math;

max_delay = 10000
final_delay = 510
acc = 100
ramp_steps = int(math.ceil(float(max_delay - final_delay) / acc))
counter = 0
for delay in range(max_delay, final_delay, -acc):
    counter += 1

print "counter: "+str(counter)+"    calcsteps: "+ str(ramp_steps)
#stepper = Stp.Stepper(4, 17, 700, 5000, 100)
#stepper.steps_right(133)
#stepper.steps_left(133)


