#!/usr/bin/env python3
"""
🎮 Game Basics - Introduction to Robot Gaming

This example introduces the concept of robot games - fun, interactive
applications that combine robotics with gameplay mechanics.

Learn to:
- Game design principles for robots
- Player interaction and controls
- Scoring systems and objectives
- Real-time gameplay mechanics
- Multi-modal feedback (visual, audio, haptic)
- Game state management
"""

from picarx import Picarx
from vilib import Vilib
import time
import random
import threading
from collections import deque


def explain_robot_games():
    """Explain robot gaming concepts"""
    print("🎮 Robot Gaming Concepts:")
    print()
    print("🎯 Game Design Elements:")
    print("   • Objectives: Clear goals and win conditions")
    print("   • Challenges: Obstacles and skill requirements")
    print("   • Feedback: Visual, audio, and haptic responses")
    print("   • Progression: Difficulty scaling and achievements")
    print()
    print("🕹️ Control Schemes:")
    print("   • Manual control: Direct player input")
    print("   • Autonomous: Robot plays independently")
    print("   • Hybrid: Mixed manual and autonomous control")
    print("   • Voice commands: Spoken instructions")
    print()
    print("📊 Game Mechanics:")
    print("   • Scoring: Points, time, efficiency metrics")
    print("   • Lives/Health: Failure tolerance systems")
    print("   • Power-ups: Temporary ability enhancements")
    print("   • Multiplayer: Competitive or cooperative play")
    print()


def simple_reaction_game():
    """Simple reaction time game"""
    print("⚡ Reaction Time Game")
    print("Test your reflexes with the robot!")
    print("Press spacebar when you see the robot move forward")
    print("Press Ctrl+C to quit")
    print()
    
    scores = []
    round_number = 0
    
    with Picarx() as px:
        try:
            while True:
                round_number += 1
                print(f"\n🎮 Round {round_number}")
                print("Get ready... robot will move in 1-5 seconds")
                
                # Random delay before robot moves
                delay = random.uniform(1, 5)
                time.sleep(delay)
                
                # Robot moves forward - player should react
                start_time = time.time()
                px.forward(50)
                print("🤖 GO! Press spacebar NOW!")
                
                # Wait for player input (simplified - in real implementation use proper input)
                input("Press Enter when you see the robot move: ")
                reaction_time = time.time() - start_time
                
                px.stop()
                
                # Score the reaction
                scores.append(reaction_time)
                print(f"⏱️ Reaction time: {reaction_time:.3f} seconds")
                
                if reaction_time < 0.3:
                    print("🏆 Excellent reflexes!")
                elif reaction_time < 0.5:
                    print("👍 Good reaction!")
                elif reaction_time < 1.0:
                    print("😐 Not bad, but you can do better")
                else:
                    print("🐌 Too slow! Try to react faster")
                
                # Show statistics
                if len(scores) >= 3:
                    avg_time = sum(scores) / len(scores)
                    best_time = min(scores)
                    print(f"📊 Average: {avg_time:.3f}s | Best: {best_time:.3f}s")
                
                # Ask for another round
                continue_game = input("\nPlay another round? (y/n): ").lower().strip()
                if continue_game != 'y':
                    break
        
        except KeyboardInterrupt:
            pass
        
        finally:
            px.stop()
            if scores:
                print(f"\n🎮 Game Over! Final Statistics:")
                print(f"   Rounds played: {len(scores)}")
                print(f"   Best time: {min(scores):.3f}s")
                print(f"   Average time: {sum(scores)/len(scores):.3f}s")


