#!/bin/bash
# Clean audio test runner - suppresses ALSA warnings

echo "🎤 Running Direct Audio Test (Clean Output)"
echo "============================================"

export ALSA_LOG_LEVEL=0

sudo python3 direct_audio_test.py 2>&1 | \
grep -v "ALSA lib" | \
grep -v "Cannot connect to server" | \
grep -v "jack server is not running" | \
grep -v "JackShmReadWritePtr" | \
grep -v "Expression.*failed"