#!/usr/bin/env python3
"""
🚗 Basic Movement - Learn Robot Locomotion

This example teaches fundamental robot movement concepts:
- Forward and backward motion
- Steering control
- Camera positioning
- Safe movement patterns
- Understanding robot coordinate system

This is your foundation for all future movement programming!
"""

from picarx import Picarx
import time


def demonstrate_forward_backward():
    """Show basic forward and backward movement"""
    print("➡️ Testing forward and backward movement...")
    
    with Picarx() as px:
        print("   Moving forward...")
        px.forward(30)  # 30% speed forward
        time.sleep(1.0)
        
        print("   Stopping...")
        px.stop()
        time.sleep(0.5)
        
        print("   Moving backward...")
        px.backward(30)  # 30% speed backward  
        time.sleep(1.0)
        
        print("   Final stop")
        px.stop()
        
        print("   ✅ Forward/backward test complete")


def demonstrate_steering():
    """Show steering servo control"""
    print("🎯 Testing steering control...")
    
    with Picarx() as px:
        print("   Center position (0°)")
        px.set_dir_servo_angle(0)
        time.sleep(1)
        
        print("   Turning right (30°)")
        px.set_dir_servo_angle(30)
        time.sleep(1)
        
        print("   Back to center")
        px.set_dir_servo_angle(0)
        time.sleep(1)
        
        print("   Turning left (-30°)")
        px.set_dir_servo_angle(-30)
        time.sleep(1)
        
        print("   Return to center")
        px.set_dir_servo_angle(0)
        
        print("   ✅ Steering test complete")


def demonstrate_smooth_steering():
    """Show smooth steering transitions"""
    print("🌊 Demonstrating smooth steering...")
    
    with Picarx() as px:
        print("   Smooth sweep from left to right...")
        
        # Smooth sweep from left to right
        for angle in range(-30, 31, 2):  # Step by 2 degrees
            px.set_dir_servo_angle(angle)
            time.sleep(0.05)  # Small delay for smooth motion
        
        print("   Smooth return to center...")
        
        # Smooth return to center
        for angle in range(30, -1, -2):
            px.set_dir_servo_angle(angle)
            time.sleep(0.05)
        
        print("   ✅ Smooth steering complete")


def demonstrate_camera_control():
    """Show camera servo control"""
    print("📹 Testing camera control...")
    
    with Picarx() as px:
        print("   Camera pan (left-right) test...")
        
        # Pan camera left and right
        for angle in range(0, 35, 5):
            px.set_cam_pan_angle(angle)
            time.sleep(0.2)
        
        for angle in range(35, -36, -5):
            px.set_cam_pan_angle(angle)
            time.sleep(0.2)
        
        for angle in range(-35, 1, 5):
            px.set_cam_pan_angle(angle)
            time.sleep(0.2)
        
        print("   Camera tilt (up-down) test...")
        
        # Tilt camera up and down
        for angle in range(0, 31, 5):
            px.set_cam_tilt_angle(angle)
            time.sleep(0.2)
        
        for angle in range(30, -31, -5):
            px.set_cam_tilt_angle(angle)
            time.sleep(0.2)
        
        for angle in range(-30, 1, 5):
            px.set_cam_tilt_angle(angle)
            time.sleep(0.2)
        
        print("   ✅ Camera control test complete")


def demonstrate_combined_movement():
    """Show combined movement and steering"""
    print("🎪 Demonstrating combined movement...")
    print("   (Ensure robot has clear space around it)")
    
    with Picarx() as px:
        print("   Moving forward while steering right...")
        px.set_dir_servo_angle(20)  # Turn right
        px.forward(25)              # Move forward slowly
        time.sleep(1.5)
        px.stop()
        
        print("   Moving forward while steering left...")
        px.set_dir_servo_angle(-20) # Turn left
        px.forward(25)              # Move forward slowly
        time.sleep(1.5)
        px.stop()
        
        print("   Return to center and stop")
        px.set_dir_servo_angle(0)   # Center steering
        
        print("   ✅ Combined movement complete")


def explain_coordinate_system():
    """Explain the robot's coordinate system"""
    print("\n🧭 Robot Coordinate System:")
    print("   Forward/Backward:")
    print("     • forward(speed) - Move forward")
    print("     • backward(speed) - Move backward")
    print("     • stop() - Stop all motors")
    print()
    print("   Steering Angles:")
    print("     • Positive angles (+) = Turn RIGHT")
    print("     • Negative angles (-) = Turn LEFT")
    print("     • Range typically: -30° to +30°")
    print()
    print("   Camera Angles:")
    print("     • Pan: -90° (left) to +90° (right)")
    print("     • Tilt: -30° (down) to +30° (up)")
    print()
    print("   Speed Values:")
    print("     • Range: 0 to 100 (percentage)")
    print("     • Start with low speeds (20-30) for safety")


def main():
    """Main demonstration function"""
    print("🚗 PiCar-X Basic Movement Tutorial")
    print("Learning fundamental robot locomotion")
    print("=" * 45)
    
    # Explain coordinate system first
    explain_coordinate_system()
    
    print("\n🚀 Starting movement demonstrations...")
    print("Ensure your robot has clear space to move!")
    
    try:
        # Wait for user confirmation
        input("Press Enter when ready to start demonstrations...")
        
        # Run demonstrations
        demonstrate_forward_backward()
        time.sleep(1)
        
        demonstrate_steering()
        time.sleep(1)
        
        demonstrate_smooth_steering()
        time.sleep(1)
        
        demonstrate_camera_control()
        time.sleep(1)
        
        demonstrate_combined_movement()
        
        print("\n🎉 All movement demonstrations complete!")
        print("\n📚 What you learned:")
        print("   ✅ Basic forward/backward movement")
        print("   ✅ Steering servo control")  
        print("   ✅ Smooth motion techniques")
        print("   ✅ Camera positioning")
        print("   ✅ Combined movement patterns")
        print("   ✅ Robot coordinate system")
        
        print("\n🎯 Next steps:")
        print("   • Try the speed control example")
        print("   • Learn about turn angles")
        print("   • Create movement patterns")
        
    except KeyboardInterrupt:
        print("\n⚠️ Demonstration interrupted by user")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        print("💡 Check robot connections and calibration")
    
    print("\n👋 Movement tutorial complete!")


