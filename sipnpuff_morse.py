import time
import board, busio
import adafruit_mprls

i2c = busio.I2C(board.SCL, board.SDA)
mpr = adafruit_mprls.MPRLS(i2c)

THRESH_LOW    = 10 # delta in hPa
THRESH_HIGH   = 10 # delta in hPa
DEBOUNCE = 0.005

def pressure_sensor_init(count=10, delay=0.1):
    reading = 0
    for _ in range(count):
        reading += mpr.pressure
        time.sleep(delay)
    reading /= count
    return reading - THRESH_LOW, reading + THRESH_HIGH

sip_threshold , puff_threshold = pressure_sensor_init()

while True:
    # driver checks conversion ready status, so OK do run this as fast as needed
    pressure = mpr.pressure

    # PUFF = dit
    if pressure > puff_threshold:
        print("dit ", end='')
        time.sleep(DEBOUNCE)

    # SIP = dah
    if pressure < sip_threshold:
        print("dah ", end='')
        time.sleep(DEBOUNCE)
