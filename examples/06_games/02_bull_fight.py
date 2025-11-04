#!/usr/bin/env python3
"""
🐂 Bull Fight - Color Tracking Combat Game

This game simulates a bull fight where the robot acts as a bull,
chasing and charging at red objects (the matador's cape).

Learn to:
- Color-based object tracking
- Aggressive pursuit behaviors
- Dynamic speed and direction control
- Game state management
- Player vs robot interactions
- Visual feedback and scoring
"""

from picarx import Picarx
from time import sleep, time
from vilib import Vilib
import random


def explain_bull_fight():
    """Explain the bull fight game"""
    print("🐂 Bull Fight Game Concept:")
    print()
    print("🎯 Game Objective:")
    print("   • Robot (bull) chases red objects (cape)")
    print("   • Player waves red object to lure the bull")
    print("   • Bull charges aggressively at red targets")
    print("   • Score based on successful charges and evasion")
    print()
    print("🤖 Bull Behavior:")
    print("   • Tracks red objects with camera and movement")
    print("   • Builds up anger and charges faster over time")
    print("   • Becomes more aggressive when target is close")
    print("   • Searches for targets when none visible")
    print()
    print("🎮 Game Mechanics:")
    print("   • Charging speed increases with anger level")
    print("   • Bull gets frustrated if target escapes")
    print("   • Different difficulty levels available")
    print("   • Time-based scoring system")
    print()


def clamp_number(num, min_val, max_val):
    """Clamp a number between min and max values"""
    return max(min(num, max_val), min_val)


def basic_bull_fight():
    """Basic bull fight game"""
    print("🐂 Basic Bull Fight")
    print("Wave a red object in front of the camera!")
    print("The robot bull will chase and charge at it")
    print("Press Ctrl+C to stop the game")
    print()
    
    with Picarx() as px:
        # Start camera and color detection
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=True, web=True)
        Vilib.color_detect_switch(True)
        Vilib.color_detect("red")
        
        # Initialize game state
        x_angle = 0
        y_angle = 0
        dir_angle = 0
        base_speed = 40
        anger_level = 0
        charges = 0
        last_detection_time = time()
        
        px.set_cam_pan_angle(x_angle)
        px.set_cam_tilt_angle(y_angle)
        
        print("🐂 Bull is ready to fight!")
        print("Show a red object to anger the bull...")
        
        try:
            while True:
                # Check for red object detection
                if Vilib.detect_obj_parameter['color_n'] != 0:
                    coordinate_x = Vilib.detect_obj_parameter['color_x']
                    coordinate_y = Vilib.detect_obj_parameter['color_y']
                    
                    last_detection_time = time()
                    anger_level = min(anger_level + 1, 100)
                    
                    # Camera tracking
                    x_adjustment = (coordinate_x * 10 / 640) - 5
                    y_adjustment = (coordinate_y * 10 / 480) - 5
                    
                    x_angle += x_adjustment
                    x_angle = clamp_number(x_angle, -35, 35)
                    
                    y_angle -= y_adjustment
                    y_angle = clamp_number(y_angle, -35, 35)
                    
                    px.set_cam_pan_angle(x_angle)
                    px.set_cam_tilt_angle(y_angle)
                    
                    # Movement direction follows camera more slowly
                    if dir_angle > x_angle:
                        dir_angle -= 1
                    elif dir_angle < x_angle:
                        dir_angle += 1
                    
                    # Calculate charging speed based on anger
                    charge_speed = base_speed + (anger_level * 0.5)
                    charge_speed = min(charge_speed, 80)
                    
                    px.set_dir_servo_angle(dir_angle)
                    px.forward(charge_speed)
                    
                    charges += 1
                    
                    # Show bull's state
                    anger_description = "😠" if anger_level < 25 else "😡" if anger_level < 50 else "🤬" if anger_level < 75 else "💢"
                    print(f"🐂 CHARGE #{charges}! {anger_description} Anger: {anger_level}/100 | "
                          f"Speed: {charge_speed:.0f} | Target: ({coordinate_x}, {coordinate_y})")
                    
                    sleep(0.05)
                
                else:
                    # No red object - bull searches and gets frustrated
                    px.stop()
                    anger_level = max(anger_level - 2, 0)
                    
                    elapsed_since_detection = time() - last_detection_time
                    
                    if elapsed_since_detection > 3:
                        # Bull gets frustrated and searches
                        if random.random() < 0.3:  # 30% chance to turn randomly
                            search_angle = random.choice([-30, -15, 15, 30])
                            px.set_dir_servo_angle(search_angle)
                            px.forward(25)
                            sleep(1)
                            px.stop()
                            print(f"🔍 Bull searching... Anger cooling: {anger_level}/100")
                    
                    sleep(0.05)
        
        except KeyboardInterrupt:
            print(f"\n🐂 Bull fight ended!")
            print(f"   Total charges: {charges}")
            print(f"   Final anger level: {anger_level}/100")
        
        finally:
            px.stop()
            Vilib.color_detect_switch(False)
            Vilib.camera_close()


