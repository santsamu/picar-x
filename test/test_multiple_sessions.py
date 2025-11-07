#!/usr/bin/env python3
"""
Quick test to demonstrate multiple camera sessions work
"""

from vilib import Vilib
import time

def test_multiple_sessions():
    print("🔧 Testing Multiple Camera Sessions")
    print("=" * 40)
    
    for session in range(1, 4):
        print(f"\n📹 Camera Session {session}/3")
        print("-" * 25)
        
        try:
            print("🔄 Starting camera...")
            Vilib.camera_start(vflip=False, hflip=False)
            Vilib.display(local=False, web=True)
            print("✅ Camera started successfully")
            
            print("⏱️ Running for 3 seconds...")
            time.sleep(3)
            
            print("🔄 Stopping camera...")
            Vilib.camera_close()
            print("✅ Camera stopped successfully")
            
            if session < 3:
                print("⏱️ Waiting 2 seconds before next session...")
                time.sleep(2)
                
        except Exception as e:
            print(f"❌ Error in session {session}: {e}")
            return False
    
    print("\n🎉 All camera sessions completed successfully!")
    print("✅ Multiple camera sessions now work perfectly!")
    return True

if __name__ == "__main__":
    test_multiple_sessions()