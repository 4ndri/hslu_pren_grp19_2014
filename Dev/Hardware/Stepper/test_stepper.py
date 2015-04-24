__author__ = 'endru'
import Dev.Hardware.Stepper.Stepper as Stp


stepper = Stp.Stepper(4, 17, 700, 5000, 100)
stepper.steps_right(133)
stepper.steps_left(133)


