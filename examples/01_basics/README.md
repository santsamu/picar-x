# 🌱 01_basics - Getting Started

## 📚 **Learning Objectives**

In this section, you'll learn:
- ✅ How to import and initialize PiCar-X
- ✅ Basic safety patterns with context managers
- ✅ Understanding the robot's coordinate system
- ✅ Basic error handling and troubleshooting

## 🎯 **Prerequisites**

- ✅ Completed hardware setup (`../setup/first_time_setup.py`)
- ✅ Basic Python knowledge (variables, functions, loops)
- ✅ PiCar-X properly calibrated

## 📝 **Examples in This Section**

### **01_hello_world.py** 🌍
**Your first PiCar-X program!**
- Initialize the robot safely
- Test basic robot functions
- Learn the basic code structure
- **Difficulty**: ⭐☆☆

### **02_context_manager.py** 🔒
**Learn safe programming patterns**
- Understand `with` statements
- Automatic cleanup and safety
- Handle errors gracefully
- **Difficulty**: ⭐☆☆

### **03_robot_status.py** 📊
**Check your robot's health**
- Read system information
- Monitor battery levels
- Check sensor status
- **Difficulty**: ⭐☆☆
- Debug connection issues
- **Difficulty**: ⭐⭐☆

### **04_rgb_led_extension.py** 💡
**RGB signals + headlights**
- Control RGB status LED (signals)
- Control left/right headlights on P6/P7
- Learn brightness control patterns
- **Difficulty**: ⭐☆☆

### **05_headlights.py** 🔦
**Front headlights control**
- Turn headlights on/off
- Set shared brightness for both headlights
- **Difficulty**: ⭐☆☆

## 🚀 **Getting Started**

### **Run Your First Example**
```bash
# Make sure you're in the right directory
cd /picar-x/examples/01_basics

# Run the hello world example
python3 01_hello_world.py
```

### **What to Expect**
- Terminal output showing status
- Robot should respond to basic commands
- Servo movements during testing
- No movement (just initialization)

## 💡 **Key Concepts**

### **Context Managers (IMPORTANT!)**
Always use `with` statements for safety:
```python
with Picarx() as px:
    # Your code here
    # Automatic cleanup happens
```

### **Basic Robot Structure**
```python
from picarx import Picarx

# Safe initialization
with Picarx() as px:
    # Test basic functions
    px.forward(30)
    px.stop()
    
    # Basic info
    print(f"Robot initialized: {px}")
```

## 🔧 **Troubleshooting**

### **Common Issues**

**"Module not found" error:**
```bash
# Check if you're in the right directory
pwd  # Should show: /picar-x/examples/01_basics

# Check if picarx is installed
python3 -c "import picarx; print('OK')"
```

**"Permission denied" error:**
```bash
# Make sure you're not running as root
whoami  # Should NOT show 'root'

# Check hardware connections
python3 ../../setup/diagnostics/hardware_check.py
```

**Hardware not responding:**
- Check power connections
- Verify hardware setup completed
- Run calibration again: `../../setup/first_time_setup.py`

## ✅ **Success Criteria**

You're ready for the next section when you can:
- [ ] Run `01_hello_world.py` without errors
- [ ] Understand context manager syntax
- [ ] Test basic robot functions
- [ ] Handle basic errors gracefully
- [ ] Explain the robot's coordinate system

## 🎯 **Next Steps**

Once comfortable with basics, move to:
- **[02_movement/](../02_movement/)** - Make your robot move!
- **[03_sensors/](../03_sensors/)** - Add environmental awareness

## 💬 **Tips for Success**

1. **Start simple** - Run examples in order
2. **Read the code** - Understand each line
3. **Experiment** - Modify values and see what happens
4. **Be patient** - Hardware takes time to respond
5. **Stay safe** - Always use context managers

Happy coding! 🎉