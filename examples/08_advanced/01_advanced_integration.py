#!/usr/bin/env python3
"""
🚀 Advanced Integration - Complex Multi-System Robotics

This example demonstrates advanced integration of multiple robot systems
working together in coordinated, sophisticated ways.

Learn to:
- Multi-sensor fusion and coordination
- Complex behavior state machines
- Real-time decision making systems
- Advanced navigation algorithms
- System-level performance optimization
- Fault tolerance and error recovery
"""

from picarx import Picarx
from time import sleep, time
from robot_hat import TTS, Music
from vilib import Vilib
import threading
import queue
import json
import math
import random
from datetime import datetime, timedelta
from collections import deque
import numpy as np


def explain_advanced_integration():
    """Explain advanced integration concepts"""
    print("🚀 Advanced Integration Concepts:")
    print()
    print("🔧 Multi-System Coordination:")
    print("   • Sensor fusion for enhanced perception")
    print("   • Simultaneous multi-modal operation")
    print("   • Real-time system synchronization")
    print("   • Complex behavior orchestration")
    print()
    print("⚡ Advanced Features:")
    print("   • Predictive navigation algorithms")
    print("   • Adaptive performance optimization")
    print("   • Fault tolerance and graceful degradation")
    print("   • Dynamic resource management")
    print("   • Machine learning integration")
    print()
    print("🎯 Real-World Applications:")
    print("   • Autonomous navigation systems")
    print("   • Industrial automation robots")
    print("   • Search and rescue operations")
    print("   • Advanced surveillance systems")
    print()


class AdvancedSensorFusion:
    """Advanced sensor fusion system for enhanced robot perception"""
    
    def __init__(self):
        self.sensor_data = {
            "ultrasonic": deque(maxlen=10),
            "camera": deque(maxlen=5),
            "line_following": deque(maxlen=15),
            "movement": deque(maxlen=20)
        }
        
        self.fusion_weights = {
            "ultrasonic": 0.4,
            "camera": 0.3,
            "line_following": 0.2,
            "movement": 0.1
        }
        
        self.environment_map = {
            "obstacles": [],
            "paths": [],
            "interesting_objects": [],
            "safe_zones": []
        }
        
        self.confidence_scores = {
            "obstacle_detection": 0.5,
            "path_planning": 0.5,
            "object_recognition": 0.5,
            "navigation": 0.5
        }
    
    def update_sensor_data(self, sensor_type, data):
        """Update sensor data with timestamp and confidence"""
        timestamped_data = {
            "value": data,
            "timestamp": time(),
            "confidence": self.calculate_sensor_confidence(sensor_type, data)
        }
        self.sensor_data[sensor_type].append(timestamped_data)
    
    def calculate_sensor_confidence(self, sensor_type, data):
        """Calculate confidence score for sensor reading"""
        if sensor_type == "ultrasonic":
            # Higher confidence for consistent readings
            if len(self.sensor_data[sensor_type]) > 3:
                recent_values = [reading["value"] for reading in list(self.sensor_data[sensor_type])[-3:]]
                variance = np.var(recent_values) if len(recent_values) > 1 else 0
                return max(0.2, 1.0 - (variance / 100))  # Normalize variance
            return 0.5
        
        elif sensor_type == "camera":
            # Confidence based on detection count and clarity
            detected_objects = data.get("objects", 0)
            return min(0.9, 0.3 + (detected_objects * 0.15))
        
        elif sensor_type == "line_following":
            # Confidence based on line detection quality
            line_quality = data.get("quality", 0.5)
            return min(0.95, max(0.1, line_quality))
        
        else:
            return 0.5
    
    def fuse_sensor_data(self):
        """Perform advanced sensor fusion for comprehensive environment understanding"""
        fused_perception = {
            "obstacle_distance": None,
            "path_confidence": 0.0,
            "object_count": 0,
            "navigation_safety": 0.5,
            "recommended_action": "explore"
        }
        
        # Weighted sensor fusion
        total_weight = 0
        distance_sum = 0
        
        # Process ultrasonic data
        if self.sensor_data["ultrasonic"]:
            recent_ultrasonic = list(self.sensor_data["ultrasonic"])[-3:]
            avg_distance = np.mean([reading["value"] for reading in recent_ultrasonic])
            avg_confidence = np.mean([reading["confidence"] for reading in recent_ultrasonic])
            
            weight = self.fusion_weights["ultrasonic"] * avg_confidence
            distance_sum += avg_distance * weight
            total_weight += weight
        
        # Process camera data
        if self.sensor_data["camera"]:
            latest_camera = self.sensor_data["camera"][-1]
            object_count = latest_camera["value"].get("objects", 0)
            camera_confidence = latest_camera["confidence"]
            
            fused_perception["object_count"] = object_count
            
            # Camera influences navigation safety
            camera_weight = self.fusion_weights["camera"] * camera_confidence
            if object_count > 2:
                fused_perception["navigation_safety"] -= 0.2 * camera_weight
        
        # Process line following data
        if self.sensor_data["line_following"]:
            latest_line = self.sensor_data["line_following"][-1]
            line_quality = latest_line["value"].get("quality", 0.5)
            line_confidence = latest_line["confidence"]
            
            path_weight = self.fusion_weights["line_following"] * line_confidence
            fused_perception["path_confidence"] = line_quality * path_weight
        
        # Finalize distance fusion
        if total_weight > 0:
            fused_perception["obstacle_distance"] = distance_sum / total_weight
        
        # Determine recommended action
        fused_perception["recommended_action"] = self.determine_optimal_action(fused_perception)
        
        return fused_perception
    
    def determine_optimal_action(self, perception):
        """Use fused sensor data to determine optimal robot action"""
        safety = perception["navigation_safety"]
        distance = perception["obstacle_distance"]
        path_conf = perception["path_confidence"]
        objects = perception["object_count"]
        
        # Decision matrix based on fused perception
        if distance and distance < 20:
            if safety > 0.6:
                return "careful_navigation"
            else:
                return "obstacle_avoidance"
        
        elif path_conf > 0.7:
            return "follow_path"
        
        elif objects > 3:
            return "investigate_objects"
        
        elif safety > 0.8:
            return "explore_forward"
        
        else:
            return "cautious_exploration"


