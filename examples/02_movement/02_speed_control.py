#!/usr/bin/env python3
"""
⚡ Speed Control - Master Robot Velocity

Learn to control robot speed precisely:
- Variable speed control
- Acceleration and deceleration
- Speed ramping techniques
- Timing-based movement
- Performance optimization

Understanding speed control is crucial for smooth robot behavior!
"""

from picarx import Picarx
import time


def demonstrate_speed_levels():
    """Show different speed levels"""
    print("📊 Testing different speed levels...")
    
    speeds = [20, 40, 60, 80, 100]
    
    with Picarx() as px:
        for speed in speeds:
            print(f"   Speed: {speed}% for 1 second")
            
            px.forward(speed)
            time.sleep(1.0)
            px.stop()
            time.sleep(0.5)  # Pause between tests
        
        print("   ✅ Speed level test complete")


def demonstrate_gradual_acceleration():
    """Show smooth acceleration from stop to full speed"""
    print("🚀 Demonstrating gradual acceleration...")
    
    with Picarx() as px:
        print("   Accelerating from 0 to 80% speed...")
        
        # Gradual acceleration
        for speed in range(0, 81, 5):  # 0, 5, 10, 15... 80
            px.forward(speed)
            print(f"      Speed: {speed}%")
            time.sleep(0.2)  # Short delay for smooth acceleration
        
        print("   Maintaining speed for 2 seconds...")
        time.sleep(2.0)
        
        print("   ✅ Acceleration complete")
        px.stop()


def demonstrate_gradual_deceleration():
    """Show smooth deceleration from full speed to stop"""
    print("🛑 Demonstrating gradual deceleration...")
    
    with Picarx() as px:
        print("   Starting at 80% speed...")
        px.forward(80)
        time.sleep(1.0)
        
        print("   Decelerating to stop...")
        
        # Gradual deceleration
        for speed in range(80, -1, -5):  # 80, 75, 70... 0
            px.forward(speed)
            print(f"      Speed: {speed}%")
            time.sleep(0.2)
        
        print("   ✅ Deceleration complete")
        px.stop()


def demonstrate_speed_ramping():
    """Show advanced speed ramping (acceleration + deceleration)"""
    print("🌊 Demonstrating speed ramping...")
    
    with Picarx() as px:
        print("   Ramping up...")
        # Ramp up
        for speed in range(0, 61, 10):
            px.forward(speed)
            time.sleep(0.3)
        
        print("   Constant speed...")
        # Maintain speed
        px.forward(60)
        time.sleep(2.0)
        
        print("   Ramping down...")
        # Ramp down
        for speed in range(60, -1, -10):
            px.forward(speed)
            time.sleep(0.3)
        
        print("   ✅ Speed ramping complete")
        px.stop()


def demonstrate_precise_timing():
    """Show timing-based movement control"""
    print("⏱️ Demonstrating precise timing control...")
    
    with Picarx() as px:
        movements = [
            ("Forward 30%", 30, 1.0),
            ("Forward 50%", 50, 0.5),
            ("Backward 40%", -40, 0.8),
            ("Forward 70%", 70, 0.3)
        ]
        
        for description, speed, duration in movements:
            print(f"   {description} for {duration}s")
            
            if speed > 0:
                px.forward(speed)
            else:
                px.backward(abs(speed))
            
            time.sleep(duration)
            px.stop()
            time.sleep(0.3)  # Brief pause
        
        print("   ✅ Timing control complete")


def demonstrate_variable_movement():
    """Show variable speed with direction changes"""
    print("🔀 Demonstrating variable movement patterns...")
    
    with Picarx() as px:
        print("   Pattern: Fast forward, slow backward, medium forward")
        
        # Fast forward
        print("   Phase 1: Fast forward (80%)")
        px.forward(80)
        time.sleep(0.8)
        px.stop()
        time.sleep(0.2)
        
        # Slow backward
        print("   Phase 2: Slow backward (25%)")
        px.backward(25)
        time.sleep(1.5)
        px.stop()
        time.sleep(0.2)
        
        # Medium forward
        print("   Phase 3: Medium forward (50%)")
        px.forward(50)
        time.sleep(1.0)
        px.stop()
        
        print("   ✅ Variable movement complete")


