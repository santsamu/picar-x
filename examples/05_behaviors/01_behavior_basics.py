#!/usr/bin/env python3
"""
🤖 Behavior Basics - Introduction to Robot Behaviors

This example introduces the concept of robot behaviors - complex actions
that combine multiple sensors, movement, and decision-making to create
intelligent robot responses.

Learn to:
- Understand behavior-based robotics
- Create simple reactive behaviors
- Combine sensors for complex responses
- Implement behavior state machines
- Handle behavior interruptions
- Debug behavior execution
"""

from picarx import Picarx
from vilib import Vilib
import time
import random


def explain_robot_behaviors():
    """Explain behavior-based robotics concepts"""
    print("🤖 Robot Behavior Concepts:")
    print()
    print("🧠 What are Robot Behaviors?")
    print("   • Complex actions combining sensors and movement")
    print("   • Goal-oriented responses to environment")
    print("   • State-based decision making")
    print("   • Reactive and proactive responses")
    print()
    print("🔄 Behavior Types:")
    print("   • Reactive: Immediate response to stimuli")
    print("   • Deliberative: Planned actions with goals")
    print("   • Hybrid: Combination of reactive and planned")
    print("   • Emergent: Complex behaviors from simple rules")
    print()
    print("⚙️ Behavior Components:")
    print("   • Perception: Sensor input processing")
    print("   • Decision: Logic and state management")
    print("   • Action: Motor control and movement")
    print("   • Feedback: Monitoring and adjustment")
    print()


def simple_reactive_behavior():
    """Demonstrate simple reactive behavior"""
    print("⚡ Simple Reactive Behavior")
    print("Robot reacts immediately to sensor inputs")
    print("Press Ctrl+C to stop")
    print()
    
    with Picarx() as px:
        print("🤖 Starting reactive behavior...")
        print("Place objects in front of robot to see reactions")
        
        reaction_count = 0
        start_time = time.time()
        
        try:
            while True:
                # Get sensor data
                distance = px.get_distance()
                gray_data = px.get_grayscale_data()
                left_gray = gray_data[0]
                center_gray = gray_data[1]
                right_gray = gray_data[2]
                
                # Simple reactive rules
                if distance > 0 and distance < 15:
                    # Very close obstacle - back away
                    px.backward(40)
                    px.set_dir_servo_angle(0)
                    reaction_count += 1
                    print(f"⚠️ Reaction {reaction_count}: Backing away from obstacle ({distance:.1f}cm)")
                    time.sleep(0.5)
                    
                elif distance > 0 and distance < 30:
                    # Close obstacle - turn away
                    turn_direction = random.choice([-30, 30])
                    px.set_dir_servo_angle(turn_direction)
                    px.forward(30)
                    reaction_count += 1
                    direction = "left" if turn_direction < 0 else "right"
                    print(f"🔄 Reaction {reaction_count}: Turning {direction} to avoid obstacle")
                    time.sleep(0.3)
                    
                elif any(sensor < 30 for sensor in [left_gray, center_gray, right_gray]):
                    # Dark line detected - stop and alert
                    px.stop()
                    reaction_count += 1
                    print(f"⚫ Reaction {reaction_count}: Dark line detected - stopping for safety")
                    time.sleep(1)
                    
                else:
                    # No immediate threats - explore slowly
                    px.forward(25)
                    px.set_dir_servo_angle(0)
                    
                    # Show status every few seconds
                    elapsed = time.time() - start_time
                    if int(elapsed) % 3 == 0 and elapsed > 0:
                        print(f"🔍 Exploring... {reaction_count} reactions in {elapsed:.0f}s")
                
                time.sleep(0.1)
        
        except KeyboardInterrupt:
            px.stop()
            elapsed = time.time() - start_time
            print(f"\n⚡ Reactive behavior complete: {reaction_count} reactions in {elapsed:.1f}s")


