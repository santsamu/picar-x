# 🎓 PiCar-X Learning Examples

Welcome to the comprehensive PiCar-X learning platform! This directory contains **36+ progressive examples** organized into 9 categories, taking you from basic robot control to advanced AI integration and professional robotics development.

## 🚨 Important: Setup First!

Before running any examples, complete the hardware setup and calibration:

```bash
# Initial setup and calibration
cd ../setup
python3 first_time_setup.py

# Validate your hardware
cd ../examples/09_testing
python3 01_hardware_validation.py
```

## �️ Complete Learning Path

### 🌱 **Beginner Level** - Master the Fundamentals

#### [01_basics/](01_basics/) - Robot Fundamentals 
**⏱️ 30 minutes | 📊 Difficulty: ⭐**
- `01_hello_world.py` - Your first robot program
- `02_context_manager.py` - Safe programming practices  
- `03_robot_status.py` - Monitoring robot health

**Learn:** Basic robot control, safety patterns, status monitoring

#### [02_movement/](02_movement/) - Movement Mastery
**⏱️ 45 minutes | 📊 Difficulty: ⭐⭐**
- `01_basic_movement.py` - Forward, backward, turning
- `02_speed_control.py` - Precise speed and timing

**Learn:** Motor control, navigation patterns, movement coordination

#### [03_sensors/](03_sensors/) - Environmental Awareness
**⏱️ 1 hour | 📊 Difficulty: ⭐⭐**
- `01_sensor_reading.py` - Reading all sensor types
- `02_obstacle_avoidance.py` - Autonomous navigation
- `03_cliff_detection.py` - Safety and edge detection

**Learn:** Sensor integration, data processing, safety systems

---

### 🌿 **Intermediate Level** - Build Real Applications

#### [04_vision/](04_vision/) - Computer Vision & Cameras
**⏱️ 2 hours | 📊 Difficulty: ⭐⭐⭐**
- `01_camera_basics.py` - Camera setup and image capture
- `02_computer_vision.py` - Object detection and tracking
- `03_video_recording.py` - Recording and streaming
- `04_photo_car.py` - Photography robot

**Learn:** OpenCV, image processing, object detection, visual tracking

#### [05_behaviors/](05_behaviors/) - Complex Robot Behaviors
**⏱️ 1.5 hours | 📊 Difficulty: ⭐⭐⭐**
- `01_behavior_basics.py` - State machine foundations
- `02_face_tracking.py` - Human interaction
- `03_behavior_coordination.py` - Multi-behavior systems

**Learn:** State machines, behavior trees, coordination systems

#### [06_games/](06_games/) - Interactive Gaming
**⏱️ 2 hours | 📊 Difficulty: ⭐⭐⭐**
- `01_game_basics.py` - Game development fundamentals
- `02_bull_fight.py` - Color-based chase game
- `03_racing_minecart.py` - Racing simulation
- `04_treasure_hunt.py` - Multi-modal adventure game

**Learn:** Game loops, user interaction, real-time programming

---

### 🌳 **Advanced Level** - Master Professional Robotics

#### [07_ai_integration/](07_ai_integration/) - AI & Machine Learning
**⏱️ 3 hours | 📊 Difficulty: ⭐⭐⭐⭐**
- `01_ai_basics.py` - AI integration fundamentals
- `02_gpt_integration.py` - Natural language processing
- `03_voice_commands.py` - Speech recognition and synthesis
- `04_intelligent_behaviors.py` - Adaptive AI behaviors

**Learn:** Modern AI integration, NLP, voice processing, adaptive systems

#### [08_advanced/](08_advanced/) - Expert-Level Systems
**⏱️ 4 hours | 📊 Difficulty: ⭐⭐⭐⭐⭐**
- `01_advanced_integration.py` - Multi-system coordination

**Learn:** System architecture, sensor fusion, performance optimization, fault tolerance

#### [09_testing/](09_testing/) - Professional Development
**⏱️ 2 hours | 📊 Difficulty: ⭐⭐⭐⭐**
- `01_hardware_validation.py` - Hardware testing framework
- `02_integration_testing.py` - System-level validation
- `03_unit_testing.py` - Component-level testing

**Learn:** Professional testing, quality assurance, validation frameworks

## 🚀 Quick Start Guide

### For New Users
```bash
# Step 1: Setup (one time only)
cd ../setup
python3 first_time_setup.py

# Step 2: Start learning
cd ../examples/01_basics
python3 01_hello_world.py

# Step 3: Follow the progression
cd ../02_movement
python3 01_basic_movement.py
```

### For Experienced Users
```bash
# Jump to any category
cd examples/04_vision
python3 02_computer_vision.py

# Try advanced features
cd ../07_ai_integration
python3 02_gpt_integration.py
```

### For Developers
```bash
# Run tests first
cd examples/09_testing
python3 01_hardware_validation.py

# Explore advanced patterns
cd ../08_advanced
python3 01_advanced_integration.py
```

## 📖 How to Use These Examples

### Study Approach
1. **Read the README** in each category first
2. **Understand learning objectives** before running code
3. **Follow the progression** - each example builds on previous knowledge
4. **Experiment** - modify examples to deepen understanding

### Code Structure
Each example includes:
- **📝 Clear documentation** with learning objectives
- **🔧 Interactive modes** for hands-on learning
- **📚 Educational explanations** throughout the code
- **💡 Pro tips** and best practices
- **🚨 Safety considerations** and error handling

