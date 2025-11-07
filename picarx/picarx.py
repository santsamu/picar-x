from robot_hat import Pin, ADC, PWM, Servo, fileDB
from robot_hat import Grayscale_Module, Ultrasonic, utils
import time
import os
from typing import List, Union, Optional


def constrain(x: Union[int, float], min_val: Union[int, float], max_val: Union[int, float]) -> Union[int, float]:
    """Constrains value to be within a range.
    
    Args:
        x: Value to constrain
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        
    Returns:
        Constrained value between min_val and max_val
    """
    return max(min_val, min(max_val, x))


class PicarxConstants:
    """Configuration constants for PiCar-X hardware and behavior."""
    
    # === HARDWARE CONFIGURATION ===
    CONFIG_PATH = '/opt/picar-x/picar-x.conf'
    
    # Motor control constants
    MOTOR_SPEED_DIVISOR = 2
    MOTOR_SPEED_OFFSET = 50
    MOTOR_STOP_ITERATIONS = 2
    MOTOR_STOP_DELAY = 0.002
    
    # PWM configuration
    PWM_PERIOD = 4095
    PWM_PRESCALER = 10
    PWM_TIMEOUT = 0.02
    
    # Servo angle limits
    SERVO_LIMITS = {
        'direction': {'min': -30, 'max': 30},
        'cam_pan': {'min': -90, 'max': 90},
        'cam_tilt': {'min': -35, 'max': 65}
    }
    
    # Default sensor reference values (calibrated for typical lighting)
    DEFAULT_LINE_REFERENCE = [500, 500, 500]  # Line detection threshold
    DEFAULT_CLIFF_REFERENCE = [400, 400, 400]  # Cliff detection threshold
    
    # Default turn calibration values
    DEFAULT_TURN_TIMES = {
        'tank_turn_360': 4.0,
        'pivot_turn_360': 8.0
    }
    
    DEFAULT_TURN_SPEEDS = {
        'tank_turn_calibration': 50,
        'pivot_turn_calibration': 50
    }
    
    # Hardware initialization delays
    MCU_RESET_DELAY = 0.2
    
    # Motor indices (for validation)
    VALID_MOTOR_INDICES = [1, 2]
    VALID_DIRECTION_VALUES = [1, -1]
    
    # Turn direction mappings
    VALID_TURN_DIRECTIONS = ['left', 'right', -1, 1]
    
    # Speed and angle constraints
    SPEED_MIN = 0
    SPEED_MAX = 100
    FULL_CIRCLE_DEGREES = 360.0

