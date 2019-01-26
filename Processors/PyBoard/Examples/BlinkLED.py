import machine, utime
from pyb import LED

# Read (1) Green (2) Yellow (3) and Blue (4)

led = LED(1) # 1=red, 2=green, 3=yellow, 4=blue
led.toggle()
led.on()
led.off()

# LEDs 3 and 4 support PWM intensity (0-255)
LED(4).intensity()    # get intensity
LED(4).intensity(10) # set intensity to half

for i in range(5):
     LED(2).on()
     utime.sleep(1)
     LED(2).off()
     utime.sleep(1)

