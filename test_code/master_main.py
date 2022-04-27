"""
MAIN FUNCTION
"""

from machine import Pin, SPI, I2C, PWM
import time
# DRIVERS
import gc9a01 as lcd
from imu import MPU6050
from rotary_irq_rp2 import RotaryIRQ
# HELPER
import italicc
import NotoSansMono_32 as font
from math import radians, sin, cos, floor, pi, degrees
LCD_SIZE = [240, 240]

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)
led = Pin(25, Pin.OUT)
spi = SPI(1, baudrate=40000000, sck=Pin(14), mosi=Pin(15))
screen = lcd.GC9A01(
    spi,
    LCD_SIZE[0],
    LCD_SIZE[1],
    reset=Pin(11, Pin.OUT),
    cs=Pin(13, Pin.OUT),
    dc=Pin(12, Pin.OUT),
    backlight=Pin(10, Pin.OUT),
    rotation=0)
endoer_switch = Pin(20, Pin.OUT, Pin.PULL_UP)
encoder = RotaryIRQ(pin_num_clk=18,
                    pin_num_dt=19,
                    min_val=0,
                    max_val=5,
                    range_mode=RotaryIRQ.RANGE_UNBOUNDED,
                    pull_up=True)
buzzer = PWM(Pin(16))
def writeCenterText(text, y, fg=lcd.WHITE, bg=lcd.BLACK):
    screen.write(font, text, 120 - screen.write_len(font, text)//2, y, fg, bg)
    

    
    
def dropAnimation():
    for i in range(0, 240):
        screen.fill_rect(0,0,i,240,lcd.BLUE)
        print("i:" + str(i))
        
def buzzerChime():
    buzzer.duty_u16(1000)
    buzzer.freq(440)
    time.sleep_ms(100)
    buzzer.freq(784)
    time.sleep_ms(200)
    buzzer.deinit();
    
def writeAccel(switch=""):
    screen.fill(lcd.RED)
    ax = round(imu.accel.x, 2)
    ay = round(imu.accel.y, 2)
    az = round(imu.accel.z, 2)
    writeCenterText("R:" + str(encoder.value()), 20)
    writeCenterText("X: " + str(ax), 70)
    writeCenterText("Y: " + str(ay), 120)
    writeCenterText("Z: " + str(az), 170)
    print("AX:" + str(ax) + "\tAY:" + str(ay) + "\tAZ:" + str(az))
    buzzerChime();
        
endoer_switch.irq(trigger=Pin.IRQ_RISING, handler=writeAccel)   
screen.init()
screen.rotation(0)
screen.fill(lcd.RED)


