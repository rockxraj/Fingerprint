import time
from RPi_GPIO_i2c_LCD import lcd

class Sender:
    
    def __init__(self):
        self.lcd_display = lcd.HD44780(0x27)

    def set(self, message, line):
        self.lcd_display.set(message, line)

    def clear(self):
        #        self.lcd_display.lcd.clear()
        self.set(" " * 20, 1)
        self.set(" " * 20, 2)
        self.set(" " * 20, 3)
        self.set(" " * 20, 4)
        time.sleep(0.2)
