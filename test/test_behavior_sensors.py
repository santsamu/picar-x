#!/usr/bin/env python3
"""
Simple test for behavior basics sensor reading
"""

from picarx import Picarx
import time

def test_reactive_behavior():
    print("Testing reactive behavior sensor reading...")
    
    with Picarx() as px:
        print("🤖 Starting sensor test...")
        
        for i in range(3):
            print(f"\nReading {i+1}/3:")
            
            # Get sensor data (the same way as in behavior_basics)
            distance = px.get_distance()
            gray_data = px.get_grayscale_data()
            left_gray = gray_data[0]
            center_gray = gray_data[1] 
            right_gray = gray_data[2]
            
            print(f"Distance: {distance}")
            print(f"Grayscale - Left: {left_gray}, Center: {center_gray}, Right: {right_gray}")
            
            time.sleep(1)
        
        print("✅ Test completed successfully!")

if __name__ == "__main__":
    test_reactive_behavior()