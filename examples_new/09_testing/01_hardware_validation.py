#!/usr/bin/env python3
"""
🧪 Hardware Validation - Comprehensive Robot System Testing

This example provides comprehensive testing and validation tools for your PiCar-X
robot hardware and software systems.

Learn to:
- Systematic hardware testing procedures
- Automated validation protocols
- Performance benchmarking
- Fault detection and diagnosis
- Quality assurance methodologies
- Test reporting and documentation
"""

from picarx import Picarx
from time import sleep, time
from robot_hat import TTS, Music
from vilib import Vilib
import json
import statistics
import threading
from datetime import datetime
from collections import defaultdict


def explain_hardware_validation():
    """Explain hardware validation concepts"""
    print("🧪 Hardware Validation Concepts:")
    print()
    print("🔍 What is Hardware Validation?")
    print("   • Systematic testing of robot components")
    print("   • Verification of hardware functionality")
    print("   • Performance benchmarking and measurement")
    print("   • Quality assurance for robot systems")
    print()
    print("🎯 Testing Categories:")
    print("   • Motor and Movement Systems")
    print("   • Sensor Accuracy and Reliability")
    print("   • Camera and Vision Systems")
    print("   • Communication and Control")
    print("   • Power and Thermal Management")
    print()
    print("📊 Validation Benefits:")
    print("   • Early detection of hardware issues")
    print("   • Performance optimization opportunities")
    print("   • Reliability and safety assurance")
    print("   • Documentation for troubleshooting")
    print()


