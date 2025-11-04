# 🔧 PiCar-X Setup & Calibration

## 🚨 **Important: Start Here First!**

Before using any examples or running the robot, you **must** complete the hardware setup and calibration process. This ensures your PiCar-X operates safely and correctly.

## 🚀 **Quick Setup (Recommended)**

Run the automated setup wizard:
```bash
python3 first_time_setup.py
```

This will guide you through:
- Hardware connection verification
- Servo calibration (direction, camera pan/tilt)
- Motor calibration (direction and speed)
- Sensor calibration (grayscale, cliff detection)
- Final verification tests

## 📁 **Setup Components**

### **🎯 Calibration Tools** (`calibration/`)
Essential hardware calibration utilities:
- `hardware_calibration.py` - Complete interactive calibration (recommended)
- `servo_calibration.py` - Individual servo calibration
- `motor_calibration.py` - Motor direction and speed calibration
- `sensor_calibration.py` - Grayscale and cliff sensor setup
- `verify_calibration.py` - Test your calibration results

### **🔍 Diagnostics** (`diagnostics/`)
Hardware verification and troubleshooting:
- `hardware_check.py` - Comprehensive hardware test
- `connection_test.py` - Verify GPIO pin connections
- `performance_test.py` - Baseline performance measurements

### **🛠️ Tools** (`tools/`)
Maintenance and configuration utilities:
- `config_backup.py` - Backup/restore your settings
- `factory_reset.py` - Reset to default configuration
- `update_config.py` - Modify configuration settings

## ⚡ **Quick Start Guide**

### **1. First Time Setup**
```bash
# Run the setup wizard
python3 first_time_setup.py

# Or manual step-by-step:
python3 calibration/hardware_calibration.py
python3 diagnostics/hardware_check.py
```

### **2. Verify Everything Works**
```bash
# Test basic functionality
python3 ../examples_new/01_basics/hello_world.py
```

### **3. If Something's Wrong**
```bash
# Run diagnostics
python3 diagnostics/hardware_check.py

# Reset and try again
python3 tools/factory_reset.py
python3 first_time_setup.py
```

## 🔧 **Manual Calibration Steps**

If you prefer manual calibration:

### **Step 1: Servo Calibration**
```bash
python3 calibration/servo_calibration.py
```
- Calibrate direction servo (front wheels)
- Calibrate camera pan/tilt servos
- Save calibration values

### **Step 2: Motor Calibration**
```bash
python3 calibration/motor_calibration.py
```
- Set correct motor directions
- Calibrate motor speeds
- Test forward/backward movement

### **Step 3: Sensor Calibration**
```bash
python3 calibration/sensor_calibration.py
```
- Set grayscale sensor references for line following
- Set cliff detection thresholds
- Test sensor readings

### **Step 4: Verification**
```bash
python3 calibration/verify_calibration.py
```
- Test all calibrated components
- Verify robot moves correctly
- Check sensor accuracy

## 🎛️ **Configuration Files**

Your calibration settings are stored in:
- **Main config**: `/opt/picar-x/picar-x.conf`
- **Backup location**: `~/.picar-x/backups/`

## 🆘 **Troubleshooting**

### **Common Issues**

**Robot moves in wrong direction:**
```bash
python3 calibration/motor_calibration.py
# Use 'Q' key to flip motor directions
```

**Servos don't center properly:**
```bash
python3 calibration/servo_calibration.py
# Use W/S/D/A keys to adjust angles
```

**Sensors give wrong readings:**
```bash
python3 calibration/sensor_calibration.py
# Recalibrate reference values
```

### **Getting Help**

1. **Run diagnostics**: `python3 diagnostics/hardware_check.py`
2. **Check connections**: Verify all wires are secure
3. **Factory reset**: `python3 tools/factory_reset.py`
4. **Re-run setup**: `python3 first_time_setup.py`

## ✅ **After Setup**

Once setup is complete, you can:

1. **🌱 Start Learning**: Go to `../examples_new/01_basics/`
2. **🎮 Try Examples**: Explore different categories
3. **🧪 Run Tests**: Validate with `../test/`

## 🔒 **Safety Notes**

- Always run setup **before** using examples
- Use context managers for safety: `with Picarx() as px:`
- Keep calibration values backed up
- Test in a safe, open area first

---

**Next Step**: Run `python3 first_time_setup.py` to get started! 🚀