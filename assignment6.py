import time
import Adafruit_ADS1x15
from datetime import datetime

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport, sevensegment

def main():
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=1)
    seg = sevensegment(device)
   
    while True :
        now = datetime.now()
        dt_string = now.strftime("  %H.%M.%S")
        print("date and time =", dt_string)
        seg.text = dt_string
        time.sleep(1)

if __name__ == '__main__':
    main()
