#!/usr/bin/env python3
"""
🧠 Intelligent Behaviors - AI-Driven Robot Decision Making

This example demonstrates intelligent robot behaviors using AI decision trees,
machine learning concepts, and adaptive response systems.

Learn to:
- AI-driven behavior selection
- Adaptive learning systems
- Context-aware decision making
- Intelligent goal seeking
- Behavior state machines
- Emergent behaviors from simple rules
"""

from picarx import Picarx
from time import sleep, time
from robot_hat import TTS
import random
import json
import math
from datetime import datetime, timedelta
from collections import deque


def explain_intelligent_behaviors():
    """Explain intelligent behavior concepts"""
    print("🧠 Intelligent Behaviors:")
    print()
    print("🤖 What are Intelligent Behaviors?")
    print("   • AI-driven decision making processes")
    print("   • Adaptive responses to environmental changes")
    print("   • Goal-oriented autonomous actions")
    print("   • Learning from experience and feedback")
    print()
    print("🎯 Key Components:")
    print("   • Behavior State Machines: Structured decision trees")
    print("   • Adaptive Learning: Improving through experience")
    print("   • Context Awareness: Understanding surroundings")
    print("   • Goal Seeking: Working toward objectives")
    print("   • Emergent Behaviors: Complex results from simple rules")
    print()
    print("💡 Applications:")
    print("   • Autonomous exploration and navigation")
    print("   • Adaptive interaction with humans")
    print("   • Intelligent task planning and execution")
    print("   • Self-optimizing performance")
    print()


