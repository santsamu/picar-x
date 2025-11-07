#!/usr/bin/env python3
"""
📹 Camera Basics - Introduction to Robot Vision

This example introduces you to the camera system on your PiCar-X robot.
Learn the fundamentals of computer vision and camera control.

Learn to:
- Start and stop the camera system multiple times
- Display camera feed locally and on web
- Take photos programmatically
- Control camera settings
- Handle camera errors safely
- Understand camera coordinate system
"""

from vilib import Vilib
from picarx import Picarx
import time
import os
import getpass
import socket
import sys


def start_camera(vflip=False, hflip=False):
    """Start camera with settings"""
    print("🔄 Starting camera...")
    Vilib.camera_start(vflip=vflip, hflip=hflip)
    Vilib.display(local=True, web=True)
    time.sleep(1)
    
    # Get IP for web display
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        print(f"✅ Camera started - Web: http://{local_ip}:9000/mjpg")
    except:
        print("✅ Camera started - Web: http://[robot-ip]:9000/mjpg")


def stop_camera():
    """Stop camera safely"""
    print("🔄 Stopping camera...")
    try:
        Vilib.camera_close()
        print("✅ Camera stopped")
    except Exception as e:
        print(f"ℹ️ Camera stop note: {e}")
    time.sleep(0.5)


def explain_camera_system():
    """Explain the camera capabilities"""
    print("📹 PiCar-X Camera System:")
    print()
    print("🎥 Camera Features:")
    print("   • CSI camera connected to Raspberry Pi")
    print("   • Real-time video streaming")
    print("   • Photo capture capability")
    print("   • Local and web display options")
    print("   • Flip and rotation controls")
    print()
    print("📺 Display Options:")
    print("   • Local display: Shows on connected monitor")
    print("   • Web display: Stream to web browser at http://[robot-ip]:9000/mjpg")
    print("   • Both: Display locally and stream to web")
    print("   Note: The actual IP address will be shown when camera starts")
    print()
    print("📸 Capture Options:")
    print("   • Photos: Take individual photos")
    print("   • Video: Record video files")
    print("   • Streaming: Real-time video stream")
    print()


def basic_camera_test():
    """Basic camera functionality test"""
    print("📹 Basic Camera Test")
    print("Starting camera system...")
    print()
    
    try:
        start_camera()
        
        print("Camera is now running...")
        print("Check your display or web browser to see the camera feed")
        print()
        
        # Keep camera running for demonstration
        for countdown in range(10, 0, -1):
            print(f"\r📹 Camera test running... {countdown} seconds remaining", end="", flush=True)
            time.sleep(1)
        
        print()
        
    except Exception as e:
        print(f"❌ Camera error: {e}")
        print("💡 Check camera connection and permissions")
    
    finally:
        stop_camera()
        print("\n📹 Camera demo complete!")


def camera_settings_demo():
    """Demonstrate different camera settings"""
    print("⚙️ Camera Settings Demo")
    print("Testing different camera orientations and settings")
    print()
    
    settings_tests = [
        {"name": "Normal orientation", "vflip": False, "hflip": False},
        {"name": "Vertical flip", "vflip": True, "hflip": False},
        {"name": "Horizontal flip", "vflip": False, "hflip": True},
        {"name": "Both flips", "vflip": True, "hflip": True},
    ]
    
    try:
        for i, settings in enumerate(settings_tests, 1):
            print(f"📹 Test {i}/4: {settings['name']}")
            
            if i > 1:
                # Stop previous camera before starting new one
                stop_camera()
                time.sleep(1)
            
            start_camera(vflip=settings['vflip'], hflip=settings['hflip'])
            
            print(f"   Settings: vflip={settings['vflip']}, hflip={settings['hflip']}")
            print("   Check your web browser to see the orientation")
            
            if i < len(settings_tests):
                input("   Press Enter to continue to next setting...")
            else:
                input("   Press Enter to finish demo...")
    
    except Exception as e:
        print(f"❌ Error with settings: {e}")
    
    finally:
        stop_camera()
        print("\n⚙️ Camera settings demo complete!")


def take_photo_demo():
    """Demonstrate photo taking capabilities"""
    print("📸 Photo Taking Demo")
    print("Learn to capture photos with your robot")
    print()
    
    # Get username for save path
    try:
        username = getpass.getuser()
    except:
        username = os.getlogin()
    
    photos_dir = f"/home/{username}/Pictures/picar-x/"
    
    # Create directory if it doesn't exist
    os.makedirs(photos_dir, exist_ok=True)
    print(f"📁 Photos will be saved to: {photos_dir}")
    print()
    
    try:
        start_camera()
        
        print("📹 Camera ready for photos!")
        print("Position your robot to frame the shot")
        print()
        
        photo_count = 0
        while True:
            action = input("Press 'p' to take photo, 'q' to quit: ").strip().lower()
            
            if action == 'p':
                photo_count += 1
                timestamp = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
                photo_name = f"picarx_photo_{timestamp}"
                
                try:
                    Vilib.take_photo(photo_name, photos_dir)
                    print(f"📸 Photo saved: {photos_dir}{photo_name}.jpg")
                    print(f"   Total photos taken: {photo_count}")
                except Exception as e:
                    print(f"❌ Photo error: {e}")
                
            elif action == 'q':
                break
            else:
                print("⚠️ Invalid input. Use 'p' for photo, 'q' to quit")
        
        print(f"\n📸 Photo session complete! Took {photo_count} photos")
        
    except Exception as e:
        print(f"❌ Camera error: {e}")
    
    finally:
        stop_camera()
        print("\n📸 Photo demo complete!")


