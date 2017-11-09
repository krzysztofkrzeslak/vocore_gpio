import vo_gpio as gpio
import time

gpio.setup(44,gpio.DIR_OUT)
while True:
        gpio.data(44,gpio.LOW_STATE)
        time.sleep(1)
        gpio.data(44,gpio.HIGH_STATE)
        time.sleep(1)

