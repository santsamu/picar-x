# 🧠 07_ai_integration - Artificial Intelligence & Machine Learning

## 📚 **Learning Objectives**

In this section, you'll learn:
- ✅ Integrating AI/ML models with robotics
- ✅ Voice recognition and natural language processing
- ✅ Computer vision with deep learning
- ✅ Reinforcement learning for robot behavior
- ✅ Cloud AI services and edge computing

## 🎯 **Prerequisites**

- ✅ Mastery of all previous sections
- ✅ Basic understanding of machine learning concepts
- ✅ Python ML libraries (TensorFlow, PyTorch, scikit-learn)
- ✅ Sufficient computing power (Pi 4+ recommended)
- ✅ Internet connectivity for cloud services
- ✅ Microphone for voice examples (USB microphone recommended)

## 📝 **Examples in This Section**

### **01_voice_control.py** 🎤
**Talk to your robot**
- Speech-to-text processing
- Voice command recognition
- Natural language parsing
- **Difficulty**: ⭐⭐☆

### **02_gpt_conversation.py** 💬
**Conversational AI robot**
- OpenAI GPT integration
- Context-aware responses
- Personality and character
- **Difficulty**: ⭐⭐☆

### **03_object_recognition.py** 👁️
**Deep learning vision**
- Pre-trained CNN models
- Real-time object classification
- Custom object training
- **Difficulty**: ⭐⭐⭐

### **04_gesture_control.py** 👋
**Hand gesture recognition**
- MediaPipe hand tracking
- Gesture command mapping
- Real-time interaction
- **Difficulty**: ⭐⭐⭐

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
cd /picar-x/examples_new/07_ai_integration
python3 01_voice_control.py
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