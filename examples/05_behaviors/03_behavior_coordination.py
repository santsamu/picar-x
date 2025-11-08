#!/usr/bin/env python3
"""
🧠 Behavior Coordination - Advanced Multi-Behavior Systems

This example demonstrates how to coordinate multiple behaviors simultaneously.
Learn to manage competing behaviors, priorities, and complex decision making.

Learn to:
- Behavior arbitration and priority systems
- Subsumption architecture implementation
- Behavior fusion and blending
- Real-time behavior switching
- Conflict resolution between behaviors
- Performance monitoring and optimization
"""

from picarx import Picarx
from vilib import Vilib
import time
import random
import threading
from collections import deque


class BehaviorCoordinator:
    """Coordinates multiple robot behaviors with priorities"""
    
    def __init__(self, px):
        self.px = px
        self.behaviors = {}
        self.active_behaviors = set()
        self.behavior_outputs = {}
        self.coordination_mode = 'subsumption'  # 'subsumption', 'fusion', 'arbitration'
        self.running = False
        
        # Obstacle avoidance state for persistent behavior
        self.avoidance_state = {
            'avoiding': False,
            'avoid_direction': 0,
            'avoid_start_time': 0,
            'min_avoid_duration': 2.0  # Minimum time to maintain avoidance maneuver
        }
        
    def register_behavior(self, name, behavior_func, priority=1):
        """Register a behavior with its priority"""
        self.behaviors[name] = {
            'function': behavior_func,
            'priority': priority,
            'active': False,
            'last_output': None,
            'execution_time': 0
        }
    
    def activate_behavior(self, name):
        """Activate a behavior"""
        if name in self.behaviors:
            self.active_behaviors.add(name)
            self.behaviors[name]['active'] = True
            print(f"✅ Activated behavior: {name}")
    
    def deactivate_behavior(self, name):
        """Deactivate a behavior"""
        if name in self.active_behaviors:
            self.active_behaviors.remove(name)
            self.behaviors[name]['active'] = False
            print(f"❌ Deactivated behavior: {name}")
    
    def coordinate_behaviors(self):
        """Main coordination loop"""
        if self.coordination_mode == 'subsumption':
            return self._subsumption_coordination()
        elif self.coordination_mode == 'fusion':
            return self._fusion_coordination()
        elif self.coordination_mode == 'arbitration':
            return self._arbitration_coordination()
    
    def _subsumption_coordination(self):
        """Subsumption architecture - higher priority behaviors suppress lower ones"""
        if not self.active_behaviors:
            return None
        
        # Sort by priority (highest first)
        sorted_behaviors = sorted(
            self.active_behaviors,
            key=lambda name: self.behaviors[name]['priority'],
            reverse=True
        )
        
        # Execute highest priority behavior that can run
        for behavior_name in sorted_behaviors:
            start_time = time.time()
            try:
                output = self.behaviors[behavior_name]['function']()
                execution_time = time.time() - start_time
                self.behaviors[behavior_name]['execution_time'] = execution_time
                
                if output is not None:
                    self.behaviors[behavior_name]['last_output'] = output
                    return behavior_name, output
            except Exception as e:
                print(f"❌ Behavior {behavior_name} failed: {e}")
        
        return None
    
    def _fusion_coordination(self):
        """Fusion - blend outputs from multiple behaviors"""
        outputs = []
        total_priority = 0
        
        for behavior_name in self.active_behaviors:
            try:
                output = self.behaviors[behavior_name]['function']()
                if output is not None:
                    priority = self.behaviors[behavior_name]['priority']
                    outputs.append((behavior_name, output, priority))
                    total_priority += priority
            except Exception as e:
                print(f"❌ Behavior {behavior_name} failed: {e}")
        
        if not outputs:
            return None
        
        # Weighted average of outputs
        if total_priority > 0:
            blended_output = self._blend_outputs(outputs, total_priority)
            return "FUSION", blended_output
        
        return None
    
    def _arbitration_coordination(self):
        """Arbitration - select one behavior based on current conditions"""
        # Simple arbitration: choose behavior with highest activation level
        best_behavior = None
        best_score = -1
        
        for behavior_name in self.active_behaviors:
            # Calculate activation score (could be based on sensors, time, etc.)
            score = self._calculate_activation_score(behavior_name)
            if score > best_score:
                best_score = score
                best_behavior = behavior_name
        
        if best_behavior:
            try:
                output = self.behaviors[best_behavior]['function']()
                return best_behavior, output
            except Exception as e:
                print(f"❌ Behavior {best_behavior} failed: {e}")
        
        return None
    
    def _blend_outputs(self, outputs, total_priority):
        """Blend multiple behavior outputs"""
        # This is a simplified blending - in practice, you'd blend speeds, directions, etc.
        # For now, return the output from the highest priority behavior
        return max(outputs, key=lambda x: x[2])[1]
    
    def _calculate_activation_score(self, behavior_name):
        """Calculate how strongly a behavior should be activated"""
        # Simplified scoring - in practice, this would consider sensor inputs, goals, etc.
        base_priority = self.behaviors[behavior_name]['priority']
        random_factor = random.random() * 0.5  # Add some variability
        return base_priority + random_factor
    
    def obstacle_avoidance_behavior(self):
        """Enhanced obstacle avoidance behavior with state persistence"""
        distance = self.px.get_distance()
        current_time = time.time()
        
        # Check if we're currently in an avoidance maneuver
        if self.avoidance_state['avoiding']:
            time_avoiding = current_time - self.avoidance_state['avoid_start_time']
            
            # Continue avoidance for minimum duration, or until clear
            if time_avoiding < self.avoidance_state['min_avoid_duration'] or (distance > 0 and distance < 60):
                # Continue current avoidance maneuver
                if distance > 0 and distance < 15:
                    return {'action': 'sharp_avoid', 'speed': 25, 'angle': self.avoidance_state['avoid_direction'], 'urgency': 'high'}
                else:
                    return {'action': 'avoid_turn', 'speed': 30, 'angle': self.avoidance_state['avoid_direction'], 'urgency': 'medium'}
            else:
                # Avoidance complete
                self.avoidance_state['avoiding'] = False
                print("🛡️ Obstacle cleared - resuming normal operation")
        
        # New obstacle detection
        if distance > 0 and distance < 50:  # Extended detection range
            if not self.avoidance_state['avoiding']:
                # Start new avoidance maneuver
                self.avoidance_state['avoiding'] = True
                self.avoidance_state['avoid_start_time'] = current_time
                # Choose smarter direction (could be enhanced with side sensors)
                self.avoidance_state['avoid_direction'] = random.choice([-70, 70])  # Aggressive turn
                print(f"🛡️ Obstacle detected at {distance:.1f}cm - avoiding {self.avoidance_state['avoid_direction']}°")
            
            if distance < 10:
                # Emergency - full reverse
                return {'action': 'emergency_reverse', 'speed': 50, 'angle': 0, 'urgency': 'critical'}
            elif distance < 20:
                # Very close - sharp turn with backing
                return {'action': 'sharp_avoid', 'speed': 25, 'angle': self.avoidance_state['avoid_direction'], 'urgency': 'high'}
            elif distance < 35:
                # Close - moderate avoidance turn
                return {'action': 'avoid_turn', 'speed': 30, 'angle': self.avoidance_state['avoid_direction'], 'urgency': 'medium'}
            else:
                # Detected but not immediate threat - gentle correction
                return {'action': 'gentle_avoid', 'speed': 35, 'angle': self.avoidance_state['avoid_direction'], 'urgency': 'low'}
        
        return None


