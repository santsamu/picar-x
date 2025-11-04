#!/usr/bin/env python3
"""
🎯 Computer Vision Basics - Visual Processing Introduction

This example introduces computer vision concepts using the PiCar-X camera.
Learn how to process visual information and detect objects.

Learn to:
- Color detection and tracking
- Object detection basics
- Visual coordinate systems
- Image processing fundamentals
- Real-time vision processing
- Creating visual feedback
"""

from vilib import Vilib
from picarx import Picarx
import time
import math


def explain_computer_vision():
    """Explain computer vision concepts"""
    print("🎯 Computer Vision Concepts:")
    print()
    print("👁️ What is Computer Vision?")
    print("   • Teaching computers to 'see' and understand images")
    print("   • Processing visual information like humans do")
    print("   • Detecting objects, colors, shapes, and patterns")
    print("   • Making decisions based on visual input")
    print()
    print("🌈 Color Detection:")
    print("   • HSV color space (Hue, Saturation, Value)")
    print("   • Color ranges and thresholds")
    print("   • Filtering out unwanted colors")
    print("   • Tracking colored objects")
    print()
    print("📐 Coordinate Systems:")
    print("   • Image coordinates (x, y pixels)")
    print("   • Object positions and sizes")
    print("   • Distance estimation")
    print("   • Movement direction calculation")
    print()


def color_detection_demo():
    """Demonstrate basic color detection"""
    print("🌈 Color Detection Demo")
    print("Learn to detect and track colors")
    print()
    
    # Available color detection functions in Vilib
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
    
    print("Available colors to detect:")
    for i, color in enumerate(colors, 1):
        print(f"   {i}. {color.title()}")
    
    try:
        choice = int(input("\nSelect a color to detect (1-6): ")) - 1
        if 0 <= choice < len(colors):
            selected_color = colors[choice]
        else:
            print("Invalid choice, using red as default")
            selected_color = 'red'
    except:
        selected_color = 'red'
    
    print(f"\n🎯 Detecting {selected_color.upper()} objects")
    print("Place a colored object in front of the camera")
    print("Press Ctrl+C to stop")
    print()
    
    try:
        # Start camera
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=True, web=True)
        
        # Enable color detection
        if selected_color == 'red':
            Vilib.color_detect_switch(True)
            Vilib.color_detect('red')
        elif selected_color == 'orange':
            Vilib.color_detect_switch(True)
            Vilib.color_detect('orange')
        elif selected_color == 'yellow':
            Vilib.color_detect_switch(True)
            Vilib.color_detect('yellow')
        elif selected_color == 'green':
            Vilib.color_detect_switch(True)
            Vilib.color_detect('green')
        elif selected_color == 'blue':
            Vilib.color_detect_switch(True)
            Vilib.color_detect('blue')
        elif selected_color == 'purple':
            Vilib.color_detect_switch(True)
            Vilib.color_detect('purple')
        
        print(f"🔍 Color detection active for {selected_color}")
        print("You should see detection markers on the video feed")
        print()
        
        detection_count = 0
        start_time = time.time()
        
        while True:
            # Get detection results
            detected_objects = Vilib.detect_obj_parameter.get('color_n', 0)
            
            if detected_objects > 0:
                detection_count += 1
                # Get object position if available
                obj_x = Vilib.detect_obj_parameter.get('color_x', 'Unknown')
                obj_y = Vilib.detect_obj_parameter.get('color_y', 'Unknown')
                obj_w = Vilib.detect_obj_parameter.get('color_w', 'Unknown')
                obj_h = Vilib.detect_obj_parameter.get('color_h', 'Unknown')
                
                print(f"🎯 Detection #{detection_count}: {detected_objects} {selected_color} object(s)")
                if obj_x != 'Unknown':
                    print(f"   Position: x={obj_x}, y={obj_y}")
                    print(f"   Size: width={obj_w}, height={obj_h}")
                
                    # Calculate object position relative to center
                    center_x, center_y = 320, 240  # Typical camera resolution center
                    if isinstance(obj_x, (int, float)) and isinstance(obj_y, (int, float)):
                        offset_x = obj_x - center_x
                        offset_y = obj_y - center_y
                        
                        direction = ""
                        if abs(offset_x) > 50:
                            direction += "Left" if offset_x < 0 else "Right"
                        if abs(offset_y) > 50:
                            direction += " Up" if offset_y < 0 else " Down"
                        
                        if direction:
                            print(f"   Direction from center: {direction.strip()}")
                        else:
                            print(f"   Direction from center: Centered")
                
                time.sleep(0.5)
            else:
                print(f"\r🔍 Scanning for {selected_color} objects... {time.time() - start_time:.1f}s", end="", flush=True)
                time.sleep(0.1)
        
    except KeyboardInterrupt:
        print(f"\n🌈 Detected {detection_count} {selected_color} objects total")
    except Exception as e:
        print(f"\n❌ Color detection error: {e}")
    finally:
        try:
            Vilib.color_detect_switch(False)
            Vilib.camera_close()
            print("🌈 Color detection stopped")
        except:
            pass


