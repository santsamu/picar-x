#!/usr/bin/env python3
"""
🏴‍☠️ Treasure Hunt - Interactive Color Quest Game

This exciting treasure hunt game combines manual control with color detection
missions. Hunt for colored treasures while navigating obstacles!

Learn to:
- Multi-modal game interaction
- Color-based quest systems
- Manual control with objectives
- Audio feedback and narration
- Dynamic mission generation
- Scoring and achievement systems
"""

from picarx import Picarx
from time import sleep, time
from robot_hat import Music, TTS
from vilib import Vilib
import readchar
import random
import threading


def explain_treasure_hunt():
    """Explain the treasure hunt game"""
    print("🏴‍☠️ Treasure Hunt Game Concept:")
    print()
    print("🗺️ Quest Objectives:")
    print("   • Navigate using manual controls")
    print("   • Hunt for specific colored treasures")
    print("   • Complete quests within time limits")
    print("   • Collect points and achievements")
    print()
    print("🎮 Game Controls:")
    print("   • W/A/S/D: Manual movement control")
    print("   • Space: Repeat current treasure target")
    print("   • Camera provides visual feedback")
    print("   • Audio announces new targets")
    print()
    print("🏆 Scoring System:")
    print("   • Points for finding correct treasures")
    print("   • Time bonuses for quick discoveries")
    print("   • Penalty for wrong color detections")
    print("   • Achievement unlocks and streaks")
    print()


class TreasureHuntGame:
    """Main treasure hunt game class"""
    
    def __init__(self):
        self.px = None
        self.music = Music()
        self.tts = TTS()
        self.current_treasure = None
        self.treasure_colors = ["red", "orange", "yellow", "green", "blue", "purple"]
        self.score = 0
        self.treasures_found = 0
        self.wrong_detections = 0
        self.game_time = 0
        self.quest_start_time = 0
        self.running = False
        self.key = None
        self.key_lock = threading.Lock()
        
    def say_treasure_target(self):
        """Announce the current treasure target"""
        if self.current_treasure:
            self.tts.say(f"Find the {self.current_treasure} treasure!")
    
    def new_treasure_quest(self):
        """Generate a new treasure quest"""
        self.current_treasure = random.choice(self.treasure_colors)
        Vilib.color_detect_switch(True)
        Vilib.color_detect(self.current_treasure)
        self.quest_start_time = time()
        
        print(f"\n🗺️ NEW QUEST: Find the {self.current_treasure.upper()} treasure!")
        self.say_treasure_target()
    
    def key_scan_thread(self):
        """Background thread for key scanning"""
        while self.running:
            try:
                key_temp = readchar.readkey()
                with self.key_lock:
                    self.key = key_temp.lower()
                    if self.key == readchar.key.SPACE:
                        self.key = 'space'
                    elif self.key == readchar.key.CTRL_C:
                        self.key = 'quit'
                        self.running = False
                        break
                sleep(0.01)
            except:
                break
    
    def handle_movement(self, key):
        """Handle robot movement based on key input"""
        if key == 'w':
            self.px.set_dir_servo_angle(0)
            self.px.forward(60)
            return "🤖 Moving forward"
        elif key == 's':
            self.px.set_dir_servo_angle(0)
            self.px.backward(60)
            return "🤖 Moving backward"
        elif key == 'a':
            self.px.set_dir_servo_angle(-35)
            self.px.forward(60)
            return "🤖 Turning left"
        elif key == 'd':
            self.px.set_dir_servo_angle(35)
            self.px.forward(60)
            return "🤖 Turning right"
        elif key == 'space':
            self.say_treasure_target()
            return f"🔊 Target: {self.current_treasure}"
        else:
            self.px.stop()
            return "🤖 Stopped"
    
    def check_treasure_detection(self):
        """Check if current treasure is detected"""
        if Vilib.detect_obj_parameter['color_n'] > 0:
            # Treasure found!
            quest_time = time() - self.quest_start_time
            self.treasures_found += 1
            
            # Scoring based on speed
            time_bonus = max(0, 20 - int(quest_time))
            quest_points = 100 + time_bonus
            self.score += quest_points
            
            print(f"\n🏆 TREASURE FOUND! {self.current_treasure.upper()}")
            print(f"   Quest time: {quest_time:.1f}s")
            print(f"   Points earned: {quest_points} (+{time_bonus} time bonus)")
            print(f"   Total score: {self.score}")
            
            # Audio celebration
            self.tts.say("Treasure found! Well done!")
            
            # Generate new quest
            sleep(2)
            self.new_treasure_quest()
            
            return True
        return False