def explain_behavior_coordination():
    """Explain behavior coordination concepts"""
    print("🧠 Behavior Coordination Concepts:")
    print()
    print("🏗️ Coordination Architectures:")
    print("   • Subsumption: Higher priority behaviors suppress lower ones")
    print("   • Fusion: Blend outputs from multiple behaviors")
    print("   • Arbitration: Select one behavior based on activation")
    print("   • Hybrid: Combine multiple coordination strategies")
    print()
    print("⚖️ Priority Systems:")
    print("   • Static priorities: Fixed behavior importance")
    print("   • Dynamic priorities: Priorities change with context")
    print("   • Activation levels: Behaviors compete for control")
    print()
    print("🔄 Behavior Types:")
    print("   • Reactive: Immediate response to stimuli")
    print("   • Goal-oriented: Working toward specific objectives")
    print("   • Maintenance: Background tasks and monitoring")
    print()


def obstacle_avoidance_behavior(px):
    """Simple obstacle avoidance behavior (stateless version)"""
    distance = px.get_distance()
    
    if distance > 0 and distance < 30:
        if distance < 15:
            # Very close - back away
            return {'action': 'backward', 'speed': 40, 'angle': 0, 'urgency': 'high'}
        else:
            # Close - turn away
            turn_direction = random.choice([-45, 45])  # Sharper turns
            return {'action': 'turn', 'speed': 35, 'angle': turn_direction, 'urgency': 'medium'}
    
    return None


