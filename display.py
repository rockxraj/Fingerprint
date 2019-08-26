from RPi_GPIO_i2c_LCD import lcd

class Sender:
    def __init__(self):
        self.lcd_display = lcd.HD44780(0x27)

    def set(self, message, line):
        self.lcd_display.set(message, line)
