#!/usr/bin/env python3
"""
🎤 Simple Audio Capture & Playback Test

This is a minimal test to capture audio from microphone and play it back.
Perfect for testing audio quality and microphone functionality.
"""

import speech_recognition as sr
import wave
import tempfile
import subprocess
import os
from contextlib import contextmanager

@contextmanager
def suppress_alsa_warnings():
    """Suppress ALSA warnings for cleaner output"""
    original_stderr = os.dup(2)
    try:
        with open(os.devnull, 'w') as devnull:
            os.dup2(devnull.fileno(), 2)
        yield
    finally:
        os.dup2(original_stderr, 2)
        os.close(original_stderr)

def capture_and_playback():
    """Capture audio and play it back immediately"""
    print("🎤 Simple Audio Capture & Playback Test")
    print("=" * 40)
    
    # Initialize microphone
    recognizer = sr.Recognizer()
    
    try:
        with suppress_alsa_warnings():
            microphone = sr.Microphone(device_index=0)
        print("✅ Microphone initialized")
        
        # Quick calibration
        print("🔧 Calibrating microphone...")
        with suppress_alsa_warnings():
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
        print(f"✅ Calibrated! Energy threshold: {recognizer.energy_threshold:.1f}")
        
        # Record audio
        print("\n🎙️ Recording audio for 3 seconds...")
        print("Say something now!")
        
        with suppress_alsa_warnings():
            with microphone as source:
                audio = recognizer.listen(source, timeout=1, phrase_time_limit=3)
        
        print("🎤 Audio captured!")
        
        # Save and analyze audio
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_filename = temp_file.name
        
        # Write WAV data to file
        wav_data = audio.get_wav_data()
        with open(temp_filename, 'wb') as f:
            f.write(wav_data)
        
        # Get audio info
        try:
            with wave.open(temp_filename, 'rb') as wav_file:
                channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                framerate = wav_file.getframerate()
                frames = wav_file.getnframes()
                duration = frames / framerate
                
                print(f"📊 Audio Details:")
                print(f"   • Channels: {channels} ({'Mono' if channels == 1 else 'Stereo'})")
                print(f"   • Quality: {sample_width*8}-bit")
                print(f"   • Sample Rate: {framerate:,}Hz")
                print(f"   • Duration: {duration:.2f} seconds")
                print(f"   • File Size: {len(wav_data):,} bytes")
        except Exception as e:
            print(f"📊 Audio Size: {len(wav_data):,} bytes")
        
        # Play back the audio
        print("\n🔊 Playing back your recording...")
        
        with suppress_alsa_warnings():
            # Try with automatic format detection first
            result = subprocess.run(['aplay', temp_filename], 
                                  capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Playback completed successfully!")
        else:
            print("⚠️ Playback had issues")
            if result.stderr:
                print(f"Debug info: {result.stderr.strip()}")
        
        # Clean up
        os.unlink(temp_filename)
        
        return True
        
    except sr.WaitTimeoutError:
        print("⏰ No audio detected - try speaking louder or closer to microphone")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main test function"""
    print("🎵 Simple Audio Test")
    print("This will record 3 seconds of audio and play it back.\n")
    
    success = capture_and_playback()
    
    if success:
        print("\n🎉 Audio test completed!")
        print("💡 If the playback sounded clear, your microphone is working well.")
    else:
        print("\n⚠️ Audio test had issues")
        print("💡 Check microphone connection and try again.")
    
    print("\n" + "="*50)
    print("🔄 Run this script again to test multiple times")

if __name__ == "__main__":
    main()