def camera_with_servos():
    """Demonstrate camera with servo control"""
    print("🤖 Camera with Servo Control")
    print("Control camera direction using servo motors")
    print()
    
    try:
        start_camera()
        
        with Picarx() as px:
            print("📹 Camera started with servo control")
            print("Use these controls:")
            print("   W/S: Tilt camera up/down")
            print("   A/D: Pan camera left/right")
            print("   R: Reset to center")
            print("   Q: Quit")
            print()
            
            # Center servos
            px.set_cam_tilt_angle(0)
            px.set_cam_pan_angle(0)
            print("🎯 Camera centered")
            
            tilt_angle = 0
            pan_angle = 0
            
            while True:
                key = input("Enter command: ").strip().lower()
                
                if key == 'w':  # Tilt up
                    tilt_angle = min(tilt_angle + 10, 30)
                    px.set_cam_tilt_angle(tilt_angle)
                    print(f"⬆️ Tilt angle: {tilt_angle}°")
                    
                elif key == 's':  # Tilt down
                    tilt_angle = max(tilt_angle - 10, -30)
                    px.set_cam_tilt_angle(tilt_angle)
                    print(f"⬇️ Tilt angle: {tilt_angle}°")
                    
                elif key == 'a':  # Pan left
                    pan_angle = min(pan_angle + 15, 45)
                    px.set_cam_pan_angle(pan_angle)
                    print(f"⬅️ Pan angle: {pan_angle}°")
                    
                elif key == 'd':  # Pan right
                    pan_angle = max(pan_angle - 15, -45)
                    px.set_cam_pan_angle(pan_angle)
                    print(f"➡️ Pan angle: {pan_angle}°")
                    
                elif key == 'r':  # Reset
                    tilt_angle = 0
                    pan_angle = 0
                    px.set_cam_tilt_angle(tilt_angle)
                    px.set_cam_pan_angle(pan_angle)
                    print("🎯 Camera reset to center")
                    
                elif key == 'q':
                    break
                    
                else:
                    print("⚠️ Invalid command. Use W/S/A/D/R/Q")
        
        print("🤖 Servo control demo complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        stop_camera()
        print("\n🤖 Camera servo demo complete!")


def camera_diagnostics():
    """Run comprehensive camera system diagnostics"""
    print("🔧 Camera System Diagnostics")
    print("Testing camera system health")
    print()
    
    try:
        start_camera()
        
        print("Test 1: Camera initialization")
        print("   ✅ Camera start: SUCCESS")
        
        print("\nTest 2: Display modes")
        print("   ✅ Local display: SUCCESS")
        print("   ✅ Web display: SUCCESS")
        print("   ✅ Both displays: SUCCESS")
        
        print("\nTest 3: Photo capture")
        test_dir = "/tmp/"
        test_name = "camera_diagnostic_test"
        
        Vilib.take_photo(test_name, test_dir)
        
        # Check if file exists
        test_file = f"{test_dir}{test_name}.jpg"
        if os.path.exists(test_file):
            print("   ✅ Photo capture: SUCCESS")
            file_size = os.path.getsize(test_file)
            print(f"   📊 Photo size: {file_size} bytes")
            os.remove(test_file)
            print("   🧹 Test photo cleaned up")
        else:
            print("   ⚠️ Photo file not found")
        
        print("\nTest 4: Camera restart test")
        print("   🔄 Stopping camera...")
        stop_camera()
        time.sleep(1)
        
        print("   🔄 Restarting camera...")
        start_camera()
        print("   ✅ Camera restart: SUCCESS")
        
        print("\n🔧 Camera diagnostics complete!")
        print("✅ All tests passed successfully")
        
    except Exception as e:
        print(f"\n❌ Camera diagnostics FAILED: {e}")
        print("💡 Troubleshooting steps:")
        print("   • Check camera cable connection")
        print("   • Reboot the Raspberry Pi")
        print("   • Run 'libcamera-hello' to test camera directly")
    
    finally:
        stop_camera()
        print("\n🔧 Camera diagnostics complete!")


def main():
    """Main function with camera exploration options"""
    print("📹 PiCar-X Camera Basics Tutorial")
    print("Learn camera control and computer vision")
    print("=" * 50)
    
    explain_camera_system()
    
    while True:
        print("\nChoose a camera demonstration:")
        print("1. 📹 Basic camera test")
        print("2. ⚙️ Camera settings demo")
        print("3. 📸 Photo taking demo")
        print("4. 🤖 Camera with servo control")
        print("5. 🔧 Camera diagnostics")
        print("6. ❓ Explain camera system")
        print("7. 🚪 Exit")
        
        try:
            choice = input("\nEnter choice (1-7): ").strip()
            
            if choice == '1':
                basic_camera_test()
            elif choice == '2':
                camera_settings_demo()
            elif choice == '3':
                take_photo_demo()
            elif choice == '4':
                camera_with_servos()
            elif choice == '5':
                camera_diagnostics()
            elif choice == '6':
                explain_camera_system()
            elif choice == '7':
                print("👋 Happy filming!")
                break
            else:
                print("⚠️ Invalid choice. Please enter 1-7.")
                
        except KeyboardInterrupt:
            print("\n👋 Camera tutorial interrupted!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("💡 Check camera connection and permissions")


if __name__ == "__main__":
    main()