def exploration_behavior(px):
    """Exploration behavior"""
    # Simple exploration - move forward with slight random turns
    random_angle = random.randint(-10, 10)
    return {'action': 'explore', 'speed': 30, 'angle': random_angle, 'urgency': 'low'}


def line_following_behavior(px):
    """Line following behavior"""
    gray_data = px.get_grayscale_data()
    left = gray_data[0]
    center = gray_data[1]
    right = gray_data[2]
    
    # Check if any sensor detects a line
    if any(sensor < 40 for sensor in [left, center, right]):
        if center < 40:
            # Line in center - go straight
            return {'action': 'follow_line', 'speed': 35, 'angle': 0, 'urgency': 'medium'}
        elif left < 40:
            # Line on left - turn left
            return {'action': 'follow_line', 'speed': 30, 'angle': -20, 'urgency': 'medium'}
        elif right < 40:
            # Line on right - turn right
            return {'action': 'follow_line', 'speed': 30, 'angle': 20, 'urgency': 'medium'}
    
    return None


def face_tracking_behavior(px):
    """Simplified face tracking behavior"""
    # This would normally use Vilib face detection
    # For demo purposes, return occasional tracking commands
    if random.random() < 0.1:  # 10% chance
        return {'action': 'track_face', 'speed': 0, 'angle': 0, 'urgency': 'high'}
    return None


def execute_behavior_output(px, output):
    """Execute the coordinated behavior output"""
    if not output:
        px.stop()
        return
    
    action = output.get('action', 'stop')
    speed = output.get('speed', 0)
    angle = output.get('angle', 0)
    urgency = output.get('urgency', 'unknown')
    
    # Enhanced obstacle avoidance actions
    if action == 'emergency_reverse':
        px.set_dir_servo_angle(0)
        px.backward(speed)
        print(f"🚨 EMERGENCY REVERSE at {speed} speed!")
    elif action == 'sharp_avoid':
        px.set_dir_servo_angle(angle)
        px.backward(20)  # Brief reverse while turning
        px.forward(speed)
        print(f"🛡️ Sharp avoidance: {angle}° at {speed} speed")
    elif action == 'avoid_turn':
        px.set_dir_servo_angle(angle)
        px.forward(speed)
        print(f"🛡️ Avoidance turn: {angle}° at {speed} speed")
    elif action == 'gentle_avoid':
        px.set_dir_servo_angle(angle)
        px.forward(speed)
        print(f"🛡️ Gentle avoid: {angle}° at {speed} speed")
    # Standard actions
    elif action == 'backward':
        px.set_dir_servo_angle(0)
        px.backward(speed)
    elif action == 'turn':
        px.set_dir_servo_angle(angle)
        px.forward(speed)
    elif action == 'explore':
        px.set_dir_servo_angle(angle)
        px.forward(speed)
    elif action == 'follow_line':
        px.set_dir_servo_angle(angle)
        px.forward(speed)
    elif action == 'track_face':
        px.stop()  # Would do camera tracking here
    else:
        px.stop()


def subsumption_architecture_demo():
    """Demonstrate subsumption architecture"""
    print("🏗️ Subsumption Architecture Demo")
    print("Higher priority behaviors suppress lower priority ones")
    print("Press Ctrl+C to stop")
    print()
    
    with Picarx() as px:
        coordinator = BehaviorCoordinator(px)
        coordinator.coordination_mode = 'subsumption'
        
        # Register behaviors with priorities (higher = more important)
        coordinator.register_behavior('obstacle_avoidance', 
                                     coordinator.obstacle_avoidance_behavior, priority=10)
        coordinator.register_behavior('line_following', 
                                     lambda: line_following_behavior(px), priority=5)
        coordinator.register_behavior('exploration', 
                                     lambda: exploration_behavior(px), priority=1)
        
        # Activate all behaviors
        coordinator.activate_behavior('obstacle_avoidance')
        coordinator.activate_behavior('line_following')
        coordinator.activate_behavior('exploration')
        
        print("🏗️ Subsumption architecture active!")
        print("Priorities: Obstacle avoidance (10) > Line following (5) > Exploration (1)")
        
        behavior_history = deque(maxlen=50)
        
        try:
            while True:
                result = coordinator.coordinate_behaviors()
                
                if result:
                    active_behavior, output = result
                    behavior_history.append(active_behavior)
                    execute_behavior_output(px, output)
                    
                    urgency = output.get('urgency', 'unknown') if output else 'unknown'
                    print(f"🏗️ Active: {active_behavior} ({urgency} urgency)")
                else:
                    px.stop()
                    print("🏗️ No active behaviors")
                
                time.sleep(0.1)
        
        except KeyboardInterrupt:
            px.stop()
            if behavior_history:
                # Analyze behavior activation patterns
                behavior_counts = {}
                for behavior in behavior_history:
                    behavior_counts[behavior] = behavior_counts.get(behavior, 0) + 1
                
                print(f"\n🏗️ Subsumption demo complete!")
                print("Behavior activation frequency:")
                for behavior, count in sorted(behavior_counts.items(), key=lambda x: x[1], reverse=True):
                    percentage = (count / len(behavior_history)) * 100
                    print(f"   {behavior}: {count} times ({percentage:.1f}%)")


