#!/usr/bin/env python3
"""
🔒 Context Manager Example - Safe Robot Programming

This example demonstrates the importance of using context managers
for safe robot operation. Context managers ensure proper cleanup
even if errors occur.

Key concepts:
- Using 'with' statements for automatic resource management
- Difference between safe and unsafe patterns
- Error handling and recovery
- Graceful shutdown procedures
"""

from picarx import Picarx
import time


def unsafe_example():
    """
    ❌ UNSAFE: This pattern can leave robot in bad state if error occurs
    Don't use this pattern in production code!
    """
    print("❌ Running UNSAFE example (for demonstration only)...")
    
    px = Picarx()  # Robot initialized but no automatic cleanup
    
    try:
        px.forward(30)
        time.sleep(1)
        
        # Simulate an error condition
        # If an error occurs here, robot might keep moving!
        # raise Exception("Simulated error!")
        
        px.stop()  # Manual cleanup (might not be reached if error)
        print("   Unsafe example completed (got lucky!)")
        
    except Exception as e:
        print(f"   Error in unsafe code: {e}")
        # Robot might still be moving! Need manual intervention
    
    finally:
        # Manual cleanup in finally block
        try:
            px.stop()
            print("   Manual cleanup completed")
        except:
            pass


def safe_example():
    """
    ✅ SAFE: Using context manager ensures automatic cleanup
    This is the recommended pattern for all robot code!
    """
    print("✅ Running SAFE example with context manager...")
    
    # Context manager automatically handles initialization and cleanup
    with Picarx() as px:
        px.forward(30)
        time.sleep(1)
        
        # Even if error occurs here, context manager ensures cleanup
        # raise Exception("Simulated error!")
        
        px.stop()  # Explicit stop (good practice)
        print("   Safe example completed successfully")
        
        # When exiting 'with' block, automatic cleanup happens:
        # - Motors stopped
        # - Servos reset
        # - Resources released


def demonstrate_error_handling():
    """
    Demonstrate how context managers handle errors gracefully
    """
    print("🛡️ Demonstrating error handling with context manager...")
    
    try:
        with Picarx() as px:
            print("   Starting robot operation...")
            
            px.forward(20)
            time.sleep(0.5)
            
            # Simulate various error conditions
            print("   Simulating error condition...")
            raise ValueError("Something went wrong!")
            
            # This code won't be reached due to error above
            px.stop()
            
    except ValueError as e:
        print(f"   ⚠️ Caught error: {e}")
        print("   ✅ Robot automatically stopped by context manager")
    
    print("   Error handling demonstration complete")


def compare_patterns():
    """
    Compare different programming patterns side by side
    """
    print("\n📊 Comparing Programming Patterns:")
    print("=" * 50)
    
    print("\n1️⃣ Pattern 1: Manual management (risky)")
    print("   px = Picarx()")
    print("   px.forward(50)")
    print("   px.stop()  # Might not be reached if error occurs!")
    
    print("\n2️⃣ Pattern 2: Try/finally (better, but verbose)")
    print("   px = Picarx()")
    print("   try:")
    print("       px.forward(50)")
    print("   finally:")
    print("       px.stop()  # Always executes")
    
    print("\n3️⃣ Pattern 3: Context manager (best practice)")
    print("   with Picarx() as px:")
    print("       px.forward(50)")
    print("       # Automatic cleanup on exit!")
    
    print("\n🏆 Winner: Context manager pattern!")
    print("   ✅ Automatic resource management")
    print("   ✅ Exception safety")
    print("   ✅ Clean, readable code")
    print("   ✅ No resource leaks")


def main():
    """Main demonstration function"""
    print("🔒 PiCar-X Context Manager Tutorial")
    print("Learning safe robot programming patterns")
    print("=" * 50)
    
    # Show the differences between safe and unsafe patterns
    unsafe_example()
    print()
    
    safe_example()
    print()
    
    demonstrate_error_handling()
    print()
    
    compare_patterns()
    
    print("\n✨ Key Takeaways:")
    print("1. Always use 'with Picarx() as px:' for robot control")
    print("2. Context managers provide automatic cleanup")
    print("3. Your robot will be safer and more reliable")
    print("4. Code is cleaner and easier to understand")
    
    print("\n🎓 You're now ready for more advanced examples!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Tutorial interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    
    print("\n👋 Context manager tutorial complete!")