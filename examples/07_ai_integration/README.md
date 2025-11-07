# 🧠 AI Integration Examples

Welcome to the AI Integration section! These examples demonstrate how to integrate artificial intelligence technologies with your PiCar-X robot to create intelligent, adaptive, and interactive robotic systems.

## 🎯 Learning Objectives

By working through these examples, you will learn:

- **AI-Powered Interactions**: Create natural conversations and voice control
- **Intelligent Decision Making**: Implement AI-driven behavior selection
- **Adaptive Learning**: Build robots that improve through experience
- **Natural Language Processing**: Understand and respond to complex commands
- **Context Awareness**: Create robots that understand their environment
- **Autonomous Intelligence**: Develop self-directed robot behaviors

## 📚 Examples Overview

### 01. AI Basics (`01_ai_basics.py`)
**Difficulty**: Beginner  
**Duration**: 15-20 minutes

Introduction to AI integration concepts with your robot:
- Text-to-speech communication systems
- Basic AI personality development
- Simple decision tree implementation
- Voice command recognition basics
- Context-aware responses

**Key Concepts**: TTS integration, AI personalities, decision trees

### 02. GPT Integration (`02_gpt_integration.py`)
**Difficulty**: Intermediate  
**Duration**: 25-30 minutes

Advanced AI integration using GPT language models:
- OpenAI API integration and setup
- Contextual robot conversations
- AI-driven behavior decisions
- Dynamic response generation
- Autonomous exploration with GPT guidance

**Key Concepts**: OpenAI API, contextual AI, autonomous decision making

**Requirements**: 
- OpenAI API key (optional - includes demo mode)
- Internet connection for real GPT integration

### 03. Voice Commands (`03_voice_commands.py`)
**Difficulty**: Intermediate  
**Duration**: 20-25 minutes

Advanced natural language voice control system:
- Continuous speech recognition
- Natural language command processing
- Context-aware voice interactions
- Multi-step command sequences
- Adaptive voice recognition training

**Key Concepts**: Speech recognition, NLP, context awareness

**Requirements**:
- Working microphone
- Internet connection
- `pip install SpeechRecognition pyaudio`

### 04. Intelligent Behaviors (`04_intelligent_behaviors.py`)
**Difficulty**: Advanced  
**Duration**: 30-35 minutes

AI-driven autonomous behavior systems:
- Behavior state machines and decision trees
- Adaptive learning from experience
- Goal-oriented autonomous actions
- Personality adaptation based on environment
- Emergent behaviors from simple rules

**Key Concepts**: State machines, machine learning, autonomous behavior

## 🛠️ Setup Requirements

### Basic Requirements (All Examples)
```bash
# Text-to-speech is included with robot_hat
# No additional installation needed for basic AI examples
```

### Voice Recognition Setup
```bash
pip install SpeechRecognition
pip install pyaudio

# On Raspberry Pi, you might also need:
sudo apt install portaudio19-dev python3-pyaudio
```

### GPT Integration Setup
```bash
pip install openai

# Create API key file (optional):
```bash
# Option 1: Environment variable (most secure)
export OPENAI_API_KEY="your-api-key-here"

# Option 2: Create local keys file in current directory
echo "openai_key = 'your-api-key-here'" > ./keys.py

# Option 3: Create keys file in examples directory
echo "openai_key = 'your-api-key-here'" > ../keys.py

# Option 4: Copy and modify the example file
cp ../keys.py.example ./keys.py
# Then edit keys.py with your actual API key
```

## 🎮 Getting Started

### Quick Start - AI Basics
```bash
cd /picar-x/examples/07_ai_integration
python3 01_ai_basics.py
```

This will introduce you to:
- Robot personality systems
- Basic AI decision making
- Text-to-speech interaction
- Simple voice control (if available)

### Voice Control Demo
```bash
python3 03_voice_commands.py
```

Try saying these natural commands:
- "Hello robot"
- "Go forward slowly"
- "Turn left and explore"
- "Dance for me"
- "What's your status?"

### GPT Integration Demo
```bash
python3 02_gpt_integration.py
```

Experience conversational AI:
- Natural language conversations
- Context-aware responses
- AI-driven exploration decisions
- Dynamic personality adaptation

## 🧠 AI Concepts Explained

### Text-to-Speech (TTS)
- Convert text responses to spoken words
- Create more natural human-robot interaction
- Express robot personality through speech
- Provide real-time feedback and status updates

### Speech Recognition
- Convert spoken words to text commands
- Enable hands-free robot control
- Support natural language instructions
- Adapt to different speakers and accents

### AI Decision Trees
- Structured decision-making processes
- Context-aware behavior selection
- Adaptive response systems
- Goal-oriented action planning

### Machine Learning Integration
- Learn from experience and feedback
- Adapt behavior based on success/failure
- Improve performance over time
- Personalize interactions with users

### Natural Language Processing
- Understand complex spoken instructions
- Extract intent and parameters from speech
- Handle variations in command phrasing
- Process multi-step command sequences

## 🎯 Progressive Learning Path

### Level 1: AI Foundations
1. Run `01_ai_basics.py` - Learn core AI concepts
2. Experiment with different personality traits
3. Try voice control features (if available)
4. Understand decision tree basics

### Level 2: Advanced Integration
1. Set up voice recognition with `03_voice_commands.py`
2. Practice natural language commands
3. Train the system to recognize your voice
4. Explore context-aware interactions

### Level 3: Intelligent Automation
1. Experience GPT integration with `02_gpt_integration.py`
2. Have natural conversations with your robot
3. Watch AI-driven exploration decisions
4. Understand contextual response generation

### Level 4: Autonomous Intelligence
1. Explore `04_intelligent_behaviors.py`
2. Observe adaptive learning in action
3. Set up goal-oriented missions
4. Study emergent behavior patterns

## 🔧 Troubleshooting

### Voice Recognition Issues
```bash
# Test microphone
python3 -c "import speech_recognition as sr; print('Microphone test:', sr.Microphone.list_microphone_names())"

