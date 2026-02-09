#!/usr/bin/env python3
"""
⌨️ Advanced Keyboard Navigation with Safety Features

This example demonstrates professional teleoperation with:
- Real-time keyboard control with video feed
- Active obstacle and cliff detection
- Intelligent LED status indicators (RGB + headlights)
- Audio feedback during reverse operations
- Multi-threaded responsive control system
- Comprehensive safety override system

CONTROLS:
    Movement:
        W/↑ : Forward
        S/↓ : Backward (with blinking lights and beeping)
        A/← : Tank Turn Left
        D/→ : Tank Turn Right
        Space/F : Stop
        
    Speed Control:
        + : Increase speed
        - : Decrease speed
        
    Lights Control:
        Y : Toggle headlights on/off
        
    Camera Control:
        I : Tilt Up
        K : Tilt Down
        J : Pan Left
        L : Pan Right
        H : Home position (center camera)
        
    System:
        Q/Ctrl+C : Quit
        R : Reset (stop and center all)
        M : Toggle manual override (bypass safety)
        
SAFETY FEATURES:
    🌈 Rainbow RGB : All clear, breathing animation through colors
    🔴 Red RGB : Danger detected (obstacle or cliff)
    🟡 Yellow RGB : Manual override (all safety checks disabled)
    💡 Headlights : Always on, blink during reverse
    🔊 Audio : Beep sound effect during reverse movement
    
    Restrictive Safety Mode:
    - When obstacle/cliff detected → forward movement BLOCKED
    - Backward always allowed (to escape danger)
    - Left/right turns always allowed (to maneuver away)
    - Continuous monitoring stops robot if backing/turning into new danger
    - Forward automatically resumes when clear
    - Press M for manual override to bypass all restrictions
    
REQUIREMENTS:
    - Calibrated sensors (run setup/first_time_setup.py)
    - Camera enabled (raspi-config)
    - Dependencies: readchar, vilib, robot-hat
"""

from picarx import Picarx
from picarx.led_extension import PicarxLedController
from vilib import Vilib
from robot_hat import TTS
import readchar
import threading
import time
import sys
import math
import colorsys


def get_breathing_color(elapsed_time: float) -> str:
    """Generate a breathing color animation that cycles through rainbow colors
    
    Args:
        elapsed_time: Time in seconds since animation started
        
    Returns:
        Hex color string (e.g., "#FF00FF")
    """
    # Breathing effect: oscillate brightness with a sine wave (2 second period)
    breathing_phase = (math.sin(elapsed_time * math.pi) + 1) / 2  # 0 to 1
    brightness = 0.3 + (breathing_phase * 0.7)  # Range from 0.3 to 1.0
    
    # Color cycling: rotate through rainbow (5 second period for full cycle)
    hue = (elapsed_time / 5.0) % 1.0  # 0 to 1
    
    # Convert HSV to RGB (saturation = 1.0 for vibrant colors)
    r, g, b = colorsys.hsv_to_rgb(hue, 1.0, brightness)
    
    # Convert to hex color string
    return "#{:02x}{:02x}{:02x}".format(int(r * 255), int(g * 255), int(b * 255))


