# 📡 03_sensors - Environmental Awareness

## 📚 **Learning Objectives**

In this section, you'll learn:
- ✅ Reading and interpreting sensor data
- ✅ Grayscale sensors for line detection
- ✅ Ultrasonic distance measurement
- ✅ Cliff detection and safety
- ✅ Sensor-based decision making

## 🎯 **Prerequisites**

- ✅ Completed `01_basics` and `02_movement` sections
- ✅ Sensor calibration completed
- ✅ Understanding of basic movement commands
- ✅ Test environment with different surfaces

## 📝 **Examples in This Section**

### **01_sensor_reading.py** 📊
**Basic sensor data collection**
- Read all sensor values
- Understand sensor ranges
- Display real-time data
- Sensor calibration basics
- **Difficulty**: ⭐☆☆

### **02_obstacle_avoidance.py** 🚧
**Autonomous navigation**
- Ultrasonic distance measurement
- Obstacle detection and avoidance
- Smart navigation algorithms
- Emergency stop mechanisms
- **Difficulty**: ⭐⭐☆

### **03_cliff_detection.py** ⛰️
**Safety first - avoid falling**
- Detect table edges and cliffs
- Grayscale sensor utilization
- Safe navigation patterns
- Multi-sensor safety systems
- **Difficulty**: ⭐⭐☆

## 🚀 **Getting Started**

### **Setup Your Test Environment**
For optimal learning, prepare:
- **White surface** with black tape lines (2-3cm wide)
- **Various objects** for distance testing
- **Table edge** for cliff detection (supervised!)
- **Good lighting** for grayscale sensors

### **Run Your First Sensor Test**
```bash
cd examples/03_sensors
python3 01_sensor_reading.py
```

## 💡 **Key Concepts**

### **Grayscale Sensors**
```python
with Picarx() as px:
    # Read grayscale values (0-100)
    left = px.get_grayscale_left()
    center = px.get_grayscale_center() 
    right = px.get_grayscale_right()
    
    # Typical values:
    # White surface: 80-100
    # Black line: 0-20
    # Gray surface: 30-70
```

### **Ultrasonic Distance**
```python
with Picarx() as px:
    # Get distance in centimeters
    distance = px.get_distance()
    
    # Range: ~2cm to 300cm
    # Returns -1 if out of range or error
    if distance > 0:
        print(f"Object at {distance}cm")
```

### **Cliff Detection**
```python
with Picarx() as px:
    # Check if surface drops away
    cliff_detected = px.is_cliff_detected()
    
    if cliff_detected:
        px.stop()  # Emergency stop!
        print("Cliff detected - stopping!")
```

## 🔧 **Sensor Calibration**

### **Grayscale Calibration**
Different lighting affects sensor readings:
```bash
# Recalibrate if needed
cd ../../setup
python3 calibration/sensor_calibration.py
```

### **Distance Sensor Accuracy**
- **Best range**: 5cm to 200cm
- **Accuracy**: ±1cm in ideal conditions
- **Surface matters**: Soft/angled surfaces may give poor readings

## 📊 **Sensor Data Interpretation**

### **Grayscale Sensor Values**
| Surface | Typical Range | Line Detection |
|---------|---------------|----------------|
| White paper | 85-100 | Background |
| Black tape | 0-15 | Line detected |
| Gray surface | 40-60 | Uncertain |
| No reflection | 0-5 | Cliff/void |

### **Distance Sensor Behavior**
| Distance | Meaning | Action |
|----------|---------|---------|
| -1 | Error/Out of range | Check sensor |
| 0-10cm | Very close | Stop/back up |
| 10-30cm | Close object | Slow/prepare to turn |
| 30-100cm | Safe distance | Normal operation |
| >100cm | Far/no obstacle | Continue |

## 🎮 **Test Patterns**

### **Line Following Test**
1. Place black tape in straight line
2. Position robot sensors over line
3. Move robot slowly along line
4. Observe sensor value changes

### **Obstacle Course**
1. Place objects at various distances
2. Drive robot toward obstacles
3. Test distance measurements
4. Practice avoidance maneuvers

## ✅ **Success Criteria**

You're ready for vision when you can:
- [ ] Read and interpret all sensor values
- [ ] Detect black lines reliably
- [ ] Measure distances accurately
- [ ] Implement cliff detection safety
- [ ] Combine sensors for decision making

## 🔧 **Troubleshooting**

### **Grayscale sensors not working:**
- Check lighting conditions
- Clean sensor lenses
- Recalibrate sensors
- Verify surface contrast

### **Distance sensor erratic:**
- Check for obstacles in beam path
- Verify sensor mounting
- Test with different surfaces
- Check power connections

### **Inconsistent readings:**
- Allow sensor settling time (0.1s between reads)
- Filter noisy data (average multiple readings)
- Check for electrical interference

## 🎯 **Real-World Applications**

These sensor skills enable:
- **Line following robots** (warehouse automation)
- **Obstacle avoidance** (autonomous vehicles)
- **Edge detection** (cleaning robots)
- **Security systems** (motion detection)

## 🎯 **Next Steps**

Ready to see the world? Try:
- **[04_vision/](../04_vision/)** - Add camera capabilities
- **[05_behaviors/](../05_behaviors/)** - Create intelligent behaviors
- **[06_games/](../06_games/)** - Build sensor-based games

## 💡 **Pro Tips**

1. **Lighting matters** - Consistent lighting improves reliability
2. **Surface quality** - Clean, flat surfaces give best results
3. **Sensor height** - Keep sensors at consistent height
4. **Data filtering** - Average multiple readings for stability
5. **Safety first** - Always implement emergency stops
6. **Test thoroughly** - Verify sensor behavior in your environment

Environmental awareness unlocked! 🌍