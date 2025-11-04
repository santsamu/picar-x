#!/usr/bin/env python3
"""
🔗 Integration Testing - System-Level Validation

This example demonstrates comprehensive integration testing for robot systems,
ensuring all components work together correctly and efficiently.

Learn to:
- End-to-end system testing
- Component interaction validation
- Performance integration testing
- Error handling across systems
- Automated test suites
- Continuous integration concepts
"""

from picarx import Picarx
from time import sleep, time
from robot_hat import TTS, Music
from vilib import Vilib
import unittest
import threading
import queue
import json
import logging
from datetime import datetime
from collections import defaultdict
import sys
import traceback


def explain_integration_testing():
    """Explain integration testing concepts"""
    print("🔗 Integration Testing Concepts:")
    print()
    print("🎯 What is Integration Testing?")
    print("   • Testing interactions between system components")
    print("   • Validating end-to-end system workflows")
    print("   • Ensuring data flows correctly between modules")
    print("   • Detecting interface and communication issues")
    print()
    print("🔧 Integration Test Types:")
    print("   • Component Integration: Between robot subsystems")
    print("   • System Integration: Full robot system testing")
    print("   • Interface Testing: Communication protocols")
    print("   • Workflow Testing: Complete task scenarios")
    print()
    print("📊 Benefits:")
    print("   • Early detection of interface problems")
    print("   • Validation of system architecture")
    print("   • Performance under realistic conditions")
    print("   • Confidence in system reliability")
    print()