# Check audio system
arecord -l
```

### GPT Integration Problems
- Verify internet connection
- Check API key format in `keys.py`
- Monitor API usage and billing
- Use demo mode if API unavailable

### Common Solutions
- **No microphone detected**: Check USB microphone connection
- **Speech not recognized**: Speak clearly, check ambient noise
- **TTS not working**: Verify audio output, check volume settings
- **API errors**: Check internet connection and API key validity

## 🚀 Next Steps

After mastering AI integration:

1. **Combine with Vision**: Integrate AI with camera examples from `04_vision/`
2. **Advanced Behaviors**: Explore complex behavior combinations
3. **Custom AI Models**: Implement your own decision algorithms
4. **Multi-Robot AI**: Scale AI concepts to robot swarms
5. **Real-World Applications**: Apply AI to practical robot tasks

## 💡 Project Ideas

### Beginner Projects
- Voice-controlled pet robot
- AI conversation companion
- Intelligent room patrol system
- Adaptive exploration robot

### Advanced Projects
- Natural language task planner
- Multi-modal AI interaction system
- Learning-based navigation assistant
- Contextual behavior adaptation engine

### Expert Projects
- Custom AI personality development
- Advanced machine learning integration
- Real-time decision optimization
- Autonomous mission planning system

---

## 📖 Additional Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [SpeechRecognition Library Guide](https://pypi.org/project/SpeechRecognition/)
- [AI Robotics Concepts](https://en.wikipedia.org/wiki/Robotics)
- [Machine Learning for Robotics](https://www.coursera.org/learn/machine-learning)

Ready to create intelligent robot companions? Start with `01_ai_basics.py` and discover the future of AI robotics! 🤖✨

### **05_reinforcement_learning.py** 🎯
**Learning optimal behavior**
- Q-learning implementation
- Environment simulation
- Policy optimization
- **Difficulty**: ⭐⭐⭐

### **06_edge_ai_inference.py** ⚡
**On-device AI processing**
- TensorFlow Lite models
- Optimized edge inference
- Real-time AI decisions
- **Difficulty**: ⭐⭐⭐

## 🚀 **Getting Started**

### **AI Environment Setup**
```bash
# Install required AI/ML libraries
pip3 install speechrecognition
pip3 install openai
pip3 install tensorflow
pip3 install mediapipe
pip3 install transformers

# Test microphone setup
python3 -c "import speech_recognition as sr; print('Speech recognition ready!')"
```

### **API Keys Setup**
Create a `.env` file for API credentials:
```bash
# OpenAI API (for GPT examples)
OPENAI_API_KEY=your_api_key_here

# Google Cloud Speech API (optional)
GOOGLE_CLOUD_KEY=your_google_key_here
```

### **Your First AI Example**
```bash
cd /picar-x/examples/07_ai_integration
python3 01_ai_basics.py
```

## 💡 **Key Concepts**

### **Voice Recognition**
```python
import speech_recognition as sr

def listen_for_command():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for command...")
        audio = recognizer.listen(source)
    
    try:
        command = recognizer.recognize_google(audio)
        return command.lower()
    except sr.UnknownValueError:
        return None
```

### **GPT Integration**
```python
import openai

class RobotPersonality:
    def __init__(self, api_key):
        openai.api_key = api_key
        self.conversation_history = []
    
    def respond_to(self, user_input):
        messages = [
            {"role": "system", "content": "You are a helpful robot assistant."},
            {"role": "user", "content": user_input}
        ]
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        return response.choices[0].message.content
```

### **Computer Vision with AI**
```python
import cv2
import numpy as np
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions

# Load pre-trained model
model = MobileNetV2(weights='imagenet')

