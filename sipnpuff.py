import time
import board, busio
import adafruit_mprls

i2c = busio.I2C(board.SCL, board.SDA)
mpr = adafruit_mprls.MPRLS(i2c)

THRESH_LOW    = 10 # delta in hPa
THRESH_HIGH   = 10 # delta in hPa

def pressure_sensor_init(count=10, delay=0.1):
    reading = 0
    for _ in range(count):
        reading += mpr.pressure
        time.sleep(delay)
    reading /= count
    return reading - THRESH_LOW, reading + THRESH_HIGH

sip_threshold , puff_threshold = pressure_sensor_init()
puff_count = sip_count = 0

while True:
    # driver checks conversion ready status, so OK do run this as fast as needed
    pressure = mpr.pressure

    # PUFF
    if pressure > puff_threshold:
        while pressure > puff_threshold:
            pressure = mpr.pressure
            puff_count += 1
            time.sleep(0.005)
        #
        # do something based on puff_count
        #
        print("puff count = {}".format(puff_count))
        puff_count = 0

    # SIP
    if pressure < sip_threshold:
        while pressure < sip_threshold:
            pressure = mpr.pressure
            sip_count += 1
            time.sleep(0.005)
        #
        # do something based on sip_count
        #
        print("sip count = {}".format(sip_count))
        sip_count = 0