#!/usr/bin/env python3
"""
📸 Photo Car - Drive and Capture

This example combines robot movement with photo capture capabilities.
Drive your robot around while taking high-quality photos.

Learn to:
- Control robot movement with camera active
- Take photos while driving
- Manage photo storage and organization
- Coordinate movement and photography
- Handle real-time photo feedback
- Create photo galleries from robot exploration
"""

from robot_hat.utils import reset_mcu
from picarx import Picarx
from vilib import Vilib
from time import sleep, time, strftime, localtime
import readchar
import os
import getpass


def explain_photo_car():
    """Explain the photo car concept"""
    print("📸 Photo Car System:")
    print()
    print("🚗 Movement + Photography:")
    print("   • Drive robot with real-time camera view")
    print("   • Capture photos during exploration")
    print("   • Automatic photo organization")
    print("   • Speed control for better photos")
    print()
    print("🎮 Controls:")
    print("   • W/S: Forward/Backward")
    print("   • A/D: Turn left/right")
    print("   • F: Stop movement")
    print("   • O/P: Speed up/down")
    print("   • T: Take photo")
    print("   • C: Continuous photo mode")
    print("   • Ctrl+C: Quit")
    print()
    print("📁 Photo Management:")
    print("   • Photos saved to ~/Pictures/picar-x/")
    print("   • Automatic timestamp naming")
    print("   • JPEG format for compatibility")
    print()


def setup_photo_directory():
    """Setup and verify photo directory"""
    try:
        username = getpass.getuser()
    except:
        username = os.getlogin()
    
    photo_dir = f"/home/{username}/Pictures/picar-x/"
    
    # Create directory if it doesn't exist
    os.makedirs(photo_dir, exist_ok=True)
    
    print(f"📁 Photo directory: {photo_dir}")
    
    # Check directory permissions
    if os.access(photo_dir, os.W_OK):
        print("✅ Directory is writable")
        return photo_dir
    else:
        print("❌ Directory is not writable - check permissions")
        return None


def take_photo_enhanced(photo_dir, photo_count):
    """Enhanced photo taking with feedback"""
    timestamp = strftime('%Y-%m-%d-%H-%M-%S', localtime(time()))
    name = f'picar_photo_{timestamp}'
    
    try:
        Vilib.take_photo(name, photo_dir)
        file_path = f"{photo_dir}{name}.jpg"
        
        # Verify photo was created
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path) / 1024  # KB
            print(f'\n📸 Photo #{photo_count}: {name}.jpg ({file_size:.1f} KB)')
            return True
        else:
            print(f'\n❌ Photo failed: {name}.jpg')
            return False
    except Exception as e:
        print(f'\n❌ Photo error: {e}')
        return False


def move_robot(px, operation: str, speed: int):
    """Enhanced movement function with feedback"""
    if operation == 'stop':
        px.stop()
        px.set_dir_servo_angle(0)
    else:
        if operation == 'forward':
            px.set_dir_servo_angle(0)
            px.forward(speed)
        elif operation == 'backward':
            px.set_dir_servo_angle(0)
            px.backward(speed)
        elif operation == 'turn left':
            px.set_dir_servo_angle(-30)
            px.forward(speed)
        elif operation == 'turn right':
            px.set_dir_servo_angle(30)
            px.forward(speed)
