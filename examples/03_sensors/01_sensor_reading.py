#!/usr/bin/env python3
"""
📊 Sensor Reading - Understanding Your Robot's Senses

This example teaches you how to read and interpret all the sensors
on your PiCar-X robot. Understanding sensor data is fundamental
to creating intelligent robot behaviors.

Learn to:
- Read ultrasonic distance sensor
- Read grayscale sensors
- Understand sensor ranges and limitations
- Handle sensor errors gracefully
- Display real-time sensor data
"""

from picarx import Picarx
import time


def explain_sensors():
    """Explain the robot's sensor capabilities"""
    print("🤖 PiCar-X Sensor System:")
    print()
    print("📏 Ultrasonic Distance Sensor:")
    print("   • Measures distance to objects (2-300cm)")
    print("   • Used for obstacle detection")
    print("   • Returns -1 on error or out of range")
    print()
    print("⚫⚪ Grayscale Sensors (3 sensors):")
    print("   • Left, Center, Right sensors")
    print("   • Detect light vs dark surfaces")
    print("   • Range: 0-100 (0=dark, 100=bright)")
    print("   • Used for line following and cliff detection")
    print()


def test_distance_sensor():
    """Test the ultrasonic distance sensor"""
    print("📏 Testing Ultrasonic Distance Sensor")
    print("Move objects in front of the robot to see changes")
    print("Press Ctrl+C to stop")
    print()
    
    with Picarx() as px:
        try:
            while True:
                distance = px.get_distance()
                
                if distance < 0:
                    status = "❌ Error/Out of range"
                elif distance < 10:
                    status = "🚨 Very close!"
                elif distance < 30:
                    status = "⚠️ Close"
                elif distance < 100:
                    status = "✅ Moderate distance"
                else:
                    status = "📡 Far away"
                
                print(f"📏 Distance: {distance:6.1f} cm - {status}")
                time.sleep(0.2)
                
        except KeyboardInterrupt:
            print("\n📏 Distance sensor test stopped")


def test_grayscale_sensors():
    """Test the grayscale sensors"""
    print("⚫⚪ Testing Grayscale Sensors")
    print("Place robot on different colored surfaces")
    print("Press Ctrl+C to stop")
    print()
    
    with Picarx() as px:
        try:
            while True:
                left = px.get_grayscale_left()
                center = px.get_grayscale_center()
                right = px.get_grayscale_right()
                
                # Determine surface types
                def classify_surface(value):
                    if value > 80:
                        return "⚪ Very bright"
                    elif value > 60:
                        return "🔆 Bright"
                    elif value > 40:
                        return "🔅 Medium"
                    elif value > 20:
                        return "🔘 Dark"
                    else:
                        return "⚫ Very dark"
                
                left_type = classify_surface(left)
                center_type = classify_surface(center)
                right_type = classify_surface(right)
                
                print(f"⚫⚪ L:{left:5.1f} ({left_type}) | C:{center:5.1f} ({center_type}) | R:{right:5.1f} ({right_type})")
                time.sleep(0.3)
                
        except KeyboardInterrupt:
            print("\n⚫⚪ Grayscale sensor test stopped")


def combined_sensor_display():
    """Display all sensors simultaneously"""
    print("📊 Combined Sensor Display")
    print("Real-time display of all sensor data")
    print("Press Ctrl+C to stop")
    print()
    
    with Picarx() as px:
        try:
            sample_count = 0
            
            while True:
                sample_count += 1
                
                # Read all sensors
                distance = px.get_distance()
                left = px.get_grayscale_left()
                center = px.get_grayscale_center()
                right = px.get_grayscale_right()
                
                # Distance status
                if distance < 0:
                    dist_status = "ERR"
                elif distance < 20:
                    dist_status = "CLOSE"
                elif distance < 50:
                    dist_status = "MED"
                else:
                    dist_status = "FAR"
                
                # Average grayscale
                avg_grayscale = (left + center + right) / 3
                
                # Line detection (simple)
                line_detected = any(sensor < 30 for sensor in [left, center, right])
                line_status = "LINE" if line_detected else "----"
                
                print(f"📊 #{sample_count:4d} | Dist:{distance:6.1f}cm ({dist_status}) | "
                      f"Gray: L{left:4.0f} C{center:4.0f} R{right:4.0f} | Avg:{avg_grayscale:4.0f} | {line_status}")
                
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print(f"\n📊 Collected {sample_count} sensor samples")


