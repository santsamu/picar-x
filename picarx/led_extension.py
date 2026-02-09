import time
from typing import List, Optional, Tuple, Union

from robot_hat import PWM

ColorInput = Union[str, int, Tuple[int, int, int], List[int]]


class PicarxLedController:
    """RGB LED helper with optional headlights for PiCar-X.

    Defaults RGB to P4/P5/P6 and headlights to P7/P8.
    """

    ANODE = 1
    CATHODE = 0

    def __init__(
        self,
        r_pin: str = "P4",
        g_pin: str = "P5",
        b_pin: str = "P6",
        headlight_left_pin: str = "P7",
        headlight_right_pin: str = "P8",
        common: int = CATHODE,
        freq_hz: int = 1000,
        color_order: str = "RGB",
        brightness: float = 1.0,
        headlight_brightness: float = 1.0,
    ) -> None:
        self.r_pwm = PWM(r_pin)
        self.g_pwm = PWM(g_pin)
        self.b_pwm = PWM(b_pin)
        self.headlight_left_pwm = PWM(headlight_left_pin)
        self.headlight_right_pwm = PWM(headlight_right_pin)

        self.r_pwm.freq(freq_hz)
        self.g_pwm.freq(freq_hz)
        self.b_pwm.freq(freq_hz)
        self.headlight_left_pwm.freq(freq_hz)
        self.headlight_right_pwm.freq(freq_hz)
        if common not in (self.ANODE, self.CATHODE):
            raise ValueError("common must be PicarxLedController.ANODE or PicarxLedController.CATHODE")
        self.common = common
        self.color_order = self._validate_color_order(color_order)
        self.brightness = self._clamp_brightness(brightness)
        self.headlight_brightness = self._clamp_brightness(headlight_brightness)

    def set_color(self, color: ColorInput) -> None:
        """Set LED color (hex str, 24-bit int, tuple/list)."""
        rgb = self._to_rgb_tuple(color)
        rgb = self._apply_order(rgb)
        self._write_pwm(rgb)

    def off(self) -> None:
        """Turn LED off."""
        self.set_color((0, 0, 0))

    def headlights_on(self, brightness: Optional[float] = None) -> None:
        """Turn headlights on with optional brightness (0.0-1.0)."""
        if brightness is not None:
            self.headlight_brightness = self._clamp_brightness(brightness)
        self._write_headlights(self.headlight_brightness)

    def headlights_off(self) -> None:
        """Turn headlights off."""
        self._write_headlights(0.0)

    def set_headlight_brightness(self, brightness: float) -> None:
        """Set headlight brightness (0.0-1.0)."""
        self.headlight_brightness = self._clamp_brightness(brightness)
        self._write_headlights(self.headlight_brightness)

    def set_brightness(self, brightness: float) -> None:
        """Set global brightness (0.0-1.0)."""
        self.brightness = self._clamp_brightness(brightness)

    @staticmethod
    def _clamp_brightness(brightness: float) -> float:
        return max(0.0, min(1.0, float(brightness)))

    @staticmethod
    def _validate_color_order(color_order: str) -> str:
        color_order = color_order.upper()
        valid_orders = {"RGB", "RBG", "GRB", "GBR", "BRG", "BGR"}
        if color_order not in valid_orders:
            raise ValueError(f"color_order must be one of {sorted(valid_orders)}, got {color_order}")
        return color_order

    @staticmethod
    def _to_rgb_tuple(color: ColorInput) -> Tuple[int, int, int]:
        if not isinstance(color, (str, int, tuple, list)):
            raise TypeError("color must be str, int, tuple or list")
        if isinstance(color, str):
            color = color.strip("#")
            color = int(color, 16)
        if isinstance(color, (tuple, list)):
            r, g, b = color
        elif isinstance(color, int):
            r = (color & 0xFF0000) >> 16
            g = (color & 0x00FF00) >> 8
            b = (color & 0x0000FF)
        else:
            raise TypeError("color must be str, int, tuple or list")
        return int(r), int(g), int(b)

    def _apply_order(self, rgb: Tuple[int, int, int]) -> Tuple[int, int, int]:
        r, g, b = rgb
        mapping = {"R": r, "G": g, "B": b}
        return tuple(mapping[c] for c in self.color_order)

    def _write_pwm(self, rgb: Tuple[int, int, int]) -> None:
        r, g, b = rgb
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))

        if self.brightness < 1.0:
            r = int(r * self.brightness)
            g = int(g * self.brightness)
            b = int(b * self.brightness)

        if self.common == self.ANODE:
            r = 255 - r
            g = 255 - g
            b = 255 - b

        r = r / 255.0 * 100.0
        g = g / 255.0 * 100.0
        b = b / 255.0 * 100.0

        self.r_pwm.pulse_width_percent(r)
        self.g_pwm.pulse_width_percent(g)
        self.b_pwm.pulse_width_percent(b)

    def _write_headlights(self, brightness: float) -> None:
        duty = self._clamp_brightness(brightness) * 100.0
        self.headlight_left_pwm.pulse_width_percent(duty)
        self.headlight_right_pwm.pulse_width_percent(duty)

    @staticmethod
    def _hsv_to_rgb(h: float, s: float, v: float) -> Tuple[int, int, int]:
        """Convert HSV (0-360, 0-1, 0-1) to RGB 0-255."""
        h = h % 360
        s = max(0.0, min(1.0, s))
        v = max(0.0, min(1.0, v))

        c = v * s
        x = c * (1 - abs(((h / 60.0) % 2) - 1))
        m = v - c

        if 0 <= h < 60:
            rp, gp, bp = c, x, 0
        elif 60 <= h < 120:
            rp, gp, bp = x, c, 0
        elif 120 <= h < 180:
            rp, gp, bp = 0, c, x
        elif 180 <= h < 240:
            rp, gp, bp = 0, x, c
        elif 240 <= h < 300:
            rp, gp, bp = x, 0, c
        else:
            rp, gp, bp = c, 0, x

        r = int((rp + m) * 255)
        g = int((gp + m) * 255)
        b = int((bp + m) * 255)
        return r, g, b

    def rainbow(
        self,
        cycles: int = 1,
        step_degrees: int = 5,
        delay: float = 0.02,
        brightness: float = 1.0,
        start_hue: int = 0,
        saturation: float = 1.0,
    ) -> None:
        """Run a rainbow effect.

        Args:
            cycles: Number of full 0-360 sweeps.
            step_degrees: Hue increment per step.
            delay: Delay between steps in seconds.
            brightness: Overall brightness (0.0-1.0).
            start_hue: Starting hue angle.
            saturation: Saturation level (0.0-1.0).
        """
        if cycles <= 0:
            return
        step_degrees = max(1, int(step_degrees))
        brightness = max(0.0, min(1.0, float(brightness)))
        saturation = max(0.0, min(1.0, float(saturation)))

        steps_per_cycle = int(360 / step_degrees)
        total_steps = steps_per_cycle * cycles

        for i in range(total_steps):
            hue = (start_hue + i * step_degrees) % 360
            r, g, b = self._hsv_to_rgb(hue, saturation, brightness)
            self.set_color((r, g, b))
            if delay > 0:
                time.sleep(delay)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.off()
        self.headlights_off()
        return False
