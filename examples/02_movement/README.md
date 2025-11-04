# 🚗 02_movement - Robot Locomotion

## 📚 **Learning Objectives**

In this section, you'll learn:
- ✅ Basic movement commands (forward, backward, turn)
- ✅ Speed control and timing
- ✅ Differential drive principles
- ✅ Creating movement patterns and sequences
- ✅ Precise positioning and navigation

## 🎯 **Prerequisites**

- ✅ Completed `01_basics` section
- ✅ Motor calibration completed
- ✅ Safe open area for robot movement (2m x 2m minimum)
- ✅ Understanding of context managers

## 📝 **Examples in This Section**

### **01_basic_movement.py** 🏃
**First steps with your robot**
- Forward and backward motion
- Simple left and right turns
- Speed control basics
- **Difficulty**: ⭐☆☆

### **02_speed_control.py** ⚡
**Master speed and timing**
- Variable speed control
- Acceleration and deceleration
- Timing-based movement
- **Difficulty**: ⭐⭐☆

### **03_turn_angles.py** 🔄
**Precise turning control**
- 90-degree turns
- Custom angle turns
- Pivot vs. tank turns
- **Difficulty**: ⭐⭐☆

### **04_movement_patterns.py** 🎨
**Create complex movements**
- Square and circle patterns
- Figure-8 movements
- Custom choreography
- **Difficulty**: ⭐⭐⭐

### **05_navigation_basics.py** 🧭
**Simple navigation concepts**
- Point-to-point movement
- Dead reckoning
- Position tracking
- **Difficulty**: ⭐⭐⭐

## 🚀 **Getting Started**

### **Safety First! ⚠️**
- Clear area of obstacles
- Start with low speeds
- Keep robot on ground level
- Have emergency stop ready (Ctrl+C)

### **Run Your First Movement**
```bash
cd /picar-x/examples_new/02_movement
python3 01_basic_movement.py
```

## 💡 **Key Concepts**

### **Movement Commands**
```python
with Picarx() as px:
    # Basic movements
    px.forward(50)      # 50% speed forward
    px.backward(30)     # 30% speed backward
    px.turn_left(40)    # Turn left at 40% speed
    px.turn_right(40)   # Turn right at 40% speed
    px.stop()           # Stop all motors
```

### **Timing Control**
```python
import time

with Picarx() as px:
    px.forward(50)      # Start moving
    time.sleep(2.0)     # Move for 2 seconds
    px.stop()           # Stop
```

### **Differential Drive**
The PiCar-X uses differential drive:
- **Both wheels forward** → Robot moves forward
- **Both wheels backward** → Robot moves backward  
- **Left wheel forward, right wheel backward** → Turn right
- **Different speeds** → Curved movement

## 🔧 **Movement Parameters**

### **Speed Values**
- **Range**: -100 to +100
- **Positive**: Forward direction
- **Negative**: Backward direction
- **0**: Stop
- **Recommended start**: ±30 to ±50

### **Turn Types**
```python
# Pivot turn (one wheel stops)
px.turn_left(50)

# Tank turn (wheels in opposite directions)  
px.set_motor_speed(-50, 50)  # Left back, right forward
```

## 📊 **Calibration Check**

If your robot doesn't move straight:
```bash
# Recalibrate motors
cd ../../setup
python3 calibration/motor_calibration.py
```

## 🎮 **Interactive Controls**

Many examples include keyboard controls:
- **W/S**: Forward/Backward
- **A/D**: Turn Left/Right
- **Q**: Quit
- **Space**: Emergency Stop

## ✅ **Success Criteria**

You're ready for sensors when you can:
- [ ] Move robot forward/backward smoothly
- [ ] Execute precise 90-degree turns
- [ ] Control speed and timing accurately
- [ ] Create a square movement pattern
- [ ] Handle emergency stops safely

## 🔧 **Troubleshooting**

### **Robot doesn't move:**
- Check motor connections
- Verify power supply
- Run motor calibration
- Check for obstacles

### **Robot turns when going straight:**
- Motor speed calibration needed
- Check wheel alignment
- Verify equal motor speeds

### **Jerky or erratic movement:**
- Lower the speed values
- Check for loose connections
- Verify smooth surface

## 🎯 **Next Steps**

Ready for more? Try:
- **[03_sensors/](../03_sensors/)** - Add environmental awareness
- **[04_vision/](../04_vision/)** - See where you're going
- **[05_behaviors/](../05_behaviors/)** - Combine movement with intelligence

## 💡 **Pro Tips**

1. **Start slow** - Use speeds 30-50 for learning
2. **Clear space** - 2m x 2m minimum safe area
3. **Gradual changes** - Avoid sudden speed changes
4. **Emergency ready** - Always know how to stop (Ctrl+C)
5. **Surface matters** - Smooth, flat surfaces work best
6. **Battery check** - Low battery affects movement quality

Happy driving! 🏁