class SafetyMonitor:
    """Background thread monitoring sensors for obstacles and cliffs"""
    
    def __init__(self, px: Picarx):
        self.px = px
        self.distance = 100.0  # cm
        self.grayscale = [4095, 4095, 4095]  # [left, center, right]
        self.obstacle_detected = False
        self.cliff_detected = False
        self.running = False
        self.thread = None
        
        # Safety thresholds
        self.OBSTACLE_THRESHOLD = 20  # cm - closer distance before stopping
        self.CLIFF_REFERENCE = [200, 200, 200]  # Same as working cliff_detection example
        
        # Set cliff detection reference (use built-in method)
        self.px.set_cliff_reference(self.CLIFF_REFERENCE)
        
        # Filtering for cliff detection (prevent flickering)
        self.cliff_detection_counter = 0
        self.CLIFF_DETECTION_REQUIRED = 25  # Need 25 consecutive detections to trigger (2.5 seconds)
        self.CLIFF_CLEAR_REQUIRED = 40     # Need 40 consecutive clears to reset (4 seconds)
        self.cliff_raw_status = False  # Raw cliff reading before filtering
        
    def start(self):
        """Start the safety monitoring thread"""
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        
    def stop(self):
        """Stop the safety monitoring thread"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
            
    def _monitor_loop(self):
        """Continuously monitor sensors"""
        while self.running:
            try:
                # Read ultrasonic distance
                dist = self.px.get_distance()
                if dist > 0:  # Valid reading
                    self.distance = dist
                    
                # Read grayscale sensors
                self.grayscale = self.px.get_grayscale_data()
                
                # Update obstacle flag (simple threshold)
                self.obstacle_detected = (self.distance < self.OBSTACLE_THRESHOLD)
                
                # Update cliff flag with filtering (use built-in method like cliff_detection.py)
                cliff_reading = self.px.get_cliff_status(self.grayscale)
                self.cliff_raw_status = cliff_reading  # Store for debugging
                
                if cliff_reading:
                    # Cliff detected in this reading
                    self.cliff_detection_counter += 1
                    if self.cliff_detection_counter >= self.CLIFF_DETECTION_REQUIRED:
                        self.cliff_detected = True
                        self.cliff_detection_counter = self.CLIFF_DETECTION_REQUIRED  # Cap at max
                else:
                    # No cliff in this reading
                    if self.cliff_detected:
                        # Currently in cliff state, need consecutive clears to exit
                        self.cliff_detection_counter -= 1
                        if self.cliff_detection_counter <= 0:
                            # Start counting clears
                            pass
                        if self.cliff_detection_counter <= -self.CLIFF_CLEAR_REQUIRED:
                            self.cliff_detected = False
                            self.cliff_detection_counter = 0
                    else:
                        # Not in cliff state, reset counter toward zero
                        if self.cliff_detection_counter > 0:
                            self.cliff_detection_counter = max(0, self.cliff_detection_counter - 2)  # Decay faster
                
            except Exception as e:
                # Silently continue on sensor errors
                pass
                
            time.sleep(0.1)  # 10 Hz update rate
            
    def is_safe_forward(self) -> bool:
        """Check if it's safe to move forward"""
        return not (self.obstacle_detected or self.cliff_detected)
        
    def is_safe_backward(self) -> bool:
        """Check if it's safe to move backward"""
        return not self.cliff_detected
        
    def is_safe_turn(self) -> bool:
        """Check if it's safe to turn"""
        return not self.cliff_detected
        
    def get_status_text(self) -> str:
        """Get formatted status text"""
        if self.cliff_detected:
            return f"⚠️  CLIFF DETECTED (clearing: {-self.cliff_detection_counter}/{self.CLIFF_CLEAR_REQUIRED})"
        elif self.cliff_raw_status and self.cliff_detection_counter > 0:
            return f"⚠️  Cliff raw detected (count: {self.cliff_detection_counter}/{self.CLIFF_DETECTION_REQUIRED})"
        elif self.obstacle_detected:
            return "⚠️  OBSTACLE AHEAD"
        else:
            return "✅ All Clear"


class AudioController:
    """Manages audio feedback (beeping during reverse)"""
    
    def __init__(self):
        self.beeping = False
        self.running = False
        self.thread = None
        
        # Initialize TTS for beep sounds (same as integration testing)
        try:
            self.tts = TTS()
            self.tts_available = True
            print("🔊 TTS initialized successfully")
        except Exception as e:
            print(f"❌ TTS initialization failed: {e}")
            self.tts_available = False
            
    def start(self):
        """Start the audio controller thread"""
        self.running = True
        self.thread = threading.Thread(target=self._audio_loop, daemon=True)
        self.thread.start()
        
    def stop(self):
        """Stop the audio controller"""
        self.running = False
        self.beeping = False
        if self.thread:
            self.thread.join(timeout=1.0)
            
    def enable_beeping(self):
        """Enable reverse beep sound"""
        self.beeping = True
        
    def disable_beeping(self):
        """Disable reverse beep sound"""
        self.beeping = False
        
    def _audio_loop(self):
        """Beep at regular intervals when enabled"""
        while self.running:
            if self.beeping and self.tts_available:
                try:
                    # Say beep
                    self.tts.say("beep")
                    time.sleep(0.5)  # Wait before next beep
                except Exception as e:
                    print(f"TTS error: {e}")
                    time.sleep(0.5)
            else:
                time.sleep(0.1)


