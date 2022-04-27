# advanced-palmadoro-timer

This project was produced for a class at my University

## Features

* Orentation based presets
* Rotatry Encdoer to select time
* Round LCD

## Used Projects

To run the round LCD from Waveshare I used [this](https://github.com/russhughes/gc9a01_mpy) driver designed by [@russhughes](https://github.com/russhughes)

The rotatry encoder used [this](https://github.com/miketeachman/micropython-rotary) code from [@miketeachman](https://github.com/miketeachman)

The MPU6050 gyroscope used [this](https://github.com/micropython-IMU/micropython-mpu9150) code from [@micropython-IMU](https://github.com/micropython-IMU)

## Functional Description

This system uses four modes to funtion properly:

### IDLE

No timer is active and no new timer was set. <br>
If oentation is changed sets mode to **PRIMED**. <br>
If button is pressed for more than two seconds sets mode to **CUSTOM**. <br>

### PRIMED

Holding state between **IDLE** and **ACTIVE**. If orientation has not been changed in the last two seconds changed mode to **ACTIVE**.

### ACTIVE
The timer is currently active.

Checks if the integer precent changed has chagned adjusted the view to such that the display represents that. Also updates the dispayed text to MM:SS format

### CUSTOM

If the rotary encoder is chagned the time is set to the value at that postiont.

RANGE: 0 Minutes to 99 Minutes and 59 Seconds.

## DEMO

https://www.youtube.com/watch?v=qtnIyW7uaUU
