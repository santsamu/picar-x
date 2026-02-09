#!/usr/bin/env python3
"""
🤖 Advanced Autonomous Navigation System
=======================================

This advanced example demonstrates intelligent robot navigation using:
- 🎥 Camera vision for object detection and navigation
- 📏 Ultrasonic sensor for distance measurement
- 🌫️ Grayscale sensors for edge/cliff detection
- 🧠 AI decision-making for obstacle avoidance
- 🗺️ Basic mapping and path planning

The robot will:
1. Move forward while monitoring all sensors
2. Detect obstacles using camera and ultrasonic
3. Avoid cliffs/edges using grayscale sensors
4. Make intelligent navigation decisions
5. Map its environment and remember obstacles
6. Find alternative paths when blocked
"""

from picarx import Picarx
import time
import math
import json
import cv2
import numpy as np
from datetime import datetime
from collections import deque
import threading
import logging

# Configure logging for debug information
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SensorData:
    """Container for all sensor readings"""
    def __init__(self):
        self.ultrasonic_distance = 0
        self.grayscale_values = [0, 0, 0]  # Left, Center, Right
        self.camera_frame = None
        self.obstacles_detected = []
        self.cliff_detected = False
        self.timestamp = time.time()

class NavigationMap:
    """Simple occupancy grid map for navigation"""
    def __init__(self, size=50, resolution=0.1):
        self.size = size
        self.resolution = resolution  # meters per cell
        self.grid = np.zeros((size, size), dtype=int)  # 0=free, 1=obstacle, -1=unknown
        self.robot_pos = [size//2, size//2]  # Center position
        self.robot_heading = 0  # degrees
        
    def add_obstacle(self, distance, angle):
        """Add obstacle to map based on sensor reading"""
        if distance > 0 and distance < 3.0:  # Valid range
            # Calculate obstacle position relative to robot
            x_offset = distance * math.cos(math.radians(self.robot_heading + angle))
            y_offset = distance * math.sin(math.radians(self.robot_heading + angle))
            
            # Convert to grid coordinates
            grid_x = int(self.robot_pos[0] + x_offset / self.resolution)
            grid_y = int(self.robot_pos[1] + y_offset / self.resolution)
            
            if 0 <= grid_x < self.size and 0 <= grid_y < self.size:
                self.grid[grid_y, grid_x] = 1
                
    def is_path_clear(self, distance, angle):
        """Check if path in given direction is clear"""
        steps = int(distance / self.resolution)
        for i in range(1, steps + 1):
            x_offset = (i * self.resolution) * math.cos(math.radians(self.robot_heading + angle))
            y_offset = (i * self.resolution) * math.sin(math.radians(self.robot_heading + angle))
            
            grid_x = int(self.robot_pos[0] + x_offset / self.resolution)
            grid_y = int(self.robot_pos[1] + y_offset / self.resolution)
            
            if (0 <= grid_x < self.size and 0 <= grid_y < self.size and 
                self.grid[grid_y, grid_x] == 1):
                return False
        return True

class VisionProcessor:
    """Computer vision processing for obstacle detection"""
    def __init__(self):
        self.obstacle_cascade = None
        self.setup_detection()
        
    def setup_detection(self):
        """Setup vision-based obstacle detection"""
        # For now, we'll use simple edge detection and contour finding
        # In a full implementation, you could train specific object detectors
        pass
        
    def detect_obstacles(self, frame):
        """Detect obstacles in camera frame"""
        if frame is None:
            return []
            
        obstacles = []
        
        try:
            # Convert to grayscale for processing
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Edge detection
            edges = cv2.Canny(blurred, 50, 150)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Analyze contours for obstacles
            height, width = frame.shape[:2]
            for contour in contours:
                area = cv2.contourArea(contour)
                
                # Filter by size - only consider significant obstacles
                if area > 500:  # Minimum obstacle size
                    # Get bounding rectangle
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Calculate position relative to robot
                    center_x = x + w // 2
                    center_y = y + h // 2
                    
                    # Estimate distance based on obstacle size (rough approximation)
                    estimated_distance = max(0.5, 1000 / area)  # Inverse relationship
                    
                    # Calculate angle from center of view
                    angle_from_center = (center_x - width // 2) * 45 / (width // 2)  # FOV ~90 degrees
                    
                    obstacles.append({
                        'x': center_x,
                        'y': center_y,
                        'distance': estimated_distance,
                        'angle': angle_from_center,
                        'area': area
                    })
                    
        except Exception as e:
            logging.error(f"Vision processing error: {e}")
            
        return obstacles

class AutonomousNavigator:
    """Main autonomous navigation system"""
    
    def __init__(self):
        self.px = None
        self.running = False
        self.sensor_data = SensorData()
        self.nav_map = NavigationMap()
        self.vision_processor = VisionProcessor()
        
        # Navigation parameters
        self.cruise_speed = 30
        self.turn_speed = 50
        self.safe_distance = 30  # centimeters (distance sensor returns cm)
        self.cliff_threshold = 100  # grayscale threshold for cliff detection
        
        # Behavior state
        self.current_behavior = "exploring"  # exploring, avoiding, turning, stopped
        self.last_turn_direction = 1  # 1 = right, -1 = left
        self.stuck_counter = 0
        self.exploration_timer = 0
        
        # Performance tracking
        self.stats = {
            'distance_traveled': 0,
            'obstacles_avoided': 0,
            'cliff_detections': 0,
            'exploration_time': 0,
            'start_time': time.time()
        }
        
    def read_sensors(self):
        """Read all sensor values"""
        try:
            # Ultrasonic distance
            self.sensor_data.ultrasonic_distance = self.px.get_distance()
            
            # Grayscale sensors
            self.sensor_data.grayscale_values = self.px.get_grayscale_data()
            
            # Camera frame
            self.sensor_data.camera_frame = self.px.camera.read()
            
            # Process vision data
            if self.sensor_data.camera_frame is not None:
                self.sensor_data.obstacles_detected = self.vision_processor.detect_obstacles(
                    self.sensor_data.camera_frame
                )
            
            # Check for cliff detection
            self.sensor_data.cliff_detected = any(
                val > self.cliff_threshold for val in self.sensor_data.grayscale_values
            )
            
            self.sensor_data.timestamp = time.time()
            
        except Exception as e:
            logging.error(f"Sensor reading error: {e}")
    
    def update_map(self):
        """Update navigation map with current sensor data"""
        # Add ultrasonic obstacle
        if (self.sensor_data.ultrasonic_distance > 0 and 
            self.sensor_data.ultrasonic_distance < 2.0):
            self.nav_map.add_obstacle(self.sensor_data.ultrasonic_distance, 0)
        
        # Add vision-detected obstacles
        for obstacle in self.sensor_data.obstacles_detected:
            self.nav_map.add_obstacle(obstacle['distance'], obstacle['angle'])
    
    def decide_action(self):
        """Main decision-making logic"""
        ultrasonic = self.sensor_data.ultrasonic_distance
        cliff = self.sensor_data.cliff_detected
        vision_obstacles = len(self.sensor_data.obstacles_detected)
        
        # Priority 1: Emergency stop for cliffs
        if cliff:
            self.stats['cliff_detections'] += 1
            return "emergency_stop"
        
        # Priority 2: Obstacle avoidance
        if ultrasonic > 0 and ultrasonic < self.safe_distance:
            self.stats['obstacles_avoided'] += 1
            return "avoid_obstacle"
            
        # Priority 3: Vision-based obstacle avoidance
        if vision_obstacles > 0:
            # Check if any obstacles are directly ahead
            for obstacle in self.sensor_data.obstacles_detected:
                if abs(obstacle['angle']) < 30 and obstacle['distance'] < 1.0:
                    return "avoid_vision_obstacle"
        
        # Priority 4: Continue exploration
        return "explore"
    
    def execute_action(self, action):
        """Execute the decided action"""
        if action == "emergency_stop":
            self.emergency_stop()
        elif action == "avoid_obstacle":
            self.avoid_obstacle()
        elif action == "avoid_vision_obstacle":
            self.avoid_vision_obstacle()
        elif action == "explore":
            self.explore_forward()
        
        # Update behavior state
        self.current_behavior = action
    
    def emergency_stop(self):
        """Emergency stop for cliff detection"""
        logging.warning("🚨 CLIFF DETECTED! Emergency stop!")
        self.px.stop()
        
        # Back away from cliff
        self.px.backward(self.cruise_speed)
        time.sleep(0.5)
        self.px.stop()
        
        # Turn away from cliff
        cliff_values = self.sensor_data.grayscale_values
        if cliff_values[0] > self.cliff_threshold:  # Left cliff
            self.px.turn_right(self.turn_speed)
        elif cliff_values[2] > self.cliff_threshold:  # Right cliff
            self.px.turn_left(self.turn_speed)
        else:  # Center or multiple cliffs
            self.px.turn_right(self.turn_speed)
        
        time.sleep(1.0)
        self.px.stop()
    
    def avoid_obstacle(self):
        """Avoid obstacle detected by ultrasonic sensor"""
        distance = self.sensor_data.ultrasonic_distance
        logging.info(f"🚧 Avoiding obstacle at {distance:.2f}m")
        
        self.px.stop()
        time.sleep(0.2)
        
        # Decide turn direction based on map and last turn
        if self.nav_map.is_path_clear(1.0, -45):  # Check left
            self.px.turn_left(self.turn_speed)
            self.last_turn_direction = -1
        elif self.nav_map.is_path_clear(1.0, 45):  # Check right
            self.px.turn_right(self.turn_speed)
            self.last_turn_direction = 1
        else:
            # Both sides blocked, turn around
            self.px.turn_right(self.turn_speed)
            time.sleep(0.5)  # Longer turn for 180 degrees
            
        time.sleep(0.8)
        self.px.stop()
    
    def avoid_vision_obstacle(self):
        """Avoid obstacle detected by camera"""
        obstacles = self.sensor_data.obstacles_detected
        logging.info(f"👁️ Avoiding {len(obstacles)} vision obstacle(s)")
        
        # Find the closest obstacle
        closest = min(obstacles, key=lambda x: x['distance'])
        
        # Turn away from obstacle
        if closest['angle'] < 0:  # Obstacle on left, turn right
            self.px.turn_right(self.turn_speed)
        else:  # Obstacle on right, turn left
            self.px.turn_left(self.turn_speed)
            
        time.sleep(0.5)
        self.px.stop()
    
    def explore_forward(self):
        """Move forward while exploring"""
        self.px.forward(self.cruise_speed)
        
        # Add some random exploration behavior
        self.exploration_timer += 0.1
        if self.exploration_timer > 5.0:  # Change direction occasionally
            if np.random.random() > 0.7:  # 30% chance to turn
                if np.random.random() > 0.5:
                    self.px.turn_right(self.turn_speed)
                else:
                    self.px.turn_left(self.turn_speed)
                time.sleep(0.3)
            self.exploration_timer = 0
    
    def print_status(self):
        """Print current status information"""
        elapsed = time.time() - self.stats['start_time']
        
        print(f"\n🤖 Navigation Status (Running {elapsed:.1f}s)")
        print(f"   Behavior: {self.current_behavior}")
        print(f"   Ultrasonic: {self.sensor_data.ultrasonic_distance:.2f}m")
        print(f"   Grayscale: {self.sensor_data.grayscale_values}")
        print(f"   Vision Obstacles: {len(self.sensor_data.obstacles_detected)}")
        print(f"   Cliff Detected: {'YES' if self.sensor_data.cliff_detected else 'No'}")
        print(f"   Obstacles Avoided: {self.stats['obstacles_avoided']}")
        print(f"   Cliff Detections: {self.stats['cliff_detections']}")
        
        # Show vision obstacle details
        if self.sensor_data.obstacles_detected:
            print("   👁️ Vision Obstacles:")
            for i, obs in enumerate(self.sensor_data.obstacles_detected[:3]):  # Show top 3
                print(f"      {i+1}: {obs['distance']:.2f}m at {obs['angle']:.0f}°")
    
    def run(self, duration=60):
        """Main navigation loop"""
        print("🚀 Starting Advanced Autonomous Navigation")
        print("=" * 50)
        
        try:
            with Picarx() as px:
                self.px = px
                self.running = True
                
                start_time = time.time()
                last_status_time = 0
                
                while self.running and (time.time() - start_time) < duration:
                    loop_start = time.time()
                    
                    # Read all sensors
                    self.read_sensors()
                    
                    # Update navigation map
                    self.update_map()
                    
                    # Decide what to do
                    action = self.decide_action()
                    
                    # Execute the action
                    self.execute_action(action)
                    
                    # Print status every 3 seconds
                    if time.time() - last_status_time > 3.0:
                        self.print_status()
                        last_status_time = time.time()
                    
                    # Maintain loop timing (10 Hz)
                    elapsed = time.time() - loop_start
                    if elapsed < 0.1:
                        time.sleep(0.1 - elapsed)
                
                # Stop robot
                self.px.stop()
                
        except KeyboardInterrupt:
            print("\n🛑 Navigation interrupted by user")
        except Exception as e:
            print(f"❌ Navigation error: {e}")
        finally:
            self.running = False
            if self.px:
                self.px.stop()
    
    def save_map(self, filename="navigation_map.json"):
        """Save the navigation map to file"""
        map_data = {
            'grid': self.nav_map.grid.tolist(),
            'size': self.nav_map.size,
            'resolution': self.nav_map.resolution,
            'robot_pos': self.nav_map.robot_pos,
            'stats': self.stats,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(map_data, f, indent=2)
            print(f"💾 Navigation map saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving map: {e}")

def main():
    """Main function with menu system"""
    navigator = AutonomousNavigator()
    
    print("🤖 Advanced Autonomous Navigation System")
    print("=" * 45)
    print()
    print("This system combines:")
    print("• 📏 Ultrasonic sensor for distance measurement")
    print("• 🌫️ Grayscale sensors for cliff detection") 
    print("• 🎥 Camera vision for obstacle detection")
    print("• 🗺️ Navigation mapping and path planning")
    print("• 🧠 AI decision-making for autonomous behavior")
    print()
    
    while True:
        print("\nChoose navigation mode:")
        print("1. 🚀 Start autonomous navigation (60 seconds)")
        print("2. ⏱️ Quick test run (15 seconds)")
        print("3. 🏃 Extended exploration (5 minutes)")
        print("4. 📊 Sensor test mode")
        print("5. 💾 Save current map")
        print("6. 🚪 Exit")
        
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == '1':
            navigator.run(duration=60)
        elif choice == '2':
            navigator.run(duration=15)
        elif choice == '3':
            navigator.run(duration=300)
        elif choice == '4':
            sensor_test_mode(navigator)
        elif choice == '5':
            navigator.save_map()
        elif choice == '6':
            break
        else:
            print("❌ Invalid choice. Please try again.")
    
    print("\n🤖 Advanced navigation system shutdown complete!")

def sensor_test_mode(navigator):
    """Test all sensors without movement"""
    print("\n🔍 Sensor Test Mode")
    print("=" * 20)
    print("Testing sensors for 10 seconds (no movement)...")
    
    try:
        with Picarx() as px:
            navigator.px = px
            
            for i in range(20):  # 10 seconds at 2Hz
                navigator.read_sensors()
                
                print(f"\n📊 Sensor Reading #{i+1}:")
                print(f"   Ultrasonic: {navigator.sensor_data.ultrasonic_distance:.2f}m")
                print(f"   Grayscale: L={navigator.sensor_data.grayscale_values[0]} "
                      f"C={navigator.sensor_data.grayscale_values[1]} "
                      f"R={navigator.sensor_data.grayscale_values[2]}")
                print(f"   Vision obstacles: {len(navigator.sensor_data.obstacles_detected)}")
                print(f"   Cliff detected: {'YES' if navigator.sensor_data.cliff_detected else 'No'}")
                
                time.sleep(0.5)
                
    except KeyboardInterrupt:
        print("\n🛑 Sensor test interrupted")
    except Exception as e:
        print(f"❌ Sensor test error: {e}")

if __name__ == "__main__":
    main()