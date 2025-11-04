#!/usr/bin/env python3
"""
🎬 Video Recording - Advanced Camera Recording

This example teaches you how to record high-quality videos with your PiCar-X robot.
Learn professional video recording techniques and file management.

Learn to:
- Record videos with proper settings
- Control recording with keyboard
- Manage video files and storage
- Handle recording errors safely
- Create time-stamped video files
- Monitor recording status
"""

from time import sleep, strftime, localtime, time
from vilib import Vilib
import readchar
import os
import getpass


def explain_video_recording():
    """Explain video recording capabilities"""
    print("🎬 Video Recording System:")
    print()
    print("📹 Recording Features:")
    print("   • High-quality video capture")
    print("   • Real-time recording control")
    print("   • Automatic file naming with timestamps")
    print("   • Pause/resume functionality")
    print("   • Safe file handling")
    print()
    print("🎮 Recording Controls:")
    print("   • Q: Start recording, pause, or resume")
    print("   • E: Stop recording and save file")
    print("   • Ctrl+C: Emergency quit")
    print()
    print("📁 File Management:")
    print("   • Videos saved to ~/Videos/ directory")
    print("   • Automatic timestamp naming")
    print("   • .avi format for compatibility")
    print()


def print_overwrite(msg, end='', flush=True):
    """Helper function for updating console output"""
    print('\r\033[2K', end='', flush=True)
    print(msg, end=end, flush=flush)

def setup_recording_directory():
    """Setup and verify video recording directory"""
    try:
        username = getpass.getuser()
    except:
        username = os.getlogin()
    
    video_dir = f"/home/{username}/Videos/"
    
    # Create directory if it doesn't exist
    os.makedirs(video_dir, exist_ok=True)
    
    print(f"📁 Video directory: {video_dir}")
    
    # Check directory permissions
    if os.access(video_dir, os.W_OK):
        print("✅ Directory is writable")
    else:
        print("❌ Directory is not writable - check permissions")
        return None
    
    return video_dir


def basic_video_recording():
    """Basic video recording with manual controls"""
    print("🎬 Basic Video Recording")
    print("Manual recording control with keyboard")
    print()
    
    video_dir = setup_recording_directory()
    if not video_dir:
        return
    
    try:
        # Configure recording settings
        Vilib.rec_video_set["path"] = video_dir
        
        # Start camera
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=True, web=True)
        sleep(0.8)  # Wait for camera startup
        
        print("📹 Camera ready for recording!")
        print()
        print("Recording Controls:")
        print("   Q: Start recording / Pause / Resume")
        print("   E: Stop recording and save")
        print("   Ctrl+C: Quit")
        print()
        
        rec_flag = 'stop'  # start, pause, stop
        vname = None
        recording_start_time = None
        
        while True:
            # Read keyboard input
            key = readchar.readkey()
            key = key.lower()
            
            # Start, pause, resume recording
            if key == 'q':
                if rec_flag == 'stop':
                    # Start new recording
                    rec_flag = 'start'
                    vname = strftime("%Y-%m-%d-%H.%M.%S", localtime())
                    Vilib.rec_video_set["name"] = vname
                    
                    Vilib.rec_video_run()
                    Vilib.rec_video_start()
                    recording_start_time = time()
                    
                    print_overwrite(f'🔴 Recording started: {vname}')
                    
                elif rec_flag == 'start':
                    # Pause recording
                    rec_flag = 'pause'
                    Vilib.rec_video_pause()
                    elapsed = time() - recording_start_time if recording_start_time else 0
                    print_overwrite(f'⏸️ Recording paused after {elapsed:.1f}s')
                    
                elif rec_flag == 'pause':
                    # Resume recording
                    rec_flag = 'start'
                    Vilib.rec_video_start()
                    print_overwrite(f'▶️ Recording resumed: {vname}')
            
            # Stop recording
            elif key == 'e' and rec_flag != 'stop':
                rec_flag = 'stop'
                Vilib.rec_video_stop()
                
                elapsed = time() - recording_start_time if recording_start_time else 0
                file_path = f"{video_dir}{vname}.avi"
                
                print_overwrite(f"✅ Video saved: {file_path}")
                print(f"\n📊 Recording duration: {elapsed:.1f} seconds")
                
                # Check if file was created successfully
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                    print(f"📁 File size: {file_size:.2f} MB")
                else:
                    print("⚠️ Warning: Video file not found")
                
                recording_start_time = None
                print("\nReady for next recording...")
            
            # Quit
            elif key == readchar.key.CTRL_C:
                if rec_flag != 'stop':
                    print_overwrite("Stopping current recording...")
                    Vilib.rec_video_stop()
                break
    
    except Exception as e:
        print(f"\n❌ Recording error: {e}")
    
    finally:
        try:
            Vilib.camera_close()
            print("\n📹 Camera stopped")
        except:
            pass


