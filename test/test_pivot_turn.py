#!/usr/bin/env python3
"""
Test script for PiCar-X pivot turn functionality
Tests basic pivot turn and angle-based pivot turns

Run modes:
1. Interactive demo with keyboard controls
2. Automated angle testing
3. Speed comparison tests
"""

import sys
import os
import time

# Add the parent directory to the path so we can import picarx
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from picarx import Picarx

def test_basic_pivot_turn():
    """Test basic pivot turn functionality"""
    print("=== Testing Basic Pivot Turn ===")
    px = Picarx()
    
    try:
        print("Testing left pivot turn for 2 seconds...")
        px.pivot_turn('left', 50)
        time.sleep(2)
        px.stop()
        time.sleep(1)
        
        print("Testing right pivot turn for 2 seconds...")
        px.pivot_turn('right', 50)
        time.sleep(2)
        px.stop()
        time.sleep(1)
        
        print("Basic pivot turn test completed!")
        
    except KeyboardInterrupt:
        px.stop()
        print("\nTest interrupted by user")
    except Exception as e:
        px.stop()
        print(f"Error during basic test: {e}")

def test_angle_based_pivot_turns():
    """Test angle-based pivot turn functionality"""
    print("=== Testing Angle-Based Pivot Turns ===")
    px = Picarx()
    
    test_angles = [90, -90, 180, -180, 45, -45, 360]
    
    try:
        for angle in test_angles:
            print(f"Testing pivot turn: {angle}° at speed 50...")
            px.pivot_turn_angle(angle, 50)
            time.sleep(1)  # Pause between tests
            
        print("Angle-based pivot turn tests completed!")
        
    except KeyboardInterrupt:
        px.stop()
        print("\nTest interrupted by user")
    except Exception as e:
        px.stop()
        print(f"Error during angle test: {e}")

def test_speed_variations():
    """Test pivot turns at different speeds"""
    print("=== Testing Pivot Turn Speed Variations ===")
    px = Picarx()
    
    speeds = [30, 50, 70, 90]
    angle = 90  # Test 90-degree pivot turns
    
    try:
        for speed in speeds:
            print(f"Testing 90° pivot turn at speed {speed}...")
            px.pivot_turn_angle(angle, speed)
            time.sleep(2)  # Pause between tests
            
        print("Speed variation tests completed!")
        
    except KeyboardInterrupt:
        px.stop()
        print("\nTest interrupted by user")
    except Exception as e:
        px.stop()
        print(f"Error during speed test: {e}")

def interactive_demo():
    """Interactive demo with keyboard controls"""
    print("=== Interactive Pivot Turn Demo ===")
    print("Controls:")
    print("  a/A - Pivot left 45°/90°")
    print("  d/D - Pivot right 45°/90°")
    print("  q - Quit")
    print("\nPress keys to control the car...")
    
    px = Picarx()
    
    try:
        import readchar
        
        while True:
            key = readchar.readkey().lower()
            
            if key == 'q':
                break
            elif key == 'a':
                print("Pivot left 45°")
                px.pivot_turn_angle(-45, 50)
            elif key == 'A':
                print("Pivot left 90°")
                px.pivot_turn_angle(-90, 50)
            elif key == 'd':
                print("Pivot right 45°")
                px.pivot_turn_angle(45, 50)
            elif key == 'D':
                print("Pivot right 90°")
                px.pivot_turn_angle(90, 50)
            else:
                print(f"Unknown key: {key}")
                
    except ImportError:
        print("readchar not available, skipping interactive demo")
        print("Install with: pip3 install readchar")
    except KeyboardInterrupt:
        pass
    finally:
        px.stop()
        print("\nDemo ended")

def calibration_helper():
    """Helper for pivot turn calibration"""
    print("=== Pivot Turn Calibration Helper ===")
    px = Picarx()
    
    print("This will help you calibrate pivot turn timing.")
    print("Make sure you have enough space around the car.")
    
    try:
        input("Position the car and press Enter when ready...")
        
        print("Starting calibration pivot turn...")
        print("The car will start pivoting. Press Enter when it completes 360°")
        
        start_time = time.time()
        px.pivot_turn('right', 50)
        input()  # Wait for user to press Enter
        px.stop()
        
        elapsed_time = time.time() - start_time
        print(f"\nMeasured time for 360° pivot turn: {elapsed_time:.2f} seconds")
        print(f"You can save this value in the calibration: {elapsed_time:.2f}")
        
    except KeyboardInterrupt:
        px.stop()
        print("\nCalibration interrupted")

def main():
    """Main test function"""
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    else:
        print("Available test modes:")
        print("1. basic - Test basic pivot turn functionality")
        print("2. angles - Test angle-based pivot turns")
        print("3. speeds - Test different speeds")
        print("4. demo - Interactive demo")
        print("5. calibrate - Calibration helper")
        print("\nUsage: python3 test_pivot_turn.py [mode]")
        print("Or run without arguments for this menu")
        
        mode = input("\nSelect mode (1-5): ").strip()
        
        mode_map = {
            '1': 'basic',
            '2': 'angles', 
            '3': 'speeds',
            '4': 'demo',
            '5': 'calibrate'
        }
        mode = mode_map.get(mode, mode)
    
    if mode == 'basic':
        test_basic_pivot_turn()
    elif mode == 'angles':
        test_angle_based_pivot_turns()
    elif mode == 'speeds':
        test_speed_variations()
    elif mode == 'demo':
        interactive_demo()
    elif mode == 'calibrate':
        calibration_helper()
    else:
        print(f"Unknown mode: {mode}")
        print("Available modes: basic, angles, speeds, demo, calibrate")

if __name__ == "__main__":
    main()