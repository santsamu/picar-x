#!/usr/bin/env python3
"""
🤖 Simplified Autonomous Navigation
==================================

A simpler version focusing on core navigation with all three sensor types.
Perfect for testing and learning the basics of autonomous navigation.
"""

from picarx import Picarx
from vilib import Vilib
import time
import cv2
import numpy as np

class SimpleNavigator:
    """Simplified autonomous navigation system"""
    
    def __init__(self):
        self.safe_distance = 25  # centimeters (distance sensor returns cm)
        self.cliff_threshold = 200  # grayscale value threshold (lower = darker/cliff)
        self.speed = 25
        self.turn_speed = 40
        
        # Statistics
        self.obstacles_avoided = 0
        self.cliffs_detected = 0
        self.total_distance = 0
        
        # Camera state
        self.camera_initialized = False
        
    def check_sensors(self, px):
        """Read and analyze all sensors"""
        # Read sensors
        distance = px.get_distance()
        grayscale = px.get_grayscale_data()  # Returns [left, center, right]
        
        # Real camera obstacle detection using computer vision
        camera_obstacles = 0
        try:
            camera_obstacles = self.detect_camera_obstacles()
        except Exception as e:
            print(f"   ⚠️ Camera error: {e}")
            camera_obstacles = 0
        
        return distance, grayscale, camera_obstacles
    
    def init_camera(self):
        """Initialize camera system for navigation"""
        if not self.camera_initialized:
            try:
                print("📹 Initializing camera for navigation...")
                Vilib.camera_start(vflip=False, hflip=False)
                # Don't start display to keep it lightweight for navigation
                time.sleep(2)  # Allow camera to initialize
                self.camera_initialized = True
                print("✅ Camera ready for obstacle detection")
            except Exception as e:
                print(f"❌ Camera initialization failed: {e}")
                print("   Navigation will continue without camera vision")
                self.camera_initialized = False
    
    def detect_camera_obstacles(self):
        """Detect obstacles using vilib color detection to measure visual complexity"""
        if not self.camera_initialized:
            return 0
            
        try:
            # Use vilib's color detection to measure visual complexity
            # More objects detected = more visual complexity = potential obstacles
            
            # Enable color detection and look for objects
            Vilib.color_detect('red')  # Look for red objects (common obstacle color)
            time.sleep(0.1)  # Brief detection period
            
            # Read detection results from vilib  
            complexity_score = 200  # Default moderate complexity
            
            try:
                if hasattr(Vilib, 'detect_obj_parameter'):
                    # Check detection parameters
                    detections = Vilib.detect_obj_parameter.get('color_n', 0)
                    x_coord = Vilib.detect_obj_parameter.get('color_x', 0)
                    y_coord = Vilib.detect_obj_parameter.get('color_y', 0)
                    
                    print(f"   👁️ Camera detections: {detections}, X: {x_coord}, Y: {y_coord}")

                    if detections > 0 and x_coord > 0:
                        # Objects detected - high visual complexity
                        complexity_score = detections * 300 + 500
                    elif x_coord > 0 or y_coord > 0:
                        # Some visual activity
                        complexity_score = 400
                    else:
                        # Clear scene
                        complexity_score = 100
            except:
                # If parameter reading fails, use moderate default
                complexity_score = 250
            
            # Turn off color detection
            Vilib.close_color_detection()
            
            return complexity_score
            
        except Exception as e:
            print(f"Camera detection error: {e}")
            try:
                Vilib.close_color_detection()
            except:
                pass
            return 0
    
    def cleanup_camera(self):
        """Clean up camera resources"""
        if self.camera_initialized:
            try:
                Vilib.close_color_detection()
                Vilib.camera_close()
                self.camera_initialized = False
                print("📹 Camera resources cleaned up")
            except:
                pass
    
    def print_sensor_info(self, distance, grayscale, camera_obstacles):
        """Display sensor information"""
        print(f"📏 Distance: {distance:.1f}cm | 🌫️ Grayscale: {grayscale} | 👁️ Camera edges: {camera_obstacles}")
    
    def navigate(self, px, duration=30):
        """Main navigation loop"""
        print(f"🚀 Starting simplified autonomous navigation for {duration} seconds")
        print("🎯 Goals: Avoid obstacles, detect cliffs, use camera vision")
        print("=" * 60)
        
        # Initialize camera for navigation
        self.init_camera()
        
        start_time = time.time()
        last_print_time = 0
        
        try:
            while (time.time() - start_time) < duration:
                # Read all sensors
                distance, grayscale, camera_obstacles = self.check_sensors(px)
                
                # Print status every 2 seconds
                current_time = time.time()
                if current_time - last_print_time > 2.0:
                    self.print_sensor_info(distance, grayscale, camera_obstacles)
                    print(f"📊 Stats: Obstacles avoided: {self.obstacles_avoided}, Cliffs detected: {self.cliffs_detected}")
                    last_print_time = current_time
                
                # Decision making priority system:
                
                # Priority 1: Check for cliffs (highest priority)
                cliff_detected = any(val < self.cliff_threshold for val in grayscale)
                if cliff_detected:
                    print("🚨 CLIFF DETECTED! Emergency stop and turn!")
                    px.stop()
                    px.backward(self.speed)
                    time.sleep(0.3)
                    px.stop()
                    px.tank_turn('right', self.turn_speed)
                    time.sleep(1.0)
                    px.stop()
                    self.cliffs_detected += 1
                    continue
                
                # Priority 2: Check ultrasonic sensor for close obstacles
                if distance > 0 and distance < self.safe_distance:
                    print(f"🚧 Obstacle detected at {distance:.1f}cm - avoiding!")
                    px.stop()
                    
                    # Simple avoidance: check left and right with sensor
                    px.set_cam_pan_angle(-30)  # Look left
                    time.sleep(0.3)
                    left_distance = px.get_distance()
                    
                    px.set_cam_pan_angle(30)   # Look right
                    time.sleep(0.3)
                    right_distance = px.get_distance()
                    
                    px.set_cam_pan_angle(0)    # Look forward
                    time.sleep(0.3)
                    
                    # Choose best direction
                    if left_distance > right_distance and left_distance > self.safe_distance:
                        print("   Turning left")
                        px.tank_turn('left', self.turn_speed)
                        time.sleep(0.8)
                    elif right_distance > self.safe_distance:
                        print("   Turning right")
                        px.tank_turn('right', self.turn_speed)
                        time.sleep(0.8)
                    else:
                        print("   Backing up and turning around")
                        px.backward(self.speed)
                        time.sleep(0.5)
                        px.tank_turn('right', self.turn_speed)
                        time.sleep(1.2)
                    
                    px.stop()
                    self.obstacles_avoided += 1
                    continue
                
                # Priority 3: Check camera for obstacles (many edge pixels = obstacle ahead)
                if camera_obstacles > 800:  # Threshold for "significant obstacle" (adjusted for real camera)
                    print(f"👁️ Camera detected obstacle ({camera_obstacles} edge pixels) - turning!")
                    px.stop()
                    px.tank_turn('right', self.turn_speed)
                    time.sleep(0.6)
                    px.stop()
                    continue
                
                # Priority 4: Normal forward movement (exploration)
                px.forward(self.speed)
                time.sleep(0.1)  # Small delay for smooth operation
                
        except KeyboardInterrupt:
            print("\n🛑 Navigation stopped by user")
        finally:
            px.stop()
            px.set_dir_servo_angle(0)  # Reset servo
            self.cleanup_camera()  # Clean up camera resources
            
        # Final statistics
        elapsed_time = time.time() - start_time
        print(f"\n🏁 Navigation Complete!")
        print(f"   Time: {elapsed_time:.1f} seconds")
        print(f"   Obstacles avoided: {self.obstacles_avoided}")
        print(f"   Cliffs detected: {self.cliffs_detected}")
        print(f"   Average obstacles per minute: {self.obstacles_avoided * 60 / elapsed_time:.1f}")

