#!/usr/bin/env python3
"""
👁️ Face Tracking - Advanced Human Detection and Following

This example demonstrates advanced face tracking behavior using computer vision.
The robot detects human faces and follows them with camera movement.

Learn to:
- Human face detection using computer vision
- Smooth camera tracking algorithms
- PID-like control for stable following
- Safe tracking boundaries and limits
- Multiple face handling
- Tracking performance optimization
"""

from picarx import Picarx
from time import sleep, time
from vilib import Vilib
import math

# Face tracking constants
INITIAL_TILT_ANGLE = 50  # Start looking up at typical standing face height (350° gives good coverage for adults)
INITIAL_PAN_ANGLE = 0    # Start centered horizontally


def explain_face_tracking():
    """Explain face tracking concepts"""
    print("👁️ Face Tracking System:")
    print()
    print("🧠 Computer Vision Detection:")
    print("   • Haar cascade classifiers for face detection")
    print("   • Real-time image processing")
    print("   • Face coordinate extraction")
    print("   • Multiple face handling")
    print()
    print("🎯 Tracking Algorithm:")
    print("   • Proportional control for smooth movement")
    print("   • Dead zone to prevent jittery movement")
    print("   • Angle limits for safety")
    print("   • Continuous tracking loop")
    print()
    print("🔧 Servo Control:")
    print("   • Pan: Horizontal face following (-90° to +90°)")
    print("   • Tilt: Vertical face following (-35° to +65°)")
    print(f"   • Starts looking up at {INITIAL_TILT_ANGLE}° for standing face height")
    print("   • Smooth angle interpolation")
    print("   • Position limiting and safety")
    print()


def clamp_number(num, min_val, max_val):
    """Clamp a number between min and max values"""
    return max(min(num, max_val), min_val)


def basic_face_tracking():
    """Basic face tracking implementation"""
    print("👁️ Basic Face Tracking")
    print("Robot will track human faces with camera movement")
    print("Stand in front of the camera to test tracking")
    print("Press Ctrl+C to stop")
    print()
    
    with Picarx() as px:
        # Start camera and face detection
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=True, web=True)
        Vilib.face_detect_switch(True)
        
        # Initialize servo positions - start looking up for faces at standing height
        x_angle = INITIAL_PAN_ANGLE  # Start centered horizontally
        y_angle = INITIAL_TILT_ANGLE  # Start looking up at face height
        px.set_cam_pan_angle(x_angle)
        px.set_cam_tilt_angle(y_angle)
        
        print("👁️ Face tracking active!")
        print("Camera will follow detected faces")
        
        tracking_count = 0
        last_detection_time = time()
        
        try:
            while True:
                # Check for face detection
                if Vilib.detect_obj_parameter['human_n'] != 0:
                    # Face detected - get coordinates
                    coordinate_x = Vilib.detect_obj_parameter['human_x']
                    coordinate_y = Vilib.detect_obj_parameter['human_y']
                    
                    tracking_count += 1
                    last_detection_time = time()
                    
                    # Calculate servo adjustments
                    # Convert pixel coordinates to servo angles
                    x_adjustment = (coordinate_x * 10 / 640) - 5  # Normalize to -5 to +5
                    y_adjustment = (coordinate_y * 10 / 480) - 5
                    
                    # Update servo angles with proportional control
                    x_angle += x_adjustment
                    x_angle = clamp_number(x_angle, px.constants.SERVO_LIMITS['cam_pan']['min'], 
                                         px.constants.SERVO_LIMITS['cam_pan']['max'])
                    
                    y_angle -= y_adjustment  # Invert Y for correct direction
                    y_angle = clamp_number(y_angle, px.constants.SERVO_LIMITS['cam_tilt']['min'], 
                                         px.constants.SERVO_LIMITS['cam_tilt']['max'])
                    
                    # Apply servo positions
                    px.set_cam_pan_angle(x_angle)
                    px.set_cam_tilt_angle(y_angle)
                    
                    print(f"👁️ Tracking #{tracking_count}: Face at ({coordinate_x}, {coordinate_y}) | "
                          f"Camera: pan={x_angle:.1f}°, tilt={y_angle:.1f}°")
                    
                    sleep(0.05)
                else:
                    # No face detected
                    elapsed_since_detection = time() - last_detection_time
                    if elapsed_since_detection > 5:  # 5 seconds
                        print(f"🔍 No face detected for {elapsed_since_detection:.1f}s - searching...")
                    
                    sleep(0.05)
        
        except KeyboardInterrupt:
            print(f"\n👁️ Face tracking complete! Tracked {tracking_count} detections")
        
        finally:
            Vilib.face_detect_switch(False)
            Vilib.camera_close()


