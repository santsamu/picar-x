"""
🤖 Advanced Navigation Configuration
===================================

Configuration file for autonomous navigation examples
Tune these values for optimal performance on your PiCar-X
"""

# 📏 DISTANCE THRESHOLDS (in meters)
SAFE_DISTANCE = 0.25           # Minimum safe distance from obstacles
CLIFF_DISTANCE = 0.15          # Critical cliff detection distance
SCAN_DISTANCES = {             # Servo scanning positions and safe thresholds
    'left': (-45, 0.30),       # (angle, min_distance)
    'center': (0, 0.25),
    'right': (45, 0.30)
}

# 🌫️ GRAYSCALE SENSOR THRESHOLDS
GRAYSCALE_THRESHOLDS = {
    'cliff': 60,               # Values above this indicate cliff/edge
    'line': 30,                # Values below this indicate dark line/surface
    'normal': 40               # Normal surface reflection value
}

# 👁️ CAMERA VISION SETTINGS
CAMERA_CONFIG = {
    'edge_threshold_low': 50,   # Canny edge detection lower threshold
    'edge_threshold_high': 150, # Canny edge detection upper threshold
    'obstacle_pixel_count': 1000, # Min edge pixels to consider obstacle
    'roi_top_ratio': 0.3,      # ROI: top 30% of image
    'roi_bottom_ratio': 0.7,   # ROI: bottom 70% of image
    'roi_left_ratio': 0.3,     # ROI: left 30% of image
    'roi_right_ratio': 0.7     # ROI: right 70% of image
}

# 🚗 MOVEMENT PARAMETERS
MOVEMENT_SPEEDS = {
    'forward': 25,             # Normal forward speed
    'backward': 20,            # Backing up speed
    'turn': 40,                # Turning speed
    'scan_turn': 30,           # Slower turning while scanning
    'emergency': 50            # Emergency avoidance speed
}

# ⏱️ TIMING SETTINGS (in seconds)
TIMING = {
    'sensor_delay': 0.1,       # Delay between sensor readings
    'servo_move_delay': 0.3,   # Time to wait after moving servo
    'turn_duration': 0.8,      # Standard turn duration
    'emergency_backup': 0.3,   # Emergency backup duration
    'emergency_turn': 1.2,     # Emergency turn duration
    'scan_delay': 0.5,         # Delay during scanning
    'status_print_interval': 2.0  # How often to print status
}

# 🎯 BEHAVIOR PRIORITIES
PRIORITY_WEIGHTS = {
    'cliff_avoidance': 100,    # Highest priority
    'obstacle_avoidance': 80,
    'camera_obstacles': 60,
    'exploration': 40,
    'wall_following': 30       # Lowest priority
}

# 🗺️ MAPPING SETTINGS
MAP_CONFIG = {
    'grid_size': 0.1,          # Grid resolution in meters
    'map_width': 50,           # Map width in grid cells
    'map_height': 50,          # Map height in grid cells
    'occupied_threshold': 0.7, # Probability threshold for occupied cell
    'free_threshold': 0.3,     # Probability threshold for free cell
    'update_radius': 3         # Cells to update around robot position
}

# 📊 PERFORMANCE TRACKING
STATS_CONFIG = {
    'track_distance': True,    # Track total distance traveled
    'track_obstacles': True,   # Count obstacles avoided
    'track_cliffs': True,      # Count cliff detections
    'track_turns': True,       # Count turns made
    'save_map': True,          # Save exploration map
    'log_sensors': False       # Log all sensor readings (verbose)
}

# 🔧 HARDWARE CALIBRATION
CALIBRATION = {
    'servo_center': 0,         # Servo center position offset
    'wheel_circumference': 0.21, # Wheel circumference in meters
    'wheelbase': 0.15,         # Distance between wheels in meters
    'ultrasonic_offset': 0.02, # Ultrasonic sensor mounting offset
    'camera_height': 0.08,     # Camera height above ground
    'camera_angle': 0          # Camera tilt angle in degrees
}

# 🚨 EMERGENCY SETTINGS
EMERGENCY_CONFIG = {
    'max_consecutive_obstacles': 5, # Stop after this many consecutive obstacles
    'min_battery_voltage': 6.0,     # Minimum operating voltage
    'max_operation_time': 300,      # Maximum run time in seconds (5 min)
    'stuck_detection_time': 10,     # Time to detect if robot is stuck
    'recovery_attempts': 3          # Max recovery attempts before stopping
}

# 🎮 USER INTERFACE
UI_CONFIG = {
    'show_sensor_values': True,     # Display real-time sensor values
    'show_decision_logic': True,    # Show decision making process
    'show_performance_stats': True, # Display performance statistics
    'update_frequency': 2.0,        # UI update frequency in Hz
    'verbose_mode': False           # Enable verbose logging
}

def get_config_summary():
    """Return a summary of current configuration"""
    return {
        'Safe Distance': f"{SAFE_DISTANCE}m",
        'Cliff Threshold': GRAYSCALE_THRESHOLDS['cliff'],
        'Forward Speed': MOVEMENT_SPEEDS['forward'],
        'Turn Speed': MOVEMENT_SPEEDS['turn'],
        'Camera Edge Threshold': CAMERA_CONFIG['obstacle_pixel_count'],
        'Map Grid Size': f"{MAP_CONFIG['grid_size']}m",
        'Max Operation Time': f"{EMERGENCY_CONFIG['max_operation_time']}s"
    }

def print_config():
    """Print current configuration in a readable format"""
    print("🔧 Current Navigation Configuration:")
    print("=" * 40)
    
    config_summary = get_config_summary()
    for key, value in config_summary.items():
        print(f"  {key}: {value}")
    
    print("\n💡 Tip: Edit navigation_config.py to customize these values!")