def behavior_fusion_demo():
    """Demonstrate behavior fusion"""
    print("🔀 Behavior Fusion Demo")
    print("Multiple behaviors contribute to final action")
    print("Press Ctrl+C to stop")
    print()
    
    with Picarx() as px:
        coordinator = BehaviorCoordinator(px)
        coordinator.coordination_mode = 'fusion'
        
        # Register behaviors with weights for fusion
        coordinator.register_behavior('obstacle_avoidance', 
                                     coordinator.obstacle_avoidance_behavior, priority=3)
        coordinator.register_behavior('exploration', 
                                     lambda: exploration_behavior(px), priority=1)
        
        coordinator.activate_behavior('obstacle_avoidance')
        coordinator.activate_behavior('exploration')
        
        print("🔀 Behavior fusion active!")
        print("Behaviors are blended based on their priority weights")
        
        fusion_count = 0
        
        try:
            while True:
                result = coordinator.coordinate_behaviors()
                
                if result:
                    coordination_type, output = result
                    if coordination_type == "FUSION":
                        fusion_count += 1
                        print(f"🔀 Fusion #{fusion_count}: Blended behavior output")
                    
                    execute_behavior_output(px, output)
                else:
                    px.stop()
                    print("🔀 No behaviors to fuse")
                
                time.sleep(0.1)
        
        except KeyboardInterrupt:
            px.stop()
            print(f"\n🔀 Fusion demo complete! {fusion_count} fusion operations")


def behavior_arbitration_demo():
    """Demonstrate behavior arbitration"""
    print("⚖️ Behavior Arbitration Demo")
    print("Behaviors compete for control based on activation levels")
    print("Press Ctrl+C to stop")
    print()
    
    with Picarx() as px:
        coordinator = BehaviorCoordinator(px)
        coordinator.coordination_mode = 'arbitration'
        
        # Register behaviors
        coordinator.register_behavior('obstacle_avoidance', 
                                     coordinator.obstacle_avoidance_behavior, priority=8)
        coordinator.register_behavior('line_following', 
                                     lambda: line_following_behavior(px), priority=6)
        coordinator.register_behavior('exploration', 
                                     lambda: exploration_behavior(px), priority=3)
        
        coordinator.activate_behavior('obstacle_avoidance')
        coordinator.activate_behavior('line_following')
        coordinator.activate_behavior('exploration')
        
        print("⚖️ Behavior arbitration active!")
        print("Behaviors compete based on activation scores")
        
        arbitration_decisions = []
        
        try:
            while True:
                result = coordinator.coordinate_behaviors()
                
                if result:
                    winning_behavior, output = result
                    arbitration_decisions.append(winning_behavior)
                    execute_behavior_output(px, output)
                    
                    print(f"⚖️ Arbitration winner: {winning_behavior}")
                else:
                    px.stop()
                    print("⚖️ No behaviors competing")
                
                time.sleep(0.2)
        
        except KeyboardInterrupt:
            px.stop()
            print(f"\n⚖️ Arbitration demo complete!")
            if arbitration_decisions:
                behavior_wins = {}
                for behavior in arbitration_decisions:
                    behavior_wins[behavior] = behavior_wins.get(behavior, 0) + 1
                
                print("Arbitration winners:")
                for behavior, wins in sorted(behavior_wins.items(), key=lambda x: x[1], reverse=True):
                    percentage = (wins / len(arbitration_decisions)) * 100
                    print(f"   {behavior}: {wins} wins ({percentage:.1f}%)")