def obstacle_course_game():
    """Timed obstacle course game"""
    print("🏁 Obstacle Course Game")
    print("Navigate through obstacles as fast as possible!")
    print("Use WASD keys to control the robot")
    print("Avoid obstacles and reach the finish line")
    print()
    
    with Picarx() as px:
        course_times = []
        attempt = 0
        
        try:
            while True:
                attempt += 1
                print(f"\n🏁 Attempt {attempt}")
                print("Controls: W=forward, S=backward, A=left, D=right, Q=quit")
                
                start_time = time.time()
                obstacles_hit = 0
                distance_traveled = 0
                game_active = True
                
                print("🚦 Course started! Navigate to avoid obstacles...")
                
                while game_active:
                    try:
                        # Simple keyboard input simulation
                        command = input("Enter command (w/s/a/d/finish/q): ").lower().strip()
                        
                        if command == 'q':
                            game_active = False
                            break
                        elif command == 'finish':
                            game_active = False
                            course_time = time.time() - start_time
                            course_times.append((course_time, obstacles_hit))
                            
                            print(f"🏆 Course completed!")
                            print(f"   Time: {course_time:.2f} seconds")
                            print(f"   Obstacles hit: {obstacles_hit}")
                            
                            # Calculate score (lower is better)
                            penalty = obstacles_hit * 5  # 5 second penalty per obstacle
                            final_score = course_time + penalty
                            print(f"   Final score: {final_score:.2f} seconds")
                            
                            break
                        
                        elif command == 'w':
                            px.forward(40)
                            distance_traveled += 1
                            print("🤖 Moving forward...")
                        elif command == 's':
                            px.backward(40)
                            distance_traveled += 0.5
                            print("🤖 Moving backward...")
                        elif command == 'a':
                            px.set_dir_servo_angle(-30)
                            px.forward(30)
                            distance_traveled += 0.8
                            print("🤖 Turning left...")
                        elif command == 'd':
                            px.set_dir_servo_angle(30)
                            px.forward(30)
                            distance_traveled += 0.8
                            print("🤖 Turning right...")
                        
                        # Check for obstacles
                        distance = px.get_distance()
                        if distance > 0 and distance < 15:
                            obstacles_hit += 1
                            px.stop()
                            print(f"💥 Obstacle hit! Total hits: {obstacles_hit}")
                            time.sleep(1)
                        
                        time.sleep(0.5)
                        px.stop()
                        px.set_dir_servo_angle(0)
                    
                    except KeyboardInterrupt:
                        game_active = False
                        break
                
                if course_times:
                    print(f"\n📊 Course Statistics:")
                    for i, (course_time, hits) in enumerate(course_times, 1):
                        score = course_time + (hits * 5)
                        print(f"   Attempt {i}: {course_time:.2f}s, {hits} hits, Score: {score:.2f}s")
                    
                    best_score = min(time + (hits * 5) for time, hits in course_times)
                    print(f"   Best score: {best_score:.2f}s")
                
                play_again = input("\nTry the course again? (y/n): ").lower().strip()
                if play_again != 'y':
                    break
        
        except KeyboardInterrupt:
            pass
        
        finally:
            px.stop()


def memory_pattern_game():
    """Memory pattern game using robot movements"""
    print("🧠 Memory Pattern Game")
    print("Watch the robot's movement pattern and repeat it!")
    print()
    
    movements = ['forward', 'left', 'right', 'backward']
    movement_symbols = {'forward': '⬆️', 'left': '⬅️', 'right': '➡️', 'backward': '⬇️'}
    
    with Picarx() as px:
        level = 1
        score = 0
        
        try:
            while True:
                print(f"\n🧠 Level {level}")
                print(f"Pattern length: {level + 1} movements")
                
                # Generate random pattern
                pattern = [random.choice(movements) for _ in range(level + 1)]
                
                print("👀 Watch the pattern:")
                for i, move in enumerate(pattern):
                    print(f"Step {i+1}: {movement_symbols[move]} {move}")
                    
                    # Execute movement
                    if move == 'forward':
                        px.forward(40)
                    elif move == 'backward':
                        px.backward(40)
                    elif move == 'left':
                        px.set_dir_servo_angle(-30)
                        px.forward(30)
                    elif move == 'right':
                        px.set_dir_servo_angle(30)
                        px.forward(30)
                    
                    time.sleep(1)
                    px.stop()
                    px.set_dir_servo_angle(0)
                    time.sleep(0.5)
                
                print("\n🔄 Now repeat the pattern!")
                player_pattern = []
                
                for i in range(len(pattern)):
                    move = input(f"Step {i+1} - Enter movement (forward/backward/left/right): ").lower().strip()
                    if move in movements:
                        player_pattern.append(move)
                    else:
                        print("Invalid input!")
                        break
                
                # Check if pattern matches
                if player_pattern == pattern:
                    score += level * 10
                    print(f"✅ Correct! Score: {score}")
                    level += 1
                    
                    if level > 5:
                        print(f"🏆 Congratulations! You completed all levels with score: {score}")
                        break
                else:
                    print(f"❌ Wrong pattern! Game over.")
                    print(f"Correct pattern was: {[movement_symbols[m] + ' ' + m for m in pattern]}")
                    print(f"Your pattern was:    {[movement_symbols[m] + ' ' + m for m in player_pattern]}")
                    print(f"Final score: {score}")
                    break
                
                time.sleep(1)
        
        except KeyboardInterrupt:
            pass
        
        finally:
            px.stop()


