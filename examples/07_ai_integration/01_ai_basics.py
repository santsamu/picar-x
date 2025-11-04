#!/usr/bin/env python3
"""
🤖 AI Integration Basics - Introduction to AI-Powered Robotics

This example introduces fundamental concepts of integrating artificial intelligence
with robotics, covering voice commands, text-to-speech, and basic AI decision making.

Learn to:
- Text-to-speech communication
- Voice command recognition
- AI-driven decision trees
- Natural language processing basics
- Intelligent behavior patterns
- Context-aware responses
"""

from picarx import Picarx
from time import sleep, time
from robot_hat import Music, TTS
import speech_recognition as sr
import random
import threading
import queue


def explain_ai_integration():
    """Explain AI integration concepts"""
    print("🤖 AI Integration Concepts:")
    print()
    print("🧠 Key AI Components:")
    print("   • Text-to-Speech (TTS): Robot talks to users")
    print("   • Speech Recognition: Robot understands voice")
    print("   • Decision Trees: AI-based behavior selection")
    print("   • Natural Language: Understanding context")
    print("   • Machine Learning: Adaptive behaviors")
    print()
    print("🔄 AI Integration Benefits:")
    print("   • More natural human-robot interaction")
    print("   • Adaptive and intelligent responses")
    print("   • Context-aware decision making")
    print("   • Learning from user interactions")
    print()
    print("⚡ This Example Demonstrates:")
    print("   • Voice-controlled robot movements")
    print("   • AI personality and responses")
    print("   • Intelligent behavior selection")
    print("   • Context-sensitive actions")
    print()


class AIPersonality:
    """Simple AI personality system for the robot"""
    
    def __init__(self):
        self.personality_traits = {
            "friendly": 0.8,
            "curious": 0.6,
            "helpful": 0.9,
            "playful": 0.5
        }
        
        self.mood = "happy"
        self.interaction_count = 0
        self.last_command_time = time()
        
        # Response templates
        self.responses = {
            "greeting": [
                "Hello there! I'm ready for adventure!",
                "Hi! What shall we explore today?",
                "Greetings, human friend! How can I help?"
            ],
            "movement_ack": [
                "Moving as requested!",
                "On my way!",
                "Let's go!",
                "Roger that, captain!"
            ],
            "confused": [
                "I didn't quite understand that. Could you try again?",
                "Hmm, that's not clear to me. Can you rephrase?",
                "I'm still learning. Could you say that differently?"
            ],
            "goodbye": [
                "Goodbye! It was fun exploring with you!",
                "See you later! Thanks for the adventure!",
                "Until next time, my friend!"
            ]
        }
    
    def get_response(self, category, context=""):
        """Get a personality-appropriate response"""
        if category in self.responses:
            base_response = random.choice(self.responses[category])
            
            # Add personality touches
            if self.personality_traits["playful"] > 0.7 and random.random() > 0.5:
                if category == "movement_ack":
                    base_response += " Wheee!"
                elif category == "greeting":
                    base_response += " Ready for some fun!"
            
            return base_response
        return "I understand!"
    
    def update_mood(self, interaction_type):
        """Update AI mood based on interactions"""
        self.interaction_count += 1
        
        if interaction_type == "successful_command":
            if self.mood == "confused":
                self.mood = "happy"
        elif interaction_type == "failed_command":
            if self.interaction_count % 3 == 0:
                self.mood = "confused"
        
        self.last_command_time = time()


