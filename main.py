"""
Operational Timer Based on Orientation
"""

#**********************************BOOTING******************************************
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
import helpers
from helpers import ProgressMessage, PalmoTimer

boot_progress = ProgressMessage('BOOTING')

#Setup Gyro
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
gyro = MPU6050(i2c)
boot_progress.tick()
tolerence = 0.05
current_orientation = "UNKNOWN"
boot_progress.tick()


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
boot_progress.tick()

encoder_switch = Pin(20, Pin.OUT, Pin.PULL_UP)
encoder = RotaryIRQ(pin_num_clk=18,
                    pin_num_dt=19,
                    min_val=0,
                    max_val=5999,
                    range_mode=RotaryIRQ.RANGE_WRAP)
SWITCH_HOLD_MS = 2000
switched_pressed_time = -1

mode = "ACTIVE"
def switchedPressed(irq= None):
    global switched_pressed_time, mode, timer_active, master_timer
    print("pressed")
    if mode == "IDLE" or mode == "CUSTOM":
        switched_pressed_time = time.ticks_ms()
    elif mode == "ACTIVE":
        if master_timer.timeLeft() > 0:
            start_time = time.ticks_ms()
            while encoder_switch.value() == 1 and master_timer.isActive:
                if time.ticks_ms() >= start_time + SWITCH_HOLD_MS:
                    timer_active = False
                    master_timer.isActive = False
                    master_timer.acknoledged = True
                    buzzer.duty_u16(1000)
                    buzzer.freq(helpers.tones["B4"])
                    buzzer.freq(helpers.tones["B3"])
                    time.sleep(0.1)
                    buzzer.duty_u16(0)
        else:
            master_timer.acknoledged = True
                

encoder_switch.irq(trigger=Pin.IRQ_RISING, handler=switchedPressed)
boot_progress.tick()

buzzer = PWM(Pin(16))
boot_progress.tick()

boot_progress.complete()

#************************SETUP ENVIRONMENT***********************************************
setup_progress = ProgressMessage('SETUP', '|')

current_orientation = helpers.getOrientationLabel(gyro.accel.x, gyro.accel.y, gyro.accel.z)
setup_progress.tick()

timer_active = False
setup_progress.tick()

setup_progress.tick()

master_timer = PalmoTimer(2000)
setup_progress.tick()

master_timer.activate()

screen.init()
screen.fill(BG)
screen.fill_rect(10, 10, 220, 220, AC)
setup_progress.tick()

ACTIVATE_DELAY_MS = 1000
prime_time = time.ticks_ms()
setup_progress.tick()

last_percent_complete = 0

setup_progress.tick()

#---FUNCTIONS---
setup_progress.updateChar = '-'
def writeCenter(text = "", y = 112):
    # Get LCD Size
    h = screen.height()
    l = screen.width()
    length = screen.write_len(font, text)
    screen.write(font, text, int((l/2)-(length/2)), y, FG, BG)