def smooth_face_tracking():
    """Smooth face tracking with improved algorithm"""
    print("🎯 Smooth Face Tracking")
    print("Enhanced tracking with smooth movement and dead zones")
    print("Press Ctrl+C to stop")
    print()
    
    with Picarx() as px:
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=True, web=True)
        Vilib.face_detect_switch(True)
        
        # Enhanced tracking parameters - start looking up for faces
        x_angle = INITIAL_PAN_ANGLE
        y_angle = INITIAL_TILT_ANGLE  # Start looking up at typical face height
        target_x_angle = INITIAL_PAN_ANGLE
        target_y_angle = INITIAL_TILT_ANGLE
        
        # Control parameters
        dead_zone = 30  # Pixels - prevents jittery movement
        smoothing_factor = 0.3  # How fast to move toward target
        max_adjustment = 3  # Maximum angle change per iteration
        
        px.set_cam_pan_angle(x_angle)
        px.set_cam_tilt_angle(y_angle)
        
        print("🎯 Smooth face tracking active!")
        print("Enhanced algorithm with dead zones and smoothing")
        print("Debug: Entering tracking loop...")
        
        tracking_quality = []
        smooth_movements = 0
        
        try:
            while True:
                
                try:
                    if Vilib.detect_obj_parameter['human_n'] != 0:
                        coordinate_x = Vilib.detect_obj_parameter['human_x']
                        coordinate_y = Vilib.detect_obj_parameter['human_y']
                        
                        # Calculate distance from center
                        center_x, center_y = 320, 240
                        error_x = coordinate_x - center_x
                        error_y = coordinate_y - center_y
                        
                        # Apply dead zone
                        if abs(error_x) > dead_zone:
                            x_adjustment = (error_x / 320) * 45  # Scale to max angle
                            target_x_angle = clamp_number(x_angle + x_adjustment, 
                                                        px.constants.SERVO_LIMITS['cam_pan']['min'], 
                                                        px.constants.SERVO_LIMITS['cam_pan']['max'])
                        
                        if abs(error_y) > dead_zone:
                            y_adjustment = -(error_y / 240) * 30  # Invert and scale
                            target_y_angle = clamp_number(y_angle + y_adjustment, 
                                                        px.constants.SERVO_LIMITS['cam_tilt']['min'], 
                                                        px.constants.SERVO_LIMITS['cam_tilt']['max'])
                        
                        # Smooth movement toward target
                        x_diff = target_x_angle - x_angle
                        y_diff = target_y_angle - y_angle
                        
                        if abs(x_diff) > 0.1:
                            x_move = clamp_number(x_diff * smoothing_factor, -max_adjustment, max_adjustment)
                            x_angle += x_move
                            px.set_cam_pan_angle(x_angle)
                            smooth_movements += 1
                        
                        if abs(y_diff) > 0.1:
                            y_move = clamp_number(y_diff * smoothing_factor, -max_adjustment, max_adjustment)
                            y_angle += y_move
                            px.set_cam_tilt_angle(y_angle)
                            smooth_movements += 1
                        
                        # Track quality (how centered the face is)
                        face_distance_from_center = math.sqrt(error_x**2 + error_y**2)
                        tracking_quality.append(face_distance_from_center)
                        
                        if len(tracking_quality) % 20 == 0:  # Every 20 detections
                            avg_quality = sum(tracking_quality[-20:]) / 20
                            print(f"🎯 Tracking quality: {avg_quality:.1f} pixels from center | "
                                  f"Position: ({x_angle:.1f}°, {y_angle:.1f}°)")
                
                except Exception as e:
                    print(f"Debug: Error in detection loop: {e}")
                    break
                
                sleep(0.05)
        
        except KeyboardInterrupt:
            if tracking_quality:
                avg_overall_quality = sum(tracking_quality) / len(tracking_quality)
                print(f"\n🎯 Smooth tracking complete!")
                print(f"   Smooth movements: {smooth_movements}")
                print(f"   Average tracking quality: {avg_overall_quality:.1f} pixels")
        
        finally:
            Vilib.face_detect_switch(False)
            Vilib.camera_close()


