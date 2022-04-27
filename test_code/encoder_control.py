import time
from rotary_irq_rp2 import RotaryIRQ
from machine import Pin

MODES = ['MINUTES', 'HOURS']
mode = 0
TIME = [0, 0]

print('SETTING UP', end='')
SW = Pin(20, Pin.IN, Pin.PULL_UP)
print('>', end='')
r = RotaryIRQ(pin_num_clk=18,
              pin_num_dt=19,
              min_val=0,
              max_val=60,
              range_mode=RotaryIRQ.RANGE_WRAP,
              pull_up=True)

print('>', end='')
val_old = r.value()
print('>', end='')

print('PROGRAM START')
while True:
    try:
        val_new = r.value()
        if SW.value() == 0 and n == 0:
            print("Button Pressed")
            print(MODES[mode] + " is : ", val_new)
            TIME[mode] = val_new
            mode = (mode + 1) % 2

            if (mode == 0):
                r._max_val = 59

            else:
                r._max_val = 23

            val_old = TIME[mode]
            n = 1
            while SW.value() == 0:
                continue
        n = 0
        if val_old != val_new:
            val_old = val_new
            print('result =', val_new)
        time.sleep_ms(50)
    except KeyboardInterrupt:
        break