def automated_recording():
    """Automated recording with timed sessions"""
    print("🤖 Automated Video Recording")
    print("Record videos with automatic timing")
    print()
    
    video_dir = setup_recording_directory()
    if not video_dir:
        return
    
    try:
        duration = float(input("Enter recording duration in seconds [default: 10]: ") or "10")
        duration = max(1, min(300, duration))  # Limit to 1-300 seconds
    except:
        duration = 10
    
    print(f"\n🎬 Will record {duration} second video")
    print("Press Enter to start recording, or Ctrl+C to cancel")
    
    try:
        input("Ready? ")
        
        # Setup recording
        Vilib.rec_video_set["path"] = video_dir
        vname = strftime("auto_%Y-%m-%d-%H.%M.%S", localtime())
        Vilib.rec_video_set["name"] = vname
        
        # Start camera and recording
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=True, web=True)
        sleep(0.8)
        
        print("🎬 Starting automated recording...")
        Vilib.rec_video_run()
        Vilib.rec_video_start()
        
        start_time = time()
        
        # Record for specified duration with countdown
        while True:
            elapsed = time() - start_time
            remaining = duration - elapsed
            
            if remaining <= 0:
                break
            
            print_overwrite(f"🔴 Recording... {remaining:.1f}s remaining")
            sleep(0.1)
        
        # Stop recording
        Vilib.rec_video_stop()
        
        file_path = f"{video_dir}{vname}.avi"
        print_overwrite(f"✅ Automated recording complete!")
        print(f"\n📁 Video saved: {file_path}")
        print(f"⏱️ Duration: {duration:.1f} seconds")
        
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path) / (1024 * 1024)
            print(f"📊 File size: {file_size:.2f} MB")
    
    except KeyboardInterrupt:
        print("\n❌ Automated recording cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    finally:
        try:
            Vilib.camera_close()
        except:
            pass


def recording_with_movement():
    """Record video while controlling robot movement"""
    print("🎬🤖 Recording with Movement")
    print("Record videos while driving the robot")
    print()
    
    from picarx import Picarx
    
    video_dir = setup_recording_directory()
    if not video_dir:
        return
    
    print("Movement Controls:")
    print("   W: Forward    S: Backward")
    print("   A: Left       D: Right")
    print("   F: Stop movement")
    print("   Q: Start/Pause/Resume recording")
    print("   E: Stop recording")
    print("   X: Quit")
    print()
    
    try:
        # Setup
        Vilib.rec_video_set["path"] = video_dir
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=True, web=True)
        sleep(0.8)
        
        with Picarx() as px:
            rec_flag = 'stop'
            vname = None
            
            print("🎬 Ready for recording with movement control")
            
            while True:
                key = readchar.readkey().lower()
                
                # Recording controls
                if key == 'q':
                    if rec_flag == 'stop':
                        rec_flag = 'start'
                        vname = strftime("movement_%Y-%m-%d-%H.%M.%S", localtime())
                        Vilib.rec_video_set["name"] = vname
                        Vilib.rec_video_run()
                        Vilib.rec_video_start()
                        print_overwrite('🔴 Recording with movement started')
                    elif rec_flag == 'start':
                        rec_flag = 'pause'
                        Vilib.rec_video_pause()
                        print_overwrite('⏸️ Recording paused')
                    elif rec_flag == 'pause':
                        rec_flag = 'start'
                        Vilib.rec_video_start()
                        print_overwrite('▶️ Recording resumed')
                
                elif key == 'e' and rec_flag != 'stop':
                    rec_flag = 'stop'
                    Vilib.rec_video_stop()
                    px.stop()
                    print_overwrite(f"✅ Movement recording saved: {video_dir}{vname}.avi", end='\n')
                
                # Movement controls
                elif key == 'w':
                    px.forward(50)
                    if rec_flag == 'start':
                        print_overwrite('🔴 Recording: Moving forward')
                    else:
                        print_overwrite('⬆️ Moving forward')
                
                elif key == 's':
                    px.backward(50)
                    if rec_flag == 'start':
                        print_overwrite('🔴 Recording: Moving backward')
                    else:
                        print_overwrite('⬇️ Moving backward')
                
                elif key == 'a':
                    px.set_dir_servo_angle(-30)
                    px.forward(40)
                    if rec_flag == 'start':
                        print_overwrite('🔴 Recording: Turning left')
                    else:
                        print_overwrite('⬅️ Turning left')
                
                elif key == 'd':
                    px.set_dir_servo_angle(30)
                    px.forward(40)
                    if rec_flag == 'start':
                        print_overwrite('🔴 Recording: Turning right')
                    else:
                        print_overwrite('➡️ Turning right')
                
                elif key == 'f':
                    px.stop()
                    px.set_dir_servo_angle(0)
                    if rec_flag == 'start':
                        print_overwrite('🔴 Recording: Stopped')
                    else:
                        print_overwrite('🛑 Robot stopped')
                
                elif key == 'x':
                    px.stop()
                    break
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    finally:
        try:
            Vilib.camera_close()
        except:
            pass


