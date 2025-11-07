#!/usr/bin/env python3
"""
Test script for PiCar-X camera pan and tilt servo functionality
Tests basic servo movements, range limits, and interactive control

Run modes:
1. Basic servo test - test full range movement
2. Interactive demo with keyboard controls
3. Range boundary tests
4. Smooth movement patterns
5. Calibration verification
"""

import sys
import os
import time

# Add the parent directory to the path so we can import picarx
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from picarx import Picarx

def test_basic_servo_movements():
    """Test basic camera servo functionality"""
    print("=== Testing Basic Camera Servo Movements ===")
    px = Picarx()
    
    try:
        print("Testing camera pan servo...")
        print("Moving to center (0°)...")
        px.set_cam_pan_angle(0)
        time.sleep(1)
        
        print("Moving to left limit (-90°)...")
        px.set_cam_pan_angle(-90)
        time.sleep(1)
        
        print("Moving to right limit (90°)...")
        px.set_cam_pan_angle(90)
        time.sleep(1)
        
        print("Returning to center...")
        px.set_cam_pan_angle(0)
        time.sleep(1)
        
        print("\nTesting camera tilt servo...")
        print("Moving to center (0°)...")
        px.set_cam_tilt_angle(0)
        time.sleep(1)
        
        print("Moving to down limit (-35°)...")
        px.set_cam_tilt_angle(-35)
        time.sleep(1)
        
        print("Moving to up limit (65°)...")
        px.set_cam_tilt_angle(65)
        time.sleep(1)
        
        print("Returning to center...")
        px.set_cam_tilt_angle(0)
        time.sleep(1)
        
        print("Basic servo test completed!")
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"Error during basic test: {e}")

def test_range_boundaries():
    """Test servo range boundary enforcement"""
    print("=== Testing Range Boundary Enforcement ===")
    px = Picarx()
    
    try:
        print("Testing pan servo boundaries...")
        test_angles = [-120, -90, -45, 0, 45, 90, 120]  # Include out-of-range values
        
        for angle in test_angles:
            print(f"Setting pan angle: {angle}° (valid range: -90° to 90°)")
            px.set_cam_pan_angle(angle)
            time.sleep(0.5)
        
        print("\nTesting tilt servo boundaries...")
        test_angles = [-50, -35, -20, 0, 20, 40, 65, 80]  # Include out-of-range values
        
        for angle in test_angles:
            print(f"Setting tilt angle: {angle}° (valid range: -35° to 65°)")
            px.set_cam_tilt_angle(angle)
            time.sleep(0.5)
        
        # Return to center
        px.set_cam_pan_angle(0)
        px.set_cam_tilt_angle(0)
        
        print("Range boundary test completed!")
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"Error during boundary test: {e}")

def test_smooth_movements():
    """Test smooth servo movement patterns"""
    print("=== Testing Smooth Movement Patterns ===")
    px = Picarx()
    
    try:
        print("Pan servo sweep pattern...")
        for angle in range(-90, 91, 10):
            print(f"Pan angle: {angle}°")
            px.set_cam_pan_angle(angle)
            time.sleep(0.2)
        
        print("\nTilt servo sweep pattern...")
        for angle in range(-35, 66, 5):
            print(f"Tilt angle: {angle}°")
            px.set_cam_tilt_angle(angle)
            time.sleep(0.2)
        
        print("\nFigure-8 pattern (pan and tilt combined)...")
        for i in range(36):  # 360 degrees in 10-degree steps
            angle_rad = i * 10 * 3.14159 / 180
            pan_angle = int(45 * 2 * 3.14159 * angle_rad / (2 * 3.14159))  # Simple sine approximation
            tilt_angle = int(20 * 2 * 3.14159 * (angle_rad * 2) / (2 * 3.14159))  # Double frequency
            
            # Clamp to valid ranges
            pan_angle = max(-90, min(90, pan_angle % 180 - 90))
            tilt_angle = max(-35, min(65, tilt_angle % 100 - 35))
            
            print(f"Figure-8: pan={pan_angle}°, tilt={tilt_angle}°")
            px.set_cam_pan_angle(pan_angle)
            px.set_cam_tilt_angle(tilt_angle)
            time.sleep(0.1)
        
        # Return to center
        px.set_cam_pan_angle(0)
        px.set_cam_tilt_angle(0)
        
        print("Smooth movement test completed!")
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"Error during smooth movement test: {e}")

