#!/usr/bin/env python3
"""Headlights example using picarx.led_extension."""

import time

from picarx.led_extension import PicarxLedController


def main() -> None:
    with PicarxLedController(headlight_left_pin="P6", headlight_right_pin="P7") as led:
        print("Headlights on (100%)")
        led.headlights_on(1.0)
        time.sleep(1)

        print("Headlights dim (30%)")
        led.set_headlight_brightness(0.3)
        time.sleep(1)

        print("Headlights off")
        led.headlights_off()
        time.sleep(0.5)

        print("RGB signal while headlights off")
        led.set_color((0, 0, 255))
        time.sleep(1)
        led.off()


if __name__ == "__main__":
    main()