def interactive_speed_control():
    """Interactive speed control demonstration"""
    print("🎮 Interactive Speed Control")
    print("   Commands:")
    print("     w/s - increase/decrease speed")
    print("     r - reverse direction")
    print("     space - stop")
    print("     q - quit")
    
    with Picarx() as px:
        speed = 0
        direction = 1  # 1 for forward, -1 for backward
        
        print(f"\n   Current: Speed={speed}%, Direction={'Forward' if direction > 0 else 'Backward'}")
        print("   Use keyboard controls (enter after each key):")
        
        try:
            while True:
                command = input("   > ").strip().lower()
                
                if command == 'q':
                    break
                elif command == 'w':
                    speed = min(100, speed + 10)
                elif command == 's':
                    speed = max(0, speed - 10)
                elif command == 'r':
                    direction *= -1
                elif command == ' ' or command == 'space':
                    speed = 0
                    px.stop()
                    print("   STOPPED")
                    continue
                
                # Apply speed and direction
                actual_speed = speed * direction
                if actual_speed > 0:
                    px.forward(actual_speed)
                elif actual_speed < 0:
                    px.backward(abs(actual_speed))
                else:
                    px.stop()
                
                direction_text = 'Forward' if direction > 0 else 'Backward'
                print(f"   Speed={speed}%, Direction={direction_text}")
                
        except KeyboardInterrupt:
            print("\n   Interactive control stopped")
        
        finally:
            px.stop()
        
        print("   ✅ Interactive control complete")


def explain_speed_concepts():
    """Explain speed control concepts"""
    print("\n⚡ Speed Control Concepts:")
    print("   Speed Range:")
    print("     • 0 = stopped")
    print("     • 1-30 = slow, precise control")
    print("     • 31-70 = normal operation")
    print("     • 71-100 = fast (use with caution)")
    print()
    print("   Acceleration Tips:")
    print("     • Start slow and gradually increase")
    print("     • Use small speed increments (5-10)")
    print("     • Add delays for smooth transitions")
    print()
    print("   Timing Control:")
    print("     • time.sleep() for duration-based movement")
    print("     • Sensor feedback for distance-based movement")
    print("     • Emergency stops should be immediate")
    print()
    print("   Best Practices:")
    print("     • Always call stop() after movement")
    print("     • Test with low speeds first")
    print("     • Consider robot's momentum")


def main():
    """Main speed control demonstration"""
    print("⚡ PiCar-X Speed Control Tutorial")
    print("Master precise robot velocity control")
    print("=" * 45)
    
    # Explain concepts first
    explain_speed_concepts()
    
    print("\n🚀 Starting speed demonstrations...")
    print("Ensure robot has adequate space to move!")
    
    try:
        input("Press Enter when ready to start...")
        
        demonstrate_speed_levels()
        time.sleep(1)
        
        demonstrate_gradual_acceleration()
        time.sleep(1)
        
        demonstrate_gradual_deceleration()
        time.sleep(1)
        
        demonstrate_speed_ramping()
        time.sleep(1)
        
        demonstrate_precise_timing()
        time.sleep(1)
        
        demonstrate_variable_movement()
        time.sleep(1)
        
        print("\n🎮 Try interactive control? (y/N): ", end="")
        response = input().strip().lower()
        if response in ['y', 'yes']:
            interactive_speed_control()
        
        print("\n🎉 Speed control tutorial complete!")
        print("\n📚 What you learned:")
        print("   ✅ Variable speed control (0-100%)")
        print("   ✅ Smooth acceleration/deceleration")
        print("   ✅ Speed ramping techniques")
        print("   ✅ Timing-based movement")
        print("   ✅ Interactive speed control")
        
        print("\n🎯 Next steps:")
        print("   • Learn about turn angles")
        print("   • Create movement patterns")
        print("   • Combine with sensor feedback")
        
    except KeyboardInterrupt:
        print("\n⚠️ Tutorial interrupted by user")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error during tutorial: {e}")
        print("💡 Check robot setup and calibration")
    
    print("\n👋 Speed control tutorial finished!")