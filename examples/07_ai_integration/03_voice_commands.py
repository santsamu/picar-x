#!/usr/bin/env python3
"""
🎤 Advanced Voice Commands - Natural Language Robot Control

This example demonstrates advanced voice command processing with natural language
understanding, context awareness, and intelligent command interpretation.

Learn to:
- Advanced speech recognition setup
- Natural language command processing
- Context-aware voice interactions
- Multi-step voice command sequences
- Voice feedback and confirmation
- Adaptive voice recognition
"""

import speech_recognition as sr
from picarx import Picarx
from time import sleep, time
from robot_hat import Music, TTS
import threading
import queue
import json
import re
from datetime import datetime


def explain_voice_commands():
    """Explain advanced voice command concepts"""
    print("🎤 Advanced Voice Commands:")
    print()
    print("🗣️ Natural Language Processing:")
    print("   • Understand complex spoken instructions")
    print("   • Process context and follow-up commands")
    print("   • Handle variations in speech patterns")
    print("   • Recognize command intent and parameters")
    print()
    print("🔊 Voice Features:")
    print("   • Continuous voice recognition")
    print("   • Background noise filtering")
    print("   • Multiple command interpretation")
    print("   • Voice feedback and confirmations")
    print("   • Adaptive recognition improvement")
    print()
    print("🎯 Command Types:")
    print("   • Movement commands (go, turn, stop)")
    print("   • Navigation commands (explore, patrol)")
    print("   • Interaction commands (introduce, dance)")
    print("   • System commands (status, help, sleep)")
    print()


