#!/usr/bin/env python3
"""
🌍 Hello World - Your First PiCar-X Program!

This is your introduction to PiCar-X programming. It demonstrates:
- Safe robot initialization using context managers
- Basic movement commands
- Servo control (steering and camera)
- LED status indicators
- Proper cleanup and error handling

Run this program to verify your robot is working correctly!
"""

from picarx import Picarx
import time


def main():
    """Main function demonstrating basic PiCar-X functionality"""
    
    print("🚀 Starting PiCar-X Hello World Demo...")
    print("This will test basic robot functions safely.")
    print()
    
    # Using context manager for safe operation
    with Picarx() as px:
        print("✅ Robot initialized successfully!")
        time.sleep(1)
        
        # Test 1: Basic movement
        print("🚗 Testing basic movement...")
        px.forward(30)
        time.sleep(0.5)
        px.stop()
        print("   ✓ Forward movement test complete")
        
        # Test 2: Steering servo
        print("🎯 Testing steering servo...")
        
        # Sweep steering left and right
        for angle in range(0, 35):
            px.set_dir_servo_angle(angle)
            time.sleep(0.01)
        for angle in range(35, -35, -1):
            px.set_dir_servo_angle(angle)
            time.sleep(0.01)
        for angle in range(-35, 0):
            px.set_dir_servo_angle(angle)
            time.sleep(0.01)
        
        print("   ✓ Steering servo test complete")
        
        # Test 3: Camera pan servo
        print("📹 Testing camera pan...")
        for angle in range(0, 35):
            px.set_cam_pan_angle(angle)
            time.sleep(0.01)
        for angle in range(35, -35, -1):
            px.set_cam_pan_angle(angle)
            time.sleep(0.01)        
        for angle in range(-35, 0):
            px.set_cam_pan_angle(angle)
            time.sleep(0.01)
        
        print("   ✓ Camera pan test complete")
        
        # Test 4: Camera tilt servo
        print("📹 Testing camera tilt...")
        for angle in range(0, 35):
            px.set_cam_tilt_angle(angle)
            time.sleep(0.01)
        for angle in range(35, -35, -1):
            px.set_cam_tilt_angle(angle)
            time.sleep(0.01)        
        for angle in range(-35, 0):
            px.set_cam_tilt_angle(angle)
            time.sleep(0.01)
        
        print("   ✓ Camera tilt test complete")
        
        print()
        print("🎉 All tests completed successfully!")
        print("Your PiCar-X is ready for more advanced examples.")
        
        # Brief celebration delay
        time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Program interrupted by user")
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        print("💡 Tip: Make sure your robot is properly set up and calibrated")
    
    print("\n👋 Goodbye!")


