#!/usr/bin/env python3
"""RGB LED and headlight example using picarx.led_extension."""

import time

from picarx.led_extension import PicarxLedController


def main() -> None:
    with PicarxLedController(r_pin="P3", g_pin="P4", b_pin="P5", headlight_left_pin="P6", headlight_right_pin="P7") as led:
        led.set_color((255, 0, 0))
        time.sleep(1)
        led.set_color((0, 255, 0))
        time.sleep(1)
        led.set_color((0, 0, 255))
        time.sleep(1)
        led.set_color("#ffffff")
        time.sleep(1)
        led.headlights_on(0.8)
        time.sleep(1)
        led.headlights_off()
        led.off()


if __name__ == "__main__":
    main()
