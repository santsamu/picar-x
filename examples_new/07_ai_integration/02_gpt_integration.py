#!/usr/bin/env python3
"""
🧠 GPT Integration - Intelligent Robot Conversations

This example demonstrates how to integrate GPT/OpenAI with your PiCar-X robot
for intelligent conversations, decision making, and contextual responses.

Learn to:
- OpenAI API integration
- Contextual robot conversations
- AI-driven behavior decisions
- Natural language command interpretation
- Dynamic response generation
- Context-aware robot personality
"""

import openai
from picarx import Picarx
from time import sleep, time
from robot_hat import TTS
import json
import random
import threading
import queue
from datetime import datetime


def explain_gpt_integration():
    """Explain GPT integration concepts"""
    print("🧠 GPT Integration Concepts:")
    print()
    print("🤖 What is GPT Integration?")
    print("   • Connect your robot to powerful AI language models")
    print("   • Enable natural conversation and decision making")
    print("   • Create context-aware and intelligent responses")
    print("   • Allow robot to understand complex instructions")
    print()
    print("⚡ Key Capabilities:")
    print("   • Natural language understanding")
    print("   • Dynamic personality and mood adaptation")
    print("   • Intelligent task planning and execution")
    print("   • Context-aware responses to situations")
    print("   • Learning from conversation history")
    print()
    print("🔧 Requirements:")
    print("   • OpenAI API key (from openai.com)")
    print("   • Internet connection")
    print("   • Python openai library")
    print("   • Text-to-speech for responses")
    print()


class GPTRobotAssistant:
    """GPT-powered robot assistant with personality and context"""
    
    def __init__(self, api_key=None):
        """Initialize the GPT robot assistant"""
        self.api_key = api_key
        self.client = None
        self.conversation_history = []
        self.robot_context = {
            "name": "PiCar-X Assistant",
            "personality": "friendly, helpful, and curious",
            "capabilities": [
                "movement (forward, backward, left, right)",
                "camera vision and object detection", 
                "sound and music playback",
                "sensor readings (ultrasonic, line following)",
                "text-to-speech communication"
            ],
            "current_mood": "happy",
            "location": "unknown",
            "battery_level": "good",
            "last_action": "none"
        }
        
        # Initialize OpenAI client if API key provided
        if api_key:
            try:
                openai.api_key = api_key
                self.client = openai
                print("✅ GPT integration ready!")
            except Exception as e:
                print(f"⚠️ GPT setup error: {e}")
                self.client = None
        else:
            print("⚠️ No OpenAI API key provided. Using mock responses.")
            self.client = None
    
    def update_context(self, key, value):
        """Update robot context information"""
        self.robot_context[key] = value
        print(f"📝 Context updated: {key} = {value}")
    
    def build_system_prompt(self):
        """Build system prompt with current robot context"""
        prompt = f"""You are {self.robot_context['name']}, a {self.robot_context['personality']} robot assistant.

Current Status:
- Mood: {self.robot_context['current_mood']}
- Location: {self.robot_context['location']}
- Battery: {self.robot_context['battery_level']}
- Last Action: {self.robot_context['last_action']}

Your Capabilities:
{chr(10).join('- ' + cap for cap in self.robot_context['capabilities'])}

Instructions:
1. Always respond as the robot, not as an AI language model
2. Keep responses concise and robot-appropriate (1-2 sentences)
3. Show personality and emotional awareness
4. When asked to move or perform actions, confirm and describe what you'll do
5. Ask clarifying questions if instructions are unclear
6. Remember and reference previous conversation context
7. Express curiosity about the world around you

Remember: You ARE the robot. Respond as if you have physical presence and capabilities."""

        return prompt
    
    def get_gpt_response(self, user_input):
        """Get response from GPT with robot context"""
        if not self.client:
            return self.get_mock_response(user_input)
        
        try:
            # Build messages with system context
            messages = [
                {"role": "system", "content": self.build_system_prompt()}
            ]
            
            # Add conversation history (last 6 messages to stay within limits)
            messages.extend(self.conversation_history[-6:])
            messages.append({"role": "user", "content": user_input})
            
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=150,
                temperature=0.7,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            gpt_response = response.choices[0].message.content.strip()
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": gpt_response})
            
            return gpt_response
            
        except Exception as e:
            print(f"⚠️ GPT API error: {e}")
            return self.get_mock_response(user_input)
    
    def get_mock_response(self, user_input):
        """Generate mock responses when GPT is unavailable"""
        user_lower = user_input.lower()
        
        # Simple keyword-based responses
        if any(word in user_lower for word in ["hello", "hi", "hey"]):
            return f"Hello! I'm {self.robot_context['name']}, ready to help!"
        
        elif any(word in user_lower for word in ["move", "go", "forward", "drive"]):
            return "I'll move forward for you! Here I go!"
        
        elif any(word in user_lower for word in ["turn", "left", "right"]):
            direction = "left" if "left" in user_lower else "right"
            return f"Turning {direction} as requested!"
        
        elif any(word in user_lower for word in ["stop", "halt", "pause"]):
            return "Stopping immediately! How can I help next?"
        
        elif any(word in user_lower for word in ["how", "status", "feeling"]):
            return f"I'm feeling {self.robot_context['current_mood']} and ready for action!"
        
        elif any(word in user_lower for word in ["what", "who", "where"]):
            return "I'm your helpful robot assistant! Ask me to move around or tell me what you'd like to explore!"
        
        elif any(word in user_lower for word in ["bye", "goodbye", "see you"]):
            return "Goodbye! It was great exploring with you today!"
        
        else:
            responses = [
                "That's interesting! Tell me more about what you'd like me to do.",
                "I'm learning every day! What would you like to explore together?",
                "I'm ready for adventure! What should we try next?",
                "That sounds fascinating! How can I help with that?"
            ]
            return random.choice(responses)
    
    def parse_action_from_response(self, response):
        """Extract actionable commands from GPT response"""
        response_lower = response.lower()
        
        if any(word in response_lower for word in ["forward", "ahead", "go"]):
            return "forward"
        elif any(word in response_lower for word in ["backward", "back", "reverse"]):
            return "backward"
        elif "left" in response_lower:
            return "left"
        elif "right" in response_lower:
            return "right"
        elif any(word in response_lower for word in ["stop", "halt", "pause"]):
            return "stop"
        elif any(word in response_lower for word in ["dance", "wiggle", "move around"]):
            return "dance"
        else:
            return None