class IntelligentBehaviorEngine:
    """AI-driven behavior engine for autonomous robot decisions"""
    
    def __init__(self):
        self.tts = TTS()
        
        # Behavior state tracking
        self.current_state = "idle"
        self.state_history = deque(maxlen=10)
        self.goal_stack = []
        
        # Environmental awareness
        self.environment = {
            "obstacles_detected": 0,
            "exploration_progress": 0.0,
            "last_movement": None,
            "stuck_counter": 0,
            "interesting_objects": []
        }
        
        # Learning and adaptation
        self.experience_memory = {
            "successful_actions": {},
            "failed_actions": {},
            "preferred_strategies": [],
            "adaptation_score": 0.5
        }
        
        # Personality traits affecting decisions
        self.personality = {
            "curiosity": 0.8,      # How much to explore
            "caution": 0.6,        # How careful to be
            "persistence": 0.7,    # How long to try something
            "sociability": 0.8,    # How much to interact
            "adaptability": 0.9    # How quickly to change strategies
        }
        
        # Behavior decision tree
        self.behavior_tree = {
            "idle": {
                "next_states": ["exploring", "socializing", "goal_seeking"],
                "triggers": {
                    "exploring": lambda: self.personality["curiosity"] > 0.5,
                    "socializing": lambda: self.personality["sociability"] > 0.7,
                    "goal_seeking": lambda: len(self.goal_stack) > 0
                }
            },
            "exploring": {
                "next_states": ["idle", "investigating", "avoiding_obstacle"],
                "triggers": {
                    "idle": lambda: self.environment["exploration_progress"] > 0.8,
                    "investigating": lambda: len(self.environment["interesting_objects"]) > 0,
                    "avoiding_obstacle": lambda: self.environment["obstacles_detected"] > 2
                }
            },
            "investigating": {
                "next_states": ["exploring", "idle", "goal_seeking"],
                "triggers": {
                    "exploring": lambda: len(self.environment["interesting_objects"]) == 0,
                    "idle": lambda: self.environment["exploration_progress"] > 0.9,
                    "goal_seeking": lambda: len(self.goal_stack) > 0
                }
            },
            "avoiding_obstacle": {
                "next_states": ["exploring", "idle", "seeking_help"],
                "triggers": {
                    "exploring": lambda: self.environment["obstacles_detected"] == 0,
                    "idle": lambda: self.environment["stuck_counter"] > 5,
                    "seeking_help": lambda: self.environment["stuck_counter"] > 8
                }
            },
            "goal_seeking": {
                "next_states": ["idle", "exploring", "celebrating"],
                "triggers": {
                    "idle": lambda: len(self.goal_stack) == 0,
                    "exploring": lambda: self.needs_more_exploration(),
                    "celebrating": lambda: self.goal_achieved()
                }
            },
            "celebrating": {
                "next_states": ["idle"],
                "triggers": {
                    "idle": lambda: True  # Always return to idle after celebrating
                }
            },
            "seeking_help": {
                "next_states": ["idle", "exploring"],
                "triggers": {
                    "idle": lambda: self.environment["stuck_counter"] == 0,
                    "exploring": lambda: self.environment["stuck_counter"] < 3
                }
            },
            "socializing": {
                "next_states": ["idle", "exploring"],
                "triggers": {
                    "idle": lambda: self.personality["sociability"] < 0.5,
                    "exploring": lambda: self.personality["curiosity"] > self.personality["sociability"]
                }
            }
        }
    
    def needs_more_exploration(self):
        """Check if more exploration is needed for current goal"""
        return self.environment["exploration_progress"] < 0.6 and len(self.goal_stack) > 0
    
    def goal_achieved(self):
        """Check if current goal has been achieved"""
        if not self.goal_stack:
            return False
        
        current_goal = self.goal_stack[-1]
        if current_goal["type"] == "exploration":
            return self.environment["exploration_progress"] >= current_goal.get("target", 0.8)
        elif current_goal["type"] == "investigation":
            return len(self.environment["interesting_objects"]) == 0
        
        return False
    
    def add_goal(self, goal_type, **kwargs):
        """Add a new goal to the goal stack"""
        goal = {"type": goal_type, "timestamp": time(), **kwargs}
        self.goal_stack.append(goal)
        print(f"🎯 New goal added: {goal_type}")
    
    def update_environment(self, **updates):
        """Update environmental awareness"""
        self.environment.update(updates)
    
    def learn_from_experience(self, action, success, context=""):
        """Learn from action outcomes to improve future decisions"""
        if success:
            if action not in self.experience_memory["successful_actions"]:
                self.experience_memory["successful_actions"][action] = 0
            self.experience_memory["successful_actions"][action] += 1
            
            # Increase adaptation score for successful actions
            self.experience_memory["adaptation_score"] = min(1.0, 
                self.experience_memory["adaptation_score"] + 0.02)
        else:
            if action not in self.experience_memory["failed_actions"]:
                self.experience_memory["failed_actions"][action] = 0
            self.experience_memory["failed_actions"][action] += 1
            
            # Slightly decrease adaptation score for failures
            self.experience_memory["adaptation_score"] = max(0.0, 
                self.experience_memory["adaptation_score"] - 0.01)
        
        print(f"📚 Learning: {action} -> {'Success' if success else 'Failure'}")
    
    def get_action_confidence(self, action):
        """Get confidence score for an action based on experience"""
        successes = self.experience_memory["successful_actions"].get(action, 0)
        failures = self.experience_memory["failed_actions"].get(action, 0)
        
        if successes + failures == 0:
            return 0.5  # Neutral confidence for untried actions
        
        return successes / (successes + failures)
    
    def decide_next_state(self):
        """Intelligent decision making for next behavior state"""
        current_behavior = self.behavior_tree.get(self.current_state, {})
        possible_states = current_behavior.get("next_states", ["idle"])
        triggers = current_behavior.get("triggers", {})
        
        # Evaluate triggers with AI weighting
        state_scores = {}
        
        for state in possible_states:
            # Base score from trigger evaluation
            trigger_func = triggers.get(state, lambda: False)
            triggered = trigger_func()
            
            base_score = 1.0 if triggered else 0.1
            
            # Modify score based on experience
            confidence = self.get_action_confidence(state)
            experience_modifier = 0.5 + (confidence * 0.5)
            
            # Personality influence
            personality_modifier = 1.0
            if state == "exploring":
                personality_modifier = self.personality["curiosity"]
            elif state == "socializing":
                personality_modifier = self.personality["sociability"]
            elif state == "avoiding_obstacle":
                personality_modifier = self.personality["caution"]
            
            # Adaptive behavior - occasionally try new things
            if random.random() < self.personality["adaptability"] * 0.1:
                personality_modifier += 0.2
            
            final_score = base_score * experience_modifier * personality_modifier
            state_scores[state] = final_score
        
        # Choose state with highest score (with some randomness)
        if state_scores:
            # Weighted random selection
            total_score = sum(state_scores.values())
            if total_score > 0:
                rand_val = random.uniform(0, total_score)
                cumulative = 0
                
                for state, score in state_scores.items():
                    cumulative += score
                    if rand_val <= cumulative:
                        return state
        
        # Fallback to random choice
        return random.choice(possible_states) if possible_states else "idle"
    
    def transition_to_state(self, new_state):
        """Transition to a new behavior state"""
        if new_state != self.current_state:
            self.state_history.append(self.current_state)
            old_state = self.current_state
            self.current_state = new_state
            
            print(f"🔄 State transition: {old_state} -> {new_state}")
            return True
        return False
    
    def get_state_description(self):
        """Get human-readable description of current state"""
        descriptions = {
            "idle": "I'm waiting and observing my surroundings.",
            "exploring": "I'm actively exploring the environment!",
            "investigating": "I found something interesting to investigate!",
            "avoiding_obstacle": "I'm carefully navigating around obstacles.",
            "goal_seeking": "I'm working toward my current objective!",
            "celebrating": "Success! I'm celebrating my achievement!",
            "seeking_help": "I might need some assistance here.",
            "socializing": "I'm ready for social interaction!"
        }
        
        return descriptions.get(self.current_state, "I'm processing what to do next.")


