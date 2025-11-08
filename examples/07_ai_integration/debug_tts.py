#!/usr/bin/env python3
"""
Debug TTS - Test if TTS is working correctly with variable text
"""

from robot_hat import TTS
import time

def test_tts_with_variables():
    """Test TTS with different variable texts"""
    print("🔊 TTS Debug Test")
    print("=" * 30)
    
    tts = TTS()
    tts.lang("en-US")
    
    # Test 1: Simple static message
    print("Test 1: Static message")
    tts.say("This is a static test message")
    time.sleep(2)
    
    # Test 2: Variable message
    print("Test 2: Variable message")
    user_input = "hello robot"
    message = f"I heard you say: {user_input}"
    print(f"Message to speak: '{message}'")
    tts.say(message)
    time.sleep(2)
    
    # Test 3: Different variable
    print("Test 3: Different variable")
    different_text = "testing microphone"
    message2 = f"You said: {different_text}"
    print(f"Message to speak: '{message2}'")
    tts.say(message2)
    time.sleep(2)
    
    # Test 4: Direct variable
    print("Test 4: Direct variable")
    direct_message = "The recognition result was: " + user_input
    print(f"Message to speak: '{direct_message}'")
    tts.say(direct_message)
    
    print("TTS debug test complete!")

if __name__ == "__main__":
    test_tts_with_variables()