### Best Practices
- **Always use context managers** (`with Picarx() as px:`)
- **Test hardware** with validation scripts first
- **Read error messages** carefully for troubleshooting
- **Start simple** and gradually increase complexity

## 🎯 Learning Objectives by Category

| Category | Primary Skills | Secondary Skills | Duration |
|----------|---------------|------------------|----------|
| **01_basics** | Robot safety, basic control | Context managers, error handling | 30 min |
| **02_movement** | Motor control, navigation | Timing, coordination | 45 min |
| **03_sensors** | Data acquisition, processing | Safety systems, filtering | 1 hour |
| **04_vision** | Computer vision, OpenCV | Image processing, tracking | 2 hours |
| **05_behaviors** | State machines, coordination | Behavior trees, multitasking | 1.5 hours |
| **06_games** | Interactive systems, UX | Game loops, real-time programming | 2 hours |
| **07_ai_integration** | Modern AI, NLP | Voice processing, adaptive systems | 3 hours |
| **08_advanced** | System architecture | Performance optimization, fault tolerance | 4 hours |
| **09_testing** | Professional testing | Quality assurance, validation | 2 hours |

## 🛠️ Technical Requirements

### Hardware
- **Raspberry Pi 4** (recommended) or Pi 3B+
- **PiCar-X robot kit** (complete assembly)
- **32GB+ microSD card** (Class 10 or better)
- **Stable power supply** (5V 3A recommended)

### Software Dependencies
```bash
# Core libraries
sudo pip3 install robot-hat vilib opencv-python

# Additional packages for advanced examples
sudo pip3 install openai pygame sounddevice numpy

# Testing frameworks
sudo pip3 install pytest unittest2
```

### Camera Setup
```bash
# Enable camera interface
sudo raspi-config
# Advanced Options > Camera > Enable

# Test camera
vcgencmd get_camera
```

## � Tips for Success

### Learning Strategy
1. **Follow the path** - Don't skip ahead too quickly
2. **Practice regularly** - Consistency beats intensity
3. **Modify examples** - Make them your own
4. **Share projects** - Teach others what you learn

### Troubleshooting
1. **Check hardware first** - Run validation scripts
2. **Read error messages** - They contain important clues
3. **Use the community** - [SunFounder Forum](https://forum.sunfounder.com)
4. **Start fresh** - Sometimes a reboot helps

### Safety First
- **Always use context managers** for safe resource management
- **Test in safe environments** - Clear space for movement
- **Monitor for overheating** - Take breaks during long sessions
- **Keep emergency stop ready** - Know how to quickly stop the robot

## 📊 Progress Tracking

Track your learning progress:

- [ ] **01_basics** - Robot fundamentals mastered
- [ ] **02_movement** - Movement control achieved  
- [ ] **03_sensors** - Sensor integration complete
- [ ] **04_vision** - Computer vision skills developed
- [ ] **05_behaviors** - Complex behaviors implemented
- [ ] **06_games** - Interactive systems created
- [ ] **07_ai_integration** - AI integration accomplished
- [ ] **08_advanced** - Expert-level skills acquired
- [ ] **09_testing** - Professional practices adopted

## 🏆 Certification Ready

After completing all examples, you'll be ready for:
- **Robotics competitions** and challenges
- **Advanced robotics courses** and certifications
- **Open source contributions** to robotics projects
- **Professional robotics development** opportunities

## 🤝 Community & Support

### Get Help
- **📖 Documentation** - Each example has detailed explanations
- **🐛 Issues** - [GitHub Issues](https://github.com/santsamu/picar-x/issues) for bugs
- **💬 Discussions** - [SunFounder Forum](https://forum.sunfounder.com) for general help
- **📧 Email** - support@sunfounder.com for specific issues

### Share Your Projects
- **🌟 Show off** your modifications and improvements
- **📝 Contribute** new examples or documentation
- **🎓 Teach** others what you've learned
- **🚀 Innovate** with your own robotics projects

---

**Ready to start your robotics journey?** Begin with **[01_basics](01_basics/)** and work your way through the complete learning path!

*Happy robot programming!* 🤖✨

Each category folder contains:
- **README.md** - Learning objectives and example descriptions
- **Numbered examples** - Progressive difficulty (01_, 02_, etc.)
- **Supporting files** - Utilities and helper modules

### **Example Naming Convention**
- `01_basic_example.py` - Simple introduction
- `02_intermediate_example.py` - More complex features
- `03_advanced_example.py` - Full implementation

## 🔒 **Safety Guidelines**

Always use context managers for safe operation:
```python
from picarx import Picarx

# ✅ Safe way (recommended)
with Picarx() as px:
    px.forward(50)

# ❌ Unsafe way (avoid)
px = Picarx()
px.forward(50)  # No cleanup if error occurs
```

## 🆘 **Getting Help**

- **Setup issues**: Check `../setup/README.md`
- **Hardware problems**: Run `../setup/diagnostics/hardware_check.py`
- **Example not working**: Verify calibration with `../setup/first_time_setup.py`

## 🎮 **Recommended Learning Order**

1. **Start here**: `01_basics/hello_world.py`
2. **Learn movement**: `02_movement/basic_movement.py`
3. **Add sensors**: `03_sensors/sensor_reading.py`
4. **Try vision**: `04_vision/camera_preview.py`
5. **Create behaviors**: `05_behaviors/line_following.py`
6. **Have fun**: `06_games/remote_control.py`
7. **Go advanced**: `07_ai_integration/voice_control.py`

Happy coding! 🚀