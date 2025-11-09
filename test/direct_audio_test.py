#!/usr/bin/env python3
"""
🎤 Direct Audio Capture & Playback Test (No Speech Recognition Library)

This uses sounddevice for direct audio hardware access.
Much simpler and doesn't require speech recognition dependencies.
"""

try:
    import sounddevice as sd
    import numpy as np
    import wave
    import tempfile
    import os
    SOUNDDEVICE_AVAILABLE = True
except ImportError:
    SOUNDDEVICE_AVAILABLE = False
    print("⚠️ sounddevice not installed. Install with: pip install sounddevice numpy")

def list_audio_devices():
    """List available audio devices"""
    if not SOUNDDEVICE_AVAILABLE:
        return
        
    print("🎤 Available Audio Devices:")
    print(sd.query_devices())
    print()

def test_audio_settings():
    """Test different audio settings to find what works"""
    if not SOUNDDEVICE_AVAILABLE:
        return None
        
    print("🔧 Testing audio settings...")
    
    # Test configurations (sample_rate, blocksize) - using supported rates
    test_configs = [
        (44100, 4096),  # CD quality, large buffer
        (48000, 4096),  # DVD quality, large buffer  
        (44100, 2048),  # CD quality, medium buffer
        (48000, 2048),  # DVD quality, medium buffer
    ]
    
    for sample_rate, blocksize in test_configs:
        try:
            print(f"   Testing {sample_rate}Hz, blocksize {blocksize}...")
            # Quick 0.5 second test
            audio_data = sd.rec(int(0.5 * sample_rate), 
                               samplerate=sample_rate, 
                               channels=1,
                               dtype='int16',
                               blocksize=blocksize)
            sd.wait()
            print(f"   ✅ {sample_rate}Hz works!")
            return (sample_rate, blocksize)
        except Exception as e:
            print(f"   ❌ {sample_rate}Hz failed: {e}")
            continue
    
    return None

def capture_and_playback_sounddevice():
    """Capture and playback using sounddevice"""
    if not SOUNDDEVICE_AVAILABLE:
        return False
        
    print("🎤 Direct Audio Capture & Playback (sounddevice)")
    print("=" * 45)
    
    # Audio parameters - using supported sample rates
    sample_rate = 44100  # USB mic supports 44100 and 48000
    duration = 3.0  # seconds
    channels = 1  # Mono
    blocksize = 2048  # Larger buffer size to prevent overflow
    
    try:
        print(f"🎙️ Recording {duration} seconds of audio...")
        print("Say something now!")
        
        # Record audio with better error handling
        try:
            audio_data = sd.rec(int(duration * sample_rate), 
                               samplerate=sample_rate, 
                               channels=channels,
                               dtype='int16',
                               blocksize=blocksize)
            sd.wait()  # Wait for recording to complete
            
            print("🎤 Audio captured!")
        except Exception as e:
            if "Input overflowed" in str(e):
                print("⚠️ Audio buffer overflow - trying with larger buffer...")
                # Try again with larger buffer
                blocksize = 4096
                audio_data = sd.rec(int(duration * sample_rate), 
                                   samplerate=sample_rate, 
                                   channels=channels,
                                   dtype='int16',
                                   blocksize=blocksize)
                sd.wait()
                print("🎤 Audio captured with larger buffer!")
            else:
                raise e
        print(f"📊 Audio Details:")
        print(f"   • Sample Rate: {sample_rate:,}Hz")
        print(f"   • Channels: {channels} (Mono)")
        print(f"   • Duration: {duration} seconds")
        print(f"   • Data Shape: {audio_data.shape}")
        print(f"   • Data Type: {audio_data.dtype}")
        
        # Save to WAV file (optional)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_filename = temp_file.name
            
        with wave.open(temp_filename, 'wb') as wav_file:
            wav_file.setnchannels(channels)
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())
        
        file_size = os.path.getsize(temp_filename)
        print(f"   • File Size: {file_size:,} bytes")
        
        # Play back the audio
        print("\n🔊 Playing back your recording...")
        sd.play(audio_data, samplerate=sample_rate)
        sd.wait()  # Wait for playback to complete
        
        print("✅ Playback completed!")
        
        # Clean up
        os.unlink(temp_filename)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# Alternative using PyAudio (if sounddevice not available)
try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False

def capture_and_playback_pyaudio():
    """Capture and playback using PyAudio"""
    if not PYAUDIO_AVAILABLE:
        print("⚠️ PyAudio not installed. Install with: pip install pyaudio")
        return False
        
    print("🎤 Direct Audio Capture & Playback (PyAudio)")
    print("=" * 42)
    
    # Audio parameters - using supported sample rates
    FORMAT = pyaudio.paInt16  # 16-bit
    CHANNELS = 1              # Mono
    RATE = 44100             # USB mic supports 44100 and 48000
    CHUNK = 4096             # Large buffer to prevent overflow
    RECORD_SECONDS = 3
    
    try:
        audio = pyaudio.PyAudio()
        
        # Open microphone stream
        stream = audio.open(format=FORMAT,
                          channels=CHANNELS,
                          rate=RATE,
                          input=True,
                          frames_per_buffer=CHUNK)
        
        print(f"🎙️ Recording {RECORD_SECONDS} seconds...")
        print("Say something now!")
        
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        
        print("🎤 Audio captured!")
        
        # Stop recording
        stream.stop_stream()
        stream.close()
        
        # Audio info
        total_frames = len(frames) * CHUNK
        duration = total_frames / RATE
        data_size = sum(len(frame) for frame in frames)
        
        print(f"📊 Audio Details:")
        print(f"   • Sample Rate: {RATE:,}Hz")
        print(f"   • Channels: {CHANNELS} (Mono)")
        print(f"   • Duration: {duration:.2f} seconds")
        print(f"   • Total Frames: {total_frames:,}")
        print(f"   • Data Size: {data_size:,} bytes")
        
        # Play back
        print("\n🔊 Playing back your recording...")
        
        stream = audio.open(format=FORMAT,
                          channels=CHANNELS,
                          rate=RATE,
                          output=True)
        
        for frame in frames:
            stream.write(frame)
        
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        print("✅ Playback completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main test function - try different libraries"""
    print("🎵 Direct Audio Test (Multiple Libraries)")
    print("This tests audio capture without speech recognition library.\n")
    
    success = False
    
    # Try sounddevice first (recommended)
    if SOUNDDEVICE_AVAILABLE:
        print("🎯 Using sounddevice library...")
        
        # Test settings first
        working_settings = test_audio_settings()
        if working_settings:
            print(f"✅ Found working settings: {working_settings[0]}Hz, blocksize {working_settings[1]}")
        
        success = capture_and_playback_sounddevice()
    elif PYAUDIO_AVAILABLE:
        print("🎯 Using PyAudio library...")
        success = capture_and_playback_pyaudio()
    else:
        print("❌ No suitable audio library found!")
        print("\nInstall one of these:")
        print("   pip install sounddevice numpy  # Recommended")
        print("   pip install pyaudio            # Alternative")
        return
    
    if success:
        print("\n🎉 Direct audio test completed!")
        print("💡 This shows your audio hardware works without speech recognition.")
    else:
        print("\n⚠️ Direct audio test had issues")
        print("💡 Check microphone connection and permissions.")
    
    if SOUNDDEVICE_AVAILABLE:
        print("\n📋 Available Audio Devices:")
        list_audio_devices()

if __name__ == "__main__":
    main()