def basic_treasure_hunt():
    """Basic treasure hunt game mode"""
    print("🏴‍☠️ Basic Treasure Hunt")
    print("Manual controls with color detection quests!")
    print()
    print("Controls:")
    print("  W: Forward    S: Backward")
    print("  A: Left       D: Right")  
    print("  Space: Repeat treasure target")
    print("  Ctrl+C: Quit game")
    print()
    
    game = TreasureHuntGame()
    
    with Picarx() as px:
        game.px = px
        game.running = True
        
        # Start camera
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=True, web=True)
        sleep(1)
        
        # Start key scanning thread
        key_thread = threading.Thread(target=game.key_scan_thread)
        key_thread.daemon = True
        key_thread.start()
        
        # Start first quest
        game.new_treasure_quest()
        game_start = time()
        
        print("🏴‍☠️ Treasure hunt started! Go find some treasure!")
        
        try:
            while game.running:
                # Handle movement
                with game.key_lock:
                    if game.key:
                        if game.key == 'quit':
                            break
                        movement_result = game.handle_movement(game.key)
                        game.key = None
                
                # Check for treasure detection
                game.check_treasure_detection()
                
                # Update game time
                game.game_time = time() - game_start
                
                # Show periodic status
                if int(game.game_time) % 10 == 0 and game.game_time > 0:
                    print(f"📊 Game time: {game.game_time:.0f}s | "
                          f"Score: {game.score} | "
                          f"Treasures: {game.treasures_found}")
                
                sleep(0.1)
        
        except KeyboardInterrupt:
            pass
        
        finally:
            game.running = False
            px.stop()
            Vilib.color_detect_switch(False)
            Vilib.camera_close()
            
            # Final statistics
            print(f"\n🏴‍☠️ Treasure Hunt Complete!")
            print(f"   Game time: {game.game_time:.1f}s")
            print(f"   Treasures found: {game.treasures_found}")
            print(f"   Final score: {game.score}")
            
            if game.treasures_found > 0:
                avg_time = game.game_time / game.treasures_found
                print(f"   Average time per treasure: {avg_time:.1f}s")


def timed_treasure_hunt():
    """Timed treasure hunt with countdown"""
    print("⏰ Timed Treasure Hunt")
    print("Find as many treasures as possible within the time limit!")
    
    try:
        time_limit = int(input("Enter time limit in seconds (30-300): "))
        time_limit = max(30, min(time_limit, 300))
    except:
        time_limit = 120
    
    print(f"⏰ {time_limit} second treasure hunt starting...")
    input("Press Enter to start...")
    
    game = TreasureHuntGame()
    
    with Picarx() as px:
        game.px = px
        game.running = True
        
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=True, web=True)
        sleep(1)
        
        key_thread = threading.Thread(target=game.key_scan_thread)
        key_thread.daemon = True
        key_thread.start()
        
        game.new_treasure_quest()
        race_start = time()
        
        print(f"⏰ GO! Find treasures in {time_limit} seconds!")
        
        try:
            while game.running and (time() - race_start) < time_limit:
                remaining_time = time_limit - (time() - race_start)
                
                # Handle movement
                with game.key_lock:
                    if game.key:
                        if game.key == 'quit':
                            break
                        game.handle_movement(game.key)
                        game.key = None
                
                # Check treasure detection
                game.check_treasure_detection()
                
                # Show countdown every 10 seconds
                if int(remaining_time) % 10 == 0 and remaining_time > 0:
                    print(f"⏰ Time remaining: {remaining_time:.0f}s | "
                          f"Treasures: {game.treasures_found} | "
                          f"Score: {game.score}")
                
                sleep(0.1)
            
            # Time's up!
            final_time = time() - race_start
            px.stop()
            
            print(f"\n⏰ TIME'S UP!")
            print(f"   Final time: {final_time:.1f}s")
            print(f"   Treasures found: {game.treasures_found}")
            print(f"   Final score: {game.score}")
            
            # Performance rating
            treasures_per_minute = (game.treasures_found / final_time) * 60
            print(f"   Rate: {treasures_per_minute:.1f} treasures/minute")
            
            if treasures_per_minute > 3:
                print("🏆 LEGENDARY TREASURE HUNTER!")
            elif treasures_per_minute > 2:
                print("🥇 Expert treasure hunter!")
            elif treasures_per_minute > 1:
                print("🥈 Good treasure hunting!")
            else:
                print("🥉 Keep practicing your treasure hunting!")
        
        except KeyboardInterrupt:
            pass
        
        finally:
            game.running = False
            px.stop()
            Vilib.color_detect_switch(False)
            Vilib.camera_close()