class VoiceController:
    """Voice command recognition and processing"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.command_queue = queue.Queue()
        self.listening = False
        
        # Calibrate microphone
        print("🎤 Calibrating microphone for ambient noise...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        print("✅ Microphone ready!")
        
        # Command mappings
        self.command_map = {
            "forward": ["forward", "go forward", "move forward", "ahead"],
            "backward": ["backward", "go back", "move back", "reverse"],
            "left": ["left", "turn left", "go left"],
            "right": ["right", "turn right", "go right"],
            "stop": ["stop", "halt", "freeze", "pause"],
            "hello": ["hello", "hi", "hey robot", "greetings"],
            "goodbye": ["goodbye", "bye", "see you", "exit"],
            "dance": ["dance", "move around", "show me moves"],
            "status": ["status", "how are you", "report"]
        }
    
    def listen_for_commands(self):
        """Background thread for continuous voice recognition"""
        while self.listening:
            try:
                with self.microphone as source:
                    # Listen for audio with timeout
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                
                # Recognize speech
                text = self.recognizer.recognize_google(audio).lower()
                command = self.parse_command(text)
                
                if command:
                    self.command_queue.put((command, text))
                    print(f"🎤 Heard: '{text}' -> Command: '{command}'")
                
            except sr.WaitTimeoutError:
                pass  # No speech detected, continue listening
            except sr.UnknownValueError:
                pass  # Speech not understood
            except sr.RequestError as e:
                print(f"⚠️ Speech recognition error: {e}")
                sleep(1)
            except Exception as e:
                print(f"⚠️ Voice recognition error: {e}")
                sleep(1)
    
    def parse_command(self, text):
        """Parse recognized text into robot commands"""
        text = text.lower().strip()
        
        for command, phrases in self.command_map.items():
            for phrase in phrases:
                if phrase in text:
                    return command
        
        return None
    
    def start_listening(self):
        """Start voice recognition thread"""
        self.listening = True
        self.listen_thread = threading.Thread(target=self.listen_for_commands)
        self.listen_thread.daemon = True
        self.listen_thread.start()
        print("🎤 Voice recognition started!")
    
    def stop_listening(self):
        """Stop voice recognition"""
        self.listening = False
        print("🎤 Voice recognition stopped!")


def ai_voice_control():
    """Basic AI voice control demonstration"""
    print("🤖 AI Voice Control Demo")
    print("Talk to your robot and watch it respond intelligently!")
    print()
    
    # Initialize components
    personality = AIPersonality()
    tts = TTS()
    
    # Try to initialize voice controller
    try:
        voice = VoiceController()
        voice_available = True
    except Exception as e:
        print(f"⚠️ Voice recognition not available: {e}")
        print("💡 Continuing with TTS-only demo...")
        voice_available = False
    
    with Picarx() as px:
        # Initial greeting
        greeting = personality.get_response("greeting")
        print(f"🤖 Robot: {greeting}")
        tts.say(greeting)
        
        if voice_available:
            voice.start_listening()
            print("\n🎤 Say commands like:")
            print("   • 'Hello robot'")
            print("   • 'Go forward'")
            print("   • 'Turn left'")
            print("   • 'Dance'")
            print("   • 'Goodbye'")
            print("\nPress Ctrl+C to exit")
        else:
            print("\n💡 Voice demo simulated with random commands...")
            simulated_commands = ["hello", "forward", "left", "right", "dance", "status"]
        
        try:
            demo_start = time()
            command_count = 0
            
            while True:
                if voice_available:
                    # Check for voice commands
                    try:
                        command, original_text = voice.command_queue.get(timeout=0.1)
                        
                        if command == "goodbye":
                            goodbye = personality.get_response("goodbye")
                            print(f"🤖 Robot: {goodbye}")
                            tts.say(goodbye)
                            break
                        
                        # Process command
                        response = process_ai_command(px, command, personality, original_text)
                        print(f"🤖 Robot: {response}")
                        tts.say(response)
                        
                        personality.update_mood("successful_command")
                        command_count += 1
                        
                    except queue.Empty:
                        pass  # No commands, continue
                
                else:
                    # Simulated demo mode
                    if time() - demo_start > 5:
                        command = random.choice(simulated_commands)
                        print(f"🎤 Simulated command: '{command}'")
                        
                        response = process_ai_command(px, command, personality)
                        print(f"🤖 Robot: {response}")
                        tts.say(response)
                        
                        demo_start = time()
                        command_count += 1
                        
                        if command_count >= 6:
                            goodbye = personality.get_response("goodbye")
                            print(f"🤖 Robot: {goodbye}")
                            tts.say(goodbye)
                            break
                
                sleep(0.1)
        
        except KeyboardInterrupt:
            print("\n🤖 AI demo interrupted!")
        
        finally:
            px.stop()
            if voice_available:
                voice.stop_listening()
            
            print(f"\n📊 AI Interaction Summary:")
            print(f"   Commands processed: {command_count}")
            print(f"   Robot mood: {personality.mood}")
            print(f"   Interactions: {personality.interaction_count}")


def process_ai_command(px, command, personality, original_text=""):
    """Process a command with AI personality"""
    
    if command == "hello":
        return personality.get_response("greeting")
    
    elif command == "forward":
        px.forward(50)
        sleep(1)
        px.stop()
        return personality.get_response("movement_ack")
    
    elif command == "backward":
        px.backward(50)
        sleep(1)
        px.stop()
        return personality.get_response("movement_ack")
    
    elif command == "left":
        px.set_dir_servo_angle(-30)
        px.forward(50)
        sleep(1)
        px.stop()
        px.set_dir_servo_angle(0)
        return "Turning left with style!"
    
    elif command == "right":
        px.set_dir_servo_angle(30)
        px.forward(50)
        sleep(1)
        px.stop()
        px.set_dir_servo_angle(0)
        return "Turning right as requested!"
    
    elif command == "stop":
        px.stop()
        return "Stopped! Ready for next command."
    
    elif command == "dance":
        # Simple dance routine
        px.set_dir_servo_angle(-30)
        px.forward(40)
        sleep(0.5)
        px.set_dir_servo_angle(30)
        sleep(0.5)
        px.set_dir_servo_angle(-30)
        sleep(0.5)
        px.set_dir_servo_angle(0)
        px.stop()
        
        if personality.personality_traits["playful"] > 0.6:
            return "That was fun! Did you like my dance moves?"
        else:
            return "Dance complete! How was that?"
    
    elif command == "status":
        uptime = time()
        mood_desc = personality.mood.title()
        return f"I'm feeling {mood_desc}! I've processed {personality.interaction_count} commands so far."
    
    else:
        personality.update_mood("failed_command")
        return personality.get_response("confused")


def ai_decision_tree():
    """Demonstrate AI decision-making based on conditions"""
    print("🧠 AI Decision Tree Demo")
    print("Watch the robot make intelligent decisions based on different scenarios!")
    
    tts = TTS()
    
    # Define decision scenarios
    scenarios = [
        {
            "name": "Exploration",
            "description": "Robot decides how to explore an unknown area",
            "conditions": ["obstacles_detected", "battery_level", "time_of_day"],
            "decisions": {
                "high_battery_clear_path": "I'll explore forward confidently!",
                "low_battery_obstacles": "I should be careful and conserve energy.",
                "nighttime_mode": "Night mode: I'll move slowly and carefully."
            }
        },
        {
            "name": "Social Interaction",
            "description": "Robot chooses how to interact based on user mood",
            "conditions": ["user_tone", "interaction_history", "robot_mood"],
            "decisions": {
                "happy_user": "You seem happy! Let's have some fun!",
                "sad_user": "You seem down. How can I cheer you up?",
                "new_user": "Nice to meet you! I'm excited to be your robot friend!"
            }
        },
        {
            "name": "Task Prioritization",
            "description": "Robot prioritizes tasks based on importance and urgency",
            "conditions": ["task_urgency", "resource_availability", "user_preferences"],
            "decisions": {
                "urgent_task": "This seems urgent! I'll handle it right away.",
                "routine_task": "This is a routine task. I'll complete it efficiently.",
                "complex_task": "This is complex. I'll break it down into steps."
            }
        }
    ]
    
    with Picarx() as px:
        print("🧠 Starting AI decision demonstration...")
        tts.say("Starting AI decision demonstration!")
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n--- Scenario {i}: {scenario['name']} ---")
            print(f"Context: {scenario['description']}")
            tts.say(f"Scenario {i}: {scenario['name']}")
            
            # Simulate conditions
            simulated_conditions = random.choice(list(scenario['decisions'].keys()))
            decision = scenario['decisions'][simulated_conditions]
            
            print(f"🔍 Conditions detected: {simulated_conditions.replace('_', ' ')}")
            print(f"🤖 AI Decision: {decision}")
            
            tts.say(decision)
            
            # Demonstrate decision with robot action
            if "forward" in decision.lower() or "explore" in decision.lower():
                px.forward(40)
                sleep(1)
                px.stop()
            elif "careful" in decision.lower() or "slow" in decision.lower():
                px.forward(20)
                sleep(2)
                px.stop()
            elif "fun" in decision.lower():
                # Happy wiggle
                px.set_dir_servo_angle(-20)
                sleep(0.3)
                px.set_dir_servo_angle(20)
                sleep(0.3)
                px.set_dir_servo_angle(0)
            
            sleep(2)
        
        print("\n🧠 AI Decision Tree demonstration complete!")
        tts.say("AI decision demonstration complete!")


def ai_personality_showcase():
    """Showcase different AI personality modes"""
    print("🎭 AI Personality Showcase")
    print("Experience different AI personalities for your robot!")
    
    personalities = {
        "enthusiastic": {
            "greeting": "WOW! Hello there! I'm SO excited to meet you!",
            "movement": "WHEEE! This is amazing! I love moving around!",
            "goodbye": "That was INCREDIBLE! Can't wait to see you again!"
        },
        "scientific": {
            "greeting": "Greetings. I am a research assistant robot. How may I assist your studies?",
            "movement": "Executing movement protocol. Analyzing environmental data during transit.",
            "goodbye": "Session complete. Data logged. Until our next research collaboration."
        },
        "friendly": {
            "greeting": "Hey there, friend! Great to see you today!",
            "movement": "Just going for a little stroll. Care to join me?",
            "goodbye": "Take care! Hope to see you soon!"
        },
        "mysterious": {
            "greeting": "Ah... another visitor. I have been... waiting.",
            "movement": "The path reveals itself... interesting...",
            "goodbye": "Our encounter was... significant. Perhaps we shall meet again."
        }
    }
    
    tts = TTS()
    
    with Picarx() as px:
        for name, personality in personalities.items():
            print(f"\n🎭 Personality Mode: {name.upper()}")
            print("=" * 40)
            
            tts.say(f"Personality mode: {name}")
            sleep(1)
            
            # Greeting
            print(f"🤖 Greeting: {personality['greeting']}")
            tts.say(personality['greeting'])
            sleep(2)
            
            # Movement with personality
            print(f"🤖 Movement: {personality['movement']}")
            tts.say(personality['movement'])
            
            # Demonstrate movement style
            if name == "enthusiastic":
                # Excited bouncy movement
                for _ in range(3):
                    px.forward(60)
                    sleep(0.3)
                    px.stop()
                    sleep(0.2)
            elif name == "scientific":
                # Precise, measured movement
                px.forward(30)
                sleep(2)
                px.stop()
            elif name == "friendly":
                # Casual, relaxed movement
                px.forward(45)
                sleep(1.5)
                px.stop()
            elif name == "mysterious":
                # Slow, deliberate movement
                px.forward(25)
                sleep(3)
                px.stop()
            
            sleep(1)
            
            # Goodbye
            print(f"🤖 Farewell: {personality['goodbye']}")
            tts.say(personality['goodbye'])
            sleep(2)
        
        print("\n🎭 Personality showcase complete!")


def main():
    """Main function with AI integration options"""
    print("🤖 PiCar-X AI Integration Examples")
    print("Explore the future of intelligent robotics!")
    print("=" * 50)
    
    explain_ai_integration()
    
    while True:
        print("\nChoose your AI adventure:")
        print("1. 🎤 AI voice control")
        print("2. 🧠 AI decision tree")
        print("3. 🎭 AI personality showcase")
        print("4. ❓ Explain AI integration")
        print("5. 🚪 Exit")
        
        try:
            choice = input("\nEnter choice (1-5): ").strip()
            
            if choice == '1':
                ai_voice_control()
            elif choice == '2':
                ai_decision_tree()
            elif choice == '3':
                ai_personality_showcase()
            elif choice == '4':
                explain_ai_integration()
            elif choice == '5':
                print("👋 Keep exploring AI robotics!")
                break
            else:
                print("⚠️ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 AI exploration interrupted!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Note: Some AI features require additional setup!")
        print("   - Speech recognition needs internet connection")
        print("   - Microphone access required for voice control")
    
    print("\n🤖 AI integration exploration complete!")