#!/usr/bin/env python3
"""
🚧 Obstacle Avoidance - Navigate Around Objects

This example demonstrates basic obstacle avoidance using the ultrasonic distance sensor.
The robot moves forward and turns when it detects obstacles in its path.

Key concepts:
- Ultrasonic distance measurement
- Threshold-based decision making
- Basic avoidance algorithms
- Safety-first navigation

Safety: Always supervise robot operation and ensure adequate space!
"""

from picarx import Picarx
import time

# Configuration constants
POWER = 50           # Movement speed (0-100)
SAFE_DISTANCE = 40   # Distance in cm considered safe
DANGER_DISTANCE = 20 # Distance requiring immediate action
TURN_ANGLE = 30      # Steering angle for avoidance


def explain_algorithm():
    """Explain the obstacle avoidance algorithm"""
    print("🧠 Obstacle Avoidance Algorithm:")
    print(f"   • Safe Distance: > {SAFE_DISTANCE}cm → Move forward")
    print(f"   • Caution Zone: {DANGER_DISTANCE}-{SAFE_DISTANCE}cm → Turn and move")
    print(f"   • Danger Zone: < {DANGER_DISTANCE}cm → Back up and turn")
    print("   • Continuous monitoring for dynamic obstacles")
    print()


def basic_obstacle_avoidance():
    """Basic obstacle avoidance behavior"""
    print("🚧 Starting basic obstacle avoidance...")
    print("Robot will navigate around obstacles autonomously")
    print("Press Ctrl+C to stop")
    print()
    
    explain_algorithm()
    
    with Picarx() as px:
        try:
            while True:
                # Read distance sensor
                distance = px.get_distance()
                
                # Handle sensor errors
                if distance < 0:
                    print("⚠️ Sensor error - stopping briefly")
                    px.stop()
                    time.sleep(0.1)
                    continue
                
                print(f"📏 Distance: {distance:.1f}cm", end=" → ")
                
                # Decision making based on distance
                if distance >= SAFE_DISTANCE:
                    # Safe to move forward
                    print("✅ Safe - Moving forward")
                    px.set_dir_servo_angle(0)  # Straight
                    px.forward(POWER)
                    
                elif distance >= DANGER_DISTANCE:
                    # Caution zone - turn and move
                    print("⚠️ Caution - Turning right")
                    px.set_dir_servo_angle(TURN_ANGLE)
                    px.forward(POWER)
                    time.sleep(0.1)
                    
                else:
                    # Danger zone - back up and turn
                    print("🚨 Danger - Backing up and turning")
                    px.set_dir_servo_angle(-TURN_ANGLE)
                    px.backward(POWER)
                    time.sleep(0.5)
                
                time.sleep(0.1)  # Small delay for stability
                
        except KeyboardInterrupt:
            print("\n🛑 Obstacle avoidance stopped by user")
        
        finally:
            px.stop()
            print("Robot stopped safely")


def interactive_distance_monitor():
    """Interactive distance monitoring without movement"""
    print("📊 Interactive Distance Monitor")
    print("Monitor distance readings without robot movement")
    print("Press Ctrl+C to stop")
    print()
    
    with Picarx() as px:
        try:
            while True:
                distance = px.get_distance()
                
                if distance < 0:
                    status = "❌ Error"
                elif distance >= SAFE_DISTANCE:
                    status = "✅ Safe"
                elif distance >= DANGER_DISTANCE:
                    status = "⚠️ Caution"
                else:
                    status = "🚨 Danger"
                
                print(f"📏 Distance: {distance:6.1f}cm - {status}")
                time.sleep(0.2)
                
        except KeyboardInterrupt:
            print("\n📊 Distance monitoring stopped")


def test_avoidance_responses():
    """Test different avoidance responses"""
    print("🧪 Testing Avoidance Responses")
    print("Robot will demonstrate different behaviors")
    print()
    
    with Picarx() as px:
        # Test 1: Safe movement
        print("Test 1: Forward movement (simulating safe distance)")
        px.set_dir_servo_angle(0)
        px.forward(30)
        time.sleep(1)
        px.stop()
        print("✅ Forward movement test complete")
        time.sleep(1)
        
        # Test 2: Turn movement
        print("Test 2: Turn movement (simulating caution zone)")
        px.set_dir_servo_angle(TURN_ANGLE)
        px.forward(30)
        time.sleep(1)
        px.stop()
        print("✅ Turn movement test complete")
        time.sleep(1)
        
        # Test 3: Backup movement
        print("Test 3: Backup movement (simulating danger zone)")
        px.set_dir_servo_angle(-TURN_ANGLE)
        px.backward(30)
        time.sleep(1)
        px.stop()
        print("✅ Backup movement test complete")
        
        # Return to center
        px.set_dir_servo_angle(0)
        print("🎯 All avoidance response tests complete")


def main():
    """Main function with user choices"""
    print("🚧 PiCar-X Obstacle Avoidance Demo")
    print("Learn autonomous navigation with distance sensors")
    print("=" * 50)
    
    while True:
        print("\nChoose an option:")
        print("1. 🚧 Run obstacle avoidance")
        print("2. 📊 Monitor distance sensor")
        print("3. 🧪 Test avoidance responses")
        print("4. ❓ Show algorithm explanation")
        print("5. 🚪 Exit")
        
        try:
            choice = input("\nEnter choice (1-5): ").strip()
            
            if choice == '1':
                basic_obstacle_avoidance()
            elif choice == '2':
                interactive_distance_monitor()
            elif choice == '3':
                test_avoidance_responses()
            elif choice == '4':
                explain_algorithm()
            elif choice == '5':
                print("👋 Goodbye!")
                break
            else:
                print("⚠️ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Program interrupted. Goodbye!")
            break


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Check robot connections and calibration")
    
    print("\n🔚 Obstacle avoidance demo finished")

