#!/usr/bin/env python3
"""
Tank Turn Function Test for PiCar-X

This test demonstrates and validates the tank_turn() functionality.
Run with: sudo python3 test_tank_turn.py

Test scenarios:
1. Basic left/right tank turns with string parameters
2. Tank turns with numeric direction parameters
3. Different speed levels
4. Error handling for invalid parameters
5. Interactive demo mode
"""

import sys
import os
import time

# Add parent directory to path to import picarx
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from picarx import Picarx

def test_basic_tank_turns():
    """Test basic tank turn functionality"""
    print("=== Testing Basic Tank Turns ===")
    
    px = Picarx()
    
    try:
        # Test left turn with string parameter
        print("Testing left tank turn (string parameter)...")
        px.tank_turn('left', 50)
        time.sleep(1.0)
        px.stop()
        time.sleep(0.5)
        
        # Test right turn with string parameter
        print("Testing right tank turn (string parameter)...")
        px.tank_turn('right', 50)
        time.sleep(1.0)
        px.stop()
        time.sleep(0.5)
        
        print("✓ Basic tank turns completed successfully")
        
    except Exception as e:
        print(f"✗ Basic tank turn test failed: {e}")
    finally:
        px.stop()

def test_numeric_directions():
    """Test tank turns with numeric direction parameters"""
    print("\n=== Testing Numeric Direction Parameters ===")
    
    px = Picarx()
    
    try:
        # Test left turn with numeric parameter (-1)
        print("Testing left tank turn (numeric: -1)...")
        px.tank_turn(-1, 40)
        time.sleep(0.8)
        px.stop()
        time.sleep(0.5)
        
        # Test right turn with numeric parameter (1)
        print("Testing right tank turn (numeric: 1)...")
        px.tank_turn(1, 40)
        time.sleep(0.8)
        px.stop()
        time.sleep(0.5)
        
        print("✓ Numeric direction tests completed successfully")
        
    except Exception as e:
        print(f"✗ Numeric direction test failed: {e}")
    finally:
        px.stop()

def test_speed_variations():
    """Test tank turns at different speeds"""
    print("\n=== Testing Speed Variations ===")
    
    px = Picarx()
    
    try:
        speeds = [20, 50, 80]
        
        for speed in speeds:
            print(f"Testing tank turn at speed {speed}...")
            
            # Left turn at current speed
            px.tank_turn('left', speed)
            time.sleep(0.6)
            px.stop()
            time.sleep(0.3)
            
            # Right turn at current speed
            px.tank_turn('right', speed)
            time.sleep(0.6)
            px.stop()
            time.sleep(0.3)
        
        print("✓ Speed variation tests completed successfully")
        
    except Exception as e:
        print(f"✗ Speed variation test failed: {e}")
    finally:
        px.stop()

def test_error_handling():
    """Test error handling for invalid parameters"""
    print("\n=== Testing Error Handling ===")
    
    px = Picarx()
    
    try:
        # Test invalid direction
        try:
            px.tank_turn('invalid', 50)
            print("✗ Should have raised ValueError for invalid direction")
        except ValueError:
            print("✓ Correctly raised ValueError for invalid direction")
        
        # Test speed constraint (should be automatically constrained)
        try:
            px.tank_turn('left', 150)  # Over 100
            print("✓ Speed constraint handled (no error expected)")
            px.stop()
        except Exception as e:
            print(f"✗ Unexpected error with speed constraint: {e}")
        
        # Test negative speed (should be constrained to 0)
        try:
            px.tank_turn('right', -10)  # Negative speed
            print("✓ Negative speed constraint handled")
            px.stop()
        except Exception as e:
            print(f"✗ Unexpected error with negative speed: {e}")
        
        print("✓ Error handling tests completed")
        
    except Exception as e:
        print(f"✗ Error handling test failed: {e}")
    finally:
        px.stop()

def interactive_demo():
    """Interactive demo for manual testing"""
    print("\n=== Interactive Tank Turn Demo ===")
    print("Controls:")
    print("  a - Tank turn left")
    print("  d - Tank turn right")
    print("  w - Increase speed")
    print("  s - Decrease speed")
    print("  q - Quit demo")
    print("  Any other key - Stop")
    
    px = Picarx()
    speed = 50
    
    try:
        import readchar
        
        while True:
            print(f"\nCurrent speed: {speed}")
            print("Press a key (a/d/w/s/q): ", end='', flush=True)
            
            key = readchar.readkey().lower()
            print(key)
            
            if key == 'q':
                print("Exiting demo...")
                break
            elif key == 'a':
                print(f"Tank turning left at speed {speed}")
                px.tank_turn('left', speed)
            elif key == 'd':
                print(f"Tank turning right at speed {speed}")
                px.tank_turn('right', speed)
            elif key == 'w':
                speed = min(100, speed + 10)
                print(f"Speed increased to {speed}")
                px.stop()
            elif key == 's':
                speed = max(10, speed - 10)
                print(f"Speed decreased to {speed}")
                px.stop()
            else:
                print("Stopping...")
                px.stop()
            
            time.sleep(0.1)
            
    except ImportError:
        print("readchar not available - skipping interactive demo")
        print("Install with: pip install readchar")
    except KeyboardInterrupt:
        print("\nDemo interrupted")
    finally:
        px.stop()

def spinning_demo():
    """Demo showing continuous spinning patterns"""
    print("\n=== Spinning Pattern Demo ===")
    
    px = Picarx()
    
    try:
        print("360° left rotation (4 x 90° turns)...")
        for i in range(4):
            print(f"  Turn {i+1}/4")
            px.tank_turn('left', 60)
            time.sleep(0.7)  # Adjust timing for ~90° turns
            px.stop()
            time.sleep(0.3)
        
        time.sleep(1)
        
        print("360° right rotation (4 x 90° turns)...")
        for i in range(4):
            print(f"  Turn {i+1}/4")
            px.tank_turn('right', 60)
            time.sleep(0.7)  # Adjust timing for ~90° turns
            px.stop()
            time.sleep(0.3)
        
        print("✓ Spinning demo completed")
        
    except Exception as e:
        print(f"✗ Spinning demo failed: {e}")
    finally:
        px.stop()

def main():
    """Main test runner"""
    print("PiCar-X Tank Turn Function Test")
    print("=" * 40)
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode == 'basic':
            test_basic_tank_turns()
        elif mode == 'numeric':
            test_numeric_directions()
        elif mode == 'speed':
            test_speed_variations()
        elif mode == 'error':
            test_error_handling()
        elif mode == 'interactive':
            interactive_demo()
        elif mode == 'spin':
            spinning_demo()
        else:
            print(f"Unknown test mode: {mode}")
            print("Available modes: basic, numeric, speed, error, interactive, spin")
    else:
        # Run all automated tests
        test_basic_tank_turns()
        test_numeric_directions()
        test_speed_variations()
        test_error_handling()
        spinning_demo()
        
        print("\n" + "=" * 40)
        print("All automated tests completed!")
        print("Run 'sudo python3 test_tank_turn.py interactive' for manual testing")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"\nTest failed with error: {e}")
    finally:
        # Ensure car is stopped
        try:
            px = Picarx()
            px.stop()
        except:
            pass
        print("Test cleanup completed")