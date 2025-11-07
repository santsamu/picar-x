#!/usr/bin/env python3
"""
Tank Turn Angle Test - Test the calibrated angle-based tank turns
"""

from picarx import Picarx
import time

def test_angle_turns():
    """Test various angle turns using calibration"""
    px = Picarx()
    
    try:
        print("Testing calibrated angle-based tank turns...")
        print("Make sure you have calibrated the tank turn first!")
        
        # Test 90° turns
        angles = [90, -90, 180, -180, 45, -45]
        
        for angle in angles:
            print(f"\nTurning {angle}° at speed 50...")
            px.tank_turn_angle(angle, 50)
            time.sleep(2)  # Pause between turns
        
        print("\nAngle turn tests completed!")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        px.stop()

def test_manual_vs_auto():
    """Compare manual timing vs automatic angle-based timing"""
    px = Picarx()
    
    try:
        print("\n=== Manual vs Auto Timing Test ===")
        
        # Manual 90° turn
        print("Manual 90° turn (you time it)...")
        input("Press ENTER to start manual turn")
        px.tank_turn('right', 50)
        input("Press ENTER when you think it's 90°")
        px.stop()
        
        time.sleep(2)
        
        # Automatic 90° turn
        print("Automatic 90° turn (using calibration)...")
        input("Press ENTER to start automatic turn")
        px.tank_turn_angle(90, 50)
        print("Automatic turn complete!")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        px.stop()

if __name__ == "__main__":
    choice = input("Choose test:\n1. Angle turns test\n2. Manual vs Auto comparison\nEnter choice (1/2): ")
    
    if choice == "1":
        test_angle_turns()
    elif choice == "2":
        test_manual_vs_auto()
    else:
        print("Invalid choice")