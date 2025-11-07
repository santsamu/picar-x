#!/usr/bin/env python3
"""
🏎️ Racing Minecart - Advanced Line Following Racing Game

This game transforms line following into an exciting racing experience
with speed control, lap timing, and performance optimization.

Learn to:
- High-speed line following algorithms
- Racing line optimization
- Lap timing and scoring systems
- Speed vs accuracy balance
- Racing strategy and pit stops
- Performance tuning and setup
"""

from picarx import Picarx
from time import sleep, time
import random


def explain_racing_minecart():
    """Explain the racing minecart game"""
    print("🏎️ Racing Minecart Game Concept:")
    print()
    print("🏁 Racing Objectives:")
    print("   • Follow line track as fast as possible")
    print("   • Complete laps with best times")
    print("   • Balance speed vs track adherence")
    print("   • Optimize racing line through corners")
    print()
    print("⚙️ Racing Mechanics:")
    print("   • Dynamic speed control based on track conditions")
    print("   • Cornering speed optimization")
    print("   • Track position monitoring")
    print("   • Lap timing and sector splits")
    print()
    print("🏆 Game Modes:")
    print("   • Time Trial: Single lap optimization")
    print("   • Endurance: Multiple lap consistency")
    print("   • Grand Prix: Full racing simulation")
    print("   • Setup tuning for different tracks")
    print()


def get_line_status(px, val_list):
    """Enhanced line detection with more states"""
    _state = px.get_line_status(val_list)
    
    if _state == [0, 0, 0]:
        return 'off_track'  # All sensors see line - likely off track
    elif _state == [1, 1, 1]:
        return 'no_line'    # No line detected
    elif _state == [1, 0, 1]:
        return 'straight'   # Center sensor on line
    elif _state == [0, 0, 1]:
        return 'sharp_left'
    elif _state == [0, 1, 1]:
        return 'left'
    elif _state == [1, 0, 0]:
        return 'sharp_right'
    elif _state == [1, 1, 0]:
        return 'right'
    else:
        return 'unknown'


def time_trial_mode():
    """Single lap time trial racing"""
    print("🏁 Time Trial Mode")
    print("Complete one lap as fast as possible!")
    print("Focus on finding the optimal racing line")
    print("Press Enter to start, Ctrl+C to stop")
    input()
    
    with Picarx() as px:
        # Racing setup
        lap_start_time = time()
        sector_times = []
        sector_start = lap_start_time
        
        # Racing parameters
        base_speed = 60
        max_speed = 80
        corner_speed = 40
        
        position_history = []
        speed_history = []
        
        print("🏎️ Time Trial Started!")
        print("Racing parameters: Base=60, Max=80, Corner=40")
        
        try:
            lap_complete = False
            distance_traveled = 0
            
            while not lap_complete:
                # Get sensor readings
                gm_val_list = px.get_grayscale_data()
                track_status = get_line_status(px, gm_val_list)
                position_history.append(track_status)
                
                current_time = time()
                
                # Racing algorithm based on track position
                if track_status == 'straight':
                    # Straight line - maximum attack!
                    current_speed = max_speed
                    px.set_dir_servo_angle(0)
                    px.forward(current_speed)
                    racing_line = "🏁 FULL SPEED STRAIGHT"
                    
                elif track_status in ['left', 'right']:
                    # Medium corner - racing speed
                    current_speed = base_speed
                    angle = -25 if track_status == 'left' else 25
                    px.set_dir_servo_angle(angle)
                    px.forward(current_speed)
                    racing_line = f"🏎️ RACING {track_status.upper()}"
                    
                elif track_status in ['sharp_left', 'sharp_right']:
                    # Sharp corner - slow down for safety
                    current_speed = corner_speed
                    angle = -35 if track_status == 'sharp_left' else 35
                    px.set_dir_servo_angle(angle)
                    px.forward(current_speed)
                    racing_line = f"⚠️ SLOW {track_status.upper()}"
                    
                elif track_status == 'off_track':
                    # Off track - emergency correction
                    px.stop()
                    current_speed = 0
                    racing_line = "🚨 OFF TRACK!"
                    
                    # Try to get back on track
                    px.backward(20)
                    sleep(0.5)
                    
                elif track_status == 'no_line':
                    # No line - could be finish line or lost
                    distance_traveled += 1
                    if distance_traveled > 100:  # Arbitrary lap completion
                        lap_complete = True
                        break
                    
                    # Continue forward slowly
                    current_speed = 30
                    px.forward(current_speed)
                    racing_line = "🔍 SEARCHING LINE"
                
                speed_history.append(current_speed)
                distance_traveled += 1
                
                # Sector timing (every 50 readings)
                if distance_traveled % 50 == 0:
                    sector_time = current_time - sector_start
                    sector_times.append(sector_time)
                    sector_start = current_time
                    print(f"📊 Sector {len(sector_times)}: {sector_time:.2f}s | {racing_line}")
                
                sleep(0.02)  # High frequency for racing
            
            # Lap complete!
            total_lap_time = time() - lap_start_time
            px.stop()
            
            print(f"\n🏁 LAP COMPLETE!")
            print(f"   Total time: {total_lap_time:.2f} seconds")
            print(f"   Sectors: {[f'{t:.2f}s' for t in sector_times]}")
            
            # Performance analysis
            avg_speed = sum(speed_history) / len(speed_history) if speed_history else 0
            max_speed_achieved = max(speed_history) if speed_history else 0
            
            print(f"   Average speed: {avg_speed:.1f}")
            print(f"   Max speed: {max_speed_achieved}")
            
            # Track position analysis
            position_counts = {}
            for pos in position_history:
                position_counts[pos] = position_counts.get(pos, 0) + 1
            
            print(f"   Track adherence:")
            for pos, count in position_counts.items():
                percentage = (count / len(position_history)) * 100
                print(f"     {pos}: {percentage:.1f}%")
        
        except KeyboardInterrupt:
            px.stop()
            print(f"\n🏁 Time trial stopped!")