def aggressive_bull_mode():
    """More aggressive bull fight with multiple colors"""
    print("🔥 Aggressive Bull Mode")
    print("Ultra-aggressive bull that chases multiple colors!")
    print("Red = primary target, Orange = secondary target")
    print("Press Ctrl+C to stop")
    print()
    
    target_colors = ["red", "orange"]
    color_priorities = {"red": 1.0, "orange": 0.7}
    
    with Picarx() as px:
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=True, web=True)
        
        # Start with red detection
        Vilib.color_detect_switch(True)
        current_target = "red"
        Vilib.color_detect(current_target)
        
        x_angle = 0
        y_angle = 0
        dir_angle = 0
        rage_meter = 0
        successful_charges = 0
        missed_charges = 0
        color_switches = 0
        
        print("🔥 AGGRESSIVE BULL ACTIVATED!")
        print(f"Current target: {current_target.upper()}")
        
        try:
            while True:
                detected = False
                
                # Check current color target
                if Vilib.detect_obj_parameter['color_n'] != 0:
                    detected = True
                    coordinate_x = Vilib.detect_obj_parameter['color_x']
                    coordinate_y = Vilib.detect_obj_parameter['color_y']
                    obj_size = Vilib.detect_obj_parameter.get('color_w', 0) * Vilib.detect_obj_parameter.get('color_h', 0)
                    
                    # Increase rage
                    rage_meter = min(rage_meter + 3, 150)
                    
                    # Camera tracking with more aggressive movement
                    x_adjustment = (coordinate_x * 12 / 640) - 6
                    y_adjustment = (coordinate_y * 12 / 480) - 6
                    
                    x_angle += x_adjustment
                    x_angle = clamp_number(x_angle, -35, 35)
                    
                    y_angle -= y_adjustment
                    y_angle = clamp_number(y_angle, -35, 35)
                    
                    px.set_cam_pan_angle(x_angle)
                    px.set_cam_tilt_angle(y_angle)
                    
                    # Aggressive direction following
                    dir_angle += (x_angle - dir_angle) * 0.5
                    
                    # Rage-based speed calculation
                    priority = color_priorities[current_target]
                    rage_speed = 30 + (rage_meter * 0.8 * priority)
                    rage_speed = min(rage_speed, 100)
                    
                    px.set_dir_servo_angle(dir_angle)
                    px.forward(rage_speed)
                    
                    # Check for successful charge (large object = close target)
                    if obj_size > 5000:  # Large object detected
                        successful_charges += 1
                        rage_meter += 10
                        print(f"💥 SUCCESSFUL CHARGE on {current_target}! Rage: {rage_meter}/150")
                    
                    rage_emoji = "😠" if rage_meter < 50 else "😡" if rage_meter < 100 else "🤬"
                    print(f"🔥 {rage_emoji} RAGING at {current_target.upper()}! "
                          f"Rage: {rage_meter}/150 | Speed: {rage_speed:.0f}")
                
                if not detected:
                    # No target found - try switching colors
                    px.stop()
                    rage_meter = max(rage_meter - 5, 0)
                    missed_charges += 1
                    
                    if missed_charges % 10 == 0:  # Every 10 misses, switch target
                        # Switch to other color
                        current_target = "orange" if current_target == "red" else "red"
                        Vilib.color_detect(current_target)
                        color_switches += 1
                        print(f"🔄 Switching target to {current_target.upper()}! (Switch #{color_switches})")
                    
                    if rage_meter > 30:  # Still angry - search aggressively
                        search_angle = random.randint(-45, 45)
                        px.set_dir_servo_angle(search_angle)
                        px.forward(40)
                        sleep(0.5)
                        px.stop()
                
                sleep(0.05)
        
        except KeyboardInterrupt:
            print(f"\n🔥 Aggressive bull session ended!")
            print(f"   Successful charges: {successful_charges}")
            print(f"   Missed targets: {missed_charges}")
            print(f"   Color switches: {color_switches}")
            print(f"   Final rage level: {rage_meter}/150")
        
        finally:
            px.stop()
            Vilib.color_detect_switch(False)
            Vilib.camera_close()