def video_recording_diagnostics():
    """Test video recording system"""
    print("🔧 Video Recording Diagnostics")
    print("Testing recording system health")
    print()
    
    video_dir = setup_recording_directory()
    if not video_dir:
        return
    
    try:
        # Test 1: Camera initialization
        print("Test 1: Camera system")
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=True, web=False)
        print("   ✅ Camera start: SUCCESS")
        sleep(1)
        
        # Test 2: Recording setup
        print("\nTest 2: Recording configuration")
        Vilib.rec_video_set["path"] = video_dir
        test_name = "diagnostic_test"
        Vilib.rec_video_set["name"] = test_name
        print("   ✅ Recording setup: SUCCESS")
        
        # Test 3: Short recording
        print("\nTest 3: Recording functionality")
        Vilib.rec_video_run()
        Vilib.rec_video_start()
        print("   📹 Recording started...")
        
        sleep(2)  # Record for 2 seconds
        
        Vilib.rec_video_stop()
        print("   ✅ Recording stopped: SUCCESS")
        
        # Test 4: File verification
        print("\nTest 4: File creation")
        test_file = f"{video_dir}{test_name}.avi"
        
        if os.path.exists(test_file):
            file_size = os.path.getsize(test_file)
            print(f"   ✅ File created: SUCCESS ({file_size} bytes)")
            # Clean up test file
            os.remove(test_file)
            print("   🗑️ Test file cleaned up")
        else:
            print("   ❌ File creation: FAILED")
        
        print("\n✅ Video recording diagnostics complete!")
    
    except Exception as e:
        print(f"\n❌ Diagnostics error: {e}")
    
    finally:
        try:
            Vilib.camera_close()
        except:
            pass


def main_menu():
    """Main function with video recording options"""
    print("🎬 PiCar-X Video Recording Tutorial")
    print("Learn professional video recording techniques")
    print("=" * 50)
    
    explain_video_recording()
    
    while True:
        print("\nChoose a recording demonstration:")
        print("1. 🎬 Basic video recording")
        print("2. 🤖 Automated recording")
        print("3. 🎬🤖 Recording with movement")
        print("4. 🔧 Recording diagnostics")
        print("5. ❓ Explain video recording")
        print("6. 🚪 Exit")
        
        try:
            choice = input("\nEnter choice (1-6): ").strip()
            
            if choice == '1':
                basic_video_recording()
            elif choice == '2':
                automated_recording()
            elif choice == '3':
                recording_with_movement()
            elif choice == '4':
                video_recording_diagnostics()
            elif choice == '5':
                explain_video_recording()
            elif choice == '6':
                print("👋 Happy recording!")
                break
            else:
                print("⚠️ Invalid choice. Please enter 1-6.")
                
        except KeyboardInterrupt:
            print("\n👋 Recording tutorial interrupted!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    try:
        main_menu()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Check camera connection and storage space")
    finally:
        # Ensure camera is closed
        try:
            Vilib.camera_close()
        except:
            pass
    
    print("\n🎬 Video recording tutorial complete!")