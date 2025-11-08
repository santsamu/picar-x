#!/bin/bash
# Universal AI Integration Runner - Suppresses ALSA warnings for cleaner output

if [ $# -eq 0 ]; then
    echo "🤖 AI Integration Runner"
    echo "Usage: ./run_ai_example.sh <python_file>"
    echo ""
    echo "Available examples:"
    echo "  - test_microphone.py"
    echo "  - 01_ai_basics.py"
    echo "  - 02_gpt_integration.py"
    echo "  - 03_voice_commands.py"
    echo "  - 04_intelligent_behaviors.py"
    echo ""
    echo "Example: ./run_ai_example.sh test_microphone.py"
    exit 1
fi

SCRIPT_NAME="$1"

# Check if file exists
if [ ! -f "$SCRIPT_NAME" ]; then
    echo "❌ Error: File '$SCRIPT_NAME' not found"
    exit 1
fi

echo "🤖 Running $SCRIPT_NAME with clean output..."
echo "========================================"

# Suppress ALSA warnings and filter stderr output
export ALSA_LOG_LEVEL=0

sudo python3 "$SCRIPT_NAME" 2>&1 | \
grep -v "ALSA lib" | \
grep -v "Cannot connect to server" | \
grep -v "jack server is not running" | \
grep -v "JackShmReadWritePtr"