def classify_object(image):
    # Preprocess image
    resized = cv2.resize(image, (224, 224))
    processed = preprocess_input(np.expand_dims(resized, axis=0))
    
    # Make prediction
    predictions = model.predict(processed)
    decoded = decode_predictions(predictions, top=3)[0]
    
    return decoded[0][1], decoded[0][2]  # class name, confidence
```

### **Gesture Recognition**
```python
import mediapipe as mp

class GestureRecognizer:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_draw = mp.solutions.drawing_utils
    
    def detect_gesture(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            for landmarks in results.multi_hand_landmarks:
                # Extract hand landmarks
                thumb_tip = landmarks.landmark[4]
                index_tip = landmarks.landmark[8]
                
                # Detect "pointing" gesture
                if index_tip.y < thumb_tip.y:
                    return "point"
        
        return None
```

## 🧠 **AI Model Options**

### **Cloud-Based AI**
| Service | Use Case | Pros | Cons |
|---------|----------|------|------|
| OpenAI GPT | Conversation | Powerful, flexible | Requires internet |
| Google Cloud Vision | Object recognition | High accuracy | Cost per request |
| AWS Polly | Text-to-speech | Natural voices | Network dependency |

### **Edge AI Models**
| Model | Use Case | Size | Performance |
|-------|----------|------|-------------|
| MobileNet | Object detection | ~17MB | Fast, efficient |
| MediaPipe | Hand/pose tracking | ~20MB | Real-time |
| TinyYOLO | Object detection | ~60MB | Good accuracy |

## 🎛️ **Voice Commands**

### **Basic Movement Commands**
```python
VOICE_COMMANDS = {
    "move forward": lambda px: px.forward(50),
    "go back": lambda px: px.backward(50),
    "turn left": lambda px: px.turn_left(50),
    "turn right": lambda px: px.turn_right(50),
    "stop": lambda px: px.stop(),
    "speed up": lambda px: px.set_speed(80),
    "slow down": lambda px: px.set_speed(30)
}
```

### **Complex Behavior Commands**
```python
BEHAVIOR_COMMANDS = {
    "follow the line": start_line_following,
    "avoid obstacles": start_obstacle_avoidance,
    "find red object": start_color_tracking,
    "patrol mode": start_patrol_behavior,
    "return home": return_to_start_position
}
```

## 🔧 **Performance Optimization**

### **Edge Computing Tips**
```python
# Use TensorFlow Lite for faster inference
import tflite_runtime.interpreter as tflite

interpreter = tflite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

# Optimize image processing
def optimize_frame(frame):
    # Reduce resolution for faster processing
    small_frame = cv2.resize(frame, (320, 240))
    return small_frame
```

### **Memory Management**
```python
import gc

def cleanup_ai_resources():
    # Clear GPU memory (if using)
    if hasattr(tf.config.experimental, 'clear_session'):
        tf.config.experimental.clear_session()
    
    # Force garbage collection
    gc.collect()
```

## ✅ **Success Criteria**

You're ready for advanced topics when you can:
- [ ] Control robot with voice commands
- [ ] Integrate conversational AI responses
- [ ] Classify objects in real-time
- [ ] Recognize and respond to gestures
- [ ] Train simple machine learning models
- [ ] Optimize AI models for edge deployment

## 🔧 **Troubleshooting**

### **Voice recognition not working:**
- Check microphone permissions and connections
- Verify internet connectivity (for cloud services)
- Test with `arecord` and `aplay` commands
- Adjust microphone sensitivity

### **Slow AI inference:**
- Use smaller, optimized models (TensorFlow Lite)
- Reduce input image resolution
- Process every nth frame instead of all frames
- Consider hardware acceleration (if available)

### **API rate limits:**
- Implement request caching
- Add delays between API calls
- Use local models when possible
- Monitor usage quotas

## 🎯 **Real-World Applications**

AI-enabled robots can:
- **Home automation** (voice-controlled smart home)
- **Elderly care** (conversational companion)
- **Education** (interactive AI tutor)
- **Security** (intelligent surveillance)
- **Industrial** (quality control with computer vision)

## 🎯 **Next Steps**

Ready for expert-level programming? Try:
- **[08_advanced/](../08_advanced/)** - Complex AI architectures
- **[09_testing/](../09_testing/)** - AI model validation
- **Custom projects** - Build your own AI-powered robot

## 💡 **Pro Tips**

1. **Start with cloud APIs** - Easier to prototype and test
2. **Optimize for your hardware** - Pi 4 vs Pi 5 have different capabilities
3. **Cache frequently used results** - Avoid redundant API calls
4. **Graceful degradation** - Have fallbacks when AI fails
5. **Privacy considerations** - Be mindful of data being sent to cloud
6. **Model versioning** - Keep track of AI model updates
7. **Continuous learning** - Collect data to improve models
8. **Safety first** - AI decisions should have human oversight options

Welcome to the future! 🤖✨