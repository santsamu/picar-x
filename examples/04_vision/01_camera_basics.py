#!/usr/bin/env python3
"""
📹 Camera Basics - Introduction to Robot Vision

This example introduces you to the camera system on your PiCar-X robot.
Learn the fundamentals of computer vision and camera control.

Learn to:
- Start and stop the camera system
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
    print("   • Web display: Stream to web browser")
    print("   • Both: Display locally and stream to web")
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
        # Start camera with basic settings
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=True, web=True)
        
        print("✅ Camera started successfully!")
        print("📺 Display modes:")
        print("   • Local display: ON")
        print("   • Web display: ON (check http://robot-ip:9000/mjpg)")
        print()
        print("Camera is now running...")
        print("Check your display or web browser to see the camera feed")
        print()
        
        # Keep camera running for demonstration
        for countdown in range(10, 0, -1):
            print(f"\r📹 Camera test running... {countdown} seconds remaining", end="", flush=True)
            time.sleep(1)
        
        print("\n")
        print("📹 Camera test complete!")
        
    except Exception as e:
        print(f"❌ Camera error: {e}")
        print("💡 Check camera connection and permissions")
    
    finally:
        try:
            Vilib.camera_close()
            print("📹 Camera stopped safely")
        except:
            pass


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
    
    for i, settings in enumerate(settings_tests, 1):
        print(f"📹 Test {i}/4: {settings['name']}")
        
        try:
            # Stop previous camera instance
            Vilib.camera_close()
            time.sleep(0.5)
            
            # Start with new settings
            Vilib.camera_start(vflip=settings['vflip'], hflip=settings['hflip'])
            Vilib.display(local=True, web=True)
            
            print(f"   Settings: vflip={settings['vflip']}, hflip={settings['hflip']}")
            print("   Check your display to see the orientation")
            
            # Wait for user to observe
            input("   Press Enter to continue to next setting...")
            
        except Exception as e:
            print(f"   ❌ Error with settings: {e}")
    
    print("⚙️ Camera settings demo complete!")


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
        # Start camera
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=True, web=True)
        time.sleep(1)  # Camera startup time
        
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
        try:
            Vilib.camera_close()
            print("📹 Camera stopped")
        except:
            pass


def camera_with_servos():
    """Demonstrate camera with servo control"""
    print("🤖 Camera with Servo Control")
    print("Control camera direction using servo motors")
    print()
    
    try:
        # Start camera
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=True, web=True)
        time.sleep(1)
        
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
        try:
            Vilib.camera_close()
            print("📹 Camera stopped")
        except:
            pass


def camera_diagnostics():
    """Run camera system diagnostics"""
    print("🔧 Camera System Diagnostics")
    print("Testing camera system health")
    print()
    
    # Test 1: Camera start/stop
    print("Test 1: Camera initialization")
    try:
        Vilib.camera_start()
        print("   ✅ Camera start: SUCCESS")
        time.sleep(0.5)
        Vilib.camera_close()
        print("   ✅ Camera stop: SUCCESS")
    except Exception as e:
        print(f"   ❌ Camera initialization: FAILED - {e}")
        return
    
    # Test 2: Display modes
    print("\nTest 2: Display modes")
    try:
        Vilib.camera_start()
        Vilib.display(local=True, web=False)
        print("   ✅ Local display: SUCCESS")
        time.sleep(0.5)
        
        Vilib.display(local=False, web=True)
        print("   ✅ Web display: SUCCESS")
        time.sleep(0.5)
        
        Vilib.display(local=True, web=True)
        print("   ✅ Both displays: SUCCESS")
        time.sleep(0.5)
        
        Vilib.camera_close()
    except Exception as e:
        print(f"   ❌ Display modes: FAILED - {e}")
    
    # Test 3: Photo capability
    print("\nTest 3: Photo capture")
    try:
        Vilib.camera_start()
        test_dir = "/tmp/"
        test_name = "camera_test"
        Vilib.take_photo(test_name, test_dir)
        print("   ✅ Photo capture: SUCCESS")
        
        # Check if file exists
        if os.path.exists(f"{test_dir}{test_name}.jpg"):
            print("   ✅ Photo file created: SUCCESS")
            # Clean up test file
            os.remove(f"{test_dir}{test_name}.jpg")
        else:
            print("   ⚠️ Photo file not found")
        
        Vilib.camera_close()
    except Exception as e:
        print(f"   ❌ Photo capture: FAILED - {e}")
    
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
        
        finally:
            # Always try to close camera safely
            try:
                Vilib.camera_close()
            except:
                pass


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Check camera connection and permissions")
    finally:
        # Ensure camera is closed
        try:
            Vilib.camera_close()
        except:
            pass
    
    print("\n📹 Camera basics tutorial complete!")