def autonomous_exploration():
    """Demonstrate intelligent autonomous exploration"""
    print("🗺️ Autonomous Intelligent Exploration")
    print("Watch the robot make intelligent decisions about exploration!")
    
    behavior_engine = IntelligentBehaviorEngine()
    
    # Set exploration goal
    behavior_engine.add_goal("exploration", target=0.8, description="Comprehensive area exploration")
    
    with Picarx() as px:
        print("🤖 Starting intelligent autonomous exploration...")
        behavior_engine.tts.say("Starting intelligent exploration mode!")
        
        exploration_start = time()
        exploration_steps = 0
        max_steps = 15
        
        while exploration_steps < max_steps:
            # Update environmental awareness (simulated)
            obstacles = random.choice([0, 1, 2]) if random.random() > 0.7 else 0
            progress = min(0.9, exploration_steps / max_steps)
            
            behavior_engine.update_environment(
                obstacles_detected=obstacles,
                exploration_progress=progress,
                last_movement=behavior_engine.current_state
            )
            
            # AI decision making
            next_state = behavior_engine.decide_next_state()
            behavior_engine.transition_to_state(next_state)
            
            # Execute behavior based on intelligent state
            action_success = execute_intelligent_behavior(px, behavior_engine)
            
            # Learn from experience
            behavior_engine.learn_from_experience(
                behavior_engine.current_state, 
                action_success,
                f"step_{exploration_steps}"
            )
            
            # Status update
            description = behavior_engine.get_state_description()
            print(f"🧠 Step {exploration_steps + 1}: {description}")
            
            if exploration_steps % 5 == 4:
                status = f"Exploration {(progress * 100):.0f}% complete!"
                print(f"📊 {status}")
                behavior_engine.tts.say(status)
            
            exploration_steps += 1
            sleep(1)
        
        # Completion
        behavior_engine.transition_to_state("celebrating")
        completion_msg = "Intelligent exploration complete! I learned a lot!"
        print(f"🎉 {completion_msg}")
        behavior_engine.tts.say(completion_msg)
        
        # Summary
        print(f"\n📊 Exploration Summary:")
        print(f"   Duration: {time() - exploration_start:.1f} seconds")
        print(f"   States visited: {len(set(behavior_engine.state_history))}")
        print(f"   Adaptation score: {behavior_engine.experience_memory['adaptation_score']:.2f}")
        print(f"   Successful actions: {len(behavior_engine.experience_memory['successful_actions'])}")