def object_tracking_demo():
    """Demonstrate object tracking with robot movement"""
    print("🎯 Object Tracking Demo")
    print("Robot will track colored objects with camera movement")
    print()
    
    color = input("Enter color to track (red/green/blue) [default: red]: ").strip().lower()
    if color not in ['red', 'green', 'blue']:
        color = 'red'
    
    print(f"\n🤖 Starting {color} object tracking")
    print("Place a colored object in view and watch the camera follow it")
    print("Press Ctrl+C to stop")
    print()
    
    try:
        # Start camera and robot
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=True, web=True)
        
        with Picarx() as px:
            # Enable color detection
            Vilib.color_detect_switch(True)
            Vilib.color_detect(color)
            
            # Center camera initially
            px.set_cam_pan_angle(0)
            px.set_cam_tilt_angle(0)
            current_pan = 0
            current_tilt = 0
            
            print(f"🎯 Tracking {color} objects...")
            print("Camera will automatically follow detected objects")
            
            no_detection_time = 0
            
            while True:
                # Check for object detection
                detected_objects = Vilib.detect_obj_parameter.get('color_n', 0)
                
                if detected_objects > 0:
                    no_detection_time = 0
                    obj_x = Vilib.detect_obj_parameter.get('color_x', 320)
                    obj_y = Vilib.detect_obj_parameter.get('color_y', 240)
                    
                    # Camera center coordinates (typical resolution)
                    center_x, center_y = 320, 240
                    
                    # Calculate offset from center
                    offset_x = obj_x - center_x
                    offset_y = obj_y - center_y
                    
                    # Convert offset to servo adjustments
                    pan_adjustment = -offset_x * 0.1  # Negative for correct direction
                    tilt_adjustment = offset_y * 0.1
                    
                    # Apply limits to prevent excessive movement
                    if abs(offset_x) > 30:  # Dead zone for stability
                        current_pan += pan_adjustment
                        current_pan = max(-45, min(45, current_pan))  # Limit range
                        px.set_cam_pan_angle(current_pan)
                    
                    if abs(offset_y) > 30:  # Dead zone for stability
                        current_tilt += tilt_adjustment
                        current_tilt = max(-30, min(30, current_tilt))  # Limit range
                        px.set_cam_tilt_angle(current_tilt)
                    
                    print(f"🎯 Tracking: Object at ({obj_x}, {obj_y}) | "
                          f"Camera: pan={current_pan:.1f}°, tilt={current_tilt:.1f}°")
                    
                else:
                    no_detection_time += 1
                    if no_detection_time % 10 == 0:  # Print every second
                        print(f"🔍 Searching for {color} objects... {no_detection_time/10:.0f}s")
                    
                    # If no object detected for a while, slowly return to center
                    if no_detection_time > 50:  # 5 seconds
                        if abs(current_pan) > 5:
                            current_pan *= 0.95  # Slowly return to center
                            px.set_cam_pan_angle(current_pan)
                        if abs(current_tilt) > 5:
                            current_tilt *= 0.95
                            px.set_cam_tilt_angle(current_tilt)
                
                time.sleep(0.1)
        
    except KeyboardInterrupt:
        print("\n🎯 Object tracking stopped")
    except Exception as e:
        print(f"\n❌ Tracking error: {e}")
    finally:
        try:
            Vilib.color_detect_switch(False)
            Vilib.camera_close()
            print("🤖 Robot camera reset")
        except:
            pass


