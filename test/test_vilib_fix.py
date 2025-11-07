#!/usr/bin/env python3
"""
Test script to verify vilib camera threading fix
This tests multiple camera start/stop cycles to ensure no threading issues
"""

import time
from vilib import Vilib

def test_camera_cycles():
    """Test multiple camera start/stop cycles"""
    print("🔧 Testing vilib camera threading fix...")
    print("=" * 50)
    
    for cycle in range(1, 4):
        print(f"\n📹 Camera Test Cycle {cycle}/3")
        print("-" * 30)
        
        try:
            print("🔄 Starting camera...")
            Vilib.camera_start(vflip=False, hflip=False)
            Vilib.display(local=False, web=True)
            print("✅ Camera started successfully")
            
            print("⏱️ Running for 2 seconds...")
            time.sleep(2)
            
            print("🔄 Stopping camera...")
            Vilib.camera_close()
            print("✅ Camera stopped successfully")
            
            print("⏱️ Waiting 1 second before next cycle...")
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Error in cycle {cycle}: {e}")
            return False
    
    print("\n🎉 All camera cycles completed successfully!")
    print("✅ vilib threading fix is working correctly")
    return True

if __name__ == "__main__":
    test_camera_cycles()