def execute_intelligent_behavior(px, behavior_engine):
    """Execute robot actions based on intelligent behavior state"""
    
    state = behavior_engine.current_state
    
    try:
        if state == "idle":
            # Observational pause
            sleep(0.5)
            return True
        
        elif state == "exploring":
            # Intelligent exploration movement
            movements = ["forward", "left", "right"]
            weights = [0.6, 0.2, 0.2]  # Prefer forward exploration
            
            movement = random.choices(movements, weights=weights)[0]
            
            if movement == "forward":
                px.forward(45)
                sleep(1.2)
                px.stop()
            elif movement == "left":
                px.set_dir_servo_angle(-25)
                px.forward(40)
                sleep(0.8)
                px.stop()
                px.set_dir_servo_angle(0)
            elif movement == "right":
                px.set_dir_servo_angle(25)
                px.forward(40)
                sleep(0.8)
                px.stop()
                px.set_dir_servo_angle(0)
            
            return True
        
        elif state == "investigating":
            # Careful investigation behavior
            px.forward(20)
            sleep(0.5)
            px.stop()
            
            # Look around
            px.set_dir_servo_angle(-30)
            sleep(0.5)
            px.set_dir_servo_angle(30)
            sleep(0.5)
            px.set_dir_servo_angle(0)
            
            # Clear investigated object
            if behavior_engine.environment["interesting_objects"]:
                behavior_engine.environment["interesting_objects"].pop()
            
            return True
        
        elif state == "avoiding_obstacle":
            # Intelligent obstacle avoidance
            avoidance_strategies = ["backup_turn", "side_step", "careful_forward"]
            
            strategy = random.choice(avoidance_strategies)
            
            if strategy == "backup_turn":
                px.backward(30)
                sleep(1)
                px.set_dir_servo_angle(-35)
                px.forward(40)
                sleep(1)
                px.set_dir_servo_angle(0)
                px.stop()
            elif strategy == "side_step":
                px.set_dir_servo_angle(45)
                px.forward(35)
                sleep(0.8)
                px.set_dir_servo_angle(-45)
                px.forward(35)
                sleep(0.8)
                px.set_dir_servo_angle(0)
                px.stop()
            elif strategy == "careful_forward":
                px.forward(25)
                sleep(0.5)
                px.stop()
            
            # Reduce obstacle detection after avoidance
            behavior_engine.environment["obstacles_detected"] = max(0, 
                behavior_engine.environment["obstacles_detected"] - 1)
            
            return True
        
        elif state == "goal_seeking":
            # Directed movement toward goal
            px.forward(50)
            sleep(1.5)
            px.stop()
            
            # Simulate goal progress
            if behavior_engine.goal_stack:
                current_goal = behavior_engine.goal_stack[-1]
                if current_goal["type"] == "exploration":
                    behavior_engine.environment["exploration_progress"] += 0.1
            
            return True
        
        elif state == "celebrating":
            # Celebration behavior
            for _ in range(3):
                px.set_dir_servo_angle(-20)
                sleep(0.3)
                px.set_dir_servo_angle(20)
                sleep(0.3)
            px.set_dir_servo_angle(0)
            
            # Clear completed goals
            if behavior_engine.goal_stack:
                completed = behavior_engine.goal_stack.pop()
                print(f"🎯 Goal completed: {completed['type']}")
            
            return True
        
        elif state == "seeking_help":
            # Help-seeking behavior
            behavior_engine.tts.say("I could use some guidance here!")
            
            # Reset stuck counter
            behavior_engine.environment["stuck_counter"] = 0
            
            return True
        
        elif state == "socializing":
            # Social interaction behavior
            greetings = [
                "Hello! I'm exploring intelligently!",
                "Hi there! Want to see my AI behaviors?",
                "Greetings! I'm learning as I go!"
            ]
            
            greeting = random.choice(greetings)
            print(f"🤖 Social: {greeting}")
            behavior_engine.tts.say(greeting)
            
            return True
        
        else:
            return False
    
    except Exception as e:
        print(f"⚠️ Behavior execution error: {e}")
        return False