def patrol_behavior():
    """Demonstrate patrol behavior with waypoints"""
    print("🚶 Patrol Behavior")
    print("Robot follows a patrol pattern while monitoring for obstacles")
    print("Press Ctrl+C to stop")
    print()
    
    with Picarx() as px:
        patrol_points = [
            {"name": "Point A", "action": "forward", "duration": 2, "speed": 40},
            {"name": "Point B", "action": "turn_right", "duration": 1, "speed": 30},
            {"name": "Point C", "action": "forward", "duration": 2, "speed": 40},
            {"name": "Point D", "action": "turn_right", "duration": 1, "speed": 30},
        ]
        
        current_point = 0
        patrol_cycles = 0
        interruptions = 0
        
        print("🚶 Starting patrol behavior...")
        print("Robot will patrol in a square pattern")
        
        try:
            while True:
                point = patrol_points[current_point]
                print(f"📍 Moving to {point['name']} - {point['action']}")
                
                start_time = time.time()
                interrupted = False
                
                # Execute patrol action
                while time.time() - start_time < point['duration']:
                    # Check for obstacles during patrol
                    distance = px.get_distance()
                    
                    if distance > 0 and distance < 25:
                        # Obstacle detected - interrupt patrol
                        px.stop()
                        interruptions += 1
                        print(f"🛑 Patrol interrupted by obstacle at {distance:.1f}cm")
                        
                        # Wait for obstacle to clear
                        while distance > 0 and distance < 25:
                            time.sleep(0.5)
                            distance = px.get_distance()
                            print(f"⏳ Waiting for obstacle to clear... {distance:.1f}cm")
                        
                        print("✅ Obstacle cleared - resuming patrol")
                        interrupted = True
                        break
                    
                    # Continue patrol action
                    if point['action'] == 'forward':
                        px.forward(point['speed'])
                        px.set_dir_servo_angle(0)
                    elif point['action'] == 'turn_right':
                        px.set_dir_servo_angle(30)
                        px.forward(point['speed'])
                    elif point['action'] == 'turn_left':
                        px.set_dir_servo_angle(-30)
                        px.forward(point['speed'])
                    
                    time.sleep(0.1)
                
                if not interrupted:
                    px.stop()
                    print(f"✅ Reached {point['name']}")
                
                # Move to next patrol point
                current_point = (current_point + 1) % len(patrol_points)
                
                if current_point == 0:
                    patrol_cycles += 1
                    print(f"🔄 Completed patrol cycle {patrol_cycles}")
                
                time.sleep(0.5)
        
        except KeyboardInterrupt:
            px.stop()
            print(f"\n🚶 Patrol behavior complete:")
            print(f"   Cycles: {patrol_cycles}")
            print(f"   Interruptions: {interruptions}")


def follow_behavior():
    """Demonstrate following behavior using distance sensor"""
    print("👥 Follow Behavior")
    print("Robot follows objects at a safe distance")
    print("Press Ctrl+C to stop")
    print()
    
    with Picarx() as px:
        target_distance = 30  # cm
        tolerance = 5  # cm
        follow_time = 0
        adjustments = 0
        
        print(f"👥 Starting follow behavior (target: {target_distance}cm)")
        print("Move an object in front of the robot to guide it")
        
        try:
            while True:
                distance = px.get_distance()
                
                if distance < 0:
                    # No object detected - search
                    px.stop()
                    print("🔍 Searching for object to follow...")
                    time.sleep(0.5)
                    continue
                
                follow_time += 0.1
                
                if distance < target_distance - tolerance:
                    # Too close - back away
                    px.backward(30)
                    px.set_dir_servo_angle(0)
                    adjustments += 1
                    print(f"⬅️ Too close ({distance:.1f}cm) - backing away")
                    
                elif distance > target_distance + tolerance:
                    # Too far - move closer
                    if distance > 100:
                        # Object very far - move faster
                        px.forward(50)
                    else:
                        px.forward(35)
                    px.set_dir_servo_angle(0)
                    adjustments += 1
                    print(f"➡️ Too far ({distance:.1f}cm) - moving closer")
                    
                else:
                    # Perfect distance - maintain position
                    px.stop()
                    if int(follow_time) % 2 == 0:
                        print(f"✅ Following at {distance:.1f}cm (target: {target_distance}cm)")
                
                time.sleep(0.1)
        
        except KeyboardInterrupt:
            px.stop()
            print(f"\n👥 Follow behavior complete:")
            print(f"   Following time: {follow_time:.1f}s")
            print(f"   Adjustments made: {adjustments}")


