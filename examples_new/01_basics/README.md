# 🌱 01_basics - Getting Started

## 📚 **Learning Objectives**

In this section, you'll learn:
- ✅ How to import and initialize PiCar-X
- ✅ Basic safety patterns with context managers
- ✅ Simple LED control and status indicators
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
- Blink LEDs to show it's working
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

### **04_coordinate_system.py** 🧭
**Understand robot orientation**
- Learn forward/backward/left/right
- Understand angles and directions
- Practice with simple movements
- **Difficulty**: ⭐⭐☆

### **05_error_handling.py** ⚠️
**Handle problems gracefully**
- Catch and handle exceptions
- Recover from common errors
- Debug connection issues
- **Difficulty**: ⭐⭐☆

## 🚀 **Getting Started**

### **Run Your First Example**
```bash
# Make sure you're in the right directory
cd /picar-x/examples_new/01_basics

# Run the hello world example
python3 01_hello_world.py
```

### **What to Expect**
- LEDs should blink in sequence
- Terminal output showing status
- Robot should respond to basic commands
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
    # Control LEDs
    px.set_led_color(255, 0, 0)  # Red
    
    # Basic info
    print(f"Robot initialized: {px}")
```

## 🔧 **Troubleshooting**

### **Common Issues**

**"Module not found" error:**
```bash
# Check if you're in the right directory
pwd  # Should show: /picar-x/examples_new/01_basics

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

**LEDs not working:**
- Check power connections
- Verify hardware setup completed
- Run calibration again: `../../setup/first_time_setup.py`

## ✅ **Success Criteria**

You're ready for the next section when you can:
- [ ] Run `01_hello_world.py` without errors
- [ ] Understand context manager syntax
- [ ] Control LED colors
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