class HeadlightController:
    """Manages headlight blinking during reverse"""
    
    def __init__(self, led_controller: PicarxLedController):
        self.led = led_controller
        self.blinking = False
        self.running = False
        self.thread = None
        self.blink_state = True
        
    def start(self):
        """Start the headlight controller thread"""
        self.running = True
        self.thread = threading.Thread(target=self._blink_loop, daemon=True)
        self.thread.start()
        
    def stop(self):
        """Stop the headlight controller"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
            
    def enable_blinking(self):
        """Enable headlight blinking"""
        self.blinking = True
        
    def disable_blinking(self):
        """Disable headlight blinking (keep on steady)"""
        self.blinking = False
        self.led.headlights_on(1.0)
        
    def _blink_loop(self):
        """Toggle headlights when blinking enabled"""
        while self.running:
            if self.blinking:
                if self.blink_state:
                    self.led.headlights_on(1.0)
                else:
                    self.led.headlights_off()
                self.blink_state = not self.blink_state
                time.sleep(0.5)  # 1 Hz blink rate
            else:
                time.sleep(0.1)


class KeyboardController:
    """Handles keyboard input in background thread"""
    
    def __init__(self):
        self.current_key = None
        self.running = False
        self.thread = None
        
    def start(self):
        """Start keyboard reading thread"""
        self.running = True
        self.thread = threading.Thread(target=self._read_loop, daemon=True)
        self.thread.start()
        
    def stop(self):
        """Stop keyboard reading"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
            
    def _read_loop(self):
        """Continuously read keyboard input"""
        while self.running:
            try:
                key = readchar.readkey()
                self.current_key = key
                time.sleep(0.05)  # Prevent key flooding
            except:
                pass
                
    def get_key(self):
        """Get current key and clear it"""
        key = self.current_key
        self.current_key = None
        return key


class StatusDisplay:
    """Terminal UI display manager"""
    
    def __init__(self):
        self.speed = 50
        self.direction = "STOPPED"
        self.distance = 0.0
        self.grayscale = [0, 0, 0]
        self.safety_status = "Unknown"
        self.manual_override = False
        self.cam_pan = 0
        self.cam_tilt = 0
        
    def clear_screen(self):
        """Clear terminal screen"""
        print("\033[2J\033[H", end='')
        
    def update_display(self):
        """Draw the complete status display"""
        print("\033[H", end='')  # Move cursor to top
        print("=" * 70)
        print(" 🤖 PICAR-X KEYBOARD NAVIGATION - Advanced Teleoperation".center(70))
        print("=" * 70)
        print()
        print(f"  🎯 Direction    : {self.direction:12s}")
        print(f"  ⚡ Speed       : {self.speed:3d}%")
        print(f"  📏 Distance    : {self.distance:5.1f} cm")
        print(f"  🌓 Grayscale   : L:{self.grayscale[0]:4d} C:{self.grayscale[1]:4d} R:{self.grayscale[2]:4d}")
        print(f"  📹 Camera Pan  : {self.cam_pan:+4.0f}°")
        print(f"  📹 Camera Tilt : {self.cam_tilt:+4.0f}°")
        print()
        print(f"  {self.safety_status}")
        
        if self.manual_override:
            print(f"  🔓 MANUAL OVERRIDE ACTIVE - All safety checks disabled!")
        
        print()
        print("-" * 70)
        print("  Movement: W/↑ forward  S/↓ backward  A/← left  D/→ right  SPACE stop")
        print("  Speed: +/- adjust     Lights: Y toggle     Camera: I/K tilt  J/L pan")
        print("  System: Q quit  R reset  M toggle manual override")
        print("-" * 70)
        print()


