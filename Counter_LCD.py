import time
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

class LCD:
    def __init__(self):
        self.setup()

    def setup(self):
        global lcd
        lcd_rs = digitalio.DigitalInOut(board.D26)
        lcd_en = digitalio.DigitalInOut(board.D13)
        lcd_d7 = digitalio.DigitalInOut(board.D6)
        lcd_d6 = digitalio.DigitalInOut(board.D22)
        lcd_d5 = digitalio.DigitalInOut(board.D24)
        lcd_d4 = digitalio.DigitalInOut(board.D25)

        lcd_columns = 16
        lcd_rows = 2

        import adafruit_character_lcd.character_lcd as characterlcd
        self.lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)
        self.lcd.clear()

    def askQuestion(self, option1, option2, bottomText="  Point to one  "):
        self.lcd.clear()
        if len(option1) + len(option2) > 11:
            print("Combined text length cannot be more than 11")
            return
        if len(bottomText) > 16:
            print("Bottom text cannot be more than 16")
        gap = 12 - (len(option1) + len(option2))
        msg = "< " + option1
        for i in range(gap):
            msg += " "
        msg += option2 + " >\n" + bottomText
        self.lcd.message = msg

    def clear(self):
        self.lcd.clear()

    def showCustomMessage(self, msg):
        self.clear()
        self.lcd.message = msg