class AdvancedNavigationSystem:
    """Advanced navigation with predictive pathfinding and optimization"""
    
    def __init__(self):
        self.position_history = deque(maxlen=50)
        self.waypoints = []
        self.path_memory = {}
        self.navigation_goals = deque(maxlen=10)
        
        # Advanced navigation parameters
        self.exploration_radius = 100  # cm
        self.path_optimization_enabled = True
        self.predictive_navigation = True
        
        # Performance metrics
        self.navigation_efficiency = 0.5
        self.collision_count = 0
        self.successful_navigations = 0
    
    def add_waypoint(self, x, y, goal_type="exploration"):
        """Add navigation waypoint with type and priority"""
        waypoint = {
            "x": x,
            "y": y,
            "type": goal_type,
            "timestamp": time(),
            "priority": self.calculate_waypoint_priority(goal_type),
            "visited": False
        }
        self.waypoints.append(waypoint)
        print(f"🎯 Waypoint added: ({x}, {y}) - {goal_type}")
    
    def calculate_waypoint_priority(self, goal_type):
        """Calculate waypoint priority based on type and context"""
        priorities = {
            "emergency": 1.0,
            "investigation": 0.8,
            "exploration": 0.6,
            "maintenance": 0.4,
            "curiosity": 0.3
        }
        return priorities.get(goal_type, 0.5)
    
    def update_position(self, x, y, heading):
        """Update current position and heading"""
        position = {
            "x": x,
            "y": y,
            "heading": heading,
            "timestamp": time()
        }
        self.position_history.append(position)
    
    def plan_optimal_path(self, target_x, target_y):
        """Plan optimal path using advanced algorithms"""
        if not self.position_history:
            return [(target_x, target_y)]
        
        current_pos = self.position_history[-1]
        start_x, start_y = current_pos["x"], current_pos["y"]
        
        # Simple A* inspired pathfinding
        path = self.astar_pathfinding(start_x, start_y, target_x, target_y)
        
        if self.path_optimization_enabled:
            path = self.optimize_path(path)
        
        return path
    
    def astar_pathfinding(self, start_x, start_y, goal_x, goal_y):
        """Simplified A* pathfinding algorithm"""
        # For demo purposes, create a simple path with intermediate points
        path = []
        
        dx = goal_x - start_x
        dy = goal_y - start_y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Create intermediate waypoints for smooth navigation
        if distance > 30:  # If distance is significant
            steps = int(distance / 20)  # Create waypoint every 20cm
            
            for i in range(1, steps + 1):
                progress = i / steps
                intermediate_x = start_x + (dx * progress)
                intermediate_y = start_y + (dy * progress)
                
                # Add some path smoothing
                path.append((intermediate_x, intermediate_y))
        
        path.append((goal_x, goal_y))
        return path
    
    def optimize_path(self, path):
        """Optimize path for efficiency and smoothness"""
        if len(path) < 3:
            return path
        
        optimized = [path[0]]
        
        for i in range(1, len(path) - 1):
            # Check if we can skip intermediate points for smoother path
            prev_point = optimized[-1]
            current_point = path[i]
            next_point = path[i + 1]
            
            # Calculate path smoothness metric
            angle_change = self.calculate_angle_change(prev_point, current_point, next_point)
            
            # Keep point if it represents a significant direction change
            if angle_change > 30:  # degrees
                optimized.append(current_point)
        
        optimized.append(path[-1])
        return optimized
    
    def calculate_angle_change(self, p1, p2, p3):
        """Calculate angle change between three points"""
        v1 = (p2[0] - p1[0], p2[1] - p1[1])
        v2 = (p3[0] - p2[0], p3[1] - p2[1])
        
        # Calculate angle between vectors
        dot_product = v1[0]*v2[0] + v1[1]*v2[1]
        mag1 = math.sqrt(v1[0]*v1[0] + v1[1]*v1[1])
        mag2 = math.sqrt(v2[0]*v2[0] + v2[1]*v2[1])
        
        if mag1 == 0 or mag2 == 0:
            return 0
        
        cos_angle = dot_product / (mag1 * mag2)
        cos_angle = max(-1, min(1, cos_angle))  # Clamp to valid range
        
        angle = math.acos(cos_angle)
        return math.degrees(angle)
    
    def execute_navigation_step(self, px, target_x, target_y):
        """Execute one step of advanced navigation"""
        if not self.position_history:
            return False
        
        current_pos = self.position_history[-1]
        
        # Calculate direction and distance
        dx = target_x - current_pos["x"]
        dy = target_y - current_pos["y"]
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < 5:  # Close enough to target
            return True
        
        # Calculate required heading
        target_heading = math.degrees(math.atan2(dy, dx))
        current_heading = current_pos["heading"]
        
        # Calculate turn angle needed
        turn_angle = target_heading - current_heading
        
        # Normalize turn angle to [-180, 180]
        while turn_angle > 180:
            turn_angle -= 360
        while turn_angle < -180:
            turn_angle += 360
        
        # Execute movement with advanced control
        if abs(turn_angle) > 10:  # Need to turn
            turn_direction = -30 if turn_angle < 0 else 30
            px.set_dir_servo_angle(turn_direction)
            px.forward(30)
            sleep(0.5)
            px.set_dir_servo_angle(0)
        else:  # Move forward
            speed = min(60, max(30, 60 - abs(turn_angle)))  # Adaptive speed
            px.forward(speed)
            sleep(0.8)
        
        px.stop()
        
        # Update position (simulated)
        new_x = current_pos["x"] + 10 * math.cos(math.radians(current_heading))
        new_y = current_pos["y"] + 10 * math.sin(math.radians(current_heading))
        new_heading = current_heading + (turn_angle * 0.5)  # Partial turn
        
        self.update_position(new_x, new_y, new_heading)
        
        return False