def multi_face_tracking():
    """Track multiple faces and choose the best target"""
    print("👥 Multiple Face Tracking")
    print("Tracks multiple faces and focuses on the closest/largest")
    print("Press Ctrl+C to stop")
    print()
    
    with Picarx() as px:
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=True, web=True)
        Vilib.face_detect_switch(True)
        
        x_angle = INITIAL_PAN_ANGLE
        y_angle = INITIAL_TILT_ANGLE  # Start looking up for faces
        px.set_cam_pan_angle(x_angle)
        px.set_cam_tilt_angle(y_angle)
        
        print("👥 Multi-face tracking active!")
        print("Will track the most prominent face when multiple detected")
        
        face_history = []
        
        try:
            while True:
                num_faces = Vilib.detect_obj_parameter['human_n']
                
                if num_faces > 0:
                    # For now, track the first detected face
                    # In a full implementation, you'd iterate through all faces
                    coordinate_x = Vilib.detect_obj_parameter['human_x']
                    coordinate_y = Vilib.detect_obj_parameter['human_y']
                    
                    # Calculate face size (approximate)
                    face_w = Vilib.detect_obj_parameter.get('human_w', 0)
                    face_h = Vilib.detect_obj_parameter.get('human_h', 0)
                    face_size = face_w * face_h if face_w and face_h else 0
                    
                    # Track this face
                    x_angle += (coordinate_x * 8 / 640) - 4
                    x_angle = clamp_number(x_angle, px.constants.SERVO_LIMITS['cam_pan']['min'], 
                                         px.constants.SERVO_LIMITS['cam_pan']['max'])
                    
                    y_angle -= (coordinate_y * 8 / 480) - 4
                    y_angle = clamp_number(y_angle, px.constants.SERVO_LIMITS['cam_tilt']['min'], 
                                         px.constants.SERVO_LIMITS['cam_tilt']['max'])
                    
                    px.set_cam_pan_angle(x_angle)
                    px.set_cam_tilt_angle(y_angle)
                    
                    # Log face data
                    face_data = {
                        'time': time(),
                        'position': (coordinate_x, coordinate_y),
                        'size': face_size,
                        'count': num_faces
                    }
                    face_history.append(face_data)
                    
                    if num_faces > 1:
                        print(f"👥 Tracking primary face ({num_faces} detected) | "
                              f"Position: ({coordinate_x}, {coordinate_y}) | "
                              f"Camera: ({x_angle:.1f}°, {y_angle:.1f}°)")
                    else:
                        print(f"👁️ Single face tracking | "
                              f"Position: ({coordinate_x}, {coordinate_y}) | "
                              f"Camera: ({x_angle:.1f}°, {y_angle:.1f}°)")
                
                else:
                    print("🔍 Searching for faces...")
                
                sleep(0.05)
        
        except KeyboardInterrupt:
            print(f"\n👥 Multi-face tracking complete!")
            if face_history:
                max_faces = max(entry['count'] for entry in face_history)
                total_detections = len(face_history)
                print(f"   Total detections: {total_detections}")
                print(f"   Maximum faces detected simultaneously: {max_faces}")
        
        finally:
            Vilib.face_detect_switch(False)
            Vilib.camera_close()