def endurance_racing():
    """Multi-lap endurance racing"""
    print("🏁 Endurance Racing Mode")
    print("Complete multiple laps with consistent times!")
    print("Focus on consistency over pure speed")
    
    try:
        num_laps = int(input("Enter number of laps (1-10): "))
        num_laps = max(1, min(num_laps, 10))
    except:
        num_laps = 3
    
    print(f"🏁 {num_laps} lap endurance race starting...")
    input("Press Enter to start race...")
    
    with Picarx() as px:
        lap_times = []
        total_race_start = time()
        
        # Conservative endurance settings
        base_speed = 50
        max_speed = 65
        corner_speed = 35
        
        try:
            for lap_num in range(1, num_laps + 1):
                print(f"\n🏁 LAP {lap_num}/{num_laps}")
                lap_start = time()
                
                # Simplified endurance algorithm - prioritize consistency
                lap_distance = 0
                off_track_count = 0
                
                while lap_distance < 150:  # Lap completion distance
                    gm_val_list = px.get_grayscale_data()
                    track_status = get_line_status(px, gm_val_list)
                    
                    if track_status == 'straight':
                        px.set_dir_servo_angle(0)
                        px.forward(max_speed)
                    elif track_status in ['left', 'right']:
                        angle = -20 if track_status == 'left' else 20
                        px.set_dir_servo_angle(angle)
                        px.forward(base_speed)
                    elif track_status in ['sharp_left', 'sharp_right']:
                        angle = -30 if track_status == 'sharp_left' else 30
                        px.set_dir_servo_angle(angle)
                        px.forward(corner_speed)
                    elif track_status == 'off_track':
                        off_track_count += 1
                        px.stop()
                        sleep(0.2)
                        px.backward(15)
                        sleep(0.3)
                    else:
                        px.forward(base_speed)
                    
                    lap_distance += 1
                    sleep(0.03)
                
                lap_time = time() - lap_start
                lap_times.append(lap_time)
                px.stop()
                
                print(f"✅ Lap {lap_num} complete: {lap_time:.2f}s (Off track: {off_track_count} times)")
                
                if lap_num < num_laps:
                    sleep(1)  # Brief rest between laps
            
            # Race results
            total_race_time = time() - total_race_start
            best_lap = min(lap_times)
            worst_lap = max(lap_times)
            avg_lap = sum(lap_times) / len(lap_times)
            consistency = worst_lap - best_lap
            
            print(f"\n🏆 ENDURANCE RACE COMPLETE!")
            print(f"   Total race time: {total_race_time:.2f}s")
            print(f"   Best lap: {best_lap:.2f}s")
            print(f"   Worst lap: {worst_lap:.2f}s")
            print(f"   Average lap: {avg_lap:.2f}s")
            print(f"   Consistency: {consistency:.2f}s spread")
            
            if consistency < 2.0:
                print("🥇 EXCELLENT consistency!")
            elif consistency < 5.0:
                print("🥈 Good consistency!")
            else:
                print("🥉 Work on consistency!")
        
        except KeyboardInterrupt:
            px.stop()
            print(f"\n🏁 Endurance race stopped!")