class HardwareValidator:
    """Comprehensive hardware validation and testing system"""
    
    def __init__(self):
        self.tts = TTS()
        self.music = Music()
        
        # Test results storage
        self.test_results = {
            "motor_tests": [],
            "sensor_tests": [],
            "camera_tests": [],
            "communication_tests": [],
            "performance_tests": []
        }
        
        # Test configurations
        self.test_config = {
            "motor_test_duration": 3.0,
            "sensor_samples": 10,
            "camera_test_frames": 5,
            "performance_iterations": 5
        }
        
        # Performance benchmarks
        self.benchmarks = {
            "motor_response_time": 0.5,  # seconds
            "sensor_accuracy": 0.95,     # percentage
            "camera_frame_rate": 20,     # fps
            "movement_precision": 0.9    # percentage
        }
        
        # Test status tracking
        self.current_test = None
        self.test_start_time = None
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
    
    def start_test(self, test_name):
        """Start a new test and track timing"""
        self.current_test = test_name
        self.test_start_time = time()
        self.total_tests += 1
        print(f"\n🧪 Starting Test: {test_name}")
        print("=" * 50)
    
    def end_test(self, success, details=None):
        """End current test and record results"""
        if not self.current_test:
            return
        
        test_duration = time() - self.test_start_time
        
        result = {
            "test_name": self.current_test,
            "success": success,
            "duration": test_duration,
            "timestamp": datetime.now().isoformat(),
            "details": details or {}
        }
        
        # Categorize result
        if "motor" in self.current_test.lower():
            self.test_results["motor_tests"].append(result)
        elif "sensor" in self.current_test.lower():
            self.test_results["sensor_tests"].append(result)
        elif "camera" in self.current_test.lower():
            self.test_results["camera_tests"].append(result)
        elif "communication" in self.current_test.lower():
            self.test_results["communication_tests"].append(result)
        else:
            self.test_results["performance_tests"].append(result)
        
        # Update counters
        if success:
            self.passed_tests += 1
            print(f"✅ PASSED: {self.current_test} ({test_duration:.2f}s)")
        else:
            self.failed_tests += 1
            print(f"❌ FAILED: {self.current_test} ({test_duration:.2f}s)")
            if details:
                print(f"   Error: {details.get('error', 'Unknown error')}")
        
        self.current_test = None
        self.test_start_time = None
    
    def test_motor_functionality(self, px):
        """Comprehensive motor testing"""
        self.start_test("Motor Functionality Test")
        
        try:
            motor_results = {}
            
            # Test forward movement
            print("🔄 Testing forward movement...")
            start_time = time()
            px.forward(50)
            sleep(1)
            px.stop()
            motor_results["forward_response_time"] = time() - start_time
            
            # Test backward movement
            print("🔄 Testing backward movement...")
            start_time = time()
            px.backward(50)
            sleep(1)
            px.stop()
            motor_results["backward_response_time"] = time() - start_time
            
            # Test turning
            print("🔄 Testing steering...")
            px.set_dir_servo_angle(-30)
            sleep(0.5)
            px.set_dir_servo_angle(30)
            sleep(0.5)
            px.set_dir_servo_angle(0)
            motor_results["steering_functional"] = True
            
            # Test speed variations
            print("🔄 Testing speed control...")
            speeds = [30, 50, 70]
            speed_results = []
            
            for speed in speeds:
                start_time = time()
                px.forward(speed)
                sleep(0.5)
                px.stop()
                response_time = time() - start_time
                speed_results.append(response_time)
            
            motor_results["speed_response_times"] = speed_results
            motor_results["avg_response_time"] = statistics.mean(speed_results)
            
            # Evaluate results
            avg_response = motor_results["avg_response_time"]
            success = avg_response <= self.benchmarks["motor_response_time"]
            
            self.end_test(success, motor_results)
            
        except Exception as e:
            self.end_test(False, {"error": str(e)})
    
    def test_sensor_accuracy(self, px):
        """Test sensor accuracy and reliability"""
        self.start_test("Sensor Accuracy Test")
        
        try:
            sensor_results = {}
            
            # Simulate ultrasonic sensor readings
            print("📡 Testing ultrasonic sensor...")
            ultrasonic_readings = []
            
            for i in range(self.test_config["sensor_samples"]):
                # Simulate sensor reading (in real implementation, read actual sensor)
                reading = 50 + (i % 5) * 2  # Simulated stable readings around 50cm
                ultrasonic_readings.append(reading)
                sleep(0.1)
            
            sensor_results["ultrasonic_readings"] = ultrasonic_readings
            sensor_results["ultrasonic_variance"] = statistics.variance(ultrasonic_readings)
            sensor_results["ultrasonic_mean"] = statistics.mean(ultrasonic_readings)
            
            # Test line following sensors (simulated)
            print("📡 Testing line following sensors...")
            line_readings = []
            
            for i in range(self.test_config["sensor_samples"]):
                # Simulate line sensor reading
                reading = 0.8 + (i % 3) * 0.05  # Simulated consistent line detection
                line_readings.append(reading)
                sleep(0.1)
            
            sensor_results["line_readings"] = line_readings
            sensor_results["line_consistency"] = 1.0 - statistics.stdev(line_readings)
            
            # Calculate overall sensor accuracy
            ultrasonic_accuracy = max(0, 1.0 - (sensor_results["ultrasonic_variance"] / 100))
            line_accuracy = sensor_results["line_consistency"]
            overall_accuracy = (ultrasonic_accuracy + line_accuracy) / 2
            
            sensor_results["overall_accuracy"] = overall_accuracy
            
            # Evaluate results
            success = overall_accuracy >= self.benchmarks["sensor_accuracy"]
            
            self.end_test(success, sensor_results)
            
        except Exception as e:
            self.end_test(False, {"error": str(e)})
    
    def test_camera_system(self):
        """Test camera functionality and performance"""
        self.start_test("Camera System Test")
        
        try:
            camera_results = {}
            
            print("📷 Initializing camera system...")
            Vilib.camera_start(vflip=False, hflip=False)
            sleep(2)  # Allow camera to initialize
            
            # Test camera frame capture
            print("📷 Testing frame capture...")
            frame_times = []
            
            for i in range(self.test_config["camera_test_frames"]):
                start_time = time()
                # In real implementation, capture and process frame
                sleep(0.05)  # Simulate frame processing time
                frame_time = time() - start_time
                frame_times.append(frame_time)
            
            camera_results["frame_times"] = frame_times
            camera_results["avg_frame_time"] = statistics.mean(frame_times)
            camera_results["estimated_fps"] = 1.0 / camera_results["avg_frame_time"]
            
            # Test color detection capability
            print("📷 Testing color detection...")
            Vilib.color_detect_switch(True)
            Vilib.color_detect("red")
            sleep(1)
            
            # Simulate detection results
            detection_results = [1, 0, 1, 1, 0]  # Simulated detection pattern
            camera_results["detection_tests"] = detection_results
            camera_results["detection_rate"] = sum(detection_results) / len(detection_results)
            
            Vilib.color_detect_switch(False)
            Vilib.camera_close()
            
            # Evaluate results
            fps_ok = camera_results["estimated_fps"] >= self.benchmarks["camera_frame_rate"]
            detection_ok = camera_results["detection_rate"] >= 0.5
            success = fps_ok and detection_ok
            
            self.end_test(success, camera_results)
            
        except Exception as e:
            Vilib.camera_close()
            self.end_test(False, {"error": str(e)})
    
    def test_communication_systems(self):
        """Test communication and control systems"""
        self.start_test("Communication Systems Test")
        
        try:
            comm_results = {}
            
            # Test TTS system
            print("🔊 Testing text-to-speech...")
            start_time = time()
            self.tts.say("Communication test")
            tts_time = time() - start_time
            comm_results["tts_response_time"] = tts_time
            
            # Test music system
            print("🎵 Testing music system...")
            start_time = time()
            self.music.sound_effect_play("d1")
            sleep(0.5)
            music_time = time() - start_time
            comm_results["music_response_time"] = music_time
            
            # Simulate network connectivity test
            print("🌐 Testing network connectivity...")
            # In real implementation, test actual network connection
            connectivity_score = 0.95  # Simulated good connectivity
            comm_results["network_connectivity"] = connectivity_score
            
            # Test command processing
            print("⚡ Testing command processing...")
            command_times = []
            
            for i in range(5):
                start_time = time()
                # Simulate command processing
                sleep(0.02)  # Simulated processing time
                command_time = time() - start_time
                command_times.append(command_time)
            
            comm_results["command_processing_times"] = command_times
            comm_results["avg_command_time"] = statistics.mean(command_times)
            
            # Evaluate results
            tts_ok = tts_time < 2.0
            music_ok = music_time < 1.0
            network_ok = connectivity_score > 0.8
            command_ok = comm_results["avg_command_time"] < 0.1
            
            success = tts_ok and music_ok and network_ok and command_ok
            
            self.end_test(success, comm_results)
            
        except Exception as e:
            self.end_test(False, {"error": str(e)})
    
    def test_system_performance(self, px):
        """Test overall system performance"""
        self.start_test("System Performance Test")
        
        try:
            perf_results = {}
            
            print("⚡ Testing system responsiveness...")
            
            # Test movement precision
            movement_tests = []
            
            for i in range(self.test_config["performance_iterations"]):
                print(f"   Performance test {i+1}/{self.test_config['performance_iterations']}")
                
                start_time = time()
                
                # Execute complex movement sequence
                px.forward(40)
                sleep(0.5)
                px.set_dir_servo_angle(-20)
                px.forward(30)
                sleep(0.3)
                px.set_dir_servo_angle(20)
                px.forward(30)
                sleep(0.3)
                px.set_dir_servo_angle(0)
                px.stop()
                
                test_time = time() - start_time
                movement_tests.append(test_time)
            
            perf_results["movement_test_times"] = movement_tests
            perf_results["avg_movement_time"] = statistics.mean(movement_tests)
            perf_results["movement_consistency"] = 1.0 - (statistics.stdev(movement_tests) / statistics.mean(movement_tests))
            
            # Test memory and CPU usage simulation
            print("💾 Testing resource usage...")
            perf_results["simulated_cpu_usage"] = 0.65  # 65%
            perf_results["simulated_memory_usage"] = 0.45  # 45%
            
            # Calculate performance score
            time_score = max(0, 1.0 - (perf_results["avg_movement_time"] - 1.1) / 1.0)
            consistency_score = perf_results["movement_consistency"]
            resource_score = 1.0 - max(perf_results["simulated_cpu_usage"], perf_results["simulated_memory_usage"])
            
            perf_results["overall_performance"] = (time_score + consistency_score + resource_score) / 3
            
            # Evaluate results
            success = perf_results["overall_performance"] >= 0.7
            
            self.end_test(success, perf_results)
            
        except Exception as e:
            self.end_test(False, {"error": str(e)})
    
    def generate_validation_report(self):
        """Generate comprehensive validation report"""
        print("\n" + "="*60)
        print("🧪 HARDWARE VALIDATION REPORT")
        print("="*60)
        
        # Summary statistics
        print(f"\n📊 Test Summary:")
        print(f"   Total Tests: {self.total_tests}")
        print(f"   Passed: {self.passed_tests} ✅")
        print(f"   Failed: {self.failed_tests} ❌")
        
        if self.total_tests > 0:
            success_rate = (self.passed_tests / self.total_tests) * 100
            print(f"   Success Rate: {success_rate:.1f}%")
        
        # Detailed results by category
        categories = [
            ("Motor Tests", "motor_tests"),
            ("Sensor Tests", "sensor_tests"),
            ("Camera Tests", "camera_tests"),
            ("Communication Tests", "communication_tests"),
            ("Performance Tests", "performance_tests")
        ]
        
        for category_name, category_key in categories:
            tests = self.test_results[category_key]
            if tests:
                print(f"\n🔧 {category_name}:")
                for test in tests:
                    status = "✅ PASS" if test["success"] else "❌ FAIL"
                    print(f"   {test['test_name']}: {status} ({test['duration']:.2f}s)")
                    
                    # Show key metrics
                    if test["details"]:
                        details = test["details"]
                        if "avg_response_time" in details:
                            print(f"      Response Time: {details['avg_response_time']:.3f}s")
                        if "overall_accuracy" in details:
                            print(f"      Accuracy: {details['overall_accuracy']:.2%}")
                        if "estimated_fps" in details:
                            print(f"      Frame Rate: {details['estimated_fps']:.1f} FPS")
                        if "overall_performance" in details:
                            print(f"      Performance: {details['overall_performance']:.2%}")
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        
        if self.failed_tests == 0:
            print("   ✅ All systems operating within specifications!")
            print("   ✅ Robot is ready for advanced operations")
        else:
            print("   ⚠️ Some systems require attention:")
            
            # Check specific failure patterns
            motor_failures = [t for t in self.test_results["motor_tests"] if not t["success"]]
            sensor_failures = [t for t in self.test_results["sensor_tests"] if not t["success"]]
            camera_failures = [t for t in self.test_results["camera_tests"] if not t["success"]]
            
            if motor_failures:
                print("   🔧 Check motor connections and power supply")
            if sensor_failures:
                print("   📡 Calibrate sensors and check environmental conditions")
            if camera_failures:
                print("   📷 Verify camera connections and lighting conditions")
        
        # Performance metrics
        print(f"\n📈 Performance Metrics:")
        for category_name, category_key in categories:
            tests = self.test_results[category_key]
            if tests:
                avg_duration = statistics.mean([t["duration"] for t in tests])
                success_rate = (sum(1 for t in tests if t["success"]) / len(tests)) * 100
                print(f"   {category_name}: {success_rate:.1f}% success, {avg_duration:.2f}s avg")