def curiosity_behavior():
    """Demonstrate curiosity-driven exploration behavior"""
    print("🎭 Curiosity Behavior")
    print("Robot explores environment driven by curiosity")
    print("Press Ctrl+C to stop")
    print()
    
    with Picarx() as px:
        visited_areas = []
        exploration_time = 0
        discoveries = 0
        boredom_threshold = 10  # seconds
        current_exploration_start = time.time()
        
        print("🎭 Starting curiosity-driven exploration...")
        
        try:
            while True:
                # Basic exploration movement
                px.forward(35)
                
                # Check environment
                distance = px.get_distance()
                gray_data = px.get_grayscale_data()
                left_gray = gray_data[0]
                center_gray = gray_data[1]
                right_gray = gray_data[2]
                
                exploration_time += 0.1
                
                # Detect interesting features
                if distance > 0 and distance < 20:
                    # Close object - investigate
                    px.stop()
                    discoveries += 1
                    print(f"🔍 Discovery {discoveries}: Close object at {distance:.1f}cm - investigating...")
                    
                    # Turn camera to investigate
                    for angle in [-20, 0, 20, 0]:
                        px.set_cam_pan_angle(angle)
                        time.sleep(0.5)
                    
                    # Back away after investigation
                    px.backward(30)
                    time.sleep(1)
                    current_exploration_start = time.time()
                    
                elif any(sensor < 25 for sensor in [left_gray, center_gray, right_gray]):
                    # Interesting surface - investigate
                    px.stop()
                    discoveries += 1
                    print(f"🎨 Discovery {discoveries}: Interesting surface detected - investigating...")
                    time.sleep(2)
                    current_exploration_start = time.time()
                
                # Boredom mechanism - change direction if stuck
                elif time.time() - current_exploration_start > boredom_threshold:
                    turn_angle = random.choice([-45, -30, 30, 45])
                    px.set_dir_servo_angle(turn_angle)
                    px.forward(30)
                    print(f"😴 Getting bored - turning {abs(turn_angle)}° {'left' if turn_angle < 0 else 'right'}")
                    time.sleep(2)
                    current_exploration_start = time.time()
                
                else:
                    # Continue exploring with slight randomness
                    if random.random() < 0.1:  # 10% chance to turn slightly
                        turn_angle = random.randint(-15, 15)
                        px.set_dir_servo_angle(turn_angle)
                
                time.sleep(0.1)
        
        except KeyboardInterrupt:
            px.stop()
            print(f"\n🎭 Curiosity exploration complete:")
            print(f"   Exploration time: {exploration_time:.1f}s")
            print(f"   Discoveries made: {discoveries}")


