#!/usr/bin/env python3
"""
🎤 Microphone Test - Quick test to verify voice recognition is working

This simple test will listen for speech and show if the microphone is working.
"""

# Suppress ALSA warnings at the system level
import os
os.environ['ALSA_LOG_LEVEL'] = '0'

import speech_recognition as sr
import time
import subprocess
import sys
import wave
import tempfile
from contextlib import contextmanager
from robot_hat import TTS

@contextmanager
def suppress_alsa_warnings():
    """Suppress ALSA and JACK audio warnings that flood the terminal"""
    # Save current stderr
    original_stderr = sys.stderr
    
    try:
        # Redirect stderr to devnull to hide ALSA warnings
        with open(os.devnull, 'w') as devnull:
            sys.stderr = devnull
            yield
    finally:
        # Restore original stderr
        sys.stderr = original_stderr

def play_recorded_audio(audio_data):
    """Save and play back the recorded audio for verification"""
    try:
        # Create a temporary WAV file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_filename = temp_file.name
        
        # Get the raw WAV data from the audio
        wav_data = audio_data.get_wav_data()
        
        # Write the WAV data directly to file (preserves original quality)
        with open(temp_filename, 'wb') as f:
            f.write(wav_data)
        
        # Check the actual audio format by reading the WAV header
        try:
            with wave.open(temp_filename, 'rb') as wav_file:
                channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                framerate = wav_file.getframerate()
                frames = wav_file.getnframes()
                duration = frames / framerate
                print(f"📊 Audio format: {channels} channels, {sample_width*8}-bit, {framerate}Hz, {duration:.1f}s")
        except:
            print(f"📊 Audio info: {len(wav_data)} bytes")
        
        print("🔊 Playing back recorded audio...")
        
        # Play the audio using aplay (ALSA player) with better settings
        with suppress_alsa_warnings():
            # Use aplay with specific format to ensure proper playback
            result = subprocess.run([
                'aplay', 
                '-f', 'S16_LE',  # 16-bit signed little endian
                '-r', '44100',   # Try standard sample rate first
                temp_filename
            ], capture_output=True, text=True)
            
            # If that fails, try the original format
            if result.returncode != 0:
                print("🔄 Trying alternative playback format...")
                result = subprocess.run([
                    'aplay', 
                    temp_filename
                ], capture_output=True, text=True)
            
        if result.returncode == 0:
            print("✅ Audio playback completed")
        else:
            print("⚠️ Audio playback may have had issues")
            print(f"Debug: {result.stderr}")
            
        # Clean up temporary file
        os.unlink(temp_filename)
        
    except Exception as e:
        print(f"⚠️ Could not play recorded audio: {e}")
        print("💡 This doesn't affect speech recognition functionality")

def test_microphone():
    """Test microphone and speech recognition"""
    print("🎤 Microphone Test")
    print("=" * 30)
    
    # Initialize recognizer and TTS
    recognizer = sr.Recognizer()
    tts = TTS()
    tts.lang("en-us")  # Set language for TTS
    tts.system_volume(100)
    print(f"System volume: {tts.system_volume()}")
    
    # Test USB microphone
    try:
        with suppress_alsa_warnings():
            microphone = sr.Microphone(device_index=0)  # USB PnP Sound Device
        print("✅ USB microphone initialized")
        
        # Calibrate
        print("🎤 Calibrating microphone...")
        with suppress_alsa_warnings():
            with microphone as source:
                recognizer.energy_threshold = 300
                recognizer.adjust_for_ambient_noise(source, duration=1)
        print(f"✅ Calibrated! Energy threshold: {recognizer.energy_threshold}")
        
        # Test listening
        print("\n🗣️ Say something now! (5 second test)")
        print("Try saying: 'Hello robot' or 'Testing microphone'")
        
        try:
            with suppress_alsa_warnings():
                with microphone as source:
                    # Listen for 5 seconds
                    tts.say("Processing your speech now.", blocking=True)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                
            print("🎤 Audio captured! Playing back what was recorded...")
            
            # Play back the recorded audio before recognition
            play_recorded_audio(audio)
            
            print("🤖 Now attempting speech recognition...")
            
            # Try to recognize
            try:
                text = recognizer.recognize_google(audio)
                print(f"🎯 SUCCESS! Recognized: '{text}'")
                
                # Debug: Show exactly what we're about to say
                playback_message = f"I heard you say: {text}"
                print(f"� DEBUG: About to speak: '{playback_message}'")
                
                # Play back what was heard through TTS
                print("🔊 Playing back what I heard...")
                tts.say(playback_message)
                
                return True
            except sr.UnknownValueError:
                print("⚠️ Audio captured but speech not understood")
                print("💡 This might mean the microphone is working but speech was unclear")
                
                # TTS feedback for unclear speech
                tts.say("I captured audio but could not understand what you said. Please try speaking louder or clearer.")
                
                return True  # Microphone worked, just unclear speech
            except sr.RequestError as e:
                print(f"❌ Speech recognition service error: {e}")
                print("💡 Check internet connection for Google Speech API")
                
                # TTS feedback for service error
                tts.say("Speech recognition service error. Please check your internet connection.")
                
                return False
                
        except sr.WaitTimeoutError:
            print("⚠️ No speech detected in 5 seconds")
            print("💡 Try speaking louder or closer to the microphone")
            
            # TTS feedback for timeout
            tts.say("No speech detected. Please try speaking louder or closer to the microphone.")
            
            return False
            
    except Exception as e:
        print(f"❌ Microphone initialization failed: {e}")
        
        # TTS feedback for initialization failure
        try:
            tts.say("Microphone initialization failed. Please check your microphone connection.")
        except:
            pass  # TTS might not work if there are hardware issues
            
        return False

if __name__ == "__main__":
    print("🤖 Testing AI Integration Microphone")
    print("This will help verify your voice recognition setup.\n")
    
    # Initialize TTS for announcements
    try:
        tts = TTS()
        tts.lang("en-us")
        tts.system_volume(100)
        tts.say("Starting microphone test. Please speak when prompted.")
    except:
        print("⚠️ TTS initialization issue, continuing with text output only")
    
    success = test_microphone()
    
    if success:
        print("\n🎉 Microphone test PASSED!")
        print("Your voice recognition should work in the AI examples.")
        try:
            tts.say("Microphone test passed! Voice recognition is working.")
        except:
            pass
    else:
        print("\n⚠️ Microphone test had issues")
        print("The AI examples will use simulated voice commands instead.")
        try:
            tts.say("Microphone test had issues. AI examples will use simulation mode.")
        except:
            pass
    
    print("\n💡 Run './run_microphone_test.sh' to suppress ALSA warnings for cleaner output.")