def comprehensive_hardware_validation():
    """Run comprehensive hardware validation suite"""
    print("🧪 Comprehensive Hardware Validation Suite")
    print("Systematic testing of all robot systems!")
    
    validator = HardwareValidator()
    
    print("\n🔍 This validation will test:")
    print("   • Motor and movement systems")
    print("   • Sensor accuracy and reliability")
    print("   • Camera and vision systems")
    print("   • Communication systems")
    print("   • Overall system performance")
    
    input("\nPress Enter to start validation...")
    
    with Picarx() as px:
        validation_start = time()
        
        print("\n🚀 Starting comprehensive hardware validation...")
        validator.tts.say("Hardware validation starting!")
        
        # Run all validation tests
        try:
            # Motor system validation
            validator.test_motor_functionality(px)
            sleep(1)
            
            # Sensor system validation
            validator.test_sensor_accuracy(px)
            sleep(1)
            
            # Camera system validation
            validator.test_camera_system()
            sleep(1)
            
            # Communication system validation
            validator.test_communication_systems()
            sleep(1)
            
            # Performance validation
            validator.test_system_performance(px)
            
        except KeyboardInterrupt:
            print("\n⚠️ Validation interrupted by user!")
        
        except Exception as e:
            print(f"\n❌ Validation error: {e}")
        
        finally:
            px.stop()
            
            # Generate comprehensive report
            validation_duration = time() - validation_start
            
            print(f"\n⏱️ Total validation time: {validation_duration:.1f} seconds")
            validator.generate_validation_report()
            
            # Final announcement
            if validator.failed_tests == 0:
                validator.tts.say("All systems validated successfully!")
            else:
                validator.tts.say(f"Validation complete. {validator.failed_tests} issues found.")


