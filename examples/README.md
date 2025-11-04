# 🎓 PiCar-X Learning Examples

Welcome to the PiCar-X examples! This folder contains organized learning materials that take you from basic robot control to advanced AI integration.

## 🚨 **Important: Setup First!**

Before running any examples, complete the hardware setup:
```bash
cd ../setup
python3 first_time_setup.py
```

## 📚 **Learning Path**

### **🌱 Beginner Level**
1. **[01_basics/](01_basics/)** - Hello World and fundamental concepts
2. **[02_movement/](02_movement/)** - Basic movement and motor control
3. **[03_sensors/](03_sensors/)** - Working with sensors and input

### **🚀 Intermediate Level**
4. **[04_vision/](04_vision/)** - Camera and computer vision
5. **[05_behaviors/](05_behaviors/)** - Complex robot behaviors
6. **[06_games/](06_games/)** - Fun interactive games

### **🧠 Advanced Level**
7. **[07_ai_integration/](07_ai_integration/)** - AI and machine learning
8. **[08_advanced/](08_advanced/)** - Complex programming patterns
9. **[09_testing/](09_testing/)** - Testing and validation

## 🎯 **Quick Start**

### **First Time Users**
```bash
# 1. Complete setup
cd ../setup && python3 first_time_setup.py

# 2. Start with basics
cd ../examples_new/01_basics
python3 hello_world.py
```

### **Experienced Users**
```bash
# Jump to any category
cd 04_vision
python3 camera_preview.py
```

## 📖 **How to Use These Examples**

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