def dynamic_behavior_switching():
    """Demonstrate dynamic behavior switching"""
    print("🔄 Dynamic Behavior Switching")
    print("Behaviors are activated/deactivated based on conditions")
    print("Press Ctrl+C to stop")
    print()
    
    with Picarx() as px:
        coordinator = BehaviorCoordinator(px)
        coordinator.coordination_mode = 'subsumption'
        
        # Register all behaviors
        coordinator.register_behavior('obstacle_avoidance', 
                                     coordinator.obstacle_avoidance_behavior, priority=10)
        coordinator.register_behavior('line_following', 
                                     lambda: line_following_behavior(px), priority=5)
        coordinator.register_behavior('exploration', 
                                     lambda: exploration_behavior(px), priority=1)
        
        # Start with only exploration
        coordinator.activate_behavior('exploration')
        
        print("🔄 Dynamic switching active!")
        print("Behaviors activate/deactivate based on sensor conditions")
        
        switch_events = []
        last_switch_time = time.time()
        
        try:
            while True:
                current_time = time.time()
                
                # Dynamic behavior activation logic
                distance = px.get_distance()
                gray_data = px.get_grayscale_data()
                left = gray_data[0]
                center = gray_data[1]
                right = gray_data[2]
                
                # Obstacle avoidance activation
                if distance > 0 and distance < 40:
                    if 'obstacle_avoidance' not in coordinator.active_behaviors:
                        coordinator.activate_behavior('obstacle_avoidance')
                        switch_events.append(('activate', 'obstacle_avoidance', current_time))
                else:
                    if 'obstacle_avoidance' in coordinator.active_behaviors:
                        coordinator.deactivate_behavior('obstacle_avoidance')
                        switch_events.append(('deactivate', 'obstacle_avoidance', current_time))
                
                # Line following activation
                if any(sensor < 50 for sensor in [left, center, right]):
                    if 'line_following' not in coordinator.active_behaviors:
                        coordinator.activate_behavior('line_following')
                        switch_events.append(('activate', 'line_following', current_time))
                else:
                    if 'line_following' in coordinator.active_behaviors:
                        coordinator.deactivate_behavior('line_following')
                        switch_events.append(('deactivate', 'line_following', current_time))
                
                # Always keep exploration active as fallback
                if 'exploration' not in coordinator.active_behaviors:
                    coordinator.activate_behavior('exploration')
                    switch_events.append(('activate', 'exploration', current_time))
                
                # Execute coordination
                result = coordinator.coordinate_behaviors()
                if result:
                    active_behavior, output = result
                    execute_behavior_output(px, output)
                    
                    # Show status every 2 seconds
                    if current_time - last_switch_time > 2:
                        active_list = list(coordinator.active_behaviors)
                        print(f"🔄 Active behaviors: {', '.join(active_list)} | Running: {active_behavior}")
                        last_switch_time = current_time
                
                time.sleep(0.1)
        
        except KeyboardInterrupt:
            px.stop()
            print(f"\n🔄 Dynamic switching complete!")
            print(f"Total behavior switches: {len(switch_events)}")


def main():
    """Main function with behavior coordination options"""
    print("🧠 PiCar-X Behavior Coordination Tutorial")
    print("Learn advanced multi-behavior systems")
    print("=" * 50)
    
    explain_behavior_coordination()
    
    while True:
        print("\nChoose a coordination demonstration:")
        print("1. 🏗️ Subsumption architecture")
        print("2. 🔀 Behavior fusion")
        print("3. ⚖️ Behavior arbitration")
        print("4. 🔄 Dynamic behavior switching")
        print("5. ❓ Explain behavior coordination")
        print("6. 🚪 Exit")
        
        try:
            choice = input("\nEnter choice (1-6): ").strip()
            
            if choice == '1':
                subsumption_architecture_demo()
            elif choice == '2':
                behavior_fusion_demo()
            elif choice == '3':
                behavior_arbitration_demo()
            elif choice == '4':
                dynamic_behavior_switching()
            elif choice == '5':
                explain_behavior_coordination()
            elif choice == '6':
                print("👋 Happy coordinating!")
                break
            else:
                print("⚠️ Invalid choice. Please enter 1-6.")
                
        except KeyboardInterrupt:
            print("\n👋 Coordination tutorial interrupted!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Check robot connections and sensor calibration")
    
    print("\n🧠 Behavior coordination tutorial complete!")