def interactive_demo():
    """Interactive demo with keyboard controls"""
    print("=== Interactive Camera Control Demo ===")
    print("Controls:")
    print("  w/s - Tilt up/down")
    print("  a/d - Pan left/right")
    print("  c - Center both servos")
    print("  r - Reset to home position")
    print("  i - Show current calibration info")
    print("  q - Quit")
    print("\nPress keys to control the camera...")
    
    px = Picarx()
    current_pan = 0
    current_tilt = 0
    step_size = 15  # degrees per keypress
    
    try:
        import readchar
        
        while True:
            key = readchar.readkey().lower()
            
            if key == 'q':
                break
            elif key == 'w':  # Tilt up
                current_tilt = min(px.CAM_TILT_MAX, current_tilt + step_size)
                print(f"Tilt up: {current_tilt}°")
                px.set_cam_tilt_angle(current_tilt)
            elif key == 's':  # Tilt down
                current_tilt = max(px.CAM_TILT_MIN, current_tilt - step_size)
                print(f"Tilt down: {current_tilt}°")
                px.set_cam_tilt_angle(current_tilt)
            elif key == 'a':  # Pan left
                current_pan = max(px.CAM_PAN_MIN, current_pan - step_size)
                print(f"Pan left: {current_pan}°")
                px.set_cam_pan_angle(current_pan)
            elif key == 'd':  # Pan right
                current_pan = min(px.CAM_PAN_MAX, current_pan + step_size)
                print(f"Pan right: {current_pan}°")
                px.set_cam_pan_angle(current_pan)
            elif key == 'c':  # Center
                current_pan = 0
                current_tilt = 0
                print("Centering camera...")
                px.set_cam_pan_angle(current_pan)
                px.set_cam_tilt_angle(current_tilt)
            elif key == 'r':  # Reset to calibrated home
                current_pan = 0
                current_tilt = 0
                print("Resetting to home position...")
                px.set_cam_pan_angle(current_pan)
                px.set_cam_tilt_angle(current_tilt)
            elif key == 'i':  # Show info
                print(f"Current position: Pan={current_pan}°, Tilt={current_tilt}°")
                print(f"Pan range: {px.CAM_PAN_MIN}° to {px.CAM_PAN_MAX}°")
                print(f"Tilt range: {px.CAM_TILT_MIN}° to {px.CAM_TILT_MAX}°")
                print(f"Calibration: Pan={px.cam_pan_cali_val:.2f}, Tilt={px.cam_tilt_cali_val:.2f}")
            else:
                print(f"Unknown key: {key}")
                
    except ImportError:
        print("readchar not available, skipping interactive demo")
        print("Install with: pip3 install readchar")
    except KeyboardInterrupt:
        pass
    finally:
        # Return to center
        px.set_cam_pan_angle(0)
        px.set_cam_tilt_angle(0)
        print("\nDemo ended - camera centered")

def test_calibration_info():
    """Display current calibration information"""
    print("=== Camera Servo Calibration Information ===")
    px = Picarx()
    
    print(f"Pan servo calibration value: {px.cam_pan_cali_val:.2f}°")
    print(f"Tilt servo calibration value: {px.cam_tilt_cali_val:.2f}°")
    print(f"Pan range: {px.CAM_PAN_MIN}° to {px.CAM_PAN_MAX}°")
    print(f"Tilt range: {px.CAM_TILT_MIN}° to {px.CAM_TILT_MAX}°")
    
    # Test center position
    print("\nTesting center position (0°, 0°)...")
    px.set_cam_pan_angle(0)
    px.set_cam_tilt_angle(0)
    time.sleep(1)
    
    print("If the camera is not pointing straight ahead and level,")
    print("you may need to run the calibration helper:")
    print("sudo python3 example/calibration/calibration.py")

def search_pattern():
    """Demonstrate a camera search pattern"""
    print("=== Camera Search Pattern Demo ===")
    px = Picarx()
    
    try:
        print("Executing search pattern...")
        
        # Grid search pattern
        pan_positions = [-60, -30, 0, 30, 60]
        tilt_positions = [-20, 0, 20, 40]
        
        for tilt in tilt_positions:
            for pan in pan_positions:
                print(f"Searching position: pan={pan}°, tilt={tilt}°")
                px.set_cam_pan_angle(pan)
                px.set_cam_tilt_angle(tilt)
                time.sleep(0.8)  # Dwell time for "observation"
        
        # Return to center
        px.set_cam_pan_angle(0)
        px.set_cam_tilt_angle(0)
        
        print("Search pattern completed!")
        
    except KeyboardInterrupt:
        px.set_cam_pan_angle(0)
        px.set_cam_tilt_angle(0)
        print("\nSearch pattern interrupted")

def main():
    """Main test function"""
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    else:
        print("Available test modes:")
        print("1. basic - Test basic servo movements")
        print("2. range - Test range boundary enforcement")
        print("3. smooth - Test smooth movement patterns")
        print("4. demo - Interactive keyboard control")
        print("5. info - Show calibration information")
        print("6. search - Camera search pattern demo")
        print("\nUsage: python3 test_camera_servos.py [mode]")
        print("Or run without arguments for this menu")
        
        mode = input("\nSelect mode (1-6): ").strip()
        
        mode_map = {
            '1': 'basic',
            '2': 'range', 
            '3': 'smooth',
            '4': 'demo',
            '5': 'info',
            '6': 'search'
        }
        mode = mode_map.get(mode, mode)
    
    if mode == 'basic':
        test_basic_servo_movements()
    elif mode == 'range':
        test_range_boundaries()
    elif mode == 'smooth':
        test_smooth_movements()
    elif mode == 'demo':
        interactive_demo()
    elif mode == 'info':
        test_calibration_info()
    elif mode == 'search':
        search_pattern()
    else:
        print(f"Unknown mode: {mode}")
        print("Available modes: basic, range, smooth, demo, info, search")

if __name__ == "__main__":
    main()