time_str = "00:00"
count_up_start = -1
count_unacked = 0
last_encoder_value = encoder.value()
setup_progress.tick()
setup_progress.complete()
#*******************************LOOP**********************
while True:
    
    orientation = helpers.getOrientationLabel(gyro.accel.x, gyro.accel.y, gyro.accel.z)
    orientation_number = helpers.getOrintationNumber(orientation)
    
    if master_timer.isActive:
        percent_complete = round(master_timer.percentComplete(), 3)
        if percent_complete != last_percent_complete:
            last_percent_complete = percent_complete
            print('\r', '{:.3%}'.format(percent_complete), '--Complete', end='')
            screen.hline(0, int(screen.height() * percent_complete), 240, BG)
        
        time_left = master_timer.timeLeft()
        time_left = time_left/1000
        minutes_left = time_left//60
        seconds_left = int(time_left%60)
        format_str = '{:02n}'
        time_text = format_str.format(minutes_left) + ':' + format_str.format(seconds_left)
        
        if orientation != current_orientation:
            current_orientation = orientation
            screen.rotation(orientation_number)
            screen.fill(AC)
            screen.fill_rect(0,0,240,int(screen.height() * percent_complete), BG)
        
        
        writeCenter(time_text)
        continue
    elif mode=="ACTIVE":
        if master_timer.acknoledged:
            mode = "IDLE"
            print("\r TIMER COMPLETE        ")
            screen.fill(BG)
            time_left = master_timer.timeLeft()
            time_left = time_left/1000
            minutes_left = time_left//60
            seconds_left = int(time_left%60)
            time_text = format_str.format(minutes_left) + ':' + format_str.format(seconds_left)
            writeCenter(time_text)
        else:
            helpers.playToon(buzzer)
            time.sleep(2)
            count_unacked += 1
            print("UNACKED:", count_unacked)
            if count_unacked > 8:
                master_timer.acknoledged = True
    elif mode == "CUSTOM":
        if encoder.value() != last_encoder_value:
            #print(encoder.value())
            last_encoder_value = encoder.value()
            time_left = last_encoder_value
            #time_left = time_left/1000
            minutes_left = time_left//60
            seconds_left = int(time_left%60)
            time_text = format_str.format(minutes_left) + ':' + format_str.format(seconds_left)
            #print(time_text)
            writeCenter(time_text)
        
        if switched_pressed_time != -1:
            #print(switched_pressed_time)
            if encoder_switch.value() == 0:
                switched_pressed_time = -1
                encoder._value += 60
            
            if time.ticks_ms() - switched_pressed_time >= SWITCH_HOLD_MS:
                print(time.ticks_ms(), switched_pressed_time, time.ticks_ms() - switched_pressed_time, sep='\t')
                switched_pressed_time = -1
                master_timer = PalmoTimer(last_encoder_value * 1000)
                prime_time = time.ticks_ms()
                mode = "PRIMED"
        continue
    
    #print(switched_pressed_time)
    #print(encoder_switch.value())
    orientation = helpers.getOrientationLabel(gyro.accel.x, gyro.accel.y, gyro.accel.z)
    
    if orientation != current_orientation and orientation != "UNKNOWN":
        print(current_orientation, "----->>>", orientation)
        current_orientation = orientation
        prime_time = -1
        if current_orientation == "FACE-UP":
            if count_up_start != -1:
                time_left = (time.ticks_ms() - count_up_start)/1000
                minutes = time_left//60
                seconds = int(time_left%60)
                time_text = format_str.format(minutes_left) + ':' + format_str.format(seconds_left)
                count_up_start = -1
        elif current_orientation == "FACE-DOWN":
            count_up_start = time.ticks_ms()
        elif current_orientation == "FLAT-UP":
            master_timer = PalmoTimer(60*5*1000)
            prime_time = time.ticks_ms()
            mode = "PRIMED"
        elif current_orientation == "FLAT-DOWN":
            master_timer = PalmoTimer(60*30*1000)
            prime_time = time.ticks_ms()
            mode = "PRIMED"
        elif current_orientation == "SIDEWAYS-UP":
           master_timer = PalmoTimer(60*15*1000)
           prime_time = time.ticks_ms()
           mode = "PRIMED"
        elif current_orientation == "SIDEWAYS-DOWN":
           master_timer = PalmoTimer(60*60*1000)
           prime_time = time.ticks_ms()
           mode = "PRIMED"
        elif current_orientation == "UNKNOWN":
            current_orientation == "UNKNOWN"
        else:
            print(current_orientation)
            
            
    if mode == "PRIMED" and prime_time != -1:
        if time.ticks_ms() >= prime_time + ACTIVATE_DELAY_MS:
            master_timer.activate()
            screen.fill(AC)
            screen.fill_rect(110, 110, 20, 20, FG)
            count_up_start = -1
            mode = "ACTIVE"
            
    if switched_pressed_time != -1 and mode != "CUSTOM":
        #print(switched_pressed_time)
        if encoder_switch.value() == 0:
            switched_pressed_time = -1
            
        if time.ticks_ms() - switched_pressed_time >= SWITCH_HOLD_MS:
            
            mode = "CUSTOM"
            switched_pressed_time = -1
            writeCenter("!", y=128)
            encoder.reset()
            print(mode)