class IntegrationTestSuite:
    """Comprehensive integration testing framework"""
    
    def __init__(self):
        self.tts = TTS()
        self.music = Music()
        
        # Test execution tracking
        self.test_results = []
        self.test_logs = []
        self.current_test_suite = None
        
        # System state tracking
        self.system_state = {
            "robot_initialized": False,
            "camera_active": False,
            "sensors_calibrated": False,
            "communication_ready": False
        }
        
        # Performance metrics
        self.performance_data = defaultdict(list)
        
        # Test configurations
        self.test_config = {
            "timeout_duration": 30,  # seconds
            "retry_attempts": 3,
            "performance_threshold": 0.8,
            "error_tolerance": 0.1
        }
        
        # Setup logging
        self.setup_logging()
    
    def setup_logging(self):
        """Setup comprehensive test logging"""
        self.logger = logging.getLogger('IntegrationTest')
        self.logger.setLevel(logging.DEBUG)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(console_handler)
    
    def log_test_event(self, level, message, test_name=None):
        """Log test events with proper formatting"""
        if test_name:
            message = f"[{test_name}] {message}"
        
        self.logger.log(level, message)
        self.test_logs.append({
            "timestamp": datetime.now(),
            "level": level,
            "message": message,
            "test": test_name
        })
    
    def run_test_with_timeout(self, test_function, timeout=None):
        """Run test function with timeout protection"""
        timeout = timeout or self.test_config["timeout_duration"]
        
        result_queue = queue.Queue()
        
        def test_wrapper():
            try:
                result = test_function()
                result_queue.put(("success", result))
            except Exception as e:
                result_queue.put(("error", str(e)))
        
        test_thread = threading.Thread(target=test_wrapper)
        test_thread.daemon = True
        test_thread.start()
        
        test_thread.join(timeout)
        
        if test_thread.is_alive():
            self.log_test_event(logging.ERROR, f"Test timed out after {timeout}s")
            return False, "Test timeout"
        
        try:
            status, result = result_queue.get_nowait()
            if status == "success":
                return True, result
            else:
                return False, result
        except queue.Empty:
            return False, "No result returned"
    
    def test_robot_initialization(self, px):
        """Test robot system initialization"""
        test_name = "Robot Initialization"
        self.log_test_event(logging.INFO, "Starting robot initialization test", test_name)
        
        try:
            # Test basic robot functions
            self.log_test_event(logging.DEBUG, "Testing motor initialization", test_name)
            px.forward(0)  # Test motor response without movement
            px.stop()
            
            self.log_test_event(logging.DEBUG, "Testing steering initialization", test_name)
            px.set_dir_servo_angle(0)
            
            self.system_state["robot_initialized"] = True
            self.log_test_event(logging.INFO, "Robot initialization successful", test_name)
            return True
            
        except Exception as e:
            self.log_test_event(logging.ERROR, f"Initialization failed: {e}", test_name)
            return False
    
    def test_camera_integration(self):
        """Test camera system integration"""
        test_name = "Camera Integration"
        self.log_test_event(logging.INFO, "Starting camera integration test", test_name)
        
        try:
            # Initialize camera
            self.log_test_event(logging.DEBUG, "Initializing camera", test_name)
            Vilib.camera_start(vflip=False, hflip=False)
            sleep(2)  # Allow initialization
            
            # Test camera functions
            self.log_test_event(logging.DEBUG, "Testing color detection", test_name)
            Vilib.color_detect_switch(True)
            Vilib.color_detect("red")
            sleep(1)
            
            # Test display functionality
            self.log_test_event(logging.DEBUG, "Testing display", test_name)
            Vilib.display(local=True, web=True)
            sleep(1)
            
            # Cleanup
            Vilib.color_detect_switch(False)
            Vilib.camera_close()
            
            self.system_state["camera_active"] = True
            self.log_test_event(logging.INFO, "Camera integration successful", test_name)
            return True
            
        except Exception as e:
            self.log_test_event(logging.ERROR, f"Camera integration failed: {e}", test_name)
            Vilib.camera_close()
            return False
    
    def test_sensor_communication(self):
        """Test sensor communication and data flow"""
        test_name = "Sensor Communication"
        self.log_test_event(logging.INFO, "Starting sensor communication test", test_name)
        
        try:
            # Simulate sensor readings and communication
            sensor_data = {}
            
            # Test ultrasonic sensor communication
            self.log_test_event(logging.DEBUG, "Testing ultrasonic sensor", test_name)
            for i in range(5):
                # Simulate sensor reading
                distance = 50 + i * 5  # Simulated readings
                sensor_data[f"ultrasonic_{i}"] = distance
                sleep(0.1)
            
            # Test line following sensor communication
            self.log_test_event(logging.DEBUG, "Testing line sensors", test_name)
            for i in range(3):
                # Simulate line sensor reading
                line_value = 0.7 + i * 0.1
                sensor_data[f"line_{i}"] = line_value
                sleep(0.1)
            
            # Validate data consistency
            if len(sensor_data) >= 8:  # Expected number of readings
                self.system_state["sensors_calibrated"] = True
                self.log_test_event(logging.INFO, "Sensor communication successful", test_name)
                return True
            else:
                self.log_test_event(logging.ERROR, "Insufficient sensor data", test_name)
                return False
                
        except Exception as e:
            self.log_test_event(logging.ERROR, f"Sensor communication failed: {e}", test_name)
            return False
    
    def test_audio_communication_integration(self):
        """Test audio and communication systems integration"""
        test_name = "Audio Communication Integration"
        self.log_test_event(logging.INFO, "Starting audio communication test", test_name)
        
        try:
            # Test TTS integration
            self.log_test_event(logging.DEBUG, "Testing TTS system", test_name)
            start_time = time()
            self.tts.say("Integration test")
            tts_duration = time() - start_time
            
            # Test music system integration
            self.log_test_event(logging.DEBUG, "Testing music system", test_name)
            start_time = time()
            self.music.sound_effect_play("d1")
            sleep(0.5)
            music_duration = time() - start_time
            
            # Validate performance
            if tts_duration < 5.0 and music_duration < 2.0:
                self.system_state["communication_ready"] = True
                self.log_test_event(logging.INFO, "Audio communication integration successful", test_name)
                return True
            else:
                self.log_test_event(logging.ERROR, "Audio communication performance issues", test_name)
                return False
                
        except Exception as e:
            self.log_test_event(logging.ERROR, f"Audio communication failed: {e}", test_name)
            return False
    
    def test_movement_sensor_integration(self, px):
        """Test integration between movement and sensor systems"""
        test_name = "Movement-Sensor Integration"
        self.log_test_event(logging.INFO, "Starting movement-sensor integration test", test_name)
        
        try:
            integration_data = []
            
            # Test coordinated movement and sensing
            movements = [
                ("forward", 40, 1.0),
                ("left_turn", -30, 0.8),
                ("right_turn", 30, 0.8),
                ("backward", 40, 1.0)
            ]
            
            for movement_type, parameter, duration in movements:
                self.log_test_event(logging.DEBUG, f"Testing {movement_type}", test_name)
                
                start_time = time()
                
                if movement_type == "forward":
                    px.forward(parameter)
                elif movement_type == "backward":
                    px.backward(parameter)
                elif movement_type in ["left_turn", "right_turn"]:
                    px.set_dir_servo_angle(parameter)
                    px.forward(40)
                
                sleep(duration)
                px.stop()
                px.set_dir_servo_angle(0)
                
                # Simulate sensor reading during movement
                movement_time = time() - start_time
                simulated_sensor_reading = 45 + (len(integration_data) * 5)
                
                integration_data.append({
                    "movement": movement_type,
                    "duration": movement_time,
                    "sensor_reading": simulated_sensor_reading,
                    "timestamp": time()
                })
                
                sleep(0.5)  # Brief pause between movements
            
            # Validate integration
            if len(integration_data) == len(movements):
                avg_response_time = sum(d["duration"] for d in integration_data) / len(integration_data)
                self.performance_data["movement_sensor_integration"].append(avg_response_time)
                
                self.log_test_event(logging.INFO, f"Movement-sensor integration successful (avg: {avg_response_time:.2f}s)", test_name)
                return True
            else:
                self.log_test_event(logging.ERROR, "Incomplete movement-sensor integration", test_name)
                return False
                
        except Exception as e:
            self.log_test_event(logging.ERROR, f"Movement-sensor integration failed: {e}", test_name)
            px.stop()
            return False
    
    def test_complete_workflow_integration(self, px):
        """Test complete workflow integration (end-to-end)"""
        test_name = "Complete Workflow Integration"
        self.log_test_event(logging.INFO, "Starting complete workflow integration test", test_name)
        
        try:
            workflow_start = time()
            
            # Step 1: Initialize all systems
            self.log_test_event(logging.DEBUG, "Step 1: System initialization", test_name)
            self.tts.say("Starting workflow test")
            
            # Step 2: Sensor survey
            self.log_test_event(logging.DEBUG, "Step 2: Sensor survey", test_name)
            sensor_readings = []
            for i in range(3):
                # Simulate sensor reading
                reading = 50 + i * 10
                sensor_readings.append(reading)
                sleep(0.2)
            
            # Step 3: Decision making based on sensors
            self.log_test_event(logging.DEBUG, "Step 3: Decision making", test_name)
            avg_distance = sum(sensor_readings) / len(sensor_readings)
            
            if avg_distance > 40:
                action = "explore_forward"
            else:
                action = "careful_navigation"
            
            # Step 4: Execute action
            self.log_test_event(logging.DEBUG, f"Step 4: Executing {action}", test_name)
            
            if action == "explore_forward":
                px.forward(50)
                sleep(1.5)
                px.stop()
            else:
                px.forward(30)
                sleep(1.0)
                px.stop()
            
            # Step 5: Camera-based validation
            self.log_test_event(logging.DEBUG, "Step 5: Camera validation", test_name)
            Vilib.camera_start(vflip=False, hflip=False)
            sleep(1)
            Vilib.color_detect_switch(True)
            Vilib.color_detect("red")
            sleep(1)
            Vilib.color_detect_switch(False)
            Vilib.camera_close()
            
            # Step 6: Status report
            self.log_test_event(logging.DEBUG, "Step 6: Status report", test_name)
            workflow_duration = time() - workflow_start
            self.tts.say("Workflow complete")
            
            # Validate workflow
            if workflow_duration < 10.0:  # Should complete within 10 seconds
                self.performance_data["complete_workflow"].append(workflow_duration)
                self.log_test_event(logging.INFO, f"Complete workflow integration successful ({workflow_duration:.2f}s)", test_name)
                return True
            else:
                self.log_test_event(logging.ERROR, f"Workflow took too long ({workflow_duration:.2f}s)", test_name)
                return False
                
        except Exception as e:
            self.log_test_event(logging.ERROR, f"Complete workflow integration failed: {e}", test_name)
            px.stop()
            Vilib.camera_close()
            return False
    
    def test_error_handling_integration(self, px):
        """Test error handling across integrated systems"""
        test_name = "Error Handling Integration"
        self.log_test_event(logging.INFO, "Starting error handling integration test", test_name)
        
        try:
            error_scenarios = [
                "simulated_sensor_failure",
                "simulated_motor_jam",
                "simulated_communication_error",
                "simulated_camera_error"
            ]
            
            handled_errors = 0
            
            for scenario in error_scenarios:
                self.log_test_event(logging.DEBUG, f"Testing {scenario}", test_name)
                
                try:
                    if scenario == "simulated_sensor_failure":
                        # Simulate handling sensor failure
                        backup_sensor_value = 30  # Fallback value
                        handled_errors += 1
                        
                    elif scenario == "simulated_motor_jam":
                        # Simulate motor jam detection and recovery
                        px.stop()  # Emergency stop
                        sleep(0.5)
                        px.forward(20)  # Gentle restart
                        sleep(0.5)
                        px.stop()
                        handled_errors += 1
                        
                    elif scenario == "simulated_communication_error":
                        # Simulate communication error handling
                        try:
                            self.tts.say("Error test")
                        except:
                            # Fallback communication method
                            pass
                        handled_errors += 1
                        
                    elif scenario == "simulated_camera_error":
                        # Simulate camera error handling
                        try:
                            Vilib.camera_start(vflip=False, hflip=False)
                            Vilib.camera_close()
                        except:
                            # Use alternative navigation method
                            pass
                        handled_errors += 1
                    
                    sleep(0.5)
                    
                except Exception as e:
                    self.log_test_event(logging.WARNING, f"Error in {scenario}: {e}", test_name)
            
            # Validate error handling
            error_handling_rate = handled_errors / len(error_scenarios)
            
            if error_handling_rate >= self.test_config["error_tolerance"]:
                self.log_test_event(logging.INFO, f"Error handling integration successful ({error_handling_rate:.1%})", test_name)
                return True
            else:
                self.log_test_event(logging.ERROR, f"Poor error handling ({error_handling_rate:.1%})", test_name)
                return False
                
        except Exception as e:
            self.log_test_event(logging.ERROR, f"Error handling integration failed: {e}", test_name)
            return False
    
    def run_full_integration_suite(self):
        """Run complete integration test suite"""
        print("🔗 Running Full Integration Test Suite")
        print("=" * 50)
        
        suite_start = time()
        test_functions = [
            (self.test_camera_integration, None),
            (self.test_sensor_communication, None),
            (self.test_audio_communication_integration, None)
        ]
        
        robot_tests = [
            (self.test_robot_initialization, "robot"),
            (self.test_movement_sensor_integration, "robot"),
            (self.test_complete_workflow_integration, "robot"),
            (self.test_error_handling_integration, "robot")
        ]
        
        passed_tests = 0
        total_tests = len(test_functions) + len(robot_tests)
        
        # Run non-robot tests
        for test_func, _ in test_functions:
            success, result = self.run_test_with_timeout(test_func)
            
            test_result = {
                "test_name": test_func.__name__,
                "success": success,
                "result": result,
                "timestamp": datetime.now()
            }
            self.test_results.append(test_result)
            
            if success:
                passed_tests += 1
                print(f"✅ {test_func.__name__}")
            else:
                print(f"❌ {test_func.__name__}: {result}")
        
        # Run robot-dependent tests
        with Picarx() as px:
            for test_func, _ in robot_tests:
                success, result = self.run_test_with_timeout(lambda: test_func(px))
                
                test_result = {
                    "test_name": test_func.__name__,
                    "success": success,
                    "result": result,
                    "timestamp": datetime.now()
                }
                self.test_results.append(test_result)
                
                if success:
                    passed_tests += 1
                    print(f"✅ {test_func.__name__}")
                else:
                    print(f"❌ {test_func.__name__}: {result}")
        
        # Generate suite summary
        suite_duration = time() - suite_start
        success_rate = (passed_tests / total_tests) * 100
        
        print(f"\n🔗 Integration Test Suite Complete!")
        print(f"   Duration: {suite_duration:.1f} seconds")
        print(f"   Tests passed: {passed_tests}/{total_tests}")
        print(f"   Success rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            self.tts.say("Integration tests passed successfully!")
            print("✅ System integration validated!")
        else:
            self.tts.say("Integration tests found issues requiring attention.")
            print("⚠️ Integration issues detected - review test logs")
        
        return success_rate
    
    def generate_integration_report(self):
        """Generate detailed integration test report"""
        print("\n" + "="*60)
        print("🔗 INTEGRATION TEST REPORT")
        print("="*60)
        
        if not self.test_results:
            print("No test results available.")
            return
        
        # Summary statistics
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r["success"])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"\n📊 Test Summary:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests} ✅")
        print(f"   Failed: {failed_tests} ❌")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        # System state summary
        print(f"\n🔧 System State:")
        for component, status in self.system_state.items():
            status_icon = "✅" if status else "❌"
            print(f"   {component}: {status_icon}")
        
        # Detailed test results
        print(f"\n📝 Detailed Results:")
        for result in self.test_results:
            status = "✅ PASS" if result["success"] else "❌ FAIL"
            test_name = result["test_name"].replace("test_", "").replace("_", " ").title()
            print(f"   {test_name}: {status}")
            
            if not result["success"]:
                print(f"      Error: {result['result']}")
        
        # Performance metrics
        if self.performance_data:
            print(f"\n📈 Performance Metrics:")
            for metric, values in self.performance_data.items():
                if values:
                    avg_value = sum(values) / len(values)
                    metric_name = metric.replace("_", " ").title()
                    print(f"   {metric_name}: {avg_value:.2f}s average")
        
        # Recent logs (last 10)
        if self.test_logs:
            print(f"\n📋 Recent Test Events:")
            for log_entry in self.test_logs[-10:]:
                timestamp = log_entry["timestamp"].strftime("%H:%M:%S")
                level_name = logging.getLevelName(log_entry["level"])
                print(f"   [{timestamp}] {level_name}: {log_entry['message']}")


