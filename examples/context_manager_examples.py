#!/usr/bin/env python3
"""
Examples demonstrating PiCar-X context manager support for safe resource management.

Context managers ensure that the robot is always safely stopped and reset,
even if exceptions occur during operation.
"""

import sys
import os
import time

# Add the parent directory to the path so we can import picarx
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from picarx import Picarx

def example_basic_context_manager():
    """Basic example of context manager usage."""
    print("=== Basic Context Manager Example ===")
    
    # Robot is automatically stopped and reset when exiting the 'with' block
    with Picarx() as px:
        print("Robot initialized and ready")
        px.forward(30)
        time.sleep(2)
        px.stop()
        print("Forward movement completed")
        
        # Test servo movements
        px.set_cam_pan_angle(45)
        time.sleep(1)
        px.set_cam_pan_angle(-45)
        time.sleep(1)
        print("Camera pan test completed")
    
    print("✓ Robot automatically stopped and reset when exiting context")

def example_exception_handling():
    """Example showing context manager handles exceptions safely."""
    print("\n=== Exception Handling Example ===")
    
    try:
        with Picarx() as px:
            print("Starting robot operations...")
            px.forward(50)
            time.sleep(1)
            
            # Simulate an error condition
            print("Simulating an error...")
            raise ValueError("Simulated error during operation")
            
            # This code won't execute due to the exception
            px.stop()
            print("This won't be printed")
            
    except ValueError as e:
        print(f"Caught expected error: {e}")
        print("✓ Robot was safely stopped despite the exception")

def example_nested_operations():
    """Example with nested operations and complex movements."""
    print("\n=== Complex Operations Example ===")
    
    with Picarx() as px:
        print("Performing complex movement sequence...")
        
        # Forward movement
        px.forward(40)
        time.sleep(1)
        
        # Tank turn
        px.tank_turn_angle(90, 50)
        time.sleep(0.5)
        
        # More forward movement  
        px.forward(40)
        time.sleep(1)
        
        # Pivot turn
        px.pivot_turn_angle(-90, 50)
        time.sleep(0.5)
        
        # Camera movement sequence
        for angle in [30, -30, 0]:
            px.set_cam_pan_angle(angle)
            time.sleep(0.5)
        
        print("Complex sequence completed")
    
    print("✓ All operations completed safely with automatic cleanup")

def example_traditional_vs_context_manager():
    """Compare traditional approach vs context manager approach."""
    print("\n=== Traditional vs Context Manager Comparison ===")
    
    # Traditional approach (manual cleanup)
    print("Traditional approach:")
    px = Picarx()
    try:
        px.forward(30)
        time.sleep(1)
        print("Operations completed")
    finally:
        px.stop()
        px.reset()
        print("Manual cleanup completed")
    
    print("\nContext manager approach:")
    # Context manager approach (automatic cleanup)
    with Picarx() as px:
        px.forward(30) 
        time.sleep(1)
        print("Operations completed")
    print("✓ Automatic cleanup completed")

def example_multiple_robots():
    """Example using multiple robot instances safely."""
    print("\n=== Multiple Robot Instances Example ===")
    
    # Note: This is theoretical - you'd need multiple physical robots
    # But shows how context managers scale
    
    configs = [
        {'name': 'Robot 1', 'config': '/opt/picar-x/picar-x.conf'},
        # {'name': 'Robot 2', 'config': '/opt/picar-x/picar-x-2.conf'},  # If you had multiple
    ]
    
    for robot_config in configs:
        print(f"Operating {robot_config['name']}...")
        
        with Picarx(config=robot_config['config']) as px:
            px.forward(30)
            time.sleep(0.5)
            px.tank_turn_angle(45)
            print(f"{robot_config['name']} operations completed")
        
        print(f"✓ {robot_config['name']} safely cleaned up")

def main():
    """Run all context manager examples."""
    print("PiCar-X Context Manager Examples")
    print("=" * 50)
    
    try:
        example_basic_context_manager()
        example_exception_handling()
        example_nested_operations()
        example_traditional_vs_context_manager()
        example_multiple_robots()
        
        print("\n" + "=" * 50)
        print("✅ All context manager examples completed successfully!")
        print("Key benefits demonstrated:")
        print("  • Automatic resource cleanup")
        print("  • Exception safety")
        print("  • Cleaner, more readable code")
        print("  • Guaranteed robot safety")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Examples interrupted by user")
        print("Context managers would have ensured safe cleanup!")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        print("In real usage, context managers would handle cleanup")

if __name__ == "__main__":
    main()