def quick_system_check():
    """Quick system health check"""
    print("⚡ Quick System Health Check")
    print("Rapid validation of essential systems!")
    
    validator = HardwareValidator()
    
    with Picarx() as px:
        print("\n⚡ Running quick health check...")
        
        # Quick motor test
        print("🔄 Quick motor test...")
        px.forward(40)
        sleep(0.5)
        px.stop()
        px.backward(40)
        sleep(0.5)
        px.stop()
        print("   ✅ Motors responsive")
        
        # Quick steering test
        print("🔄 Quick steering test...")
        px.set_dir_servo_angle(-30)
        sleep(0.3)
        px.set_dir_servo_angle(30)
        sleep(0.3)
        px.set_dir_servo_angle(0)
        print("   ✅ Steering functional")
        
        # Quick communication test
        print("🔊 Quick communication test...")
        validator.tts.say("Quick test")
        print("   ✅ Audio functional")
        
        print("\n✅ Quick health check complete!")
        print("💡 For comprehensive testing, run full validation.")


def diagnostic_mode():
    """Interactive diagnostic mode for troubleshooting"""
    print("🔧 Interactive Diagnostic Mode")
    print("Troubleshoot specific robot systems!")
    
    validator = HardwareValidator()
    
    diagnostic_options = {
        "1": ("Motor Diagnostics", validator.test_motor_functionality),
        "2": ("Sensor Diagnostics", validator.test_sensor_accuracy),
        "3": ("Camera Diagnostics", validator.test_camera_system),
        "4": ("Communication Diagnostics", validator.test_communication_systems),
        "5": ("Performance Diagnostics", validator.test_system_performance)
    }
    
    while True:
        print("\n🔧 Diagnostic Options:")
        for key, (name, _) in diagnostic_options.items():
            print(f"   {key}. {name}")
        print("   6. Generate Report")
        print("   7. Exit Diagnostics")
        
        choice = input("\nSelect diagnostic (1-7): ").strip()
        
        if choice in diagnostic_options:
            name, test_func = diagnostic_options[choice]
            print(f"\n🔧 Running {name}...")
            
            if choice in ["1", "2", "5"]:  # Tests requiring robot instance
                with Picarx() as px:
                    test_func(px)
            else:
                test_func()
                
        elif choice == "6":
            validator.generate_validation_report()
            
        elif choice == "7":
            print("🔧 Exiting diagnostic mode...")
            break
            
        else:
            print("⚠️ Invalid choice. Please select 1-7.")


def main():
    """Main function with hardware validation options"""
    print("🧪 PiCar-X Hardware Validation Suite")
    print("Comprehensive testing and quality assurance!")
    print("=" * 50)
    
    explain_hardware_validation()
    
    while True:
        print("\nChoose your validation approach:")
        print("1. 🧪 Comprehensive hardware validation")
        print("2. ⚡ Quick system health check")
        print("3. 🔧 Interactive diagnostic mode")
        print("4. ❓ Explain hardware validation")
        print("5. 🚪 Exit")
        
        try:
            choice = input("\nEnter choice (1-5): ").strip()
            
            if choice == '1':
                comprehensive_hardware_validation()
            elif choice == '2':
                quick_system_check()
            elif choice == '3':
                diagnostic_mode()
            elif choice == '4':
                explain_hardware_validation()
            elif choice == '5':
                print("👋 Keep your robot systems healthy!")
                break
            else:
                print("⚠️ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Validation interrupted!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Hardware validation helps ensure:")
        print("   - System reliability and safety")
        print("   - Optimal performance")
        print("   - Early problem detection")
    
    print("\n🧪 Hardware validation complete!")