def advanced_autonomous_mission():
    """Demonstrate advanced autonomous mission with multi-system integration"""
    print("🚀 Advanced Autonomous Mission")
    print("Multi-system integration with advanced navigation and sensor fusion!")
    
    # Initialize advanced systems
    sensor_fusion = AdvancedSensorFusion()
    navigation = AdvancedNavigationSystem()
    tts = TTS()
    
    # Set up mission parameters
    mission_goals = [
        {"x": 50, "y": 0, "type": "exploration"},
        {"x": 50, "y": 50, "type": "investigation"},
        {"x": 0, "y": 50, "type": "investigation"},
        {"x": 0, "y": 0, "type": "emergency"}
    ]
    
    # Add mission waypoints
    for goal in mission_goals:
        navigation.add_waypoint(goal["x"], goal["y"], goal["type"])
    
    with Picarx() as px:
        print("🚀 Initializing advanced autonomous mission...")
        tts.say("Advanced autonomous mission initializing!")
        
        # Initialize position
        navigation.update_position(0, 0, 0)
        
        # Start camera for visual perception
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=True, web=True)
        sleep(2)
        
        mission_start = time()
        step_count = 0
        max_steps = 25
        
        print("🎯 Mission objectives:")
        for i, goal in enumerate(mission_goals, 1):
            print(f"   {i}. Navigate to ({goal['x']}, {goal['y']}) - {goal['type']}")
        
        try:
            while step_count < max_steps and navigation.waypoints:
                print(f"\n--- Mission Step {step_count + 1} ---")
                
                # Simulate sensor readings
                ultrasonic_distance = random.randint(20, 100)
                camera_objects = random.randint(0, 5)
                line_quality = random.uniform(0.3, 0.9)
                
                # Update sensor fusion system
                sensor_fusion.update_sensor_data("ultrasonic", ultrasonic_distance)
                sensor_fusion.update_sensor_data("camera", {"objects": camera_objects})
                sensor_fusion.update_sensor_data("line_following", {"quality": line_quality})
                
                # Perform sensor fusion
                perception = sensor_fusion.fuse_sensor_data()
                
                print(f"🔍 Perception: {perception['recommended_action']}")
                print(f"   Distance: {perception['obstacle_distance']:.1f}cm")
                print(f"   Objects: {perception['object_count']}")
                print(f"   Safety: {perception['navigation_safety']:.2f}")
                
                # Select next waypoint based on priority
                current_waypoint = None
                highest_priority = -1
                
                for waypoint in navigation.waypoints:
                    if not waypoint["visited"] and waypoint["priority"] > highest_priority:
                        highest_priority = waypoint["priority"]
                        current_waypoint = waypoint
                
                if current_waypoint:
                    print(f"🎯 Target: ({current_waypoint['x']}, {current_waypoint['y']}) - {current_waypoint['type']}")
                    
                    # Plan optimal path
                    path = navigation.plan_optimal_path(current_waypoint["x"], current_waypoint["y"])
                    print(f"📍 Path planned with {len(path)} waypoints")
                    
                    # Execute navigation step
                    if len(path) > 0:
                        next_x, next_y = path[0]
                        reached = navigation.execute_navigation_step(px, next_x, next_y)
                        
                        if reached:
                            current_waypoint["visited"] = True
                            navigation.successful_navigations += 1
                            print(f"✅ Waypoint reached: {current_waypoint['type']}")
                            tts.say(f"Objective complete: {current_waypoint['type']}")
                
                # Advanced decision making based on perception
                action = perception["recommended_action"]
                
                if action == "obstacle_avoidance":
                    print("⚠️ Executing advanced obstacle avoidance...")
                    # Complex avoidance maneuver
                    px.set_dir_servo_angle(-45)
                    px.forward(40)
                    sleep(1)
                    px.set_dir_servo_angle(45)
                    px.forward(40)
                    sleep(1)
                    px.set_dir_servo_angle(0)
                    navigation.collision_count += 1
                
                elif action == "investigate_objects":
                    print("🔍 Investigating detected objects...")
                    # Investigation behavior
                    px.forward(20)
                    sleep(0.5)
                    for angle in [-30, 30, -30, 0]:
                        px.set_dir_servo_angle(angle)
                        sleep(0.5)
                    px.stop()
                
                elif action == "explore_forward":
                    print("🗺️ Confident forward exploration...")
                    px.forward(50)
                    sleep(1.2)
                    px.stop()
                
                else:
                    print(f"🤖 Executing: {action}")
                    px.forward(35)
                    sleep(0.8)
                    px.stop()
                
                # Performance monitoring
                step_count += 1
                mission_time = time() - mission_start
                
                if step_count % 5 == 0:
                    completed_waypoints = sum(1 for wp in navigation.waypoints if wp["visited"])
                    print(f"📊 Mission Progress:")
                    print(f"   Time: {mission_time:.1f}s")
                    print(f"   Completed: {completed_waypoints}/{len(navigation.waypoints)}")
                    print(f"   Efficiency: {navigation.navigation_efficiency:.2f}")
                
                sleep(0.5)
        
        except KeyboardInterrupt:
            print("\n🚀 Mission interrupted!")
        
        finally:
            px.stop()
            Vilib.camera_close()
            
            # Mission summary
            mission_duration = time() - mission_start
            completed_objectives = sum(1 for wp in navigation.waypoints if wp["visited"])
            
            print(f"\n🚀 Advanced Mission Complete!")
            print(f"   Duration: {mission_duration:.1f} seconds")
            print(f"   Objectives completed: {completed_objectives}/{len(navigation.waypoints)}")
            print(f"   Navigation successes: {navigation.successful_navigations}")
            print(f"   Collision incidents: {navigation.collision_count}")
            print(f"   Final efficiency: {navigation.navigation_efficiency:.2f}")
            
            if completed_objectives == len(navigation.waypoints):
                tts.say("Mission accomplished! All objectives completed successfully!")
            else:
                tts.say("Mission partially completed. Great effort!")


