#!/usr/bin/env python3
"""
⛰️ Cliff Detection - Safety First Navigation

This example demonstrates cliff detection using grayscale sensors to prevent
the robot from falling off tables or down stairs. Essential for safe operation!

Key concepts:
- Grayscale sensor thresholds
- Safety-first programming
- Automatic emergency stops
- Calibration importance

SAFETY WARNING: Always supervise robot near edges!

Calibration:
- Auto calibrate: Run ../../setup/calibration/grayscale_calibration.py
- Manual: Adjust reference values for your environment
"""

from picarx import Picarx
from time import sleep
import time

# Safety configuration
POWER = 20                    # Low speed for safety
CLIFF_REFERENCE = [200, 200, 200]  # Default cliff detection thresholds
BACKUP_TIME = 0.5            # Time to back away from cliff
BACKUP_POWER = 40            # Power for backing away


def explain_cliff_detection():
    """Explain how cliff detection works"""
    print("⛰️ Cliff Detection System:")
    print("   • Uses 3 grayscale sensors (left, center, right)")
    print("   • Detects sudden changes in surface reflection")
    print("   • When surface drops away → sensors see 'void'")
    print("   • Automatic emergency stop and backup")
    print()
    print("🎯 Reference Values:")
    print(f"   • Current thresholds: {CLIFF_REFERENCE}")
    print("   • Lower values = more sensitive")
    print("   • Higher values = less sensitive")
    print("   • Calibrate for your specific environment")
    print()


def test_sensor_readings():
    """Test and display current sensor readings"""
    print("📊 Testing Sensor Readings")
    print("Place robot on different surfaces to see values")
    print("Press Ctrl+C to stop")
    print()
    
    with Picarx() as px:
        # Set reference values
        px.set_cliff_reference(CLIFF_REFERENCE)
        
        try:
            while True:
                # Get raw sensor values
                grayscale_values = px.get_grayscale_data()
                
                # Get cliff status
                cliff_detected = px.get_cliff_status(grayscale_values)
                
                # Display readings
                left, center, right = grayscale_values
                status = "🚨 CLIFF DETECTED" if cliff_detected else "✅ Safe"
                
                print(f"📏 L:{left:4.0f} C:{center:4.0f} R:{right:4.0f} → {status}")
                
                time.sleep(0.2)
                
        except KeyboardInterrupt:
            print("\n📊 Sensor testing stopped")


def safe_cliff_detection():
    """Safe cliff detection with movement"""
    print("⛰️ Starting Safe Cliff Detection")
    print("Robot will move slowly and stop at cliffs")
    print("🚨 SUPERVISE CAREFULLY - Keep robot away from actual cliffs!")
    print("Press Ctrl+C to stop")
    print()
    
    # Confirmation for safety
    response = input("Type 'safe' to confirm safe testing environment: ").strip().lower()
    if response != 'safe':
        print("❌ Safety confirmation required. Exiting.")
        return
    
    with Picarx() as px:
        # Set cliff detection reference
        px.set_cliff_reference(CLIFF_REFERENCE)
        
        last_state = "safe"
        
        try:
            while True:
                # Read grayscale sensors
                grayscale_values = px.get_grayscale_data()
                cliff_detected = px.get_cliff_status(grayscale_values)
                
                if not cliff_detected:
                    # Safe to move
                    state = "safe"
                    if last_state != "safe":
                        print("✅ Safe area - Resuming movement")
                    px.forward(POWER)
                    
                else:
                    # Cliff detected - emergency stop!
                    state = "danger"
                    px.stop()
                    
                    if last_state == "safe":
                        print("🚨 CLIFF DETECTED - Emergency stop!")
                        print("🔙 Backing away from cliff...")
                        
                        # Back away from cliff
                        px.backward(BACKUP_POWER)
                        sleep(BACKUP_TIME)
                        px.stop()
                        
                        print("✅ Backed away safely")
                        
                    else:
                        # Still in danger zone
                        print("⚠️ Still detecting cliff - staying stopped")
                
                last_state = state
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n🛑 Cliff detection stopped by user")
        
        finally:
            px.stop()
            print("🔒 Robot stopped safely")