def treasure_hunt_challenge():
    """Advanced treasure hunt with special challenges"""
    print("🏆 Treasure Hunt Challenge")
    print("Advanced mode with special challenges and multipliers!")
    
    challenge_types = [
        {"name": "Speed Demon", "description": "Find treasures in under 10 seconds", "multiplier": 2},
        {"name": "Precision Hunter", "description": "Find 3 treasures in a row", "multiplier": 3},
        {"name": "Rainbow Quest", "description": "Find all 6 colors", "multiplier": 5},
        {"name": "Lightning Round", "description": "Find 5 treasures in 60 seconds", "multiplier": 4}
    ]
    
    print("\nAvailable challenges:")
    for i, challenge in enumerate(challenge_types, 1):
        print(f"   {i}. {challenge['name']}: {challenge['description']} ({challenge['multiplier']}x points)")
    
    try:
        choice = int(input("\nSelect challenge (1-4): ")) - 1
        if 0 <= choice < len(challenge_types):
            selected_challenge = challenge_types[choice]
        else:
            selected_challenge = challenge_types[0]
    except:
        selected_challenge = challenge_types[0]
    
    print(f"\n🏆 Challenge: {selected_challenge['name']}")
    print(f"Objective: {selected_challenge['description']}")
    print(f"Score multiplier: {selected_challenge['multiplier']}x")
    input("Press Enter to start challenge...")
    
    game = TreasureHuntGame()
    
    with Picarx() as px:
        game.px = px
        game.running = True
        
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=True, web=True)
        sleep(1)
        
        key_thread = threading.Thread(target=game.key_scan_thread)
        key_thread.daemon = True
        key_thread.start()
        
        # Challenge-specific tracking
        challenge_progress = 0
        challenge_complete = False
        streak_count = 0
        colors_found = set()
        
        game.new_treasure_quest()
        challenge_start = time()
        
        print(f"🏆 {selected_challenge['name']} challenge started!")
        
        try:
            while game.running and not challenge_complete:
                # Handle movement
                with game.key_lock:
                    if game.key:
                        if game.key == 'quit':
                            break
                        game.handle_movement(game.key)
                        game.key = None
                
                # Check treasure detection with challenge tracking
                if Vilib.detect_obj_parameter['color_n'] > 0:
                    quest_time = time() - game.quest_start_time
                    game.treasures_found += 1
                    colors_found.add(game.current_treasure)
                    
                    # Challenge-specific logic
                    if selected_challenge['name'] == "Speed Demon":
                        if quest_time < 10:
                            challenge_progress += 1
                            print(f"⚡ SPEED BONUS! {quest_time:.1f}s")
                        if challenge_progress >= 3:
                            challenge_complete = True
                    
                    elif selected_challenge['name'] == "Precision Hunter":
                        if quest_time < 15:  # Reasonable time
                            streak_count += 1
                            print(f"🎯 Streak: {streak_count}/3")
                        else:
                            streak_count = 0
                        if streak_count >= 3:
                            challenge_complete = True
                    
                    elif selected_challenge['name'] == "Rainbow Quest":
                        print(f"🌈 Colors found: {len(colors_found)}/6")
                        if len(colors_found) >= 6:
                            challenge_complete = True
                    
                    elif selected_challenge['name'] == "Lightning Round":
                        elapsed = time() - challenge_start
                        if game.treasures_found >= 5 and elapsed < 60:
                            challenge_complete = True
                        elif elapsed >= 60:
                            print("⏰ Time limit exceeded!")
                            break
                    
                    # Score with multiplier
                    base_points = 100
                    multiplied_score = base_points * selected_challenge['multiplier']
                    game.score += multiplied_score
                    
                    print(f"💎 Treasure found! +{multiplied_score} points (Total: {game.score})")
                    
                    if not challenge_complete:
                        sleep(1)
                        game.new_treasure_quest()
                
                sleep(0.1)
            
            if challenge_complete:
                completion_time = time() - challenge_start
                bonus_points = max(0, 1000 - int(completion_time) * 10)
                game.score += bonus_points
                
                print(f"\n🏆 CHALLENGE COMPLETE!")
                print(f"   {selected_challenge['name']} conquered!")
                print(f"   Completion time: {completion_time:.1f}s")
                print(f"   Completion bonus: +{bonus_points} points")
                print(f"   Final score: {game.score}")
                
                game.tts.say("Challenge complete! Congratulations!")
            
        except KeyboardInterrupt:
            pass
        
        finally:
            game.running = False
            px.stop()
            Vilib.color_detect_switch(False)
            Vilib.camera_close()


