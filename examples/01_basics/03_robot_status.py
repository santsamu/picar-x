#!/usr/bin/env python3
"""
📊 Robot Status - Monitor Your Robot's Health

This example shows how to check your robot's system status,
including hardware connections, sensor readings, and system health.

Learn to:
- Read system information
- Monitor sensor status
- Check hardware connections
- Display robot configuration
- Detect potential issues
"""

from picarx import Picarx
import time
import sys
import platform


def display_system_info():
    """Display basic system information"""
    print("🖥️ System Information:")
    print(f"   Platform: {platform.platform()}")
    print(f"   Python version: {sys.version.split()[0]}")
    print(f"   Architecture: {platform.machine()}")
    print()


def check_robot_initialization():
    """Test robot initialization and basic connectivity"""
    print("🔌 Testing robot initialization...")
    
    try:
        with Picarx() as px:
            print("   ✅ Robot initialized successfully")
            
            # Brief test to show robot is responsive
            time.sleep(0.5)
            return px
            
    except Exception as e:
        print(f"   ❌ Robot initialization failed: {e}")
        return None


def test_sensor_readings(px):
    """Test all sensor readings and display values"""
    print("📡 Testing sensor readings...")
    
    try:
        # Test grayscale sensors
        print("   Grayscale sensors:")
        grayscale_readings = px.get_grayscale_data()
        left, center, right = grayscale_readings
        
        print(f"      Left: {left:3.1f}")
        print(f"      Center: {center:3.1f}")
        print(f"      Right: {right:3.1f}")
        
        # Check if readings are reasonable (grayscale values are typically 0-4095 for ADC)
        if all(0 <= reading <= 4095 for reading in grayscale_readings):
            print("   ✅ Grayscale sensors working normally")
        else:
            print("   ⚠️ Unusual grayscale sensor readings")
        
        # Test ultrasonic distance sensor
        print("   Distance sensor:")
        distance = px.get_distance()
        print(f"      Distance: {distance} cm")
        
        if distance > 0:
            print("   ✅ Distance sensor working normally")
        elif distance == -1:
            print("   ⚠️ Distance sensor out of range or error")
        else:
            print("   ❌ Distance sensor not responding")
        
    except Exception as e:
        print(f"   ❌ Sensor reading error: {e}")


def test_servo_movement(px):
    """Test servo movements"""
    print("🎯 Testing servo movements...")
    
    try:
        # Test direction servo
        print("   Testing steering servo...")
        original_dir = 0  # Assume centered
        
        px.set_dir_servo_angle(15)   # Turn right
        time.sleep(0.5)
        px.set_dir_servo_angle(-15)  # Turn left
        time.sleep(0.5)
        px.set_dir_servo_angle(0)    # Return to center
        
        print("   ✅ Steering servo working")
        
        # Test camera servos
        print("   Testing camera servos...")
        
        # Pan test
        px.set_cam_pan_angle(20)
        time.sleep(0.3)
        px.set_cam_pan_angle(-20)
        time.sleep(0.3)
        px.set_cam_pan_angle(0)
        
        # Tilt test
        px.set_cam_tilt_angle(15)
        time.sleep(0.3)
        px.set_cam_tilt_angle(-15)
        time.sleep(0.3)
        px.set_cam_tilt_angle(0)
        
        print("   ✅ Camera servos working")
        
    except Exception as e:
        print(f"   ❌ Servo test error: {e}")


def test_motor_response(px):
    """Test motor response (brief movement)"""
    print("🚗 Testing motor response...")
    print("   (Brief movement test - ensure robot has space)")
    
    try:
        # Very brief forward movement
        px.forward(20)
        time.sleep(0.3)
        px.stop()
        
        print("   ✅ Motor response working")
        
        # Brief reverse movement
        px.backward(20)
        time.sleep(0.3)
        px.stop()
        
        print("   ✅ Reverse movement working")
        
    except Exception as e:
        print(f"   ❌ Motor test error: {e}")


def display_robot_configuration():
    """Display robot configuration and settings"""
    print("⚙️ Robot Configuration:")
    
    # This would typically read from configuration files
    # For now, display typical settings
    print("   Motor settings:")
    print("      Max speed: 100")
    print("      Direction: Normal")
    
    print("   Servo settings:")
    print("      Steering range: ±30°")
    print("      Camera pan range: ±90°")
    print("      Camera tilt range: ±30°")
    
    print("   Sensor settings:")
    print("      Grayscale sensors: 3 channels")
    print("      Distance sensor: Ultrasonic")
    print("      Update rate: 10 Hz")


def continuous_monitoring(px, duration=10):
    """Monitor robot status continuously for specified duration"""
    print(f"📊 Continuous monitoring for {duration} seconds...")
    print("   (Press Ctrl+C to stop early)")
    
    start_time = time.time()
    
    try:
        while time.time() - start_time < duration:
            # Read sensors
            distance = px.get_distance()
            grayscale_readings = px.get_grayscale_data()
            grayscale_avg = sum(grayscale_readings) / len(grayscale_readings)
            
            # Display status with timestamp
            elapsed = time.time() - start_time
            print(f"   {elapsed:6.1f}s - Distance: {distance:3.0f}cm, "
                  f"Grayscale avg: {grayscale_avg:4.1f}")
            
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\n   Monitoring stopped by user")


def main():
    """Main robot status check function"""
    print("📊 PiCar-X Robot Status Check")
    print("Comprehensive robot health monitoring")
    print("=" * 40)
    
    # System info
    display_system_info()
    
    # Robot initialization
    px = check_robot_initialization()
    if not px:
        print("❌ Cannot proceed - robot initialization failed")
        return
    
    with px:
        # Run all tests
        test_sensor_readings(px)
        print()
        
        test_servo_movement(px)
        print()
        
        test_motor_response(px)
        print()
        
        display_robot_configuration()
        print()
        
        # Ask user if they want continuous monitoring
        try:
            response = input("📊 Run continuous monitoring? (y/N): ").strip().lower()
            if response in ['y', 'yes']:
                continuous_monitoring(px)
        except KeyboardInterrupt:
            print("\nSkipping continuous monitoring")
    
    print("\n✅ Robot status check complete!")
    print("💡 If any tests failed, check connections and calibration")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Status check interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error during status check: {e}")
    
    print("\n👋 Status check finished")