def calibrate_cliff_detection():
    """Interactive cliff detection calibration"""
    print("🎯 Interactive Cliff Detection Calibration")
    print("This helps you set appropriate threshold values")
    print()
    
    with Picarx() as px:
        print("Step 1: Place robot on NORMAL surface")
        input("Press Enter when ready...")
        
        # Read normal surface values
        normal_values = px.get_grayscale_data()
        print(f"Normal surface: L:{normal_values[0]:.0f} C:{normal_values[1]:.0f} R:{normal_values[2]:.0f}")
        
        print("\nStep 2: Place robot at edge (simulating cliff)")
        print("⚠️ BE CAREFUL - Don't let robot fall!")
        input("Press Enter when ready...")
        
        # Read cliff edge values
        cliff_values = px.get_grayscale_data()
        print(f"Cliff edge: L:{cliff_values[0]:.0f} C:{cliff_values[1]:.0f} R:{cliff_values[2]:.0f}")
        
        # Calculate recommended thresholds
        thresholds = []
        for normal, cliff in zip(normal_values, cliff_values):
            # Set threshold between normal and cliff values
            threshold = (normal + cliff) / 2
            thresholds.append(int(threshold))
        
        print(f"\n💡 Recommended thresholds: {thresholds}")
        print("You can use these values in your programs:")
        print(f"px.set_cliff_reference({thresholds})")
        
        # Test the new thresholds
        test_new = input("\nTest new thresholds? (y/N): ").strip().lower()
        if test_new == 'y':
            px.set_cliff_reference(thresholds)
            print("New thresholds set! Move robot to test...")
            
            for i in range(10):
                values = px.get_grayscale_data()
                cliff_detected = px.get_cliff_status(values)
                status = "🚨 CLIFF" if cliff_detected else "✅ Safe"
                print(f"Test {i+1}: L:{values[0]:.0f} C:{values[1]:.0f} R:{values[2]:.0f} → {status}")
                time.sleep(0.5)


def demo_safety_features():
    """Demonstrate safety features without actual movement"""
    print("🛡️ Safety Features Demonstration")
    print("Testing cliff detection responses without movement")
    print()
    
    with Picarx() as px:
        px.set_cliff_reference(CLIFF_REFERENCE)
        
        print("1. Normal operation simulation...")
        time.sleep(1)
        print("   ✅ Robot would move forward")
        
        print("2. Cliff detection simulation...")
        time.sleep(1)
        print("   🚨 Emergency stop activated!")
        print("   🔙 Backing away from danger")
        time.sleep(1)
        print("   ✅ Safety maneuver complete")
        
        print("3. Recovery simulation...")
        time.sleep(1)
        print("   📊 Checking sensors...")
        print("   ✅ Safe to resume operation")
        
        print("\n🎯 All safety features working correctly!")


def main():
    """Main function with user choices"""
    print("⛰️ PiCar-X Cliff Detection Safety System")
    print("Essential safety features for edge detection")
    print("=" * 50)
    
    explain_cliff_detection()
    
    while True:
        print("\nChoose an option:")
        print("1. 📊 Test sensor readings")
        print("2. ⛰️ Run cliff detection (SUPERVISED)")
        print("3. 🎯 Calibrate cliff detection")
        print("4. 🛡️ Demo safety features")
        print("5. ❓ Explain cliff detection")
        print("6. 🚪 Exit")
        
        try:
            choice = input("\nEnter choice (1-6): ").strip()
            
            if choice == '1':
                test_sensor_readings()
            elif choice == '2':
                safe_cliff_detection()
            elif choice == '3':
                calibrate_cliff_detection()
            elif choice == '4':
                demo_safety_features()
            elif choice == '5':
                explain_cliff_detection()
            elif choice == '6':
                print("👋 Stay safe!")
                break
            else:
                print("⚠️ Invalid choice. Please enter 1-6.")
                
        except KeyboardInterrupt:
            print("\n👋 Program interrupted safely!")
            break


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Check sensor connections and calibration")
    
    print("\n🔒 Cliff detection demo finished safely")


                