def basic_photo_car():
    """Basic photo car functionality"""
    print("📸 Basic Photo Car Mode")
    print("Drive around and take photos manually")
    print()
    
    photo_dir = setup_photo_directory()
    if not photo_dir:
        return
    
    # Reset MCU for reliable operation
    reset_mcu()
    sleep(0.2)
    
    try:
        with Picarx() as px:
            # Start camera
            Vilib.camera_start(vflip=False, hflip=False)
            Vilib.display(local=True, web=True)
            sleep(2)  # Wait for camera startup
            
            speed = 30
            status = 'stop'
            photo_count = 0
            
            print("📸 Photo car ready!")
            print("Controls: W/S/A/D=move, O/P=speed, T=photo, F=stop, Ctrl+C=quit")
            print()
            
            while True:
                print(f"\r🚗 Status: {status} | Speed: {speed} | Photos: {photo_count}    ", 
                      end='', flush=True)
                
                # Read keyboard input
                key = readchar.readkey().lower()
                
                # Speed controls
                if key == 'o':
                    speed = min(speed + 10, 100)
                elif key == 'p':
                    speed = max(speed - 10, 0)
                    if speed == 0:
                        status = 'stop'
                
                # Movement controls
                elif key in ('wsad'):
                    if speed == 0:
                        speed = 30
                    
                    if key == 'w':
                        # Speed limit when changing direction
                        if status != 'forward' and speed > 60:
                            speed = 60
                        status = 'forward'
                    elif key == 's':
                        if status != 'backward' and speed > 60:
                            speed = 60
                        status = 'backward'
                    elif key == 'a':
                        status = 'turn left'
                    elif key == 'd':
                        status = 'turn right'
                    
                    move_robot(px, status, speed)
                
                # Stop
                elif key == 'f':
                    status = 'stop'
                    move_robot(px, status, speed)
                
                # Take photo
                elif key == 't':
                    photo_count += 1
                    if take_photo_enhanced(photo_dir, photo_count):
                        print(f"    ✅ Photo {photo_count} captured!")
                    else:
                        photo_count -= 1  # Revert count on failure
                
                # Quit
                elif key == readchar.key.CTRL_C:
                    print('\n📸 Photo car session complete!')
                    px.stop()
                    break
                
                sleep(0.1)
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        try:
            Vilib.camera_close()
        except:
            pass


def continuous_photo_mode():
    """Continuous photo taking while driving"""
    print("📸🔄 Continuous Photo Mode")
    print("Automatically take photos while driving")
    print()
    
    photo_dir = setup_photo_directory()
    if not photo_dir:
        return
    
    try:
        interval = float(input("Photo interval in seconds [default: 3]: ") or "3")
        interval = max(1, min(10, interval))
    except:
        interval = 3
    
    print(f"\n📸 Will take photos every {interval} seconds while moving")
    
    reset_mcu()
    sleep(0.2)
    
    try:
        with Picarx() as px:
            Vilib.camera_start(vflip=False, hflip=False)
            Vilib.display(local=True, web=True)
            sleep(2)
            
            speed = 30
            status = 'stop'
            photo_count = 0
            last_photo_time = 0
            continuous_mode = False
            
            print("📸 Continuous photo car ready!")
            print("Controls: W/S/A/D=move, C=toggle continuous, T=manual photo, F=stop")
            print()
            
            while True:
                current_time = time()
                
                # Auto photo in continuous mode
                if (continuous_mode and status != 'stop' and 
                    current_time - last_photo_time > interval):
                    photo_count += 1
                    if take_photo_enhanced(photo_dir, photo_count):
                        last_photo_time = current_time
                        print(f"    📸 Auto photo {photo_count}")
                    else:
                        photo_count -= 1
                
                mode_indicator = "🔄ON" if continuous_mode else "⏸️OFF"
                print(f"\r🚗 {status} | Speed: {speed} | Photos: {photo_count} | Auto: {mode_indicator}    ", 
                      end='', flush=True)
                
                key = readchar.readkey().lower()
                
                # Toggle continuous mode
                if key == 'c':
                    continuous_mode = not continuous_mode
                    if continuous_mode:
                        last_photo_time = current_time
                        print(f"\n🔄 Continuous mode ON (every {interval}s)")
                    else:
                        print(f"\n⏸️ Continuous mode OFF")
                
                # Movement and other controls (same as basic mode)
                elif key == 'o':
                    speed = min(speed + 10, 100)
                elif key == 'p':
                    speed = max(speed - 10, 0)
                    if speed == 0:
                        status = 'stop'
                elif key in ('wsad'):
                    if speed == 0:
                        speed = 30
                    if key == 'w':
                        if status != 'forward' and speed > 60:
                            speed = 60
                        status = 'forward'
                    elif key == 's':
                        if status != 'backward' and speed > 60:
                            speed = 60
                        status = 'backward'
                    elif key == 'a':
                        status = 'turn left'
                    elif key == 'd':
                        status = 'turn right'
                    move_robot(px, status, speed)
                elif key == 'f':
                    status = 'stop'
                    move_robot(px, status, speed)
                elif key == 't':
                    photo_count += 1
                    if take_photo_enhanced(photo_dir, photo_count):
                        print(f"    📸 Manual photo {photo_count}")
                    else:
                        photo_count -= 1
                elif key == readchar.key.CTRL_C:
                    print(f'\n📸 Captured {photo_count} photos total!')
                    px.stop()
                    break
                
                sleep(0.1)
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        try:
            Vilib.camera_close()
        except:
            pass


