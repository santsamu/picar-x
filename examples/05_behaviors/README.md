# 🤖 05_behaviors - Intelligent Robot Behaviors

## 📚 **Learning Objectives**

In this section, you'll learn:
- ✅ Combining sensors, vision, and movement
- ✅ State machines and behavior trees
- ✅ Autonomous navigation algorithms
- ✅ Reactive and deliberative behaviors
- ✅ Complex multi-step robot behaviors

## 🎯 **Prerequisites**

- ✅ Mastery of basics, movement, sensors, and vision
- ✅ Understanding of loops and conditional logic
- ✅ Familiarity with state management
- ✅ Test environment with obstacles and markers
- ✅ Patience for behavior tuning and debugging

## 📝 **Examples in This Section**

### **01_behavior_basics.py** 🤖
**Foundation of intelligent behaviors**
- State machine fundamentals
- Basic behavior patterns
- Sensor-driven decisions
- **Difficulty**: ⭐⭐☆

### **02_face_tracking.py** �
**Follow human faces**
- Face detection using vision
- Camera servo control for tracking
- Real-time visual pursuit
- **Difficulty**: ⭐⭐⭐

### **03_behavior_coordination.py** 🎯
**Complex multi-behavior system**
- Coordinate multiple behaviors
- Priority-based behavior selection
- Advanced state management
- **Difficulty**: ⭐⭐⭐

## 🚀 **Getting Started**

### **Behavior Testing Environment**
Create a rich test environment:
- **Black tape lines** for line following
- **Cardboard obstacles** of various sizes
- **Colored objects** for visual tracking
- **Wall boundaries** for navigation testing
- **Good lighting** for vision-based behaviors

### **Run Your First Behavior**
```bash
cd /picar-x/examples/05_behaviors
python3 01_behavior_basics.py
```

## 💡 **Key Concepts**

### **State Machines**
```python
class RobotState:
    SEARCHING = "searching"
    TRACKING = "tracking"
    AVOIDING = "avoiding"
    STUCK = "stuck"

current_state = RobotState.SEARCHING

# State transition logic
if obstacle_detected:
    current_state = RobotState.AVOIDING
elif line_detected:
    current_state = RobotState.TRACKING
```

### **Sensor Fusion**
```python
with Picarx() as px:
    # Combine multiple sensor inputs
    distance = px.get_distance()
    line_sensors = [px.get_grayscale_left(), 
                   px.get_grayscale_center(),
                   px.get_grayscale_right()]
    
    # Decision making
    if distance < 20:  # Obstacle priority
        avoid_obstacle()
    elif any(sensor < 30 for sensor in line_sensors):
        follow_line()
    else:
        search_pattern()
```

### **PID Control for Line Following**
```python
class PIDController:
    def __init__(self, kp=1.0, ki=0.0, kd=0.0):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.prev_error = 0
        self.integral = 0
    
    def calculate(self, error):
        self.integral += error
        derivative = error - self.prev_error
        output = (self.kp * error + 
                 self.ki * self.integral + 
                 self.kd * derivative)
        self.prev_error = error
        return output
```

### **Behavior Trees**
```python
class Behavior:
    def __init__(self):
        self.priority = 0
    
    def can_run(self):
        """Check if behavior conditions are met"""
        return True
    
    def execute(self):
        """Run the behavior"""
        pass

# Priority-based behavior selection
behaviors = [AvoidObstacle(), FollowLine(), Explore()]
for behavior in sorted(behaviors, key=lambda b: b.priority):
    if behavior.can_run():
        behavior.execute()
        break
```

## 🎛️ **Behavior Parameters**

### **Line Following Tuning**
```python
# PID parameters (start with these)
KP = 0.5  # Proportional gain
KI = 0.0  # Integral gain (usually 0)
KD = 0.1  # Derivative gain

# Speed settings
BASE_SPEED = 30    # Base forward speed
MAX_TURN = 40      # Maximum turn speed
```

### **Obstacle Avoidance Settings**
```python
# Distance thresholds
DANGER_DISTANCE = 15    # Emergency stop
WARNING_DISTANCE = 30   # Start avoiding
SAFE_DISTANCE = 50      # Resume normal operation

# Avoidance behaviors
BACKUP_TIME = 1.0       # Seconds to back up
TURN_ANGLE = 45         # Degrees to turn
```

## 🔧 **Behavior Tuning**

### **Line Following Optimization**
1. **Test on straight line** first
2. **Adjust PID gains** for smooth tracking
3. **Test curves** and adjust turn sensitivity
4. **Handle intersections** and line breaks

### **Obstacle Avoidance Tuning**
1. **Set safe distances** for your environment
2. **Test backup maneuvers** 
3. **Verify turn angles** are sufficient
4. **Add stuck detection** and recovery

## 📊 **Performance Metrics**

### **Line Following Success**
- **Accuracy**: Percentage of line followed correctly
- **Speed**: Average forward progress
- **Smoothness**: Minimal oscillation
- **Recovery**: Handle line breaks and curves

### **Obstacle Avoidance Metrics**
- **Safety**: No collisions
- **Efficiency**: Minimal path deviation
- **Coverage**: Explore available space
- **Stuck prevention**: Escape mechanisms

## ✅ **Success Criteria**

You're ready for games when you can:
- [ ] Implement smooth line following with PID
- [ ] Navigate around obstacles safely
- [ ] Create state machine behaviors
- [ ] Combine multiple sensors effectively
- [ ] Handle behavior conflicts and priorities
- [ ] Recover from error conditions

## 🔧 **Troubleshooting**

### **Erratic line following:**
- Check sensor calibration
- Reduce PID gains (especially KP)
- Verify line contrast and width
- Ensure consistent lighting

### **Poor obstacle avoidance:**
- Verify distance sensor accuracy
- Adjust detection thresholds
- Check turn angle effectiveness
- Add stuck detection logic

### **Behavior conflicts:**
- Implement clear priority system
- Add transition delays between behaviors
- Verify sensor data reliability
- Debug state machine logic

## 🎯 **Real-World Applications**

These behaviors enable:
- **Autonomous cleaning** (Roomba-style navigation)
- **Warehouse automation** (line following robots)
- **Search and rescue** (exploration behaviors)
- **Security patrol** (monitoring behaviors)
- **Agricultural robots** (row following)

## 🎯 **Next Steps**

Ready for interactive fun? Try:
- **[06_games/](../06_games/)** - Turn behaviors into games
- **[07_ai_integration/](../07_ai_integration/)** - Add AI decision making
- **[08_advanced/](../08_advanced/)** - Complex behavior architectures

## 💡 **Pro Tips**

1. **Start simple** - Master basic behaviors before combining
2. **Tune parameters** - Spend time optimizing for your environment  
3. **Debug visually** - Use sounds/movement to show internal state
4. **Plan recovery** - Always have escape mechanisms
5. **Test thoroughly** - Behaviors need extensive real-world testing
6. **Log everything** - Record sensor data for offline analysis
7. **Safety first** - Behaviors can be unpredictable, supervise testing
8. **Modular design** - Keep behaviors independent and reusable

Intelligence emerging! 🧠✨