def grand_prix_mode():
    """Full racing simulation with pit stops and strategy"""
    print("🏆 Grand Prix Mode")
    print("Full racing simulation with pit stops and tire strategy!")
    print("Manage speed, tire wear, and pit stop timing")
    
    with Picarx() as px:
        # Race parameters
        total_laps = 5
        tire_wear = 100  # 100% = fresh tires
        fuel_level = 100  # 100% = full tank
        pit_stops = 0
        
        lap_times = []
        race_start = time()
        
        print(f"🏆 {total_laps} lap Grand Prix starting!")
        print("Monitor tire wear and fuel levels for pit stop strategy")
        input("Press Enter to start race...")
        
        try:
            for lap_num in range(1, total_laps + 1):
                print(f"\n🏁 LAP {lap_num}/{total_laps}")
                print(f"🛞 Tires: {tire_wear:.0f}% | ⛽ Fuel: {fuel_level:.0f}%")
                
                lap_start = time()
                
                # Calculate performance based on tire wear and fuel
                tire_factor = tire_wear / 100
                fuel_factor = fuel_level / 100
                performance_factor = (tire_factor * 0.7) + (fuel_factor * 0.3)
                
                # Speed calculations based on performance
                base_speed = int(45 + (performance_factor * 25))
                max_speed = int(55 + (performance_factor * 30))
                corner_speed = int(30 + (performance_factor * 15))
                
                lap_distance = 0
                
                while lap_distance < 120:  # GP lap distance
                    gm_val_list = px.get_grayscale_data()
                    track_status = get_line_status(px, gm_val_list)
                    
                    # Racing with performance degradation
                    if track_status == 'straight':
                        px.set_dir_servo_angle(0)
                        px.forward(max_speed)
                    elif track_status in ['left', 'right']:
                        angle = -18 if track_status == 'left' else 18
                        px.set_dir_servo_angle(angle)
                        px.forward(base_speed)
                    elif track_status in ['sharp_left', 'sharp_right']:
                        angle = -28 if track_status == 'sharp_left' else 28
                        px.set_dir_servo_angle(angle)
                        px.forward(corner_speed)
                    else:
                        px.forward(base_speed)
                    
                    # Simulate tire wear and fuel consumption
                    tire_wear -= 0.1
                    fuel_level -= 0.05
                    lap_distance += 1
                    
                    sleep(0.025)
                
                lap_time = time() - lap_start
                lap_times.append(lap_time)
                px.stop()
                
                print(f"✅ Lap {lap_num}: {lap_time:.2f}s | Performance: {performance_factor:.1%}")
                
                # Pit stop decision
                if (tire_wear < 40 or fuel_level < 30) and lap_num < total_laps:
                    print(f"📻 Box, box, box! Pit stop recommended")
                    pit_decision = input("Enter pit lane? (y/n): ").lower().strip()
                    
                    if pit_decision == 'y':
                        pit_stops += 1
                        pit_time = 15 + random.uniform(0, 5)  # 15-20 second pit stop
                        
                        print(f"🏁 PIT STOP #{pit_stops}: {pit_time:.1f} seconds")
                        tire_wear = 100  # Fresh tires
                        fuel_level = 100  # Refuel
                        
                        sleep(2)  # Simulate pit stop
                
                if lap_num < total_laps:
                    sleep(0.5)
            
            # Final race results
            total_race_time = time() - race_start
            best_lap = min(lap_times)
            race_average = sum(lap_times) / len(lap_times)
            
            print(f"\n🏆 GRAND PRIX COMPLETE!")
            print(f"   Total race time: {total_race_time:.2f}s")
            print(f"   Pit stops: {pit_stops}")
            print(f"   Best lap: {best_lap:.2f}s")
            print(f"   Average lap: {race_average:.2f}s")
            print(f"   Final tire wear: {tire_wear:.0f}%")
            print(f"   Final fuel: {fuel_level:.0f}%")
            
            # Championship points
            points = max(0, 25 - (pit_stops * 3) - int((total_race_time - 60) / 5))
            print(f"   Championship points: {points}")
        
        except KeyboardInterrupt:
            px.stop()
            print(f"\n🏁 Grand Prix stopped!")


def main():
    """Main function with racing game options"""
    print("🏎️ PiCar-X Racing Minecart Game")
    print("Experience high-speed line following racing!")
    print("=" * 50)
    
    explain_racing_minecart()
    
    while True:
        print("\nChoose your racing experience:")
        print("1. 🏁 Time Trial mode")
        print("2. 🏁 Endurance racing")
        print("3. 🏆 Grand Prix mode")
        print("4. ❓ Explain racing minecart")
        print("5. 🚪 Exit")
        
        try:
            choice = input("\nEnter choice (1-5): ").strip()
            
            if choice == '1':
                time_trial_mode()
            elif choice == '2':
                endurance_racing()
            elif choice == '3':
                grand_prix_mode()
            elif choice == '4':
                explain_racing_minecart()
            elif choice == '5':
                print("👋 See you at the finish line!")
                break
            else:
                print("⚠️ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Racing interrupted!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Make sure you have a line track ready for racing!")
    
    print("\n🏎️ Racing minecart game complete!")