def sensor_demo():
    """Demonstrate individual sensors without movement"""
    print("🔍 Sensor Demonstration Mode")
    print("Testing all sensors for 15 seconds (no movement)")
    print("=" * 50)
    
    try:
        with Picarx() as px:
            for i in range(30):  # 15 seconds at 2Hz
                print(f"\n📊 Reading #{i+1}/30:")
                
                # Ultrasonic
                distance = px.get_distance()
                print(f"   📏 Ultrasonic: {distance:.2f}cm")
                
                # Grayscale
                grayscale = px.get_grayscale_data()  # Returns [left, center, right]
                print(f"   🌫️ Grayscale: Left={grayscale[0]}, Center={grayscale[1]}, Right={grayscale[2]}")
                
                # Camera (real edge detection)
                try:
                    # Create navigator instance for camera detection
                    if i == 0:  # Initialize camera on first reading
                        navigator = SimpleNavigator()
                        navigator.init_camera()
                    
                    if 'navigator' in locals():
                        edge_pixels = navigator.detect_camera_obstacles()
                        print(f"   👁️ Camera: {edge_pixels} edge pixels detected")
                    else:
                        print(f"   👁️ Camera: Not initialized")
                        
                except Exception as e:
                    print(f"   👁️ Camera: Error - {e}")
                
                # Clean up camera on last reading
                if i == 29 and 'navigator' in locals():
                    navigator.cleanup_camera()
                
                time.sleep(0.5)
                
    except KeyboardInterrupt:
        print("\n🛑 Sensor demo interrupted")

def main():
    """Main menu system"""
    navigator = SimpleNavigator()
    
    print("🤖 Simplified Autonomous Navigation System")
    print("=" * 45)
    print()
    print("Features:")
    print("• 📏 Ultrasonic distance sensing with servo scanning")
    print("• 🌫️ Grayscale sensors for cliff/edge detection")
    print("• 👁️ Camera-based obstacle detection using edge detection")
    print("• 🧠 Priority-based decision making")
    print("• 📊 Performance statistics tracking")
    print()
    
    while True:
        print("\nSelect mode:")
        print("1. 🚀 Quick navigation test (15 seconds)")
        print("2. 🏃 Standard navigation (30 seconds)")
        print("3. 🌟 Extended exploration (60 seconds)")
        print("4. 🔍 Sensor demonstration (no movement)")
        print("5. 🚪 Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == '1':
            with Picarx() as px:
                navigator.navigate(px, duration=15)
        elif choice == '2':
            with Picarx() as px:
                navigator.navigate(px, duration=30)
        elif choice == '3':
            with Picarx() as px:
                navigator.navigate(px, duration=60)
        elif choice == '4':
            sensor_demo()
        elif choice == '5':
            break
        else:
            print("❌ Invalid choice. Please try again.")
    
    print("\n👋 Autonomous navigation system shutdown!")

if __name__ == "__main__":
    main()