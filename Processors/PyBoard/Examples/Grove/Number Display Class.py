'''
http://wiki.seeedstudio.com/Grove-4-Digit_Display/

connections: 
Ground  - GND 
Power    - 3V3 
SCLK - pin Y9
SDATA -  pin Y10
'''

import  utime
from machine import Pin

charmap = {
    '0': 0x3f,'1': 0x06,'2': 0x5b,'3': 0x4f,'4': 0x66,'5': 0x6d,'6': 0x7d,'7': 0x07,'8': 0x7f,
    '9': 0x6f,'A': 0x77,'B': 0x7f,'b': 0x7C,'C': 0x39,'c': 0x58,'D': 0x3f,'d': 0x5E,'E': 0x79,
    'F': 0x71,'G': 0x7d,'H': 0x76,'h': 0x74,'I': 0x06,'J': 0x1f,'K': 0x76,'L': 0x38,'l': 0x06,
    'n': 0x54,'O': 0x3f,'o': 0x5c,'P': 0x73,'r': 0x50,'S': 0x6d,'U': 0x3e,'V': 0x3e,'Y': 0x66,
    'Z': 0x5b,'-': 0x40,'_': 0x08,' ': 0x00}

ADDR_AUTO = 0x40
ADDR_FIXED = 0x44
STARTADDR = 0xC0
BRIGHT_DARKEST = 0
BRIGHT_DEFAULT = 2
BRIGHT_HIGHEST = 7

class Grove4Digit(object):
    def __init__(self, clk,dio):
         self.clk = Pin(clk,Pin.OUT,Pin.PULL_UP)
         self.dio = Pin(dio,Pin.OUT,Pin.PULL_UP)

    def value(self):
        return self.button.value()

     def start(self):
          self.clk.value(1)
          self.dio.value(1)
          self.dio.value(0)
          self.clk.value(0)
     
     def stop(self):
          self.clk.value(0)
          self.dio.value(0)
          self.clk.value(1)
          self.dio.value(1)
     
     def writeByte(self,data):
          for _ in range(8):
               self.clk.value(0)
               if data & 0x01:
                    self.dio.value(1)
               else:
                    self.dio.value(0)
               data >>= 1
               utime.sleep_us(1)
               self.clk.value(1)
               utime.sleep_us(1)

          self.clk.value(0)
          self.dio.value(1)
          self.clk.value(1)
          self.dio.init(Pin.IN,Pin.PULL_UP)
          utime.sleep_ms(50)
          ack = self.dio.value()
          if (ack == 0):
               self.dio.init(Pin.OUT,Pin.PULL_UP)
               self.dio.value(0)
          utime.sleep_ms(50)
          self.dio.init(Pin.OUT,Pin.PULL_UP)
          utime.sleep_ms(50)
     
     def display(self,data,brightness=BRIGHT_DEFAULT,colon=False):
          self.start()
          self.writeByte(ADDR_AUTO)
          self.stop()
     
          self.start()
          self.writeByte(STARTADDR)
          if len(data) < 4:
               data = data + '    '
          for i in range(4):
               self.writeByte(charmap[data[i]] | 0x80 * colon)
          self.stop()
     
          if brightness > BRIGHT_HIGHEST:
               brightness = BRIGHT_HIGHEST
          if brightness < BRIGHT_DARKEST:
               brightness = BRIGHT_DARKEST
          self.start()
          self.writeByte(0x88 +  brightness)
          self.stop()
     
     def clear(self):
          self.display('    ',4,0)

disp = Grove4Digit('Y9','Y10')
disp.display('1234', 4,True)