def bull_fight_tournament():
    """Tournament mode with scoring and rounds"""
    print("🏆 Bull Fight Tournament")
    print("Multiple rounds with increasing difficulty!")
    print("Score points for successful charges and evasion")
    print()
    
    with Picarx() as px:
        total_score = 0
        round_number = 0
        
        rounds = [
            {"name": "Rookie Bull", "speed_multiplier": 0.8, "anger_rate": 1, "duration": 30},
            {"name": "Veteran Bull", "speed_multiplier": 1.0, "anger_rate": 2, "duration": 45},
            {"name": "Champion Bull", "speed_multiplier": 1.3, "anger_rate": 3, "duration": 60},
            {"name": "LEGENDARY BULL", "speed_multiplier": 1.5, "anger_rate": 5, "duration": 90}
        ]
        
        try:
            for round_config in rounds:
                round_number += 1
                round_score = 0
                
                print(f"\n🏆 ROUND {round_number}: {round_config['name']}")
                print(f"Duration: {round_config['duration']} seconds")
                print(f"Speed multiplier: {round_config['speed_multiplier']:.1f}x")
                print("Press Enter to start round...")
                input()
                
                Vilib.camera_start(vflip=False, hflip=False)
                Vilib.display(local=True, web=True)
                Vilib.color_detect_switch(True)
                Vilib.color_detect("red")
                
                x_angle = 0
                y_angle = 0
                dir_angle = 0
                anger = 0
                charges = 0
                
                round_start = time()
                round_duration = round_config['duration']
                
                print(f"🐂 {round_config['name']} ACTIVATED!")
                
                while time() - round_start < round_duration:
                    remaining_time = round_duration - (time() - round_start)
                    
                    if Vilib.detect_obj_parameter['color_n'] != 0:
                        coordinate_x = Vilib.detect_obj_parameter['color_x']
                        coordinate_y = Vilib.detect_obj_parameter['color_y']
                        
                        anger = min(anger + round_config['anger_rate'], 100)
                        charges += 1
                        
                        # Camera tracking
                        x_adjustment = (coordinate_x * 10 / 640) - 5
                        x_angle += x_adjustment
                        x_angle = clamp_number(x_angle, -35, 35)
                        
                        y_adjustment = (coordinate_y * 10 / 480) - 5
                        y_angle -= y_adjustment
                        y_angle = clamp_number(y_angle, -35, 35)
                        
                        px.set_cam_pan_angle(x_angle)
                        px.set_cam_tilt_angle(y_angle)
                        
                        # Direction and speed
                        if dir_angle > x_angle:
                            dir_angle -= 2
                        elif dir_angle < x_angle:
                            dir_angle += 2
                        
                        speed = (40 + anger * 0.6) * round_config['speed_multiplier']
                        speed = min(speed, 95)
                        
                        px.set_dir_servo_angle(dir_angle)
                        px.forward(speed)
                        
                        # Scoring
                        round_score += 1
                        
                        if int(remaining_time) % 10 == 0 and remaining_time > 0:
                            print(f"🏆 Round {round_number} | Score: {round_score} | Time: {remaining_time:.0f}s | Anger: {anger}/100")
                    
                    else:
                        px.stop()
                        anger = max(anger - 1, 0)
                    
                    sleep(0.05)
                
                px.stop()
                Vilib.color_detect_switch(False)
                Vilib.camera_close()
                
                # Round results
                time_bonus = max(0, round_duration - (time() - round_start)) * 2
                final_round_score = round_score + int(time_bonus)
                total_score += final_round_score
                
                print(f"\n🏆 Round {round_number} Complete!")
                print(f"   Charges: {charges}")
                print(f"   Base score: {round_score}")
                print(f"   Time bonus: {int(time_bonus)}")
                print(f"   Round total: {final_round_score}")
                print(f"   Tournament total: {total_score}")
                
                if round_number < len(rounds):
                    continue_tournament = input("\nContinue to next round? (y/n): ").lower().strip()
                    if continue_tournament != 'y':
                        break
                
                time.sleep(2)
            
            print(f"\n🏆 TOURNAMENT COMPLETE!")
            print(f"Final Score: {total_score}")
            
            if total_score > 1000:
                print("🥇 LEGENDARY MATADOR! You mastered all bulls!")
            elif total_score > 750:
                print("🥈 EXPERT MATADOR! Excellent bull fighting!")
            elif total_score > 500:
                print("🥉 SKILLED MATADOR! Good bull handling!")
            else:
                print("🐂 The bulls won this time! Practice more!")
        
        except KeyboardInterrupt:
            print(f"\n🏆 Tournament interrupted! Final score: {total_score}")
        
        finally:
            px.stop()
            Vilib.color_detect_switch(False)
            Vilib.camera_close()


def main():
    """Main function with bull fight game options"""
    print("🐂 PiCar-X Bull Fight Game")
    print("Experience the thrill of robotic bull fighting!")
    print("=" * 50)
    
    explain_bull_fight()
    
    while True:
        print("\nChoose your bull fight experience:")
        print("1. 🐂 Basic bull fight")
        print("2. 🔥 Aggressive bull mode")
        print("3. 🏆 Bull fight tournament")
        print("4. ❓ Explain bull fight game")
        print("5. 🚪 Exit")
        
        try:
            choice = input("\nEnter choice (1-5): ").strip()
            
            if choice == '1':
                basic_bull_fight()
            elif choice == '2':
                aggressive_bull_mode()
            elif choice == '3':
                bull_fight_tournament()
            elif choice == '4':
                explain_bull_fight()
            elif choice == '5':
                print("👋 ¡Olé! Thanks for playing!")
                break
            else:
                print("⚠️ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Bull fight interrupted!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Check camera connection and have red objects ready!")
    finally:
        # Ensure everything is cleaned up
        try:
            with Picarx() as px:
                px.stop()
            Vilib.color_detect_switch(False)
            Vilib.camera_close()
        except:
            pass
    
    print("\n🐂 Bull fight game complete!")