def performance_optimization_demo():
    """Demonstrate advanced performance optimization techniques"""
    print("⚡ Performance Optimization Demo")
    print("Advanced techniques for maximizing robot performance!")
    
    class PerformanceMonitor:
        def __init__(self):
            self.metrics = {
                "movement_efficiency": deque(maxlen=20),
                "response_time": deque(maxlen=15),
                "resource_usage": deque(maxlen=10),
                "error_rate": deque(maxlen=25)
            }
            self.optimization_enabled = True
            self.adaptive_parameters = {
                "base_speed": 50,
                "turn_sensitivity": 30,
                "reaction_delay": 0.1
            }
        
        def record_metric(self, metric_type, value):
            self.metrics[metric_type].append({
                "value": value,
                "timestamp": time()
            })
        
        def get_average_metric(self, metric_type):
            if not self.metrics[metric_type]:
                return 0
            return np.mean([m["value"] for m in self.metrics[metric_type]])
        
        def optimize_parameters(self):
            """Dynamic parameter optimization based on performance"""
            efficiency = self.get_average_metric("movement_efficiency")
            response_time = self.get_average_metric("response_time")
            
            # Adaptive speed optimization
            if efficiency < 0.6:
                self.adaptive_parameters["base_speed"] = max(30, 
                    self.adaptive_parameters["base_speed"] - 5)
                print("🔧 Reducing speed for better control")
            elif efficiency > 0.8 and response_time < 0.2:
                self.adaptive_parameters["base_speed"] = min(70,
                    self.adaptive_parameters["base_speed"] + 3)
                print("⚡ Increasing speed for better performance")
            
            # Turn sensitivity optimization
            error_rate = self.get_average_metric("error_rate")
            if error_rate > 0.3:
                self.adaptive_parameters["turn_sensitivity"] = max(15,
                    self.adaptive_parameters["turn_sensitivity"] - 5)
                print("🎯 Reducing turn sensitivity for stability")
    
    monitor = PerformanceMonitor()
    tts = TTS()
    
    with Picarx() as px:
        print("⚡ Starting performance optimization demonstration...")
        tts.say("Performance optimization demo starting!")
        
        demo_start = time()
        optimization_cycles = 8
        
        for cycle in range(optimization_cycles):
            print(f"\n--- Optimization Cycle {cycle + 1} ---")
            
            cycle_start = time()
            
            # Simulate complex robot task
            movements = ["forward", "left", "right", "forward", "backward"]
            
            for movement in movements:
                movement_start = time()
                
                # Execute movement with current parameters
                speed = monitor.adaptive_parameters["base_speed"]
                turn_angle = monitor.adaptive_parameters["turn_sensitivity"]
                delay = monitor.adaptive_parameters["reaction_delay"]
                
                if movement == "forward":
                    px.forward(speed)
                    sleep(1.0 + delay)
                    px.stop()
                elif movement == "backward":
                    px.backward(speed)
                    sleep(0.8 + delay)
                    px.stop()
                elif movement in ["left", "right"]:
                    angle = -turn_angle if movement == "left" else turn_angle
                    px.set_dir_servo_angle(angle)
                    px.forward(speed - 10)
                    sleep(0.6 + delay)
                    px.stop()
                    px.set_dir_servo_angle(0)
                
                # Record performance metrics
                movement_time = time() - movement_start
                monitor.record_metric("response_time", movement_time)
                
                # Simulate efficiency measurement
                efficiency = random.uniform(0.4, 0.9)
                monitor.record_metric("movement_efficiency", efficiency)
                
                # Simulate error rate
                error_rate = random.uniform(0.1, 0.4)
                monitor.record_metric("error_rate", error_rate)
                
                sleep(0.2)
            
            cycle_time = time() - cycle_start
            monitor.record_metric("resource_usage", cycle_time)
            
            # Performance analysis
            avg_efficiency = monitor.get_average_metric("movement_efficiency")
            avg_response = monitor.get_average_metric("response_time")
            avg_errors = monitor.get_average_metric("error_rate")
            
            print(f"📊 Cycle {cycle + 1} Performance:")
            print(f"   Efficiency: {avg_efficiency:.2f}")
            print(f"   Response time: {avg_response:.2f}s")
            print(f"   Error rate: {avg_errors:.2f}")
            print(f"   Cycle time: {cycle_time:.2f}s")
            
            # Apply optimizations
            if monitor.optimization_enabled:
                monitor.optimize_parameters()
                print(f"🔧 Optimized parameters:")
                print(f"   Speed: {monitor.adaptive_parameters['base_speed']}")
                print(f"   Turn sensitivity: {monitor.adaptive_parameters['turn_sensitivity']}")
            
            # Announce progress
            if cycle % 3 == 2:
                tts.say(f"Optimization cycle {cycle + 1} complete!")
        
        # Final performance summary
        total_time = time() - demo_start
        final_efficiency = monitor.get_average_metric("movement_efficiency")
        initial_speed = 50
        final_speed = monitor.adaptive_parameters["base_speed"]
        
        print(f"\n⚡ Performance Optimization Complete!")
        print(f"   Total duration: {total_time:.1f} seconds")
        print(f"   Final efficiency: {final_efficiency:.2f}")
        print(f"   Speed optimization: {initial_speed} -> {final_speed}")
        print(f"   Performance improvement: {((final_efficiency - 0.5) * 100):.1f}%")
        
        tts.say("Performance optimization complete! System efficiency improved!")