class AdvancedVoiceController:
    """Advanced voice command processor with natural language understanding"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.command_queue = queue.Queue()
        self.listening = False
        self.tts = TTS()
        
        # Voice recognition settings
        self.recognition_timeout = 2
        self.phrase_time_limit = 5
        self.ambient_noise_duration = 1
        
        # Command processing
        self.last_command_time = time()
        self.command_history = []
        self.context = {
            "last_direction": None,
            "current_mode": "normal",
            "repeat_count": 0,
            "user_name": "friend"
        }
        
        # Initialize voice recognition
        self.setup_voice_recognition()
        
        # Advanced command patterns
        self.command_patterns = {
            "movement": {
                "forward": [
                    r"go forward", r"move forward", r"drive forward", r"ahead",
                    r"go straight", r"move ahead", r"drive straight"
                ],
                "backward": [
                    r"go back", r"move back", r"drive back", r"reverse",
                    r"back up", r"go backward", r"move backward"
                ],
                "left": [
                    r"turn left", r"go left", r"move left", r"left turn",
                    r"rotate left", r"spin left"
                ],
                "right": [
                    r"turn right", r"go right", r"move right", r"right turn",
                    r"rotate right", r"spin right"
                ],
                "stop": [
                    r"stop", r"halt", r"freeze", r"pause", r"wait",
                    r"hold", r"stay", r"don't move"
                ]
            },
            "navigation": {
                "explore": [
                    r"explore", r"look around", r"search", r"investigate",
                    r"patrol", r"wander", r"roam"
                ],
                "return": [
                    r"come back", r"return", r"go home", r"come here"
                ],
                "follow": [
                    r"follow me", r"come with me", r"follow"
                ]
            },
            "interaction": {
                "introduce": [
                    r"introduce yourself", r"who are you", r"what's your name",
                    r"tell me about yourself"
                ],
                "dance": [
                    r"dance", r"show me moves", r"perform", r"wiggle",
                    r"move around", r"do something fun"
                ],
                "greet": [
                    r"hello", r"hi", r"hey", r"greetings", r"good morning",
                    r"good afternoon", r"good evening"
                ]
            },
            "system": {
                "status": [
                    r"status", r"how are you", r"report", r"check",
                    r"what's your status", r"how are you doing"
                ],
                "help": [
                    r"help", r"what can you do", r"commands", r"instructions",
                    r"what are your abilities"
                ],
                "repeat": [
                    r"repeat", r"do that again", r"once more", r"again",
                    r"repeat last command"
                ],
                "sleep": [
                    r"sleep", r"rest", r"power down", r"go to sleep",
                    r"standby", r"hibernate"
                ]
            },
            "parameters": {
                "speed": {
                    "slow": [r"slow", r"slowly", r"careful", r"gently"],
                    "fast": [r"fast", r"quickly", r"rapid", r"speed"],
                    "normal": [r"normal", r"regular", r"medium"]
                },
                "duration": {
                    "short": [r"a little", r"briefly", r"short", r"quick"],
                    "long": [r"long", r"far", r"extended", r"keep going"],
                    "normal": [r"normal", r"regular", r"standard"]
                }
            }
        }
    
    def setup_voice_recognition(self):
        """Setup and calibrate voice recognition"""
        print("🎤 Setting up advanced voice recognition...")
        
        try:
            # Calibrate for ambient noise
            print("🔧 Calibrating microphone for ambient noise...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(
                    source, 
                    duration=self.ambient_noise_duration
                )
            
            # Optimize recognition settings
            self.recognizer.energy_threshold = 300
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8
            self.recognizer.phrase_threshold = 0.3
            
            print("✅ Voice recognition ready!")
            print("💡 Try saying:")
            print("   • 'Hello robot'")
            print("   • 'Go forward slowly'")
            print("   • 'Turn left and explore'")
            print("   • 'Dance for me'")
            
        except Exception as e:
            print(f"⚠️ Voice setup error: {e}")
            raise
    
    def listen_for_commands(self):
        """Advanced continuous voice recognition with context"""
        while self.listening:
            try:
                with self.microphone as source:
                    # Listen for audio with timeout
                    audio = self.recognizer.listen(
                        source, 
                        timeout=self.recognition_timeout,
                        phrase_time_limit=self.phrase_time_limit
                    )
                
                # Recognize speech
                text = self.recognizer.recognize_google(audio).lower()
                
                if text.strip():
                    command_data = self.process_natural_language(text)
                    if command_data:
                        self.command_queue.put(command_data)
                        print(f"🎤 Recognized: '{text}' -> {command_data}")
                
            except sr.WaitTimeoutError:
                pass  # No speech detected, continue
            except sr.UnknownValueError:
                pass  # Speech not understood
            except sr.RequestError as e:
                print(f"⚠️ Speech service error: {e}")
                sleep(2)
            except Exception as e:
                print(f"⚠️ Voice recognition error: {e}")
                sleep(1)
    
    def process_natural_language(self, text):
        """Process natural language input into structured commands"""
        text = text.lower().strip()
        
        # Handle multi-part commands (e.g., "turn left and go forward")
        if " and " in text:
            parts = text.split(" and ")
            # Process first part, queue others
            main_command = self.parse_single_command(parts[0])
            if main_command and len(parts) > 1:
                main_command["follow_up"] = [self.parse_single_command(part) for part in parts[1:]]
            return main_command
        else:
            return self.parse_single_command(text)
    
    def parse_single_command(self, text):
        """Parse a single command with parameters"""
        text = text.strip()
        
        # Extract command type and action
        command_data = {
            "text": text,
            "type": None,
            "action": None,
            "parameters": {},
            "timestamp": datetime.now()
        }
        
        # Check each command category
        for category, actions in self.command_patterns.items():
            if category == "parameters":
                continue
                
            for action, patterns in actions.items():
                for pattern in patterns:
                    if re.search(pattern, text):
                        command_data["type"] = category
                        command_data["action"] = action
                        break
                if command_data["action"]:
                    break
            if command_data["action"]:
                break
        
        if not command_data["action"]:
            return None
        
        # Extract parameters
        command_data["parameters"] = self.extract_parameters(text)
        
        # Update context
        if command_data["type"] == "movement":
            self.context["last_direction"] = command_data["action"]
        
        return command_data
    
    def extract_parameters(self, text):
        """Extract speed, duration, and other parameters from command"""
        parameters = {}
        
        # Extract speed parameters
        for speed, patterns in self.command_patterns["parameters"]["speed"].items():
            for pattern in patterns:
                if re.search(pattern, text):
                    parameters["speed"] = speed
                    break
        
        # Extract duration parameters  
        for duration, patterns in self.command_patterns["parameters"]["duration"].items():
            for pattern in patterns:
                if re.search(pattern, text):
                    parameters["duration"] = duration
                    break
        
        # Extract numbers (for distance, time, etc.)
        numbers = re.findall(r'\b\d+\b', text)
        if numbers:
            parameters["number"] = int(numbers[0])
        
        # Extract directional modifiers
        if "very" in text:
            parameters["intensity"] = "high"
        elif "little" in text or "bit" in text:
            parameters["intensity"] = "low"
        
        return parameters
    
    def start_listening(self):
        """Start voice recognition thread"""
        self.listening = True
        self.listen_thread = threading.Thread(target=self.listen_for_commands)
        self.listen_thread.daemon = True
        self.listen_thread.start()
        print("🎤 Advanced voice recognition started!")
    
    def stop_listening(self):
        """Stop voice recognition"""
        self.listening = False
        print("🎤 Voice recognition stopped!")
    
    def get_confirmation_response(self, action):
        """Generate contextual confirmation responses"""
        confirmations = {
            "forward": ["Moving forward!", "Going ahead!", "On my way forward!"],
            "backward": ["Moving backward!", "Going back!", "Reversing!"],
            "left": ["Turning left!", "Going left!", "Left turn coming up!"],
            "right": ["Turning right!", "Going right!", "Right turn executed!"],
            "stop": ["Stopping now!", "Halted!", "Standing by!"],
            "explore": ["Starting exploration!", "Let's explore!", "Adventure time!"],
            "dance": ["Time to dance!", "Watch my moves!", "Let's boogie!"],
            "introduce": ["Hello! I'm your PiCar-X robot assistant!"],
            "greet": ["Hello there!", "Hi friend!", "Great to see you!"]
        }
        
        if action in confirmations:
            return confirmations[action][self.context["repeat_count"] % len(confirmations[action])]
        else:
            return f"Executing {action}!"


def advanced_voice_control():
    """Advanced voice control with natural language processing"""
    print("🎤 Advanced Voice Control System")
    print("Experience natural language robot interaction!")
    print()
    
    # Initialize voice controller
    try:
        voice_controller = AdvancedVoiceController()
    except Exception as e:
        print(f"⚠️ Could not initialize voice recognition: {e}")
        print("💡 Make sure you have a microphone connected!")
        return
    
    with Picarx() as px:
        voice_controller.start_listening()
        
        print("🎤 Advanced voice control active!")
        print("💬 Try natural commands like:")
        print("   • 'Go forward slowly'")
        print("   • 'Turn left and explore'")
        print("   • 'Dance for me'")
        print("   • 'What's your status?'")
        print("\nPress Ctrl+C to exit")
        
        # Initial greeting
        voice_controller.tts.say("Hello! Advanced voice control is ready. What would you like me to do?")
        
        try:
            while True:
                try:
                    # Get voice command with timeout
                    command_data = voice_controller.command_queue.get(timeout=0.5)
                    
                    # Process command
                    response = process_advanced_command(px, command_data, voice_controller)
                    
                    if response:
                        print(f"🤖 Robot: {response}")
                        voice_controller.tts.say(response)
                    
                    # Update command history
                    voice_controller.command_history.append(command_data)
                    if len(voice_controller.command_history) > 10:
                        voice_controller.command_history.pop(0)
                    
                    # Process follow-up commands
                    if "follow_up" in command_data and command_data["follow_up"]:
                        sleep(1)  # Brief pause between commands
                        for follow_up in command_data["follow_up"]:
                            if follow_up:
                                follow_response = process_advanced_command(px, follow_up, voice_controller)
                                if follow_response:
                                    print(f"🤖 Robot: {follow_response}")
                                    voice_controller.tts.say(follow_response)
                                sleep(0.5)
                
                except queue.Empty:
                    continue  # No commands, keep listening
                
        except KeyboardInterrupt:
            print("\n🎤 Voice control interrupted!")
        
        finally:
            px.stop()
            voice_controller.stop_listening()
            
            # Summary
            print(f"\n📊 Voice Session Summary:")
            print(f"   Commands processed: {len(voice_controller.command_history)}")
            print(f"   Last mode: {voice_controller.context['current_mode']}")


def process_advanced_command(px, command_data, voice_controller):
    """Process advanced command with parameters and context"""
    
    action = command_data["action"]
    parameters = command_data["parameters"]
    
    # Determine speed based on parameters
    speed_map = {"slow": 30, "normal": 50, "fast": 70}
    speed = speed_map.get(parameters.get("speed", "normal"), 50)
    
    # Determine duration
    duration_map = {"short": 0.8, "normal": 1.5, "long": 3.0}
    duration = duration_map.get(parameters.get("duration", "normal"), 1.5)
    
    # Process command by type
    if command_data["type"] == "movement":
        return process_movement_command(px, action, speed, duration, voice_controller)
    
    elif command_data["type"] == "navigation":
        return process_navigation_command(px, action, parameters, voice_controller)
    
    elif command_data["type"] == "interaction":
        return process_interaction_command(px, action, voice_controller)
    
    elif command_data["type"] == "system":
        return process_system_command(px, action, voice_controller)
    
    else:
        return "I'm not sure how to do that yet."


def process_movement_command(px, action, speed, duration, voice_controller):
    """Process movement commands with parameters"""
    
    response = voice_controller.get_confirmation_response(action)
    
    if action == "forward":
        px.forward(speed)
        sleep(duration)
        px.stop()
    
    elif action == "backward":
        px.backward(speed)
        sleep(duration)
        px.stop()
    
    elif action == "left":
        px.set_dir_servo_angle(-30)
        px.forward(speed)
        sleep(duration)
        px.stop()
        px.set_dir_servo_angle(0)
    
    elif action == "right":
        px.set_dir_servo_angle(30)
        px.forward(speed)
        sleep(duration)
        px.stop()
        px.set_dir_servo_angle(0)
    
    elif action == "stop":
        px.stop()
    
    return response


def process_navigation_command(px, action, parameters, voice_controller):
    """Process navigation commands"""
    
    if action == "explore":
        voice_controller.context["current_mode"] = "exploring"
        
        # Simple exploration pattern
        directions = [-30, 0, 30, 0]
        for angle in directions:
            px.set_dir_servo_angle(angle)
            px.forward(40)
            sleep(1)
            px.stop()
            sleep(0.5)
        
        px.set_dir_servo_angle(0)
        return "Exploration complete! That was interesting!"
    
    elif action == "return":
        # Simple return movement (backing up)
        px.backward(40)
        sleep(2)
        px.stop()
        return "I'm back!"
    
    elif action == "follow":
        voice_controller.context["current_mode"] = "following"
        return "I'm ready to follow you! Keep talking so I know where you are."
    
    return "Navigation command executed!"


def process_interaction_command(px, action, voice_controller):
    """Process interaction commands"""
    
    if action == "introduce":
        intro = f"Hello {voice_controller.context['user_name']}! I'm your advanced PiCar-X robot. I can understand natural language commands and respond intelligently!"
        return intro
    
    elif action == "dance":
        # Fun dance routine
        dance_moves = [
            (-30, 0.5), (30, 0.5), (-30, 0.5), (30, 0.5), (0, 0.5)
        ]
        
        for angle, duration in dance_moves:
            px.set_dir_servo_angle(angle)
            px.forward(45)
            sleep(duration)
        
        px.stop()
        px.set_dir_servo_angle(0)
        return "How was that dance? I've been practicing!"
    
    elif action == "greet":
        greetings = [
            f"Hello {voice_controller.context['user_name']}!",
            "Hi there! Great to see you!",
            "Greetings! Ready for some fun?"
        ]
        return greetings[voice_controller.context["repeat_count"] % len(greetings)]
    
    return "Interaction complete!"


def process_system_command(px, action, voice_controller):
    """Process system commands"""
    
    if action == "status":
        mode = voice_controller.context["current_mode"]
        commands_count = len(voice_controller.command_history)
        
        return f"I'm feeling great! Current mode: {mode}. I've processed {commands_count} commands today."
    
    elif action == "help":
        return "I understand natural language! Try saying 'go forward slowly', 'turn left and explore', or 'dance for me'!"
    
    elif action == "repeat":
        if voice_controller.command_history:
            last_command = voice_controller.command_history[-1]
            voice_controller.context["repeat_count"] += 1
            return f"Repeating: {last_command['text']}"
        else:
            return "I don't have a previous command to repeat."
    
    elif action == "sleep":
        voice_controller.context["current_mode"] = "sleeping"
        px.stop()
        return "Going to sleep mode. Say 'hello' to wake me up!"
    
    return "System command processed!"


def voice_command_training():
    """Voice recognition training and calibration"""
    print("🏋️ Voice Command Training")
    print("Improve voice recognition accuracy through training!")
    
    training_phrases = [
        "Go forward",
        "Turn left",
        "Turn right", 
        "Go backward",
        "Stop now",
        "Dance for me",
        "What's your status",
        "Hello robot"
    ]
    
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    print("🎤 Training voice recognition...")
    print("💡 This will help the robot understand your voice better!")
    
    # Calibrate for ambient noise
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
    
    accuracy_scores = []
    
    for i, phrase in enumerate(training_phrases, 1):
        print(f"\n📢 Training {i}/{len(training_phrases)}")
        print(f"Please say: '{phrase}'")
        input("Press Enter when ready to speak...")
        
        try:
            with microphone as source:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
            
            recognized = recognizer.recognize_google(audio).lower()
            expected = phrase.lower()
            
            print(f"🎤 You said: '{recognized}'")
            print(f"📝 Expected: '{expected}'")
            
            # Simple accuracy calculation
            words_expected = set(expected.split())
            words_recognized = set(recognized.split())
            
            if words_expected and words_recognized:
                accuracy = len(words_expected.intersection(words_recognized)) / len(words_expected)
                accuracy_scores.append(accuracy)
                
                if accuracy > 0.8:
                    print("✅ Excellent recognition!")
                elif accuracy > 0.5:
                    print("👍 Good recognition!")
                else:
                    print("⚠️ Try speaking more clearly")
            
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            accuracy_scores.append(0)
        except sr.RequestError as e:
            print(f"❌ Recognition service error: {e}")
            accuracy_scores.append(0)
        except Exception as e:
            print(f"❌ Error: {e}")
            accuracy_scores.append(0)
    
    # Training summary
    avg_accuracy = sum(accuracy_scores) / len(accuracy_scores) if accuracy_scores else 0
    print(f"\n🏆 Training Complete!")
    print(f"   Average accuracy: {avg_accuracy:.1%}")
    
    if avg_accuracy > 0.8:
        print("   🌟 Excellent! Voice recognition should work great!")
    elif avg_accuracy > 0.6:
        print("   👍 Good! You can start using voice commands.")
    else:
        print("   💡 Consider speaking more clearly or adjusting microphone settings.")


def main():
    """Main function with advanced voice command options"""
    print("🎤 PiCar-X Advanced Voice Commands")
    print("Experience natural language robot control!")
    print("=" * 50)
    
    explain_voice_commands()
    
    while True:
        print("\nChoose your voice experience:")
        print("1. 🎤 Advanced voice control")
        print("2. 🏋️ Voice command training")
        print("3. ❓ Explain voice commands")
        print("4. 🚪 Exit")
        
        try:
            choice = input("\nEnter choice (1-4): ").strip()
            
            if choice == '1':
                advanced_voice_control()
            elif choice == '2':
                voice_command_training()
            elif choice == '3':
                explain_voice_commands()
            elif choice == '4':
                print("👋 Keep exploring voice robotics!")
                break
            else:
                print("⚠️ Invalid choice. Please enter 1-4.")
                
        except KeyboardInterrupt:
            print("\n👋 Voice exploration interrupted!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Voice commands require:")
        print("   - Working microphone")
        print("   - Internet connection")
        print("   - pip install SpeechRecognition")
        print("   - pip install pyaudio")
    
    print("\n🎤 Voice command exploration complete!")