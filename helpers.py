"""
 HELPERS
"""
import time

"""
    Proggress Tick Class
    Creates Progress Update Messages
"""
class ProgressMessage:
    def __init__(self, name, updateChar='>'):
        self.name = name
        self.char = updateChar
        self.ticks = 0
        print(self.name, end='')
        
    def tick(self):
        message = self.name + (self.char  * self.ticks)
        self.ticks += 1
        print('\r', message, end='')
        
    def complete(self):
        print('\r', self.name, self.char * 10, 'COMPLETE')
        


"""
    Take x, y, z acceleration and convert it into a label
"""
def getOrientationLabel(x, y, z, look_range=0.8):
    # Take Gyroscope Reading
    LOOK_RANGE = look_range
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
    
    return output


def getOrintationNumber(label):
    if label == "FLAT-UP":
        return 0
    elif label == "SIDEWAYS-UP":
        return 3
    elif label == "FLAT-DOWN":
        return 2
    elif label == "SIDEWAYS-DOWN":
        return 1
    else:
        return 0

"""
    Timer Class
        Sets up a timer
        Tracks Progress percentage
        Tracks Acknolegment
"""
class PalmoTimer:
    def __init__(self, time: int):
        self.time = time
        self.percentage = 0
        self.activateTime = 0
        self.isActive = False
        self.acknoledged = False
        
    def timeLeft(self):
        if  not self.isActive:
            return 0
        elif( self.time - (time.ticks_ms() - self.activateTime) > 0):
            return self.time - (time.ticks_ms() - self.activateTime)
        
        return 0
    
    def percentComplete(self):
        # Timer is not active 0% complete
        if not self.isActive:
            return 0
        
        
        capure_time = time.ticks_ms()
        # Timer is complete
        if capure_time > self.activateTime + self.time:
            self.isActive = False
            return 1
        
        return (time.ticks_ms() - self.activateTime)/self.time
    
    def activate(self): 
        self.isActive = True
        self.activateTime = time.ticks_ms()
        
        
chime = ["B3", "B3", "CS4", "D4", "D4", "E4", "CS4", "B3", "A3"]   
tones = {
"B0": 31,
"C1": 33,
"CS1": 35,
"D1": 37,
"DS1": 39,
"E1": 41,
"F1": 44,
"FS1": 46,
"G1": 49,
"GS1": 52,
"A1": 55,
"AS1": 58,
"B1": 62,
"C2": 65,
"CS2": 69,
"D2": 73,
"DS2": 78,
"E2": 82,
"F2": 87,
"FS2": 93,
"G2": 98,
"GS2": 104,
"A2": 110,
"AS2": 117,
"B2": 123,
"C3": 131,
"CS3": 139,
"D3": 147,
"DS3": 156,
"E3": 165,
"F3": 175,
"FS3": 185,
"G3": 196,
"GS3": 208,
"A3": 220,
"AS3": 233,
"B3": 247,
"C4": 262,
"CS4": 277,
"D4": 294,
"DS4": 311,
"E4": 330,
"F4": 349,
"FS4": 370,
"G4": 392,
"GS4": 415,
"A4": 440,
"AS4": 466,
"B4": 494,
"C5": 523,
"CS5": 554,
"D5": 587,
"DS5": 622,
"E5": 659,
"F5": 698,
"FS5": 740,
"G5": 784,
"GS5": 831,
"A5": 880,
"AS5": 932,
"B5": 988,
"C6": 1047,
"CS6": 1109,
"D6": 1175,
"DS6": 1245,
"E6": 1319,
"F6": 1397,
"FS6": 1480,
"G6": 1568,
"GS6": 1661,
"A6": 1760,
"AS6": 1865,
"B6": 1976,
"C7": 2093,
"CS7": 2217,
"D7": 2349,
"DS7": 2489,
"E7": 2637,
"F7": 2794,
"FS7": 2960,
"G7": 3136,
"GS7": 3322,
"A7": 3520,
"AS7": 3729,
"B7": 3951,
"C8": 4186,
"CS8": 4435,
"D8": 4699,
"DS8": 4978
}

from time import sleep

def playToon(buzzer):
    
    for f in chime:
        if f == 0:
            buzzer.duty_u16(0)
        else:
            buzzer.duty_u16(1000)
            buzzer.freq(tones[f])
        sleep(0.3)
    buzzer.duty_u16(0)
    
    
#buzzer = PWM(Pin(16))

#playToon(buzzer)