def behavior_state_machine():
    """Demonstrate behavior using state machine"""
    print("🔄 Behavior State Machine")
    print("Robot uses states to manage complex behaviors")
    print("Press Ctrl+C to stop")
    print()
    
    states = ['EXPLORE', 'INVESTIGATE', 'AVOID', 'REST']
    current_state = 'EXPLORE'
    state_times = {state: 0 for state in states}
    state_changes = 0
    
    with Picarx() as px:
        print("🔄 Starting state machine behavior...")
        print(f"Initial state: {current_state}")
        
        state_start_time = time.time()
        
        try:
            while True:
                # Update state time
                state_times[current_state] += 0.1
                
                # State: EXPLORE
                if current_state == 'EXPLORE':
                    px.forward(30)
                    px.set_dir_servo_angle(random.randint(-10, 10))
                    
                    distance = px.get_distance()
                    if distance > 0 and distance < 25:
                        # Transition to INVESTIGATE or AVOID
                        if distance < 15:
                            current_state = 'AVOID'
                        else:
                            current_state = 'INVESTIGATE'
                        state_changes += 1
                        print(f"🔄 State change {state_changes}: EXPLORE → {current_state}")
                        state_start_time = time.time()
                
                # State: INVESTIGATE
                elif current_state == 'INVESTIGATE':
                    px.stop()
                    
                    # Look around
                    for pan_angle in [-30, 0, 30, 0]:
                        px.set_cam_pan_angle(pan_angle)
                        time.sleep(0.3)
                    
                    # Check if still interesting
                    distance = px.get_distance()
                    if distance < 0 or distance > 40:
                        current_state = 'EXPLORE'
                    elif distance < 15:
                        current_state = 'AVOID'
                    elif time.time() - state_start_time > 3:
                        current_state = 'REST'
                    
                    if current_state != 'INVESTIGATE':
                        state_changes += 1
                        print(f"🔄 State change {state_changes}: INVESTIGATE → {current_state}")
                        state_start_time = time.time()
                
                # State: AVOID
                elif current_state == 'AVOID':
                    # Back away and turn
                    px.backward(40)
                    time.sleep(0.5)
                    
                    turn_direction = random.choice([-45, 45])
                    px.set_dir_servo_angle(turn_direction)
                    px.forward(30)
                    time.sleep(1)
                    
                    # Return to exploration
                    current_state = 'EXPLORE'
                    state_changes += 1
                    print(f"🔄 State change {state_changes}: AVOID → {current_state}")
                    state_start_time = time.time()
                
                # State: REST
                elif current_state == 'REST':
                    px.stop()
                    
                    if time.time() - state_start_time > 2:
                        current_state = 'EXPLORE'
                        state_changes += 1
                        print(f"🔄 State change {state_changes}: REST → {current_state}")
                        state_start_time = time.time()
                
                time.sleep(0.1)
        
        except KeyboardInterrupt:
            px.stop()
            print(f"\n🔄 State machine behavior complete:")
            print(f"   State changes: {state_changes}")
            for state, duration in state_times.items():
                print(f"   {state}: {duration:.1f}s")


def main():
    """Main function with behavior examples"""
    print("🤖 PiCar-X Behavior Basics Tutorial")
    print("Learn intelligent robot behavior programming")
    print("=" * 50)
    
    explain_robot_behaviors()
    
    while True:
        print("\nChoose a behavior demonstration:")
        print("1. ⚡ Simple reactive behavior")
        print("2. 🚶 Patrol behavior")
        print("3. 👥 Follow behavior")
        print("4. 🎭 Curiosity behavior")
        print("5. 🔄 Behavior state machine")
        print("6. ❓ Explain robot behaviors")
        print("7. 🚪 Exit")
        
        try:
            choice = input("\nEnter choice (1-7): ").strip()
            
            if choice == '1':
                simple_reactive_behavior()
            elif choice == '2':
                patrol_behavior()
            elif choice == '3':
                follow_behavior()
            elif choice == '4':
                curiosity_behavior()
            elif choice == '5':
                behavior_state_machine()
            elif choice == '6':
                explain_robot_behaviors()
            elif choice == '7':
                print("👋 Happy behaving!")
                break
            else:
                print("⚠️ Invalid choice. Please enter 1-7.")
                
        except KeyboardInterrupt:
            print("\n👋 Behavior tutorial interrupted!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Check robot connections and sensor calibration")
    
    print("\n🤖 Behavior basics tutorial complete!")