def main():
    """Main function with treasure hunt game options"""
    print("🏴‍☠️ PiCar-X Treasure Hunt Game")
    print("Embark on colorful treasure hunting adventures!")
    print("=" * 50)
    
    explain_treasure_hunt()
    
    while True:
        print("\nChoose your treasure hunting adventure:")
        print("1. 🏴‍☠️ Basic treasure hunt")
        print("2. ⏰ Timed treasure hunt")
        print("3. 🏆 Treasure hunt challenge")
        print("4. ❓ Explain treasure hunt")
        print("5. 🚪 Exit")
        
        try:
            choice = input("\nEnter choice (1-5): ").strip()
            
            if choice == '1':
                basic_treasure_hunt()
            elif choice == '2':
                timed_treasure_hunt()
            elif choice == '3':
                treasure_hunt_challenge()
            elif choice == '4':
                explain_treasure_hunt()
            elif choice == '5':
                print("👋 Happy treasure hunting!")
                break
            else:
                print("⚠️ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Treasure hunt interrupted!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Check camera and audio system setup!")
    
    print("\n🏴‍☠️ Treasure hunt game complete!")


def main():
    global key
    Vilib.camera_start(vflip=False,hflip=False)
    Vilib.display(local=False,web=True)
    sleep(0.8)
    print(manual)

    sleep(1)
    _key_t = threading.Thread(target=key_scan_thread)
    _key_t.setDaemon(True)
    _key_t.start()

    tts.say("game start")
    sleep(0.05)
    renew_color_detect()
    while True:

        if Vilib.detect_obj_parameter['color_n']!=0 and Vilib.detect_obj_parameter['color_w']>100:
            tts.say("will done")
            sleep(0.05)
            renew_color_detect()

        with lock:
            if key != None and key in ('wsad'):
                car_move(key)
                sleep(0.5)
                px.stop()
                key =  None
            elif key == 'space':
                tts.say("Look for " + color)
                key =  None
            elif key == 'quit':
                _key_t.join()
                print("\n\rQuit")
                break

        sleep(0.05)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        Vilib.camera_close()
        px.stop()
        sleep(.2)