def gpt_conversation_demo():
    """Interactive GPT conversation with robot actions"""
    print("🧠 GPT Robot Conversation Demo")
    print("Have natural conversations with your intelligent robot!")
    print()
    
    # Try to get API key
    api_key = None
    try:
        with open('/home/sam/picar-x/gpt_examples/keys.py', 'r') as f:
            content = f.read()
            if 'openai_key' in content:
                # Extract key from file
                exec(content)
                api_key = openai_key if 'openai_key' in locals() else None
    except:
        pass
    
    if not api_key:
        print("💡 Note: Using demo mode with mock responses")
        print("   To use real GPT, add your OpenAI API key to gpt_examples/keys.py")
        input("Press Enter to continue with demo...")
    
    # Initialize GPT assistant
    gpt_robot = GPTRobotAssistant(api_key)
    tts = TTS()
    
    with Picarx() as px:
        print("\n🤖 Robot: Hello! I'm your GPT-powered robot assistant!")
        print("💬 Type your messages and I'll respond intelligently!")
        print("🎮 I can also perform actions based on our conversation!")
        print("   (Type 'quit' to exit)")
        
        tts.say("Hello! I'm your GPT powered robot assistant!")
        
        # Update initial context
        gpt_robot.update_context("location", "ready position")
        gpt_robot.update_context("last_action", "initialized")
        
        conversation_count = 0
        
        try:
            while True:
                # Get user input
                user_input = input("\n🧑 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'goodbye']:
                    farewell = gpt_robot.get_gpt_response("The user is saying goodbye")
                    print(f"🤖 Robot: {farewell}")
                    tts.say(farewell)
                    break
                
                if not user_input:
                    continue
                
                print("🧠 (Thinking...)")
                
                # Get GPT response
                response = gpt_robot.get_gpt_response(user_input)
                print(f"🤖 Robot: {response}")
                tts.say(response)
                
                # Check if response indicates an action
                action = gpt_robot.parse_action_from_response(response)
                
                if action:
                    print(f"🎮 Performing action: {action}")
                    perform_robot_action(px, action, gpt_robot)
                
                conversation_count += 1
                
                # Update mood based on conversation
                if conversation_count % 3 == 0:
                    moods = ["happy", "excited", "curious", "helpful"]
                    new_mood = random.choice(moods)
                    gpt_robot.update_context("current_mood", new_mood)
        
        except KeyboardInterrupt:
            print("\n🤖 Conversation interrupted!")
        
        finally:
            px.stop()
            print(f"\n📊 Conversation Summary:")
            print(f"   Messages exchanged: {conversation_count * 2}")
            print(f"   Final mood: {gpt_robot.robot_context['current_mood']}")


def perform_robot_action(px, action, gpt_robot):
    """Perform physical robot action and update context"""
    
    if action == "forward":
        px.forward(50)
        sleep(1.5)
        px.stop()
        gpt_robot.update_context("last_action", "moved forward")
    
    elif action == "backward":
        px.backward(50)
        sleep(1.5)
        px.stop()
        gpt_robot.update_context("last_action", "moved backward")
    
    elif action == "left":
        px.set_dir_servo_angle(-30)
        px.forward(50)
        sleep(1)
        px.stop()
        px.set_dir_servo_angle(0)
        gpt_robot.update_context("last_action", "turned left")
    
    elif action == "right":
        px.set_dir_servo_angle(30)
        px.forward(50)
        sleep(1)
        px.stop()
        px.set_dir_servo_angle(0)
        gpt_robot.update_context("last_action", "turned right")
    
    elif action == "stop":
        px.stop()
        gpt_robot.update_context("last_action", "stopped")
    
    elif action == "dance":
        # Fun dance routine
        for _ in range(2):
            px.set_dir_servo_angle(-30)
            px.forward(40)
            sleep(0.5)
            px.set_dir_servo_angle(30)
            sleep(0.5)
        px.set_dir_servo_angle(0)
        px.stop()
        gpt_robot.update_context("last_action", "performed dance")
        gpt_robot.update_context("current_mood", "playful")


def gpt_autonomous_exploration():
    """GPT decides where to explore autonomously"""
    print("🗺️ GPT Autonomous Exploration")
    print("Let GPT make intelligent decisions about where to explore!")
    
    # Initialize (with mock responses for demo)
    gpt_robot = GPTRobotAssistant()
    tts = TTS()
    
    exploration_scenarios = [
        "I see an open space ahead. Should I explore it?",
        "There's something interesting to my left. What do you think?",
        "I notice a narrow passage. Should I investigate?",
        "The area ahead looks complex. How should I approach?",
        "I've been moving forward for a while. Should I change direction?"
    ]
    
    with Picarx() as px:
        print("🗺️ Starting autonomous exploration with GPT guidance...")
        tts.say("Starting autonomous exploration with GPT guidance!")
        
        gpt_robot.update_context("location", "starting position")
        gpt_robot.update_context("current_mood", "adventurous")
        
        for i in range(5):
            print(f"\n--- Exploration Step {i+1} ---")
            
            # Present scenario to GPT
            scenario = exploration_scenarios[i]
            print(f"🤖 Robot observes: {scenario}")
            
            # Get GPT decision
            decision_prompt = f"I'm exploring and {scenario.lower()} What should I do next? Keep responses short and action-oriented."
            decision = gpt_robot.get_gpt_response(decision_prompt)
            
            print(f"🧠 GPT Decision: {decision}")
            tts.say(decision)
            
            # Parse and execute action
            action = gpt_robot.parse_action_from_response(decision)
            
            if action:
                print(f"🎮 Executing: {action}")
                perform_robot_action(px, action, gpt_robot)
            else:
                # Default exploration action
                print("🎮 Continuing exploration...")
                px.forward(40)
                sleep(2)
                px.stop()
                gpt_robot.update_context("last_action", "continued exploring")
            
            # Simulate some exploration time
            sleep(1)
            
            # Update location context
            gpt_robot.update_context("location", f"exploration point {i+1}")
        
        print("\n🗺️ Autonomous exploration complete!")
        
        # Final reflection
        reflection = gpt_robot.get_gpt_response("We just completed an exploration mission. How was it?")
        print(f"🤖 Final thoughts: {reflection}")
        tts.say(reflection)


def gpt_task_planning():
    """Use GPT to plan and execute complex tasks"""
    print("📋 GPT Task Planning")
    print("Watch GPT break down complex tasks into manageable steps!")
    
    gpt_robot = GPTRobotAssistant()
    tts = TTS()
    
    # Example complex tasks
    complex_tasks = [
        "Explore the room and find the best spot for a robot charging station",
        "Navigate around obstacles while looking for colorful objects",
        "Perform a security patrol of the area",
        "Search for the optimal location for robot photography"
    ]
    
    print("\nAvailable complex tasks:")
    for i, task in enumerate(complex_tasks, 1):
        print(f"   {i}. {task}")
    
    try:
        choice = int(input("\nSelect task (1-4): ")) - 1
        if 0 <= choice < len(complex_tasks):
            selected_task = complex_tasks[choice]
        else:
            selected_task = complex_tasks[0]
    except:
        selected_task = complex_tasks[0]
    
    print(f"\n📋 Selected Task: {selected_task}")
    
    with Picarx() as px:
        tts.say(f"Planning task: {selected_task}")
        
        # Get GPT to break down the task
        planning_prompt = f"""I need to accomplish this task: {selected_task}

Please break this down into 3-4 specific, actionable steps that a robot can execute. Each step should be clear and mention specific robot actions like movement, observation, or positioning. Keep each step to one sentence."""

        plan = gpt_robot.get_gpt_response(planning_prompt)
        print(f"🧠 GPT Task Plan:\n{plan}")
        tts.say("Here's my plan for the task")
        
        # Simulate executing the plan
        steps = plan.split('. ')
        
        for i, step in enumerate(steps[:4], 1):  # Limit to 4 steps
            if step.strip():
                print(f"\n--- Step {i}: {step.strip()} ---")
                tts.say(f"Step {i}")
                
                # Determine action from step
                action = gpt_robot.parse_action_from_response(step)
                
                if action:
                    perform_robot_action(px, action, gpt_robot)
                else:
                    # Default action for exploration/observation
                    px.forward(30)
                    sleep(1.5)
                    px.stop()
                    
                    # Look around
                    px.set_dir_servo_angle(-20)
                    sleep(1)
                    px.set_dir_servo_angle(20)
                    sleep(1)
                    px.set_dir_servo_angle(0)
                
                sleep(1)
        
        # Get completion summary from GPT
        completion_prompt = f"I just completed the task: {selected_task}. Give a brief summary of what was accomplished."
        summary = gpt_robot.get_gpt_response(completion_prompt)
        
        print(f"\n✅ Task Complete!")
        print(f"📊 Summary: {summary}")
        tts.say("Task completed successfully!")


def main():
    """Main function with GPT integration options"""
    print("🧠 PiCar-X GPT Integration Examples")
    print("Experience the power of AI-driven robotics!")
    print("=" * 50)
    
    explain_gpt_integration()
    
    while True:
        print("\nChoose your GPT experience:")
        print("1. 💬 GPT conversation demo")
        print("2. 🗺️ GPT autonomous exploration")
        print("3. 📋 GPT task planning")
        print("4. ❓ Explain GPT integration")
        print("5. 🚪 Exit")
        
        try:
            choice = input("\nEnter choice (1-5): ").strip()
            
            if choice == '1':
                gpt_conversation_demo()
            elif choice == '2':
                gpt_autonomous_exploration()
            elif choice == '3':
                gpt_task_planning()
            elif choice == '4':
                explain_gpt_integration()
            elif choice == '5':
                print("👋 Keep exploring AI robotics!")
                break
            else:
                print("⚠️ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 GPT exploration interrupted!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 GPT integration requires:")
        print("   - OpenAI API key")
        print("   - Internet connection")
        print("   - pip install openai")
    
    print("\n🧠 GPT integration exploration complete!")