def simon_says_robot():
    """Simon Says game with robot commands"""
    print("🤖 Simon Says Robot Edition")
    print("Follow commands only when 'Simon says'!")
    print()
    
    commands = [
        ("move forward", lambda px: px.forward(40)),
        ("move backward", lambda px: px.backward(40)),
        ("turn left", lambda px: (px.set_dir_servo_angle(-30), px.forward(30))),
        ("turn right", lambda px: (px.set_dir_servo_angle(30), px.forward(30))),
        ("stop", lambda px: px.stop()),
        ("camera up", lambda px: px.set_cam_tilt_angle(20)),
        ("camera down", lambda px: px.set_cam_tilt_angle(-20)),
        ("camera center", lambda px: px.set_cam_tilt_angle(0))
    ]
    
    with Picarx() as px:
        score = 0
        round_num = 0
        strikes = 0
        max_strikes = 3
        
        try:
            print(f"🎮 Simon Says Robot Game Started!")
            print(f"You have {max_strikes} strikes before game over")
            print("Commands: follow ONLY when 'Simon says' is mentioned!")
            print()
            
            while strikes < max_strikes:
                round_num += 1
                
                # Choose random command
                command_text, command_func = random.choice(commands)
                simon_says = random.choice([True, False])
                
                if simon_says:
                    instruction = f"Simon says {command_text}"
                    should_follow = True
                else:
                    instruction = f"{command_text.title()}"
                    should_follow = False
                
                print(f"Round {round_num}: {instruction}")
                
                # Get player response
                response = input("Follow command? (y/n): ").lower().strip()
                player_follows = response == 'y'
                
                # Check if correct
                if player_follows == should_follow:
                    score += 10
                    print(f"✅ Correct! Score: {score}")
                    
                    if player_follows:
                        # Execute the command
                        command_func(px)
                        time.sleep(1)
                        px.stop()
                        px.set_dir_servo_angle(0)
                        px.set_cam_tilt_angle(0)
                else:
                    strikes += 1
                    print(f"❌ Wrong! Strikes: {strikes}/{max_strikes}")
                    if should_follow:
                        print("You should have followed that command!")
                    else:
                        print("You shouldn't have followed that command!")
                
                print()
                time.sleep(0.5)
            
            print(f"🎮 Game Over!")
            print(f"Final score: {score}")
            print(f"Rounds survived: {round_num}")
        
        except KeyboardInterrupt:
            pass
        
        finally:
            px.stop()
            px.set_dir_servo_angle(0)
            px.set_cam_tilt_angle(0)


def main():
    """Main function with game options"""
    print("🎮 PiCar-X Game Basics Tutorial")
    print("Learn robot gaming and interactive applications")
    print("=" * 50)
    
    explain_robot_games()
    
    while True:
        print("\nChoose a game to play:")
        print("1. ⚡ Reaction time game")
        print("2. 🏁 Obstacle course game")
        print("3. 🧠 Memory pattern game")
        print("4. 🤖 Simon Says robot edition")
        print("5. ❓ Explain robot games")
        print("6. 🚪 Exit")
        
        try:
            choice = input("\nEnter choice (1-6): ").strip()
            
            if choice == '1':
                simple_reaction_game()
            elif choice == '2':
                obstacle_course_game()
            elif choice == '3':
                memory_pattern_game()
            elif choice == '4':
                simon_says_robot()
            elif choice == '5':
                explain_robot_games()
            elif choice == '6':
                print("👋 Thanks for playing!")
                break
            else:
                print("⚠️ Invalid choice. Please enter 1-6.")
                
        except KeyboardInterrupt:
            print("\n👋 Game interrupted!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Check robot connections and controls")
    
    print("\n🎮 Game basics tutorial complete!")