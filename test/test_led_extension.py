#!/usr/bin/env python3
"""Test script for PicarxLedController RGB LED functions.

Usage:
    sudo python3 test/test_led_extension.py --r P4 --g P5 --b P6 --hl-left P7 --hl-right P8
    sudo python3 test/test_led_extension.py --r P4 --g P5 --b P6 --hl-left P7 --hl-right P8 --common cathode --order BGR --brightness 0.5 --hl-brightness 0.7
"""

import argparse
import time

from picarx.led_extension import PicarxLedController


def parse_args():
    parser = argparse.ArgumentParser(description="Test RGB LED extension functions")
    parser.add_argument("--r", default="P4", help="PWM pin for red channel")
    parser.add_argument("--g", default="P5", help="PWM pin for green channel")
    parser.add_argument("--b", default="P6", help="PWM pin for blue channel")
    parser.add_argument("--common", choices=["anode", "cathode"], default="cathode")
    parser.add_argument(
        "--order",
        default="RGB",
        help="Channel order mapping (RGB, RBG, GRB, GBR, BRG, BGR)",
    )
    parser.add_argument("--hl-left", default="P7", help="PWM pin for left headlight")
    parser.add_argument("--hl-right", default="P8", help="PWM pin for right headlight")
    parser.add_argument("--delay", type=float, default=0.8, help="Delay between colors")
    parser.add_argument("--cycles", type=int, default=2, help="Rainbow cycles")
    parser.add_argument("--brightness", type=float, default=1.0, help="Global brightness (0.0-1.0)")
    parser.add_argument("--hl-brightness", type=float, default=1.0, help="Headlight brightness (0.0-1.0)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    common = PicarxLedController.ANODE if args.common == "anode" else PicarxLedController.CATHODE

    with PicarxLedController(
        r_pin=args.r,
        g_pin=args.g,
        b_pin=args.b,
        headlight_left_pin=args.hl_left,
        headlight_right_pin=args.hl_right,
        common=common,
        color_order=args.order,
        brightness=args.brightness,
        headlight_brightness=args.hl_brightness,
    ) as led:
        print("=== Basic color test ===")
        print("Red")
        led.set_color((255, 0, 0))
        time.sleep(args.delay)
        print("Green")
        led.set_color((0, 255, 0))
        time.sleep(args.delay)
        print("Blue")       
        led.set_color((0, 0, 255))
        time.sleep(args.delay)
        print("White")
        led.set_color("#ffffff")
        time.sleep(args.delay)
        led.off()

        print("=== Headlights test ===")
        led.headlights_on()
        time.sleep(args.delay)
        led.set_headlight_brightness(args.hl_brightness)
        time.sleep(args.delay)
        led.headlights_off()

        print("=== Brightness test ===")
        for b in [1.0, 0.5, 0.25, 0.1]:
            print(f"Brightness: {b}")
            led.set_brightness(b)
            led.set_color((255, 255, 255))
            time.sleep(args.delay)
        led.off()

        print("=== Rainbow effect ===")
        led.rainbow(cycles=args.cycles, step_degrees=5, delay=0.02, brightness=0.7)
        led.off()


if __name__ == "__main__":
    main()
