#!/usr/bin/env python3
"""
🎤 Minimal Audio Test (Standard Library + System Commands)

Uses only built-in Python libraries + system audio commands.
No external dependencies required!
"""

import subprocess
import tempfile
import wave
import os
import time

def record_with_arecord(duration=3, sample_rate=44100):
    """Record audio using system arecord command"""
    print("🎤 Minimal Audio Test (System Commands)")
    print("=" * 38)
    
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_filename = temp_file.name
        
        print(f"🎙️ Recording {duration} seconds with arecord...")
        print("Say something now!")
        
        # Record using arecord (ALSA) - specify USB device directly
        result = subprocess.run([
            'arecord',
            '-D', 'hw:3,0',      # USB PnP Sound Device (card 3)
            '-f', 'S16_LE',      # 16-bit signed little endian
            '-c', '1',           # Mono
            '-r', str(sample_rate), # Sample rate
            '-d', str(duration), # Duration
            temp_filename
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Recording failed: {result.stderr}")
            return False
        
        print("🎤 Audio captured!")
        
        # Analyze the WAV file
        try:
            with wave.open(temp_filename, 'rb') as wav_file:
                channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                framerate = wav_file.getframerate()
                frames = wav_file.getnframes()
                duration_actual = frames / framerate
                
                file_size = os.path.getsize(temp_filename)
                
                print(f"📊 Audio Details:")
                print(f"   • Channels: {channels} ({'Mono' if channels == 1 else 'Stereo'})")
                print(f"   • Quality: {sample_width*8}-bit")
                print(f"   • Sample Rate: {framerate:,}Hz")
                print(f"   • Duration: {duration_actual:.2f} seconds")
                print(f"   • Total Frames: {frames:,}")
                print(f"   • File Size: {file_size:,} bytes")
        except Exception as e:
            print(f"📊 Could not analyze audio: {e}")
        
        # Play back using aplay
        print("\n🔊 Playing back with aplay...")
        
        result = subprocess.run([
            'aplay', temp_filename
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Playback completed!")
        else:
            print(f"⚠️ Playback issues: {result.stderr}")
        
        # Clean up
        os.unlink(temp_filename)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_audio_devices():
    """Test what audio devices are available"""
    print("\n🔍 Checking available audio devices...")
    
    # Check ALSA devices
    try:
        result = subprocess.run(['arecord', '-l'], capture_output=True, text=True)
        if result.returncode == 0:
            print("\n🎤 Available Recording Devices (ALSA):")
            print(result.stdout)
        else:
            print("⚠️ Could not list ALSA recording devices")
    except:
        print("⚠️ arecord command not available")
    
    try:
        result = subprocess.run(['aplay', '-l'], capture_output=True, text=True)
        if result.returncode == 0:
            print("🔊 Available Playback Devices (ALSA):")
            print(result.stdout)
        else:
            print("⚠️ Could not list ALSA playback devices")
    except:
        print("⚠️ aplay command not available")

def main():
    """Main test using only system commands"""
    print("🎵 Minimal Audio Test")
    print("Uses only standard Python + system audio commands.\n")
    
    # Test basic recording and playback
    success = record_with_arecord(duration=3)
    
    if success:
        print("\n🎉 Minimal audio test completed!")
        print("💡 Your system audio tools (arecord/aplay) are working.")
    else:
        print("\n⚠️ Minimal audio test had issues")
        print("💡 Check ALSA audio system and microphone connection.")
    
    # Show available devices
    test_audio_devices()
    
    print("\n" + "="*50)
    print("💡 This test uses no external Python audio libraries!")
    print("   Just standard library + system commands (arecord/aplay)")

if __name__ == "__main__":
    main()