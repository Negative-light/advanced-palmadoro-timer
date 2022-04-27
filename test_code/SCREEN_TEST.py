"""
DISPLAY TESTING
--TIMER
--SETUP A TIMER
--RUN IT
"""

from machine import Pin, SPI, I2C, PWM, Timer
import time
import rp2
# DRIVERS
import gc9a01 as lcd
from imu import MPU6050
from rotary_irq_rp2 import RotaryIRQ
# HELPER
import italicc
import NotoSansMono_32 as font


print("BOOTING", end='')

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
gyro = MPU6050(i2c)
tolerence = 0.05
current_orientation = "UNKNOWN"
print('>', end='')


LCD_SIZE = [240, 240]
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

BG = lcd.BLACK # Background Color
FG = lcd.WHITE # Forground Color
AC = lcd.MAGENTA # ACCENT COLOR


encoder_switch = Pin(20, Pin.OUT, Pin.PULL_UP)
encoder = RotaryIRQ(pin_num_clk=18,
                    pin_num_dt=19,
                    min_val=0,
                    max_val=240,
                    range_mode=RotaryIRQ.RANGE_WRAP)
times = [0, 0] # Time in Minutes and Seconds
timeMode = 0 # Time Mode 0 = seconds 1 = minutes
switch_holdTime = 0
print('>', end='')

buzzer = PWM(Pin(16))
print('>', end='')

timer_length = 100000
startTime = time.ticks_ms()
screen.init()
screen.fill(BG)
r = 100
g = 0
b = 0
last_line_y = 0
while True:
     delta = time.ticks_diff(time.ticks_ms(), startTime)
     percent = delta/timer_length
     line_y = int(percent * screen.height())
     if line_y != last_line_y:
         screen.line(0, line_y, 240, line_y, AC)
         last_line_y = line_y
     time_left = int((timer_length-delta)/1000)%60
     minutes_left = int((timer_length-delta)/1000)//60
     time_left_str = '{:02d}:{:02d}'.format(minutes_left, time_left)
     screen.write(font, time_left_str, 120, 120, FG, BG)
     if(percent >= 1):
        startTime = time.ticks_ms()
        AC = lcd.color565(r, g, b)
        g += 10
        b += 10
