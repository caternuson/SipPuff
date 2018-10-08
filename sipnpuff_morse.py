import time
import board, busio
import adafruit_mprls

i2c = busio.I2C(board.SCL, board.SDA)
mpr = adafruit_mprls.MPRLS(i2c)

THRESH_LOW    = 10 # delta in hPa
THRESH_HIGH   = 10 # delta in hPa
CHAR_PAUSE = 1

def pressure_sensor_init(count=10, delay=0.1):
    reading = 0
    for _ in range(count):
        reading += mpr.pressure
        time.sleep(delay)
    reading /= count
    return reading - THRESH_LOW, reading + THRESH_HIGH

sip_threshold , puff_threshold = pressure_sensor_init()
last_blip = time.monotonic()
char_start = False
char = ""

while True:
    # driver checks conversion ready status, so OK to run this as fast as needed
    pressure = mpr.pressure

    # PUFF = dit
    if pressure > puff_threshold:
        last_blip = time.monotonic()
        char += "."
        char_start = True
        #print(".", end='')
        # park here until pressure goes back down
        while pressure > puff_threshold:
            pressure = mpr.pressure

    # SIP = dah
    if pressure < sip_threshold:
        last_blip = time.monotonic()
        char += "-"
        char_start = True
        #print("-", end='')
        # park here until pressure goes back up
        while pressure < sip_threshold:
            pressure = mpr.pressure

    if char_start and time.monotonic() - last_blip > CHAR_PAUSE:
        char_start = False
        print(char+"   ", end='')
        char = ""
        # lets do a quick re-cal while we're here...
        sip_threshold , puff_threshold = pressure_sensor_init(5, 0.01)