def main():
    """Main keyboard navigation control loop"""
    
    # Initialize display
    display = StatusDisplay()
    display.clear_screen()
    print("🚀 Initializing Advanced Keyboard Navigation System...")
    print()
    
    # Initialize robot and subsystems
    try:
        px = Picarx()
        print("✅ Robot initialized")
        
        led = PicarxLedController()
        print("✅ LED controller initialized")
        
        safety = SafetyMonitor(px)
        safety.start()
        print("✅ Safety monitor started")
        
        audio = AudioController()
        audio.start()
        print("✅ Audio controller started")
        
        # Test TTS
        print("🔊 Testing audio...")
        if audio.tts_available:
            try:
                audio.tts.say("Welcome to keyboard navigation")
                print("✅ Audio test successful")
            except Exception as e:
                print(f"⚠️ Audio test failed: {e}")
        else:
            print("⚠️ TTS not available")
        
        headlight = HeadlightController(led)
        headlight.start()
        print("✅ Headlight controller started")
        
        keyboard = KeyboardController()
        keyboard.start()
        print("✅ Keyboard controller started")
        
        # Initialize camera
        print("📹 Starting camera...")
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=True, web=True)
        print("✅ Camera started (web view: http://[robot-ip]:9000/mjpg)")
        
        time.sleep(2)  # Allow camera to initialize
        
        # Turn on headlights
        led.headlights_on(1.0)
        led.set_color(get_breathing_color(0))  # Start with breathing animation
        
        print()
        print("🎮 System ready! Use keyboard controls (press Q to quit)")
        time.sleep(2)
        
        # Main control variables
        speed = 50
        manual_override = False
        headlights_on = True  # Track headlight state
        cam_pan_angle = 0
        cam_tilt_angle = 0
        current_movement = "STOPPED"  # Track current movement state
        
        # Animation state for breathing LED effect
        animation_start_time = time.time()
        
        # Animation state
        animation_start_time = time.time()
        
        # Start main control loop
        display.clear_screen()
        
        try:
            while True:
                # Get keyboard input
                key = keyboard.get_key()
                
                if key:
                    key_lower = key.lower()
                    
                    # Quit command
                    if key_lower == 'q' or key == readchar.key.CTRL_C:
                        break
                        
                    # Manual override toggle
                    elif key_lower == 'm':
                        manual_override = not manual_override
                        
                    # Reset command
                    elif key_lower == 'r':
                        px.stop()
                        px.set_dir_servo_angle(0)
                        cam_pan_angle = 0
                        cam_tilt_angle = 0
                        px.set_cam_pan_angle(cam_pan_angle)
                        px.set_cam_tilt_angle(cam_tilt_angle)
                        current_movement = "STOPPED"
                        display.direction = "RESET"
                        audio.disable_beeping()
                        headlight.disable_blinking()
                        
                    # Speed adjustment
                    elif key == '+' or key == '=':
                        speed = min(100, speed + 10)
                    elif key == '-' or key == '_':
                        speed = max(20, speed - 10)
                        
                    # Headlight toggle
                    elif key_lower == 'y':
                        headlights_on = not headlights_on
                        if headlights_on:
                            led.headlights_on(1.0)
                        else:
                            led.headlights_off()
                        
                    # Camera control
                    elif key_lower == 'h':
                        cam_pan_angle = 0
                        cam_tilt_angle = 0
                        px.set_cam_pan_angle(cam_pan_angle)
                        px.set_cam_tilt_angle(cam_tilt_angle)
                    elif key_lower == 'j':
                        cam_pan_angle = max(-90, cam_pan_angle - 10)
                        px.set_cam_pan_angle(cam_pan_angle)
                    elif key_lower == 'l':
                        cam_pan_angle = min(90, cam_pan_angle + 10)
                        px.set_cam_pan_angle(cam_pan_angle)
                    elif key_lower == 'i':
                        cam_tilt_angle = min(65, cam_tilt_angle + 10)
                        px.set_cam_tilt_angle(cam_tilt_angle)
                    elif key_lower == 'k':
                        cam_tilt_angle = max(-35, cam_tilt_angle - 10)
                        px.set_cam_tilt_angle(cam_tilt_angle)
                        
                    # Movement commands with safety checks
                    elif key_lower == 'w' or key == readchar.key.UP:
                        # Forward only allowed if safe OR manual override
                        if manual_override or safety.is_safe_forward():
                            px.set_dir_servo_angle(0)
                            px.forward(speed)
                            current_movement = "FORWARD"
                            display.direction = "FORWARD"
                            audio.disable_beeping()
                            headlight.disable_blinking()
                        else:
                            px.stop()
                            current_movement = "STOPPED"
                            if safety.obstacle_detected:
                                display.direction = "BLOCKED - Obstacle ahead"
                            elif safety.cliff_detected:
                                display.direction = "BLOCKED - Cliff ahead"
                            
                    elif key_lower == 's' or key == readchar.key.DOWN:
                        # Backward always allowed (even with obstacle/cliff) to escape danger
                        # Continuous monitor will stop if backing into new danger
                        px.backward(speed)
                        current_movement = "BACKWARD"
                        display.direction = "BACKWARD ⚠️"
                        audio.enable_beeping()
                        headlight.enable_blinking()
                            
                    elif key_lower == 'a' or key == readchar.key.LEFT:
                        # Turn left always allowed to maneuver away from danger
                        # Continuous monitor will stop if turning into new danger
                        px.tank_turn('left', speed)
                        current_movement = "TANK_LEFT"
                        display.direction = "TANK LEFT ↺"
                        audio.disable_beeping()
                        headlight.disable_blinking()
                            
                    elif key_lower == 'd' or key == readchar.key.RIGHT:
                        # Turn right always allowed to maneuver away from danger
                        # Continuous monitor will stop if turning into new danger
                        px.tank_turn('right', speed)
                        current_movement = "TANK_RIGHT"
                        display.direction = "TANK RIGHT ↻"
                        audio.disable_beeping()
                        headlight.disable_blinking()
                            
                    elif key == ' ' or key_lower == 'f':
                        px.stop()
                        current_movement = "STOPPED"
                        display.direction = "STOPPED"
                        audio.disable_beeping()
                        headlight.disable_blinking()
                
                # CONTINUOUS SAFETY OVERRIDE - Stop if danger detected while moving
                if not manual_override and current_movement != "STOPPED":
                    should_stop = False
                    stop_reason = ""
                    
                    if current_movement == "FORWARD" and not safety.is_safe_forward():
                        should_stop = True
                        stop_reason = "SAFETY STOP - Obstacle"
                    elif current_movement == "BACKWARD" and not safety.is_safe_backward():
                        should_stop = True
                        stop_reason = "SAFETY STOP - Cliff"
                    elif current_movement in ["TANK_LEFT", "TANK_RIGHT"] and not safety.is_safe_turn():
                        should_stop = True
                        stop_reason = "SAFETY STOP - Cliff"
                    
                    if should_stop:
                        px.stop()
                        current_movement = "STOPPED"
                        display.direction = stop_reason
                        audio.disable_beeping()
                        headlight.disable_blinking()
                
                # Update LED based on safety status
                if not manual_override:
                    if safety.cliff_detected or safety.obstacle_detected:
                        led.set_color("#FF0000")  # Red for danger
                    else:
                        # Breathing rainbow animation for safe mode
                        elapsed = time.time() - animation_start_time
                        led.set_color(get_breathing_color(elapsed))
                else:
                    led.set_color("#FFFF00")  # Yellow for manual override
                
                # Update display data
                display.speed = speed
                display.distance = safety.distance
                display.grayscale = safety.grayscale
                display.safety_status = safety.get_status_text()
                display.manual_override = manual_override
                display.cam_pan = cam_pan_angle
                display.cam_tilt = cam_tilt_angle
                display.update_display()
                
                time.sleep(0.05)  # 20 Hz main loop
                
        except KeyboardInterrupt:
            pass
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Cleanup
        print("\n\n🛑 Shutting down...")
        
        try:
            px.stop()
            print("✅ Robot stopped")
        except:
            pass
            
        try:
            safety.stop()
            print("✅ Safety monitor stopped")
        except:
            pass
            
        try:
            audio.stop()
            print("✅ Audio controller stopped")
        except:
            pass
            
        try:
            headlight.stop()
            print("✅ Headlight controller stopped")
        except:
            pass
            
        try:
            keyboard.stop()
            print("✅ Keyboard controller stopped")
        except:
            pass
            
        try:
            led.headlights_off()
            led.off()
            print("✅ LEDs turned off")
        except:
            pass
            
        try:
            Vilib.camera_close()
            print("✅ Camera closed")
        except:
            pass
            
        print("\n👋 Navigation system shutdown complete!")


if __name__ == "__main__":
    main()