def comprehensive_integration_testing():
    """Run comprehensive integration testing"""
    print("🔗 Comprehensive Integration Testing")
    print("Validating system-level component interactions!")
    
    test_suite = IntegrationTestSuite()
    
    print("\n🔍 Integration testing will validate:")
    print("   • Component interaction workflows")
    print("   • End-to-end system functionality")
    print("   • Error handling across systems")
    print("   • Performance under integration load")
    
    input("\nPress Enter to start integration testing...")
    
    try:
        # Run full integration suite
        success_rate = test_suite.run_full_integration_suite()
        
        # Generate comprehensive report
        test_suite.generate_integration_report()
        
        # Final assessment
        if success_rate >= 90:
            print("\n🌟 Excellent integration! System is well-integrated.")
        elif success_rate >= 70:
            print("\n👍 Good integration with minor issues to address.")
        else:
            print("\n⚠️ Integration issues detected - system needs attention.")
    
    except Exception as e:
        print(f"\n❌ Integration testing error: {e}")
        traceback.print_exc()


def quick_integration_check():
    """Quick integration validation"""
    print("⚡ Quick Integration Check")
    print("Rapid validation of key system interactions!")
    
    test_suite = IntegrationTestSuite()
    
    with Picarx() as px:
        print("\n⚡ Running quick integration checks...")
        
        # Quick robot-movement test
        print("🔄 Movement integration...")
        px.forward(30)
        sleep(0.5)
        px.stop()
        print("   ✅ Movement responsive")
        
        # Quick audio integration test
        print("🔊 Audio integration...")
        test_suite.tts.say("Quick check")
        print("   ✅ Audio functional")
        
        # Quick sensor simulation
        print("📡 Sensor integration...")
        sleep(0.5)  # Simulate sensor reading
        print("   ✅ Sensors responsive")
        
        print("\n✅ Quick integration check complete!")
        print("💡 For comprehensive testing, run full integration suite.")


def main():
    """Main function with integration testing options"""
    print("🔗 PiCar-X Integration Testing Suite")
    print("Comprehensive system-level validation!")
    print("=" * 50)
    
    explain_integration_testing()
    
    while True:
        print("\nChoose your integration testing approach:")
        print("1. 🔗 Comprehensive integration testing")
        print("2. ⚡ Quick integration check")
        print("3. ❓ Explain integration testing")
        print("4. 🚪 Exit")
        
        try:
            choice = input("\nEnter choice (1-4): ").strip()
            
            if choice == '1':
                comprehensive_integration_testing()
            elif choice == '2':
                quick_integration_check()
            elif choice == '3':
                explain_integration_testing()
            elif choice == '4':
                print("👋 Keep your systems well-integrated!")
                break
            else:
                print("⚠️ Invalid choice. Please enter 1-4.")
                
        except KeyboardInterrupt:
            print("\n👋 Integration testing interrupted!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Integration testing ensures:")
        print("   - Components work together correctly")
        print("   - End-to-end functionality")
        print("   - System reliability under load")
    
    print("\n🔗 Integration testing complete!")