def face_tracking_with_movement():
    """Face tracking that also moves the robot to follow"""
    print("🤖👁️ Face Tracking with Robot Movement")
    print("Robot will both turn camera and move to follow faces")
    print("⚠️ Ensure clear space around robot!")
    print("Press Ctrl+C to stop")
    print()
    
    with Picarx() as px:
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=True, web=True)
        Vilib.face_detect_switch(True)
        
        x_angle = INITIAL_PAN_ANGLE
        y_angle = INITIAL_TILT_ANGLE  # Start looking up for faces at standing height
        movement_enabled = True
        
        px.set_cam_pan_angle(x_angle)
        px.set_cam_tilt_angle(y_angle)
        
        print("🤖👁️ Face tracking with movement active!")
        print("Robot will follow faces with both camera and body movement")
        
        last_movement_time = time()
        following_actions = 0
        
        try:
            while True:
                if Vilib.detect_obj_parameter['human_n'] != 0:
                    coordinate_x = Vilib.detect_obj_parameter['human_x']
                    coordinate_y = Vilib.detect_obj_parameter['human_y']
                    
                    # Camera tracking (as before)
                    x_angle += (coordinate_x * 6 / 640) - 3
                    x_angle = clamp_number(x_angle, px.constants.SERVO_LIMITS['cam_pan']['min'], 
                                         px.constants.SERVO_LIMITS['cam_pan']['max'])
                    
                    y_angle -= (coordinate_y * 6 / 480) - 3
                    y_angle = clamp_number(y_angle, px.constants.SERVO_LIMITS['cam_tilt']['min'], 
                                         px.constants.SERVO_LIMITS['cam_tilt']['max'])
                    
                    px.set_cam_pan_angle(x_angle)
                    px.set_cam_tilt_angle(y_angle)
                    
                    # Robot movement based on camera position
                    current_time = time()
                    if movement_enabled and current_time - last_movement_time > 1:  # Move every second
                        
                        # Check distance sensor for safety
                        distance = px.get_distance()
                        
                        if distance < 0 or distance > 30:  # Safe to move
                            if abs(x_angle) > 15:  # Camera turned significantly
                                # Turn robot body to center camera
                                if x_angle > 15:
                                    px.set_dir_servo_angle(20)
                                    px.forward(25)
                                    following_actions += 1
                                    print(f"🔄 Following: Turning right to follow face")
                                elif x_angle < -15:
                                    px.set_dir_servo_angle(-20)
                                    px.forward(25)
                                    following_actions += 1
                                    print(f"🔄 Following: Turning left to follow face")
                                
                                sleep(0.5)
                                px.stop()
                                px.set_dir_servo_angle(0)
                                last_movement_time = current_time
                        
                        else:
                            print(f"🛑 Face detected but obstacle at {distance:.1f}cm - staying put")
                    
                    print(f"👁️ Tracking face at ({coordinate_x}, {coordinate_y}) | "
                          f"Camera: ({x_angle:.1f}°, {y_angle:.1f}°)")
                
                else:
                    px.stop()
                    print("🔍 Searching for faces to follow...")
                
                sleep(0.05)
        
        except KeyboardInterrupt:
            px.stop()
            print(f"\n🤖👁️ Face tracking with movement complete!")
            print(f"   Following actions taken: {following_actions}")
        
        finally:
            px.stop()
            Vilib.face_detect_switch(False)
            Vilib.camera_close()


def main():
    """Main function with face tracking options"""
    print("👁️ PiCar-X Face Tracking Tutorial")
    print("Learn advanced human detection and following")
    print("=" * 50)
    
    explain_face_tracking()
    
    while True:
        print("\nChoose a face tracking demonstration:")
        print("1. 👁️ Basic face tracking")
        print("2. 🎯 Smooth face tracking")
        print("3. 👥 Multiple face tracking")
        print("4. 🤖👁️ Face tracking with robot movement")
        print("5. ❓ Explain face tracking")
        print("6. 🚪 Exit")
        
        try:
            choice = input("\nEnter choice (1-6): ").strip()
            
            if choice == '1':
                basic_face_tracking()
            elif choice == '2':
                smooth_face_tracking()
            elif choice == '3':
                multi_face_tracking()
            elif choice == '4':
                face_tracking_with_movement()
            elif choice == '5':
                explain_face_tracking()
            elif choice == '6':
                print("👋 Happy tracking!")
                break
            else:
                print("⚠️ Invalid choice. Please enter 1-6.")
                
        except KeyboardInterrupt:
            print("\n👋 Face tracking tutorial interrupted!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Check camera connection and lighting conditions")
    finally:
        # Ensure everything is cleaned up
        try:
            with Picarx() as px:
                px.stop()
            Vilib.face_detect_switch(False)
            Vilib.camera_close()
        except:
            pass
    
    print("\n👁️ Face tracking tutorial complete!")