def fault_tolerance_demo():
    """Demonstrate advanced fault tolerance and error recovery"""
    print("🛡️ Fault Tolerance & Error Recovery Demo")
    print("Advanced error handling and system resilience!")
    
    class FaultTolerantSystem:
        def __init__(self):
            self.health_status = {
                "motors": "healthy",
                "sensors": "healthy", 
                "camera": "healthy",
                "communication": "healthy"
            }
            self.error_history = deque(maxlen=50)
            self.recovery_strategies = {
                "motor_fault": self.recover_motor_fault,
                "sensor_fault": self.recover_sensor_fault,
                "camera_fault": self.recover_camera_fault,
                "communication_fault": self.recover_communication_fault
            }
            self.backup_systems = {
                "navigation": True,
                "obstacle_detection": True,
                "manual_override": True
            }
        
        def simulate_fault(self, system, severity="moderate"):
            """Simulate system fault for demonstration"""
            self.health_status[system] = f"fault_{severity}"
            fault_data = {
                "system": system,
                "severity": severity,
                "timestamp": time(),
                "recovered": False
            }
            self.error_history.append(fault_data)
            print(f"⚠️ {severity.upper()} FAULT: {system} system malfunction!")
            return fault_data
        
        def diagnose_system(self):
            """Comprehensive system diagnosis"""
            diagnosis = {
                "overall_health": "healthy",
                "critical_faults": [],
                "warning_faults": [],
                "recovery_needed": []
            }
            
            for system, status in self.health_status.items():
                if "fault" in status:
                    severity = status.split("_")[1]
                    if severity in ["critical", "severe"]:
                        diagnosis["critical_faults"].append(system)
                        diagnosis["overall_health"] = "critical"
                    elif severity == "moderate":
                        diagnosis["warning_faults"].append(system)
                        if diagnosis["overall_health"] == "healthy":
                            diagnosis["overall_health"] = "degraded"
                    
                    diagnosis["recovery_needed"].append(system)
            
            return diagnosis
        
        def recover_motor_fault(self, fault_data):
            """Motor fault recovery procedures"""
            print("🔧 Initiating motor fault recovery...")
            
            # Simulate recovery steps
            recovery_steps = [
                "Stopping all motor activity",
                "Running motor diagnostics",
                "Recalibrating motor controllers",
                "Testing motor functionality",
                "Switching to backup navigation mode"
            ]
            
            for step in recovery_steps:
                print(f"   {step}...")
                sleep(0.5)
            
            # Recovery success simulation
            if random.random() > 0.3:  # 70% success rate
                self.health_status["motors"] = "healthy"
                fault_data["recovered"] = True
                print("✅ Motor system recovery successful!")
                return True
            else:
                print("❌ Motor recovery failed - activating manual override")
                self.backup_systems["manual_override"] = True
                return False
        
        def recover_sensor_fault(self, fault_data):
            """Sensor fault recovery procedures"""
            print("🔧 Initiating sensor fault recovery...")
            
            recovery_steps = [
                "Isolating faulty sensor",
                "Switching to redundant sensors",
                "Recalibrating sensor array",
                "Validating sensor readings"
            ]
            
            for step in recovery_steps:
                print(f"   {step}...")
                sleep(0.4)
            
            if random.random() > 0.2:  # 80% success rate
                self.health_status["sensors"] = "healthy"
                fault_data["recovered"] = True
                print("✅ Sensor system recovery successful!")
                return True
            else:
                print("❌ Sensor recovery partial - using backup detection")
                self.backup_systems["obstacle_detection"] = True
                return False
        
        def recover_camera_fault(self, fault_data):
            """Camera fault recovery procedures"""
            print("🔧 Initiating camera fault recovery...")
            
            recovery_steps = [
                "Resetting camera interface",
                "Checking camera connections",
                "Restarting camera service",
                "Testing image capture"
            ]
            
            for step in recovery_steps:
                print(f"   {step}...")
                sleep(0.3)
            
            if random.random() > 0.4:  # 60% success rate
                self.health_status["camera"] = "healthy"
                fault_data["recovered"] = True
                print("✅ Camera system recovery successful!")
                return True
            else:
                print("❌ Camera recovery failed - using sensor navigation")
                self.backup_systems["navigation"] = True
                return False
        
        def recover_communication_fault(self, fault_data):
            """Communication fault recovery procedures"""
            print("🔧 Initiating communication fault recovery...")
            
            recovery_steps = [
                "Testing network connectivity",
                "Resetting communication modules",
                "Switching to backup protocols",
                "Validating data transmission"
            ]
            
            for step in recovery_steps:
                print(f"   {step}...")
                sleep(0.4)
            
            if random.random() > 0.25:  # 75% success rate
                self.health_status["communication"] = "healthy"
                fault_data["recovered"] = True
                print("✅ Communication system recovery successful!")
                return True
            else:
                print("❌ Communication recovery failed - operating autonomously")
                return False
        
        def execute_recovery(self, fault_data):
            """Execute appropriate recovery strategy"""
            system = fault_data["system"]
            fault_type = f"{system}_fault"
            
            if fault_type in self.recovery_strategies:
                return self.recovery_strategies[fault_type](fault_data)
            else:
                print(f"⚠️ No recovery strategy for {system} fault")
                return False
    
    fault_system = FaultTolerantSystem()
    tts = TTS()
    
    with Picarx() as px:
        print("🛡️ Starting fault tolerance demonstration...")
        tts.say("Fault tolerance demonstration starting!")
        
        # Simulate various fault scenarios
        fault_scenarios = [
            {"system": "sensors", "severity": "moderate"},
            {"system": "motors", "severity": "severe"},
            {"system": "camera", "severity": "moderate"},
            {"system": "communication", "severity": "critical"},
            {"system": "sensors", "severity": "critical"}
        ]
        
        demo_start = time()
        recovery_count = 0
        
        for i, scenario in enumerate(fault_scenarios, 1):
            print(f"\n--- Fault Scenario {i} ---")
            
            # Normal operation first
            print("🤖 Normal operation...")
            px.forward(40)
            sleep(1)
            px.stop()
            
            # Introduce fault
            fault_data = fault_system.simulate_fault(
                scenario["system"], 
                scenario["severity"]
            )
            
            tts.say(f"{scenario['system']} fault detected!")
            
            # System diagnosis
            diagnosis = fault_system.diagnose_system()
            print(f"🔍 System diagnosis: {diagnosis['overall_health']}")
            
            if diagnosis["critical_faults"]:
                print(f"🚨 Critical faults: {', '.join(diagnosis['critical_faults'])}")
            if diagnosis["warning_faults"]:
                print(f"⚠️ Warning faults: {', '.join(diagnosis['warning_faults'])}")
            
            # Attempt recovery
            if diagnosis["recovery_needed"]:
                print("🔧 Initiating fault recovery procedures...")
                
                recovery_success = fault_system.execute_recovery(fault_data)
                
                if recovery_success:
                    recovery_count += 1
                    print("✅ System recovery successful - resuming normal operation")
                    tts.say("System recovered successfully!")
                    
                    # Test recovered system
                    px.forward(30)
                    sleep(0.8)
                    px.stop()
                else:
                    print("⚠️ Recovery incomplete - operating with limitations")
                    tts.say("Operating with backup systems")
                    
                    # Limited operation mode
                    px.forward(20)
                    sleep(0.5)
                    px.stop()
            
            sleep(1)
        
        # Final system status
        demo_duration = time() - demo_start
        total_faults = len(fault_scenarios)
        recovery_rate = (recovery_count / total_faults) * 100
        
        print(f"\n🛡️ Fault Tolerance Demonstration Complete!")
        print(f"   Duration: {demo_duration:.1f} seconds")
        print(f"   Total faults simulated: {total_faults}")
        print(f"   Successful recoveries: {recovery_count}")
        print(f"   Recovery rate: {recovery_rate:.1f}%")
        
        # Final system health check
        diagnosis = fault_system.diagnose_system()
        print(f"   Final system health: {diagnosis['overall_health']}")
        
        if recovery_rate > 70:
            tts.say("Excellent fault tolerance! System resilience demonstrated!")
        else:
            tts.say("Fault tolerance demonstration complete. Backup systems operational.")


def main():
    """Main function with advanced integration options"""
    print("🚀 PiCar-X Advanced Integration Examples")
    print("Showcase complex multi-system robotics integration!")
    print("=" * 60)
    
    explain_advanced_integration()
    
    while True:
        print("\nChoose your advanced integration experience:")
        print("1. 🚀 Advanced autonomous mission")
        print("2. ⚡ Performance optimization demo")
        print("3. 🛡️ Fault tolerance demo")
        print("4. ❓ Explain advanced integration")
        print("5. 🚪 Exit")
        
        try:
            choice = input("\nEnter choice (1-5): ").strip()
            
            if choice == '1':
                advanced_autonomous_mission()
            elif choice == '2':
                performance_optimization_demo()
            elif choice == '3':
                fault_tolerance_demo()
            elif choice == '4':
                explain_advanced_integration()
            elif choice == '5':
                print("👋 Keep pushing robotics boundaries!")
                break
            else:
                print("⚠️ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Advanced integration exploration interrupted!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Advanced integration demonstrates:")
        print("   - Multi-system coordination")
        print("   - Performance optimization")
        print("   - Fault tolerance and recovery")
    
    print("\n🚀 Advanced integration exploration complete!")