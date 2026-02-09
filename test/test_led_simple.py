from robot_hat import PWM
import time

r = PWM("P4")
g = PWM("P5")
b = PWM("P6")


fr = PWM("P7")
fl = PWM("P8")

r.freq(1000)
g.freq(1000)
b.freq(1000)

fr.freq(1000)
fl.freq(1000)

def set_color(rv, gv, bv):
    r.pulse_width_percent(rv)
    g.pulse_width_percent(gv)
    b.pulse_width_percent(bv)

# Red
set_color(100,0,0)
time.sleep(3)

# Green
set_color(0,100,0)
time.sleep(3)

# Blue
set_color(0,0,100)
time.sleep(3)
set_color(0,0,0)


fr.pulse_width_percent(100)
fl.pulse_width_percent(100)
time.sleep(3)
fr.pulse_width_percent(0)
fl.pulse_width_percent(0)   