#!/usr/bin/env python3
"""
Quick demo showing the safety benefits of context manager support.
"""

from picarx import Picarx
import time

def demonstrate_context_manager():
    """Show the difference between traditional and context manager approaches."""
    
    print("=== Context Manager Safety Demo ===\n")
    
    print("❌ Traditional approach (manual cleanup):")
    print("px = Picarx()")
    print("try:")
    print("    px.forward(50)")
    print("    # If error occurs here, cleanup might be missed!")
    print("    time.sleep(1)")
    print("finally:")
    print("    px.stop()      # Manual cleanup required")
    print("    px.reset()     # Easy to forget!")
    
    print("\n✅ Context manager approach (automatic cleanup):")
    print("with Picarx() as px:")
    print("    px.forward(50)")
    print("    # Automatic cleanup happens even if error occurs!")
    print("    time.sleep(1)")
    print("# Robot automatically stopped and reset here!")
    
    print("\n🔒 Safety Benefits:")
    print("• Motors always stop, even on exceptions")
    print("• Servos always reset to safe positions")
    print("• No risk of forgetting cleanup code")
    print("• Hardware resources properly released")
    print("• Code is cleaner and more readable")
    
    print("\n💡 Best Practice:")
    print("Always use 'with Picarx() as px:' for safety!")

if __name__ == "__main__":
    demonstrate_context_manager()