def adaptive_personality_demo():
    """Demonstrate adaptive personality changes based on experience"""
    print("🎭 Adaptive Personality Demonstration")
    print("Watch the robot's personality adapt based on experiences!")
    
    behavior_engine = IntelligentBehaviorEngine()
    
    # Create different scenarios to test adaptation
    scenarios = [
        {
            "name": "Obstacle Course",
            "description": "Many obstacles test caution vs. curiosity",
            "obstacles": 5,
            "duration": 8
        },
        {
            "name": "Open Space",
            "description": "Free exploration encourages curiosity",
            "obstacles": 0,
            "duration": 6
        },
        {
            "name": "Social Environment",
            "description": "Interaction opportunities boost sociability",
            "obstacles": 1,
            "duration": 5
        }
    ]
    
    with Picarx() as px:
        print("🎭 Starting adaptive personality demonstration...")
        
        initial_personality = behavior_engine.personality.copy()
        print(f"🧠 Initial personality:")
        for trait, value in initial_personality.items():
            print(f"   {trait}: {value:.2f}")
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n--- Scenario {i}: {scenario['name']} ---")
            print(f"📝 {scenario['description']}")
            
            behavior_engine.tts.say(f"Starting scenario {i}: {scenario['name']}")
            
            # Set scenario conditions
            behavior_engine.update_environment(
                obstacles_detected=scenario['obstacles'],
                exploration_progress=0.0
            )
            
            # Run scenario
            scenario_start = time()
            steps = 0
            
            while (time() - scenario_start) < scenario['duration'] and steps < 8:
                # Simulate scenario effects on personality
                if scenario['name'] == "Obstacle Course":
                    # Obstacles increase caution, may decrease curiosity
                    if random.random() > 0.6:
                        behavior_engine.personality["caution"] = min(1.0, 
                            behavior_engine.personality["caution"] + 0.05)
                        behavior_engine.personality["curiosity"] = max(0.1,
                            behavior_engine.personality["curiosity"] - 0.02)
                
                elif scenario['name'] == "Open Space":
                    # Open space increases curiosity, decreases caution
                    if random.random() > 0.5:
                        behavior_engine.personality["curiosity"] = min(1.0,
                            behavior_engine.personality["curiosity"] + 0.08)
                        behavior_engine.personality["caution"] = max(0.1,
                            behavior_engine.personality["caution"] - 0.03)
                
                elif scenario['name'] == "Social Environment":
                    # Social scenarios boost sociability
                    if random.random() > 0.4:
                        behavior_engine.personality["sociability"] = min(1.0,
                            behavior_engine.personality["sociability"] + 0.06)
                
                # Execute adaptive behavior
                next_state = behavior_engine.decide_next_state()
                behavior_engine.transition_to_state(next_state)
                
                success = execute_intelligent_behavior(px, behavior_engine)
                behavior_engine.learn_from_experience(
                    behavior_engine.current_state, 
                    success, 
                    scenario['name']
                )
                
                steps += 1
                sleep(0.8)
            
            # Show personality changes
            print(f"🧠 Personality after {scenario['name']}:")
            for trait, value in behavior_engine.personality.items():
                change = value - initial_personality[trait]
                change_str = f"({change:+.2f})" if abs(change) > 0.01 else ""
                print(f"   {trait}: {value:.2f} {change_str}")
        
        # Final summary
        print(f"\n🎭 Personality Adaptation Complete!")
        print(f"📊 Final Changes:")
        
        for trait, final_value in behavior_engine.personality.items():
            initial_value = initial_personality[trait]
            total_change = final_value - initial_value
            
            if abs(total_change) > 0.05:
                direction = "increased" if total_change > 0 else "decreased"
                print(f"   {trait} {direction} by {abs(total_change):.2f}")


