__author__ = 'endru'
import Dev.Hardware.Stepper.Stepper as Stp


stepper = Stp.Stepper(4, 17, 5000, 20000, 100)

while True:
    stepper.steps_right(1000)

