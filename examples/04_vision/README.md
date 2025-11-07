# 📹 04_vision - Computer Vision & Camera

## 📚 **Learning Objectives**

In this section, you'll learn:
- ✅ Camera initialization and image capture
- ✅ Real-time video streaming and display
- ✅ Basic image processing and computer vision
- ✅ Color detection and object tracking
- ✅ Visual navigation and decision making

## 🎯 **Prerequisites**

- ✅ Completed previous sections (basics, movement, sensors)
- ✅ Camera properly connected and calibrated
- ✅ OpenCV and image processing libraries installed
- ✅ Good lighting environment for testing
- ✅ Understanding of coordinate systems

## 📝 **Examples in This Section**

### **01_camera_basics.py** 📷
**First look through robot's eyes**
- Initialize camera system
- Display live video feed
- Basic camera controls and setup
- **Difficulty**: ⭐☆☆

### **02_computer_vision.py** 🎨
**Computer vision fundamentals**
- Image processing techniques
- Object detection basics
- Visual recognition patterns
- **Difficulty**: ⭐⭐☆

### **03_video_recording.py** �
**Record robot's adventures**
- Video recording capabilities
- Save footage with timestamps
- Real-time video streaming
- **Difficulty**: ⭐⭐☆

### **04_photo_car.py** 📸
**Automated photography robot**
- Take photos automatically
- Camera trigger mechanisms
- Image capture sequences
- **Difficulty**: ⭐⭐☆

## 🚀 **Getting Started**

### **Camera Setup Check**
```bash
# Test camera connectivity
cd /picar-x/examples/04_vision
python3 01_camera_basics.py
```

### **Required Libraries**
The examples use these Python libraries:
- `opencv-python` (cv2) - Computer vision
- `numpy` - Numerical operations  
- `PIL/Pillow` - Image processing
- `matplotlib` - Display and plotting

## 💡 **Key Concepts**

### **Camera Initialization**
```python
with Picarx() as px:
    # Initialize camera
    px.camera_servo_pin_1.angle(0)  # Pan center
    px.camera_servo_pin_2.angle(0)  # Tilt center
    
    # Start video capture
    import cv2
    cap = cv2.VideoCapture(0)
```

### **Image Capture**
```python
import cv2

cap = cv2.VideoCapture(0)
ret, frame = cap.read()

if ret:
    # Process the image
    cv2.imshow('Robot View', frame)
    cv2.waitKey(1)
```

### **Color Detection**
```python
import cv2
import numpy as np

# Convert to HSV color space
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Define color range (example: red)
lower_red = np.array([0, 50, 50])
upper_red = np.array([10, 255, 255])

# Create mask
mask = cv2.inRange(hsv, lower_red, upper_red)
```

### **Camera Servo Control**
```python
with Picarx() as px:
    # Pan left/right (-90 to +90 degrees)
    px.camera_servo_pin_1.angle(-30)  # Look left
    px.camera_servo_pin_1.angle(30)   # Look right
    
    # Tilt up/down (-30 to +30 degrees)  
    px.camera_servo_pin_2.angle(20)   # Look up
    px.camera_servo_pin_2.angle(-20)  # Look down
```

## 🎨 **Color Detection Guide**

### **HSV Color Ranges**
| Color | Hue Range | Saturation | Value |
|-------|-----------|------------|-------|
| Red | 0-10, 170-180 | 50-255 | 50-255 |
| Blue | 100-130 | 50-255 | 50-255 |
| Green | 50-80 | 50-255 | 50-255 |
| Yellow | 20-30 | 50-255 | 50-255 |

### **Lighting Considerations**
- **Bright, even lighting** works best
- **Avoid shadows** on target objects
- **Consistent background** improves detection
- **Test different times of day** for robustness

## 📊 **Camera Specifications**

### **Default Settings**
- **Resolution**: 640x480 (adjustable)
- **Frame rate**: 30 FPS (typical)
- **Format**: BGR color space
- **Pan range**: ±90 degrees
- **Tilt range**: ±30 degrees

### **Performance Tips**
```python
# Optimize for speed
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.CAP_PROP_FPS, 15)
```

## 🎮 **Interactive Controls**

Many vision examples include:
- **Arrow keys**: Pan/tilt camera
- **Space**: Capture image
- **C**: Change color detection
- **R**: Reset camera position
- **Q**: Quit application

## ✅ **Success Criteria**

You're ready for behaviors when you can:
- [ ] Display live camera feed
- [ ] Capture and save images
- [ ] Detect objects by color
- [ ] Control camera pan/tilt smoothly
- [ ] Track moving objects
- [ ] Record video footage

## 🔧 **Troubleshooting**

### **No camera image:**
- Check camera connection
- Verify camera permissions
- Test with: `lsusb` (should show camera device)
- Try different capture indices (0, 1, 2...)

### **Poor image quality:**
- Adjust lighting conditions
- Clean camera lens
- Check camera focus
- Verify stable mounting

### **Slow performance:**
- Reduce image resolution
- Lower frame rate
- Optimize processing algorithms
- Close other applications

### **Color detection not working:**
- Adjust HSV color ranges
- Improve lighting conditions
- Use color calibration tools
- Test with high-contrast objects

## 🎯 **Real-World Applications**

Vision capabilities enable:
- **Object recognition** (sorting, identification)
- **Visual navigation** (autonomous vehicles)
- **Security monitoring** (motion detection)
- **Quality control** (industrial inspection)
- **Interactive games** (gesture control)

## 🎯 **Next Steps**

Ready for intelligent behaviors? Try:
- **[05_behaviors/](../05_behaviors/)** - Combine vision with movement
- **[06_games/](../06_games/)** - Create vision-based games
- **[07_ai_integration/](../07_ai_integration/)** - Add AI to vision

## 💡 **Pro Tips**

1. **Lighting is critical** - Consistent, bright lighting improves all vision tasks
2. **Start simple** - Master basic capture before complex processing
3. **Optimize performance** - Lower resolution for real-time applications
4. **Use HSV color space** - More robust than RGB for color detection
5. **Test extensively** - Vision algorithms need testing in various conditions
6. **Safety first** - Vision can fail, always have backup sensors
7. **Smooth movements** - Use gradual servo movements for better tracking

Welcome to the visual world! 👁️