def visual_navigation_demo():
    """Demonstrate using vision for navigation"""
    print("🧭 Visual Navigation Demo")
    print("Robot uses vision to navigate and avoid obstacles")
    print()
    
    print("This demo shows basic visual navigation concepts:")
    print("• Object detection for obstacle avoidance")
    print("• Color-based waypoint navigation")
    print("• Visual feedback for movement decisions")
    print()
    
    color_target = input("Enter target color to follow (red/green/blue) [default: green]: ").strip().lower()
    if color_target not in ['red', 'green', 'blue']:
        color_target = 'green'
    
    print(f"\n🤖 Robot will navigate toward {color_target} objects")
    print("Place colored objects to guide the robot")
    print("Robot will stop if objects are too close (obstacle avoidance)")
    print("Press Ctrl+C to stop")
    print()
    
    try:
        # Start camera
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=True, web=True)
        
        with Picarx() as px:
            # Enable color detection
            Vilib.color_detect_switch(True)
            Vilib.color_detect(color_target)
            
            # Center camera
            px.set_cam_pan_angle(0)
            px.set_cam_tilt_angle(0)
            
            print(f"🧭 Visual navigation active for {color_target} targets")
            
            while True:
                # Check distance sensor for obstacles
                distance = px.get_distance()
                
                # Check for target color
                detected_objects = Vilib.detect_obj_parameter.get('color_n', 0)
                
                if distance > 0 and distance < 20:
                    # Obstacle too close - stop
                    px.stop()
                    print(f"🛑 Obstacle detected at {distance:.1f}cm - STOPPING")
                    time.sleep(0.5)
                    
                elif detected_objects > 0:
                    # Target color detected
                    obj_x = Vilib.detect_obj_parameter.get('color_x', 320)
                    obj_w = Vilib.detect_obj_parameter.get('color_w', 0)
                    
                    center_x = 320
                    offset_x = obj_x - center_x
                    
                    print(f"🎯 Target detected at x={obj_x}, width={obj_w}")
                    
                    if obj_w > 100:  # Object is large/close
                        px.stop()
                        print("✅ Reached target!")
                        time.sleep(1)
                    elif abs(offset_x) < 50:  # Target centered
                        px.forward(30)
                        print("⬆️ Moving toward target")
                    elif offset_x < -50:  # Target on left
                        px.set_dir_servo_angle(-10)
                        px.forward(20)
                        print("↗️ Turning toward left target")
                    elif offset_x > 50:  # Target on right
                        px.set_dir_servo_angle(10)
                        px.forward(20)
                        print("↖️ Turning toward right target")
                    
                else:
                    # No target detected - search
                    px.stop()
                    print(f"🔍 Searching for {color_target} targets...")
                
                time.sleep(0.2)
        
    except KeyboardInterrupt:
        print("\n🧭 Visual navigation stopped")
    except Exception as e:
        print(f"\n❌ Navigation error: {e}")
    finally:
        try:
            with Picarx() as px:
                px.stop()
                px.set_dir_servo_angle(0)
            Vilib.color_detect_switch(False)
            Vilib.camera_close()
            print("🤖 Robot stopped and reset")
        except:
            pass


def computer_vision_diagnostics():
    """Test computer vision capabilities"""
    print("🔧 Computer Vision Diagnostics")
    print("Testing vision processing capabilities")
    print()
    
    try:
        # Start camera
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=True, web=True)
        time.sleep(1)
        
        # Test color detection for each color
        colors = ['red', 'green', 'blue']
        
        for color in colors:
            print(f"Testing {color} detection...")
            
            Vilib.color_detect_switch(True)
            Vilib.color_detect(color)
            
            # Test for 3 seconds
            start_time = time.time()
            detections = 0
            
            while time.time() - start_time < 3:
                detected = Vilib.detect_obj_parameter.get('color_n', 0)
                if detected > 0:
                    detections += 1
                time.sleep(0.1)
            
            Vilib.color_detect_switch(False)
            print(f"   {color}: {detections} detections in 3 seconds")
        
        print("\n✅ Computer vision diagnostics complete!")
        
    except Exception as e:
        print(f"❌ Diagnostics error: {e}")
    finally:
        try:
            Vilib.color_detect_switch(False)
            Vilib.camera_close()
        except:
            pass


def main():
    """Main function with computer vision options"""
    print("🎯 PiCar-X Computer Vision Basics")
    print("Learn visual processing and object detection")
    print("=" * 50)
    
    explain_computer_vision()
    
    while True:
        print("\nChoose a computer vision demonstration:")
        print("1. 🌈 Color detection demo")
        print("2. 🎯 Object tracking demo")
        print("3. 🧭 Visual navigation demo")
        print("4. 🔧 Computer vision diagnostics")
        print("5. ❓ Explain computer vision")
        print("6. 🚪 Exit")
        
        try:
            choice = input("\nEnter choice (1-6): ").strip()
            
            if choice == '1':
                color_detection_demo()
            elif choice == '2':
                object_tracking_demo()
            elif choice == '3':
                visual_navigation_demo()
            elif choice == '4':
                computer_vision_diagnostics()
            elif choice == '5':
                explain_computer_vision()
            elif choice == '6':
                print("👋 Happy computing!")
                break
            else:
                print("⚠️ Invalid choice. Please enter 1-6.")
                
        except KeyboardInterrupt:
            print("\n👋 Computer vision tutorial interrupted!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
        
        finally:
            # Always clean up
            try:
                Vilib.color_detect_switch(False)
                Vilib.camera_close()
            except:
                pass


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Check camera connection and Vilib installation")
    finally:
        # Ensure everything is cleaned up
        try:
            Vilib.color_detect_switch(False)
            Vilib.camera_close()
        except:
            pass
    
    print("\n🎯 Computer vision tutorial complete!")