def sensor_calibration_helper():
    """Help with sensor calibration"""
    print("🎯 Sensor Calibration Helper")
    print("This helps you understand your sensor environment")
    print()
    
    with Picarx() as px:
        # Distance sensor calibration
        print("📏 Distance Sensor Calibration:")
        print("1. Place a large object 10cm in front of robot")
        input("Press Enter when ready...")
        
        dist_10cm = px.get_distance()
        print(f"   10cm reading: {dist_10cm:.1f}cm")
        
        print("2. Move object to 30cm away")
        input("Press Enter when ready...")
        
        dist_30cm = px.get_distance()
        print(f"   30cm reading: {dist_30cm:.1f}cm")
        
        # Grayscale sensor calibration
        print("\n⚫⚪ Grayscale Sensor Calibration:")
        print("1. Place robot on WHITE surface")
        input("Press Enter when ready...")
        
        white_values = [px.get_grayscale_left(), px.get_grayscale_center(), px.get_grayscale_right()]
        print(f"   White surface: L{white_values[0]:.0f} C{white_values[1]:.0f} R{white_values[2]:.0f}")
        
        print("2. Place robot on BLACK surface (or black tape)")
        input("Press Enter when ready...")
        
        black_values = [px.get_grayscale_left(), px.get_grayscale_center(), px.get_grayscale_right()]
        print(f"   Black surface: L{black_values[0]:.0f} C{black_values[1]:.0f} R{black_values[2]:.0f}")
        
        # Calculate thresholds
        print("\n💡 Recommended Settings:")
        print(f"   Distance sensor accuracy: ±{abs(dist_10cm - 10):.1f}cm at 10cm")
        
        thresholds = [(w + b) / 2 for w, b in zip(white_values, black_values)]
        print(f"   Line detection threshold: ~{sum(thresholds)/3:.0f}")
        print(f"   Individual thresholds: L{thresholds[0]:.0f} C{thresholds[1]:.0f} R{thresholds[2]:.0f}")


def interactive_sensor_explorer():
    """Interactive sensor exploration"""
    print("🔍 Interactive Sensor Explorer")
    print("Get detailed information about current sensor readings")
    print()
    
    with Picarx() as px:
        while True:
            print("\nCurrent sensor readings:")
            
            # Distance
            distance = px.get_distance()
            print(f"📏 Distance: {distance:.1f}cm")
            if distance > 0:
                if distance < 5:
                    print("   → Something very close!")
                elif distance < 20:
                    print("   → Object nearby")
                elif distance < 100:
                    print("   → Clear path")
                else:
                    print("   → Nothing detected nearby")
            else:
                print("   → Sensor error or out of range")
            
            # Grayscale
            left = px.get_grayscale_left()
            center = px.get_grayscale_center()
            right = px.get_grayscale_right()
            
            print(f"⚫⚪ Grayscale: Left={left:.1f}, Center={center:.1f}, Right={right:.1f}")
            
            # Analysis
            if max(left, center, right) - min(left, center, right) > 20:
                print("   → Mixed surface detected")
            elif all(val > 70 for val in [left, center, right]):
                print("   → Very bright/white surface")
            elif all(val < 30 for val in [left, center, right]):
                print("   → Very dark/black surface")
            else:
                print("   → Uniform medium surface")
            
            # Line detection
            if any(val < 30 for val in [left, center, right]):
                if center < 30:
                    print("   🎯 Line detected in CENTER")
                elif left < 30:
                    print("   🎯 Line detected on LEFT")
                elif right < 30:
                    print("   🎯 Line detected on RIGHT")
            
            next_action = input("\nPress Enter for new reading, or 'q' to quit: ").strip().lower()
            if next_action == 'q':
                break


def main():
    """Main function with sensor exploration options"""
    print("📊 PiCar-X Sensor Reading Tutorial")
    print("Learn to read and understand robot sensors")
    print("=" * 50)
    
    explain_sensors()
    
    while True:
        print("\nChoose a sensor test:")
        print("1. 📏 Test distance sensor")
        print("2. ⚫⚪ Test grayscale sensors")
        print("3. 📊 Combined sensor display")
        print("4. 🎯 Sensor calibration helper")
        print("5. 🔍 Interactive sensor explorer")
        print("6. ❓ Explain sensors")
        print("7. 🚪 Exit")
        
        try:
            choice = input("\nEnter choice (1-7): ").strip()
            
            if choice == '1':
                test_distance_sensor()
            elif choice == '2':
                test_grayscale_sensors()
            elif choice == '3':
                combined_sensor_display()
            elif choice == '4':
                sensor_calibration_helper()
            elif choice == '5':
                interactive_sensor_explorer()
            elif choice == '6':
                explain_sensors()
            elif choice == '7':
                print("👋 Happy sensing!")
                break
            else:
                print("⚠️ Invalid choice. Please enter 1-7.")
                
        except KeyboardInterrupt:
            print("\n👋 Sensor tutorial interrupted!")
            break


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Check sensor connections and robot setup")
    
    print("\n📊 Sensor reading tutorial complete!")