class Picarx(object):
    # Legacy constants for backward compatibility
    CONFIG = PicarxConstants.CONFIG_PATH
    DEFAULT_LINE_REF = PicarxConstants.DEFAULT_LINE_REFERENCE
    DEFAULT_CLIFF_REF = PicarxConstants.DEFAULT_CLIFF_REFERENCE
    DIR_MIN = PicarxConstants.SERVO_LIMITS['direction']['min']
    DIR_MAX = PicarxConstants.SERVO_LIMITS['direction']['max']
    CAM_PAN_MIN = PicarxConstants.SERVO_LIMITS['cam_pan']['min']
    CAM_PAN_MAX = PicarxConstants.SERVO_LIMITS['cam_pan']['max']
    CAM_TILT_MIN = PicarxConstants.SERVO_LIMITS['cam_tilt']['min']
    CAM_TILT_MAX = PicarxConstants.SERVO_LIMITS['cam_tilt']['max']
    PERIOD = PicarxConstants.PWM_PERIOD
    PRESCALER = PicarxConstants.PWM_PRESCALER
    TIMEOUT = PicarxConstants.PWM_TIMEOUT

    # servo_pins: camera_pan_servo, camera_tilt_servo, direction_servo
    # motor_pins: left_swicth, right_swicth, left_pwm, right_pwm
    # grayscale_pins: 3 adc channels
    # ultrasonic_pins: trig, echo2
    # config: path of config file
    def __init__(self, 
                servo_pins: List[str] = ['P0', 'P1', 'P2'], 
                motor_pins: List[str] = ['D4', 'D5', 'P13', 'P12'],
                grayscale_pins: List[str] = ['A0', 'A1', 'A2'],
                ultrasonic_pins: List[str] = ['D2','D3'],
                config: str = CONFIG,
                ) -> None:
        """Initialize PiCar-X robot with hardware configuration.
        
        Args:
            servo_pins: List of servo pin names [camera_pan, camera_tilt, direction]
            motor_pins: List of motor pin names [left_switch, right_switch, left_pwm, right_pwm]
            grayscale_pins: List of grayscale sensor ADC channels
            ultrasonic_pins: List of ultrasonic sensor pins [trigger, echo]
            config: Path to configuration file
        """
        
        # Initialize constants for easy access
        self.constants = PicarxConstants()

        # reset robot_hat
        utils.reset_mcu()
        time.sleep(self.constants.MCU_RESET_DELAY)

        # --------- config_file ---------
        self.config_file = fileDB(config, 777, os.getlogin())

        # --------- servos init ---------
        self.cam_pan = Servo(servo_pins[0])
        self.cam_tilt = Servo(servo_pins[1])   
        self.dir_servo_pin = Servo(servo_pins[2])
        # get calibration values
        self.dir_cali_val = float(self.config_file.get("picarx_dir_servo", default_value=0))
        self.cam_pan_cali_val = float(self.config_file.get("picarx_cam_pan_servo", default_value=0))
        self.cam_tilt_cali_val = float(self.config_file.get("picarx_cam_tilt_servo", default_value=0))
        # set servos to init angle
        self.dir_servo_pin.angle(self.dir_cali_val)
        self.cam_pan.angle(self.cam_pan_cali_val)
        self.cam_tilt.angle(self.cam_tilt_cali_val)

        # --------- motors init ---------
        self.left_rear_dir_pin = Pin(motor_pins[0])
        self.right_rear_dir_pin = Pin(motor_pins[1])
        self.left_rear_pwm_pin = PWM(motor_pins[2])
        self.right_rear_pwm_pin = PWM(motor_pins[3])
        self.motor_direction_pins = [self.left_rear_dir_pin, self.right_rear_dir_pin]
        self.motor_speed_pins = [self.left_rear_pwm_pin, self.right_rear_pwm_pin]
        # get calibration values
        self.cali_dir_value = self.config_file.get("picarx_dir_motor", default_value="[1, 1]")
        self.cali_dir_value = [int(i.strip()) for i in self.cali_dir_value.strip().strip("[]").split(",")]
        self.cali_speed_value = [0, 0]
        self.dir_current_angle = 0
        # init pwm
        for pin in self.motor_speed_pins:
            pin.period(self.PERIOD)
            pin.prescaler(self.PRESCALER)

        # --------- grayscale module init ---------
        adc0, adc1, adc2 = [ADC(pin) for pin in grayscale_pins]
        self.grayscale = Grayscale_Module(adc0, adc1, adc2, reference=None)
        # get reference
        self.line_reference = self.config_file.get("line_reference", default_value=str(self.DEFAULT_LINE_REF))
        self.line_reference = [float(i) for i in self.line_reference.strip().strip('[]').split(',')]
        self.cliff_reference = self.config_file.get("cliff_reference", default_value=str(self.DEFAULT_CLIFF_REF))
        self.cliff_reference = [float(i) for i in self.cliff_reference.strip().strip('[]').split(',')]
        # transfer reference
        self.grayscale.reference(self.line_reference)

        # --------- ultrasonic init ---------
        trig, echo= ultrasonic_pins
        self.ultrasonic = Ultrasonic(Pin(trig), Pin(echo, mode=Pin.IN, pull=Pin.PULL_DOWN))
        
    # ===================================================================
    # MOTOR CONTROL METHODS
    # ===================================================================
        
    def set_motor_speed(self, motor: int, speed: int) -> None:
        """Set motor speed with direction control.
        
        Args:
            motor: Motor index (1=left motor, 2=right motor)
            speed: Motor speed (-100 to 100, negative=reverse)
            
        Raises:
            ValueError: If motor index is not 1 or 2
            RuntimeError: If motor control fails
        """
        # Validate motor index
        if motor not in self.constants.VALID_MOTOR_INDICES:
            raise ValueError(f"Motor index must be one of {self.constants.VALID_MOTOR_INDICES}, got {motor}")
        
        # Validate and constrain speed
        if not isinstance(speed, (int, float)):
            raise TypeError(f"Speed must be a number, got {type(speed)}")
        
        speed = constrain(speed, -self.constants.SPEED_MAX, self.constants.SPEED_MAX)
        motor_idx = motor - 1
        
        try:
            if speed >= 0:
                direction = 1 * self.cali_dir_value[motor_idx]
            elif speed < 0:
                direction = -1 * self.cali_dir_value[motor_idx]
            speed = abs(speed)
            
            # Convert speed to PWM range using constants
            if speed != 0:
                speed = int(speed / self.constants.MOTOR_SPEED_DIVISOR) + self.constants.MOTOR_SPEED_OFFSET
            speed = speed - self.cali_speed_value[motor_idx]
            
            # Apply motor control
            if direction < 0:
                self.motor_direction_pins[motor_idx].high()
                self.motor_speed_pins[motor_idx].pulse_width_percent(speed)
            else:
                self.motor_direction_pins[motor_idx].low()
                self.motor_speed_pins[motor_idx].pulse_width_percent(speed)
                
        except Exception as e:
            self.stop()  # Safety: stop motors on any error
            raise RuntimeError(f"Motor control failed for motor {motor}: {e}")

    def motor_speed_calibration(self, value):
        self.cali_speed_value = value
        if value < 0:
            self.cali_speed_value[0] = 0
            self.cali_speed_value[1] = abs(self.cali_speed_value)
        else:
            self.cali_speed_value[0] = abs(self.cali_speed_value)
            self.cali_speed_value[1] = 0

    # ===================================================================
    # MOTOR CALIBRATION METHODS
    # ===================================================================

    def motor_direction_calibrate(self, motor: int, value: int) -> None:
        """Set motor direction calibration value.
        
        Args:
            motor: Motor index (1=left motor, 2=right motor)
            value: Direction calibration (1=normal, -1=reversed)
            
        Raises:
            ValueError: If motor index or value is invalid
        """
        # Validate inputs using constants
        if motor not in self.constants.VALID_MOTOR_INDICES:
            raise ValueError(f"Motor index must be one of {self.constants.VALID_MOTOR_INDICES}, got {motor}")
        if value not in self.constants.VALID_DIRECTION_VALUES:
            raise ValueError(f"Direction value must be one of {self.constants.VALID_DIRECTION_VALUES}, got {value}")
        
        motor_idx = motor - 1
        self.cali_dir_value[motor_idx] = value
        self.config_file.set("picarx_dir_motor", self.cali_dir_value)

    # ===================================================================
    # SERVO CONTROL AND CALIBRATION METHODS
    # ===================================================================
    
    def _validate_angle(self, angle: Union[int, float], min_val: float, max_val: float, name: str) -> float:
        """Validate and constrain angle values.
        
        Args:
            angle: Angle to validate
            min_val: Minimum allowed angle
            max_val: Maximum allowed angle
            name: Name of the angle parameter for error messages
            
        Returns:
            Validated and constrained angle
            
        Raises:
            TypeError: If angle is not a number
        """
        if not isinstance(angle, (int, float)):
            raise TypeError(f"{name} must be a number, got {type(angle)}")
        return constrain(angle, min_val, max_val)

    def dir_servo_calibrate(self, value: Union[int, float]) -> None:
        """Calibrate direction servo offset.
        
        Args:
            value: Calibration offset value
            
        Raises:
            TypeError: If value is not a number
        """
        if not isinstance(value, (int, float)):
            raise TypeError(f"Calibration value must be a number, got {type(value)}")
        
        self.dir_cali_val = value
        self.config_file.set("picarx_dir_servo", str(value))
        self.dir_servo_pin.angle(value)

    def set_dir_servo_angle(self, value: Union[int, float]) -> None:
        """Set direction servo angle within safe limits.
        
        Args:
            value: Desired angle in degrees (constrained to -30 to 30)
            
        Raises:
            TypeError: If value is not a number
        """
        validated_angle = self._validate_angle(value, 
                                              self.constants.SERVO_LIMITS['direction']['min'], 
                                              self.constants.SERVO_LIMITS['direction']['max'], 
                                              "Direction angle")
        self.dir_current_angle = validated_angle
        angle_value = self.dir_current_angle + self.dir_cali_val
        self.dir_servo_pin.angle(angle_value)

    def cam_pan_servo_calibrate(self, value):
        self.cam_pan_cali_val = value
        self.config_file.set("picarx_cam_pan_servo", "%s"%value)
        self.cam_pan.angle(value)

    def cam_tilt_servo_calibrate(self, value):
        self.cam_tilt_cali_val = value
        self.config_file.set("picarx_cam_tilt_servo", "%s"%value)
        self.cam_tilt.angle(value)

    def set_cam_pan_angle(self, value: Union[int, float]) -> None:
        """Set camera pan servo angle within safe limits.
        
        Args:
            value: Desired pan angle in degrees (constrained to -90 to 90)
            
        Raises:
            TypeError: If value is not a number
        """
        validated_angle = self._validate_angle(value, 
                                              self.constants.SERVO_LIMITS['cam_pan']['min'], 
                                              self.constants.SERVO_LIMITS['cam_pan']['max'], 
                                              "Camera pan angle")
        self.cam_pan.angle(-1 * (validated_angle + -1 * self.cam_pan_cali_val))

    def set_cam_tilt_angle(self, value: Union[int, float]) -> None:
        """Set camera tilt servo angle within safe limits.
        
        Args:
            value: Desired tilt angle in degrees (constrained to -35 to 65)
            
        Raises:
            TypeError: If value is not a number
        """
        validated_angle = self._validate_angle(value, 
                                              self.constants.SERVO_LIMITS['cam_tilt']['min'], 
                                              self.constants.SERVO_LIMITS['cam_tilt']['max'], 
                                              "Camera tilt angle")
        self.cam_tilt.angle(-1 * (validated_angle + -1 * self.cam_tilt_cali_val))

    # ===================================================================
    # MOVEMENT CONTROL METHODS
    # ===================================================================

    def set_power(self, speed):
        self.set_motor_speed(1, speed)
        self.set_motor_speed(2, speed)

    def backward(self, speed):
        current_angle = self.dir_current_angle
        if current_angle != 0:
            abs_current_angle = abs(current_angle)
            if abs_current_angle > self.DIR_MAX:
                abs_current_angle = self.DIR_MAX
            power_scale = (100 - abs_current_angle) / 100.0 
            if (current_angle / abs_current_angle) > 0:
                self.set_motor_speed(1, -1*speed)
                self.set_motor_speed(2, speed * power_scale)
            else:
                self.set_motor_speed(1, -1*speed * power_scale)
                self.set_motor_speed(2, speed )
        else:
            self.set_motor_speed(1, -1*speed)
            self.set_motor_speed(2, speed)  

    def forward(self, speed: int) -> None:
        """Move forward with differential steering based on current direction angle.
        
        Args:
            speed: Forward speed (0-100)
            
        Raises:
            TypeError: If speed is not a number
            ValueError: If speed is negative
        """
        if not isinstance(speed, (int, float)):
            raise TypeError(f"Speed must be a number, got {type(speed)}")
        if speed < 0:
            raise ValueError(f"Forward speed must be non-negative, got {speed}")
        
        speed = constrain(speed, self.constants.SPEED_MIN, self.constants.SPEED_MAX)
        current_angle = self.dir_current_angle
        
        if current_angle != 0:
            abs_current_angle = abs(current_angle)
            if abs_current_angle > self.constants.SERVO_LIMITS['direction']['max']:
                abs_current_angle = self.constants.SERVO_LIMITS['direction']['max']
            power_scale = (self.constants.SPEED_MAX - abs_current_angle) / self.constants.SPEED_MAX
            if (current_angle / abs_current_angle) > 0:
                self.set_motor_speed(1, int(speed * power_scale))
                self.set_motor_speed(2, -speed) 
            else:
                self.set_motor_speed(1, speed)
                self.set_motor_speed(2, int(-speed * power_scale))
        else:
            self.set_motor_speed(1, speed)
            self.set_motor_speed(2, -speed)                  

    def tank_turn(self, direction: Union[str, int], speed: int, angle: Optional[float] = None) -> None:
        """Tank turn - rotate in place by driving motors in opposite directions.
        
        Args:
            direction: Turn direction ('left', 'right', -1, or 1)
            speed: Turn speed (0-100)
            angle: Optional angle in degrees (uses calibrated timing for auto-stop)
            
        Raises:
            ValueError: If direction is not valid
            TypeError: If speed or angle are not numbers
        """
        # Validate direction using constants
        if direction not in self.constants.VALID_TURN_DIRECTIONS:
            raise ValueError(f"Direction must be one of {self.constants.VALID_TURN_DIRECTIONS}, got {direction}")
        
        # Validate speed
        if not isinstance(speed, (int, float)):
            raise TypeError(f"Speed must be a number, got {type(speed)}")
        speed = constrain(speed, self.constants.SPEED_MIN, self.constants.SPEED_MAX)
        
        # Validate angle if provided
        if angle is not None:
            if not isinstance(angle, (int, float)):
                raise TypeError(f"Angle must be a number, got {type(angle)}")
        
        # Normalize direction input
        if direction == 'left' or direction == -1:
            # Left turn: left motor backward, right motor forward (relative to car forward)
            self.set_motor_speed(1, -speed)  # left motor backward
            self.set_motor_speed(2, -speed)   # right motor forward (opposite to left)
        elif direction == 'right' or direction == 1:
            # Right turn: left motor forward, right motor backward (relative to car forward)
            self.set_motor_speed(1, speed)   # left motor forward  
            self.set_motor_speed(2, speed)  # right motor backward (opposite to left)
        
        # If angle is specified, calculate timing and auto-stop
        if angle is not None:
            try:
                # Get calibrated 360° time and speed using constants
                calibrated_360_time = float(self.config_file.get("tank_turn_360_time", 
                                                               default_value=self.constants.DEFAULT_TURN_TIMES['tank_turn_360']))
                calibrated_speed = float(self.config_file.get("tank_turn_calibration_speed", 
                                                            default_value=self.constants.DEFAULT_TURN_SPEEDS['tank_turn_calibration']))
                
                # Calculate time needed for the requested angle
                # Scale by speed difference (inversely proportional to speed)
                speed_scale = calibrated_speed / speed if speed > 0 else 1.0
                turn_time = (abs(angle) / self.constants.FULL_CIRCLE_DEGREES) * calibrated_360_time * speed_scale
                
                # Execute the turn with timing
                time.sleep(turn_time)
                self.stop()
            except Exception as e:
                self.stop()  # Safety: ensure motors stop on error
                raise RuntimeError(f"Tank turn with angle failed: {e}")
    
    def tank_turn_angle(self, angle: float, speed: int = 50) -> None:
        """Convenience method for angle-based tank turns.
        
        Args:
            angle: Angle in degrees (positive=right, negative=left)
            speed: Turn speed (0-100), defaults to 50
        """
        direction = 'right' if angle >= 0 else 'left'
        self.tank_turn(direction, speed, abs(angle))

    def pivot_turn(self, direction, speed, angle=None):
        '''
        Pivot turn - turn around one stationary wheel (tighter turn radius)
        
        param direction: turn direction, 'left' or 'right' or -1/1
        type direction: str or int
        param speed: turn speed (0-100)
        type speed: int
        param angle: optional angle in degrees (uses calibrated timing)
        type angle: float or None
        '''
        speed = constrain(speed, 0, 100)
        
        # Normalize direction input
        if direction == 'left' or direction == -1:
            # Left pivot: left motor stopped, right motor forward
            self.set_motor_speed(1, 0)      # left motor stopped
            self.set_motor_speed(2, -speed)  # right motor forward
        elif direction == 'right' or direction == 1:
            # Right pivot: right motor stopped, left motor forward
            self.set_motor_speed(1, speed)  # left motor forward
            self.set_motor_speed(2, 0)      # right motor stopped
        else:
            raise ValueError("direction must be 'left', 'right', -1, or 1")
        
        # If angle is specified, calculate timing and auto-stop
        if angle is not None:
            # Get calibrated 360° time and speed
            calibrated_360_time = float(self.config_file.get("pivot_turn_360_time", default_value=8.0))
            calibrated_speed = float(self.config_file.get("pivot_turn_calibration_speed", default_value=50))
            
            # Calculate time needed for the requested angle
            # Scale by speed difference (inversely proportional to speed)
            speed_scale = calibrated_speed / speed if speed > 0 else 1.0
            turn_time = (abs(angle) / 360.0) * calibrated_360_time * speed_scale
            
            # Execute the turn with timing
            time.sleep(turn_time)
            self.stop()
    
    def pivot_turn_angle(self, angle, speed=50):
        '''
        Convenience method for angle-based pivot turns
        
        param angle: angle in degrees (positive = right, negative = left)
        type angle: float
        param speed: turn speed (0-100)
        type speed: int
        '''
        direction = 'right' if angle >= 0 else 'left'
        self.pivot_turn(direction, speed, abs(angle))

    def stop(self) -> None:
        """Stop all motors immediately.
        
        Note:
            Executes multiple times with delays to ensure reliable stopping.
        """
        for _ in range(self.constants.MOTOR_STOP_ITERATIONS):
            self.motor_speed_pins[0].pulse_width_percent(0)
            self.motor_speed_pins[1].pulse_width_percent(0)
            time.sleep(self.constants.MOTOR_STOP_DELAY)

    # ===================================================================
    # SENSOR METHODS
    # ===================================================================

    def get_distance(self) -> float:
        """Get distance measurement from ultrasonic sensor.
        
        Returns:
            Distance in centimeters, or -1 if measurement failed
            
        Raises:
            RuntimeError: If sensor reading fails consistently
        """
        try:
            distance = self.ultrasonic.read()
            return distance if distance is not None else -1
        except Exception as e:
            raise RuntimeError(f"Ultrasonic sensor reading failed: {e}")

    def set_grayscale_reference(self, value: List[float]) -> None:
        """Set grayscale sensor reference values.
        
        Args:
            value: List of 3 reference values [left, center, right]
            
        Raises:
            ValueError: If value is not a list of 3 numbers
            TypeError: If list elements are not numbers
        """
        if not isinstance(value, list):
            raise TypeError(f"Grayscale reference must be a list, got {type(value)}")
        if len(value) != 3:
            raise ValueError(f"Grayscale reference must have 3 values, got {len(value)}")
        
        # Validate all elements are numbers
        for i, val in enumerate(value):
            if not isinstance(val, (int, float)):
                raise TypeError(f"Grayscale reference[{i}] must be a number, got {type(val)}")
        
        self.line_reference = value
        self.grayscale.reference(self.line_reference)
        self.config_file.set("line_reference", str(self.line_reference))

    def get_grayscale_data(self) -> List[float]:
        """Get current grayscale sensor readings.
        
        Returns:
            List of 3 grayscale values [left, center, right]
        """
        return list.copy(self.grayscale.read())

    def get_line_status(self, gm_val_list: List[float]) -> Union[str, int]:
        """Determine line following status from grayscale readings.
        
        Args:
            gm_val_list: List of 3 grayscale sensor values
            
        Returns:
            Line status indicator (implementation dependent)
        """
        return self.grayscale.read_status(gm_val_list)

    def set_line_reference(self, value):
        self.set_grayscale_reference(value)

    def get_cliff_status(self,gm_val_list):
        for i in range(0,3):
            if gm_val_list[i]<=self.cliff_reference[i]:
                return True
        return False

    def set_cliff_reference(self, value):
        if isinstance(value, list) and len(value) == 3:
            self.cliff_reference = value
            self.config_file.set("cliff_reference", self.cliff_reference)
        else:
            raise ValueError("grayscale reference must be a 1*3 list")

    # ===================================================================
    # UTILITY METHODS
    # ===================================================================

    def __enter__(self):
        """Context manager entry - returns self for 'with' statement.
        
        Returns:
            Self for use in with statement
            
        Example:
            with Picarx() as px:
                px.forward(50)
                time.sleep(1)
                # Automatically stops and resets on exit
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensures safe cleanup.
        
        Args:
            exc_type: Exception type if an exception occurred
            exc_val: Exception value if an exception occurred  
            exc_tb: Exception traceback if an exception occurred
            
        Returns:
            False to allow exceptions to propagate
            
        Note:
            Always stops motors and resets servos for safety, even on exceptions.
        """
        try:
            self.stop()
            self.reset()
        except Exception as cleanup_error:
            # Log cleanup error but don't mask the original exception
            print(f"Warning: Cleanup error during context exit: {cleanup_error}")
        
        # Return False to let any original exceptions propagate
        return False

    def reset(self) -> None:
        """Reset robot to safe neutral state.
        
        Stops all motors and returns all servos to neutral positions.
        This method is automatically called when using context manager.
        
        Raises:
            RuntimeError: If reset operations fail
        """
        try:
            # Stop all motors first for safety
            self.stop()
            
            # Reset all servos to neutral positions
            self.set_dir_servo_angle(0)
            self.set_cam_tilt_angle(0) 
            self.set_cam_pan_angle(0)
            
        except Exception as e:
            # Ensure motors are stopped even if servo reset fails
            try:
                self.stop()
            except:
                pass  # If stop also fails, we've done our best
            raise RuntimeError(f"Robot reset failed: {e}")

if __name__ == "__main__":
    px = Picarx()
    px.forward(50)
    time.sleep(1)
    px.stop()
