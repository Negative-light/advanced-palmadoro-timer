"""
MAIN FUNCTION
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
  
MODES = {
    "IDLE":0,
    "RUNNING":1,
    "SET":2,
    "MENU":3
    }


class DisplayTimer:
    def __init__(self, minutes, seconds):
        self.minutes = minutes
        self.seconds = seconds
        self.startTime = 0
        self.isActive = False
        
    def start(self):
        self.startTime = time.ticks_ms()
        self.isActive = True
        
    def percentComplete(self):
         delta = time.ticks_diff(time.ticks_ms(), self.startTime)
         totalTime = ((60* self.minutes) + self.seconds) * 1000
         percent_complete = (delta/totalTime)
         if(percent_complete < 100):
             return percent_complete
         else:
            self.isActive = False
            return 100

print('>', end='')

encoder_switch = Pin(20, Pin.OUT, Pin.PULL_UP)
encoder = RotaryIRQ(pin_num_clk=18,
                    pin_num_dt=19,
                    min_val=0,
                    max_val=99,
                    range_mode=RotaryIRQ.RANGE_WRAP)
times = [0, 0] # Time in Minutes and Seconds
timeMode = 0 # Time Mode 0 = seconds 1 = minutes
switch_holdTime = 0
print('>', end='')

buzzer = PWM(Pin(16))
print('>', end='')

#%% Helper Funcitons
"""
Get the Laabel for the current Orientation
"""
def getOrientationLabel(irq = None):
    global current_orientation
    # Take Gyroscope Reading
    x = gyro.accel.x
    y = gyro.accel.y
    z = gyro.accel.z
    LOOK_RANGE = 0.9
    output = ""
    look_val = 0
    if abs(z) > LOOK_RANGE:
        output = "FLAT"
        look_val = z
    elif abs(x) > LOOK_RANGE:
        output = "SIDEWAYS"
        look_val = x
    elif abs(y) > LOOK_RANGE:
        output = "FACE"
        look_val = y
    elif abs(x) + abs(z) > 1:
        output = "ANGLE"
        if x > 0:
            output += "-UP"
        else:
            output += "-DOWN"
        
        if z > 0:
            output += "-R"
        else:
            output += "-L"
            
    else:
        output = "UNKNOWN"
        
    if output == "FACE" or output == "SIDEWAYS" or output == "FLAT":
        if look_val > 0:
            output += "-UP"
        else:
            output += "-DOWN"
    
    # If being handled by an event, 
    if irq != None:
        current_orientation = output
        
    return output


def writeCenter(text = "", y = 120):
    # Get LCD Size
    h = screen.height()
    l = screen.width()
    length = screen.write_len(font, text)
    screen.write(font, text, int((l/2)-(length/2)), y, FG, BG)
    
def updateScreenRotation():
    if current_orientation == "FLAT-UP":
        screen.rotation(0)
    elif current_orientation == "FLAT-DOWN":
        screen.rotation(2)
    elif current_orientation == "SIDEWAYS-UP":
        screen.rotation(1)
    elif current_orientation == "SIDEWAYS-DOWN":
        screen.rotation(3)
    elif current_orientation == "FACE-UP":
        screen.rotation(0)

def updateScreen(irq = None):
     global MODE
     screen.off()
     updateScreenRotation()
     screen.fill(BG)
     if MODE == MODE["MENU"]:
         writeCenter("MENU", 60)
     
     writeCenter(current_orientation, 120)
     screen.on()
     
last_orientation = getOrientationLabel()
last_switch_state = 0
SWITCH_TO_MENU_TIME = 2000
MODE = 0 # MODES, 0 = Idle, 1 = Timer, 2 = Menu
def tickEvent(irq = None):
    global last_orientation, last_switch_state, switch_holdTime, MODE
    if last_orientation != current_orientation:
        last_orientation = current_orientation
        updateScreen(irq)
        
    
    
def switchTimeMode(switch):
    global switch_holdTime, switch_down, MODE
    #print("SWITCH PRESSED")
    if(MODE == 0):
        switch_holdTime = time.ticks_ms()
    
def switchPressed(switch):
    switchTimeMode(switch)
    

test = DisplayTimer(0,  10)
# SETUP
print('\nSETUP', end='')
getOrientationLabel()
orientation_timer = Timer(period=1000, mode=Timer.PERIODIC, callback=getOrientationLabel)
print('>', end='')
#tick = Timer(period=100, mode=Timer.PERIODIC, callback=tickEvent)
print('>', end='')
screen.init()
print('>', end='')
encoder_switch.irq(trigger=Pin.IRQ_RISING, handler=switchPressed)
print('>', end='')
test.start()

while True:
    tickEvent()