def goal_oriented_behavior():
    """Demonstrate goal-oriented intelligent behavior"""
    print("🎯 Goal-Oriented Behavior System")
    print("Watch the robot intelligently work toward multiple goals!")
    
    behavior_engine = IntelligentBehaviorEngine()
    
    # Set multiple goals
    goals = [
        {"type": "exploration", "target": 0.6, "description": "Explore 60% of area"},
        {"type": "investigation", "target": 3, "description": "Investigate 3 objects"},
        {"type": "social", "target": 2, "description": "Complete 2 social interactions"}
    ]
    
    for goal in goals:
        goal_type = goal.pop("type")  # Extract the type as positional argument
        behavior_engine.add_goal(goal_type, **goal)
    
    with Picarx() as px:
        print("🎯 Starting goal-oriented behavior demonstration...")
        behavior_engine.tts.say("Starting goal oriented behavior system!")
        
        print(f"📋 Active goals:")
        for i, goal in enumerate(behavior_engine.goal_stack, 1):
            print(f"   {i}. {goal['description']}")
        
        demo_start = time()
        steps = 0
        max_steps = 20
        goals_completed = 0
        
        while steps < max_steps and behavior_engine.goal_stack:
            # Simulate discovering interesting objects for investigation
            if random.random() > 0.8 and len(behavior_engine.environment["interesting_objects"]) < 2:
                behavior_engine.environment["interesting_objects"].append(f"object_{steps}")
                print(f"🔍 Discovered interesting object: object_{steps}")
            
            # Update exploration progress
            behavior_engine.environment["exploration_progress"] = min(0.9, steps / max_steps)
            
            # AI goal-oriented decision making
            next_state = behavior_engine.decide_next_state()
            
            # Check for goal completion before state transition
            if behavior_engine.goal_achieved():
                completed_goal = behavior_engine.goal_stack.pop()
                goals_completed += 1
                
                print(f"🎉 Goal completed: {completed_goal['description']}")
                behavior_engine.tts.say("Goal achieved!")
                
                # Celebrate goal completion
                behavior_engine.transition_to_state("celebrating")
            else:
                behavior_engine.transition_to_state(next_state)
            
            # Execute behavior
            success = execute_intelligent_behavior(px, behavior_engine)
            behavior_engine.learn_from_experience(
                behavior_engine.current_state,
                success,
                f"goal_step_{steps}"
            )
            
            # Status updates
            description = behavior_engine.get_state_description()
            print(f"🧠 Step {steps + 1}: {description}")
            
            if steps % 5 == 4:
                remaining_goals = len(behavior_engine.goal_stack)
                progress_msg = f"{goals_completed} goals completed, {remaining_goals} remaining"
                print(f"📊 Progress: {progress_msg}")
            
            steps += 1
            sleep(1.2)
        
        # Final summary
        total_time = time() - demo_start
        print(f"\n🎯 Goal-Oriented Behavior Complete!")
        print(f"   Duration: {total_time:.1f} seconds")
        print(f"   Goals completed: {goals_completed}")
        print(f"   Remaining goals: {len(behavior_engine.goal_stack)}")
        print(f"   Adaptation score: {behavior_engine.experience_memory['adaptation_score']:.2f}")
        
        behavior_engine.tts.say(f"Completed {goals_completed} goals successfully!")


def main():
    """Main function with intelligent behavior options"""
    print("🧠 PiCar-X Intelligent Behaviors")
    print("Experience AI-driven autonomous robot intelligence!")
    print("=" * 50)
    
    explain_intelligent_behaviors()
    
    while True:
        print("\nChoose your intelligent behavior experience:")
        print("1. 🗺️ Autonomous exploration")
        print("2. 🎭 Adaptive personality demo")
        print("3. 🎯 Goal-oriented behavior")
        print("4. ❓ Explain intelligent behaviors")
        print("5. 🚪 Exit")
        
        try:
            choice = input("\nEnter choice (1-5): ").strip()
            
            if choice == '1':
                autonomous_exploration()
            elif choice == '2':
                adaptive_personality_demo()
            elif choice == '3':
                goal_oriented_behavior()
            elif choice == '4':
                explain_intelligent_behaviors()
            elif choice == '5':
                print("👋 Keep exploring intelligent robotics!")
                break
            else:
                print("⚠️ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Intelligent behavior exploration interrupted!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Intelligent behaviors demonstrate:")
        print("   - AI decision making concepts")
        print("   - Adaptive learning systems") 
        print("   - Autonomous goal-oriented behavior")
    
    print("\n🧠 Intelligent behavior exploration complete!")