def photo_exploration_mode():
    """Guided photo exploration with waypoints"""
    print("🗺️📸 Photo Exploration Mode")
    print("Systematic photo exploration with guided movement")
    print()
    
    photo_dir = setup_photo_directory()
    if not photo_dir:
        return
    
    print("This mode helps you systematically photograph an area:")
    print("• Structured movement patterns")
    print("• Automatic photo waypoints")
    print("• Coverage tracking")
    print()
    
    reset_mcu()
    sleep(0.2)
    
    try:
        with Picarx() as px:
            Vilib.camera_start(vflip=False, hflip=False)
            Vilib.display(local=True, web=True)
            sleep(2)
            
            photo_count = 0
            waypoint = 1
            
            print("🗺️ Photo exploration started!")
            print("Follow the waypoint instructions and take photos")
            print()
            
            waypoints = [
                "Move forward and photo the area ahead",
                "Turn left 90° and photo the left side",
                "Move forward again and photo",
                "Turn right 90° and photo the front",
                "Turn right 90° again and photo the right side",
                "Return to center and photo overview"
            ]
            
            for i, instruction in enumerate(waypoints, 1):
                print(f"📍 Waypoint {i}: {instruction}")
                print("Drive to position, then press 'T' to take photo, 'N' for next waypoint")
                
                while True:
                    key = readchar.readkey().lower()
                    
                    # Movement controls
                    if key == 'w':
                        px.forward(40)
                        print("⬆️ Moving forward...")
                    elif key == 's':
                        px.backward(40)
                        print("⬇️ Moving backward...")
                    elif key == 'a':
                        px.set_dir_servo_angle(-30)
                        px.forward(30)
                        print("↪️ Turning left...")
                    elif key == 'd':
                        px.set_dir_servo_angle(30)
                        px.forward(30)
                        print("↩️ Turning right...")
                    elif key == 'f':
                        px.stop()
                        px.set_dir_servo_angle(0)
                        print("🛑 Stopped")
                    
                    # Take photo
                    elif key == 't':
                        photo_count += 1
                        if take_photo_enhanced(photo_dir, photo_count):
                            print(f"✅ Waypoint {i} photo captured!")
                        else:
                            photo_count -= 1
                    
                    # Next waypoint
                    elif key == 'n':
                        px.stop()
                        break
                    
                    # Quit
                    elif key == readchar.key.CTRL_C:
                        px.stop()
                        print(f"\n🗺️ Exploration ended. Captured {photo_count} photos.")
                        return
                    
                    sleep(0.1)
            
            print(f"\n🎉 Photo exploration complete! Captured {photo_count} photos.")
            print(f"📁 Photos saved in: {photo_dir}")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        try:
            Vilib.camera_close()
        except:
            pass


def main():
    """Main function with photo car options"""
    print("📸 PiCar-X Photo Car Tutorial")
    print("Drive and capture the world around you")
    print("=" * 50)
    
    explain_photo_car()
    
    while True:
        print("\nChoose a photo car mode:")
        print("1. 📸 Basic photo car")
        print("2. 📸🔄 Continuous photo mode")
        print("3. 🗺️📸 Photo exploration mode")
        print("4. ❓ Explain photo car")
        print("5. 🚪 Exit")
        
        try:
            choice = input("\nEnter choice (1-5): ").strip()
            
            if choice == '1':
                basic_photo_car()
            elif choice == '2':
                continuous_photo_mode()
            elif choice == '3':
                photo_exploration_mode()
            elif choice == '4':
                explain_photo_car()
            elif choice == '5':
                print("👋 Happy photographing!")
                break
            else:
                print("⚠️ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Photo car tutorial interrupted!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Check camera connection and storage space")
    finally:
        # Ensure everything is stopped
        try:
            with Picarx() as px:
                px.stop()
            Vilib.camera_close()
        except:
            pass
    
    print("\n📸 Photo car tutorial complete!")