#!/bin/bash
# Wrapper script to run enhanced microphone test with audio playback

echo "🎤 Enhanced Microphone Test with Audio Playback"
echo "=============================================="
echo "This test will:"
echo "1. Record your voice for 5 seconds"
echo "2. Play back what was recorded (so you can hear it)"
echo "3. Send the audio to Google for speech recognition"
echo ""

# Suppress ALSA warnings and filter stderr output
export ALSA_LOG_LEVEL=0

cd /picar-x/test
sudo python3 test_microphone.py 2>&1 | \
grep -v "ALSA lib" | \
grep -v "Cannot connect to server" | \
grep -v "jack server is not running" | \
grep -v "JackShmReadWritePtr"