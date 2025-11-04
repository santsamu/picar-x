#!/usr/bin/env python3
"""
🧩 Unit Testing - Component-Level Validation

This example demonstrates comprehensive unit testing for individual robot
components and functions, ensuring each piece works correctly in isolation.

Learn to:
- Unit test design patterns
- Mock objects and test doubles
- Automated test execution
- Test-driven development (TDD)
- Code coverage analysis
- Continuous testing practices
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from time import sleep, time
import threading
import json
from io import StringIO
import tempfile


def explain_unit_testing():
    """Explain unit testing concepts"""
    print("🧩 Unit Testing Concepts:")
    print()
    print("🎯 What is Unit Testing?")
    print("   • Testing individual components in isolation")
    print("   • Validating specific functions and methods")
    print("   • Using mock objects for dependencies")
    print("   • Automated and repeatable test execution")
    print()
    print("🔧 Unit Testing Benefits:")
    print("   • Early bug detection during development")
    print("   • Documentation of expected behavior")
    print("   • Safe refactoring with regression detection")
    print("   • Improved code design and modularity")
    print()
    print("📊 Testing Strategies:")
    print("   • Test-Driven Development (TDD)")
    print("   • Behavior-Driven Development (BDD)")
    print("   • Mock testing for external dependencies")
    print("   • Coverage analysis for completeness")
    print()


class MockRobotComponents:
    """Mock implementations of robot components for unit testing"""
    
    class MockPicarX:
        """Mock PiCar-X robot for testing"""
        
        def __init__(self):
            self.speed = 0
            self.direction = 0
            self.servo_angle = 0
            self.is_moving = False
            self.movement_history = []
            self.last_command = None
        
        def forward(self, speed):
            self.speed = speed
            self.direction = 1
            self.is_moving = True
            self.last_command = f"forward({speed})"
            self.movement_history.append(("forward", speed))
        
        def backward(self, speed):
            self.speed = speed
            self.direction = -1
            self.is_moving = True
            self.last_command = f"backward({speed})"
            self.movement_history.append(("backward", speed))
        
        def stop(self):
            self.speed = 0
            self.direction = 0
            self.is_moving = False
            self.last_command = "stop()"
            self.movement_history.append(("stop", 0))
        
        def set_dir_servo_angle(self, angle):
            self.servo_angle = angle
            self.last_command = f"set_dir_servo_angle({angle})"
            self.movement_history.append(("servo", angle))
        
        def get_status(self):
            return {
                "speed": self.speed,
                "direction": self.direction,
                "servo_angle": self.servo_angle,
                "is_moving": self.is_moving,
                "command_count": len(self.movement_history)
            }
    
    class MockTTS:
        """Mock Text-to-Speech for testing"""
        
        def __init__(self):
            self.messages = []
            self.is_speaking = False
        
        def say(self, message):
            self.messages.append(message)
            self.is_speaking = True
            # Simulate speaking time
            sleep(0.1)
            self.is_speaking = False
        
        def get_message_history(self):
            return self.messages.copy()
    
    class MockSensor:
        """Mock sensor for testing"""
        
        def __init__(self, sensor_type="ultrasonic"):
            self.sensor_type = sensor_type
            self.readings = []
            self.calibrated = False
            self.error_rate = 0.0
        
        def read(self):
            """Simulate sensor reading"""
            if not self.calibrated:
                raise RuntimeError("Sensor not calibrated")
            
            # Simulate reading with optional error
            if self.error_rate > 0 and len(self.readings) % int(1/self.error_rate) == 0:
                raise RuntimeError("Sensor read error")
            
            # Generate simulated reading
            if self.sensor_type == "ultrasonic":
                reading = 50 + len(self.readings) % 20  # 50-70cm range
            elif self.sensor_type == "line":
                reading = 0.7 + (len(self.readings) % 3) * 0.1  # 0.7-0.9 range
            else:
                reading = 42  # Default value
            
            self.readings.append(reading)
            return reading
        
        def calibrate(self):
            self.calibrated = True
        
        def set_error_rate(self, rate):
            self.error_rate = rate


class RobotControllerForTesting:
    """Robot controller class designed for testing"""
    
    def __init__(self, robot, tts=None, sensors=None):
        self.robot = robot
        self.tts = tts
        self.sensors = sensors or {}
        self.movement_queue = []
        self.safety_enabled = True
        self.max_speed = 100
        self.min_speed = 10
    
    def safe_move_forward(self, speed, duration=1.0):
        """Safe forward movement with validation"""
        if not self.safety_enabled:
            raise RuntimeError("Safety system disabled")
        
        if speed < self.min_speed or speed > self.max_speed:
            raise ValueError(f"Speed must be between {self.min_speed} and {self.max_speed}")
        
        self.robot.forward(speed)
        sleep(duration)
        self.robot.stop()
        
        return True
    
    def navigate_with_sensors(self, target_distance):
        """Navigate using sensor feedback"""
        if "ultrasonic" not in self.sensors:
            raise RuntimeError("Ultrasonic sensor required for navigation")
        
        sensor = self.sensors["ultrasonic"]
        current_distance = sensor.read()
        
        if current_distance > target_distance + 10:
            self.robot.forward(50)
            return "moving_forward"
        elif current_distance < target_distance - 10:
            self.robot.backward(50)
            return "moving_backward"
        else:
            self.robot.stop()
            return "target_reached"
    
    def announce_status(self, message):
        """Announce status via TTS"""
        if self.tts:
            self.tts.say(message)
            return True
        return False
    
    def emergency_stop(self):
        """Emergency stop all movement"""
        self.robot.stop()
        if self.tts:
            self.tts.say("Emergency stop activated")
        return True
    
    def complex_maneuver(self, pattern):
        """Execute complex movement pattern"""
        if pattern == "square":
            movements = [
                ("forward", 50, 1.0),
                ("turn_left", -30, 0.5),
                ("forward", 50, 1.0),
                ("turn_left", -30, 0.5),
                ("forward", 50, 1.0),
                ("turn_left", -30, 0.5),
                ("forward", 50, 1.0),
                ("turn_left", -30, 0.5)
            ]
        elif pattern == "circle":
            movements = [
                ("turn_and_move", 20, 2.0),
            ]
        else:
            raise ValueError(f"Unknown pattern: {pattern}")
        
        for movement, param, duration in movements:
            if movement == "forward":
                self.robot.forward(param)
                sleep(duration)
                self.robot.stop()
            elif movement == "turn_left":
                self.robot.set_dir_servo_angle(param)
                sleep(duration)
                self.robot.set_dir_servo_angle(0)
            elif movement == "turn_and_move":
                self.robot.set_dir_servo_angle(param)
                self.robot.forward(40)
                sleep(duration)
                self.robot.stop()
                self.robot.set_dir_servo_angle(0)
        
        return len(movements)


class TestRobotController(unittest.TestCase):
    """Unit tests for RobotController class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_robot = MockRobotComponents.MockPicarX()
        self.mock_tts = MockRobotComponents.MockTTS()
        self.mock_ultrasonic = MockRobotComponents.MockSensor("ultrasonic")
        self.mock_ultrasonic.calibrate()
        
        sensors = {"ultrasonic": self.mock_ultrasonic}
        self.controller = RobotControllerForTesting(
            self.mock_robot, 
            self.mock_tts, 
            sensors
        )
    
    def test_safe_move_forward_normal_speed(self):
        """Test safe forward movement with normal speed"""
        result = self.controller.safe_move_forward(50, 0.1)
        
        self.assertTrue(result)
        self.assertEqual(self.mock_robot.last_command, "stop()")
        self.assertIn(("forward", 50), self.mock_robot.movement_history)
        self.assertIn(("stop", 0), self.mock_robot.movement_history)
    
    def test_safe_move_forward_invalid_speed_low(self):
        """Test safe forward movement with speed too low"""
        with self.assertRaises(ValueError):
            self.controller.safe_move_forward(5)
    
    def test_safe_move_forward_invalid_speed_high(self):
        """Test safe forward movement with speed too high"""
        with self.assertRaises(ValueError):
            self.controller.safe_move_forward(150)
    
    def test_safe_move_forward_safety_disabled(self):
        """Test safe forward movement with safety disabled"""
        self.controller.safety_enabled = False
        
        with self.assertRaises(RuntimeError):
            self.controller.safe_move_forward(50)
    
    def test_navigate_with_sensors_move_forward(self):
        """Test navigation moving forward"""
        # Mock sensor to return distance > target + 10
        self.mock_ultrasonic.readings = [70]  # Pre-set reading
        
        result = self.controller.navigate_with_sensors(50)
        
        self.assertEqual(result, "moving_forward")
        self.assertEqual(self.mock_robot.direction, 1)
        self.assertEqual(self.mock_robot.speed, 50)
    
    def test_navigate_with_sensors_move_backward(self):
        """Test navigation moving backward"""
        # Mock sensor to return distance < target - 10
        self.mock_ultrasonic.readings = [30]  # Pre-set reading
        
        result = self.controller.navigate_with_sensors(50)
        
        self.assertEqual(result, "moving_backward")
        self.assertEqual(self.mock_robot.direction, -1)
        self.assertEqual(self.mock_robot.speed, 50)
    
    def test_navigate_with_sensors_target_reached(self):
        """Test navigation when target is reached"""
        # Mock sensor to return distance within target range
        self.mock_ultrasonic.readings = [52]  # Pre-set reading
        
        result = self.controller.navigate_with_sensors(50)
        
        self.assertEqual(result, "target_reached")
        self.assertFalse(self.mock_robot.is_moving)
    
    def test_navigate_without_sensor(self):
        """Test navigation without required sensor"""
        controller = RobotControllerForTesting(self.mock_robot, self.mock_tts, {})
        
        with self.assertRaises(RuntimeError):
            controller.navigate_with_sensors(50)
    
    def test_announce_status_with_tts(self):
        """Test status announcement with TTS available"""
        result = self.controller.announce_status("Test message")
        
        self.assertTrue(result)
        self.assertIn("Test message", self.mock_tts.messages)
    
    def test_announce_status_without_tts(self):
        """Test status announcement without TTS"""
        controller = RobotControllerForTesting(self.mock_robot)
        
        result = controller.announce_status("Test message")
        
        self.assertFalse(result)
    
    def test_emergency_stop(self):
        """Test emergency stop functionality"""
        # Start movement first
        self.mock_robot.forward(50)
        
        result = self.controller.emergency_stop()
        
        self.assertTrue(result)
        self.assertFalse(self.mock_robot.is_moving)
        self.assertIn("Emergency stop activated", self.mock_tts.messages)
    
    def test_complex_maneuver_square(self):
        """Test complex square maneuver"""
        result = self.controller.complex_maneuver("square")
        
        self.assertEqual(result, 8)  # 8 movements in square pattern
        
        # Check that forward and servo commands were executed
        forward_commands = [h for h in self.mock_robot.movement_history if h[0] == "forward"]
        servo_commands = [h for h in self.mock_robot.movement_history if h[0] == "servo"]
        
        self.assertEqual(len(forward_commands), 4)  # 4 forward movements
        self.assertTrue(len(servo_commands) >= 4)   # At least 4 servo commands
    
    def test_complex_maneuver_circle(self):
        """Test complex circle maneuver"""
        result = self.controller.complex_maneuver("circle")
        
        self.assertEqual(result, 1)  # 1 movement in circle pattern
    
    def test_complex_maneuver_invalid_pattern(self):
        """Test complex maneuver with invalid pattern"""
        with self.assertRaises(ValueError):
            self.controller.complex_maneuver("triangle")


class TestMockComponents(unittest.TestCase):
    """Unit tests for mock components themselves"""
    
    def test_mock_robot_forward(self):
        """Test mock robot forward movement"""
        robot = MockRobotComponents.MockPicarX()
        
        robot.forward(50)
        
        self.assertEqual(robot.speed, 50)
        self.assertEqual(robot.direction, 1)
        self.assertTrue(robot.is_moving)
        self.assertEqual(robot.last_command, "forward(50)")
    
    def test_mock_robot_movement_history(self):
        """Test mock robot movement history tracking"""
        robot = MockRobotComponents.MockPicarX()
        
        robot.forward(30)
        robot.stop()
        robot.backward(40)
        
        expected_history = [
            ("forward", 30),
            ("stop", 0),
            ("backward", 40)
        ]
        
        self.assertEqual(robot.movement_history, expected_history)
    
    def test_mock_tts_message_history(self):
        """Test mock TTS message history"""
        tts = MockRobotComponents.MockTTS()
        
        tts.say("Hello")
        tts.say("World")
        
        messages = tts.get_message_history()
        self.assertEqual(messages, ["Hello", "World"])
    
    def test_mock_sensor_calibration(self):
        """Test mock sensor calibration requirement"""
        sensor = MockRobotComponents.MockSensor()
        
        # Should fail before calibration
        with self.assertRaises(RuntimeError):
            sensor.read()
        
        # Should work after calibration
        sensor.calibrate()
        reading = sensor.read()
        self.assertIsInstance(reading, (int, float))
    
    def test_mock_sensor_error_simulation(self):
        """Test mock sensor error simulation"""
        sensor = MockRobotComponents.MockSensor()
        sensor.calibrate()
        sensor.set_error_rate(0.5)  # 50% error rate
        
        # Should get some errors with 50% rate
        errors = 0
        attempts = 10
        
        for _ in range(attempts):
            try:
                sensor.read()
            except RuntimeError:
                errors += 1
        
        # Should have some errors but not all
        self.assertGreater(errors, 0)
        self.assertLess(errors, attempts)


class TestAdvancedScenarios(unittest.TestCase):
    """Advanced unit testing scenarios"""
    
    def setUp(self):
        """Set up advanced test fixtures"""
        self.mock_robot = MockRobotComponents.MockPicarX()
        self.mock_tts = MockRobotComponents.MockTTS()
        
        # Create multiple sensors
        self.sensors = {
            "ultrasonic": MockRobotComponents.MockSensor("ultrasonic"),
            "line": MockRobotComponents.MockSensor("line")
        }
        
        for sensor in self.sensors.values():
            sensor.calibrate()
        
        self.controller = RobotControllerForTesting(
            self.mock_robot, 
            self.mock_tts, 
            self.sensors
        )
    
    def test_sensor_failure_handling(self):
        """Test handling of sensor failures"""
        # Simulate sensor failure
        self.sensors["ultrasonic"].set_error_rate(1.0)  # 100% failure rate
        
        with self.assertRaises(RuntimeError):
            self.controller.navigate_with_sensors(50)
    
    def test_multiple_navigation_calls(self):
        """Test multiple navigation calls"""
        # Set up sensor readings for multiple calls
        self.sensors["ultrasonic"].readings = [70, 60, 52]  # Moving closer
        
        results = []
        for i in range(3):
            result = self.controller.navigate_with_sensors(50)
            results.append(result)
        
        expected = ["moving_forward", "moving_forward", "target_reached"]
        self.assertEqual(results, expected)
    
    def test_concurrent_operations(self):
        """Test concurrent robot operations (thread safety)"""
        results = []
        
        def move_forward():
            results.append(self.controller.safe_move_forward(40, 0.1))
        
        def announce():
            results.append(self.controller.announce_status("Moving"))
        
        # Run operations concurrently
        threads = [
            threading.Thread(target=move_forward),
            threading.Thread(target=announce)
        ]
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Both operations should succeed
        self.assertEqual(results, [True, True])
    
    @patch('time.sleep')  # Mock sleep to speed up tests
    def test_performance_timing(self, mock_sleep):
        """Test performance timing with mocked sleep"""
        start_time = time()
        self.controller.safe_move_forward(50, 1.0)
        end_time = time()
        
        # Should complete quickly with mocked sleep
        self.assertLess(end_time - start_time, 0.1)
        
        # Verify sleep was called with correct duration
        mock_sleep.assert_called_with(1.0)


def run_unit_test_suite():
    """Run comprehensive unit test suite"""
    print("🧩 Running Unit Test Suite")
    print("=" * 50)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestRobotController,
        TestMockComponents,
        TestAdvancedScenarios
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests with detailed output
    stream = StringIO()
    runner = unittest.TextTestRunner(
        stream=stream, 
        verbosity=2,
        descriptions=True,
        failfast=False
    )
    
    print("🧪 Executing unit tests...")
    result = runner.run(test_suite)
    
    # Display results
    output = stream.getvalue()
    print(output)
    
    # Summary
    print(f"\n📊 Unit Test Summary:")
    print(f"   Tests run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    print(f"   Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\n❌ Test Failures:")
        for test, traceback in result.failures:
            print(f"   {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print(f"\n💥 Test Errors:")
        for test, traceback in result.errors:
            print(f"   {test}: {traceback.split(':', 1)[-1].strip()[:100]}")
    
    if result.wasSuccessful():
        print("\n✅ All unit tests passed!")
        return True
    else:
        print("\n⚠️ Some unit tests failed - review and fix issues")
        return False


def interactive_unit_testing():
    """Interactive unit testing mode"""
    print("🧩 Interactive Unit Testing")
    print("Test individual components interactively!")
    
    # Create mock components
    robot = MockRobotComponents.MockPicarX()
    tts = MockRobotComponents.MockTTS()
    sensor = MockRobotComponents.MockSensor("ultrasonic")
    sensor.calibrate()
    
    controller = RobotControllerForTesting(robot, tts, {"ultrasonic": sensor})
    
    while True:
        print("\n🧩 Interactive Testing Options:")
        print("1. Test safe movement")
        print("2. Test sensor navigation")
        print("3. Test emergency stop")
        print("4. Test complex maneuver")
        print("5. View component status")
        print("6. Exit")
        
        choice = input("\nSelect test (1-6): ").strip()
        
        try:
            if choice == '1':
                speed = int(input("Enter speed (10-100): "))
                result = controller.safe_move_forward(speed, 0.1)
                print(f"Result: {result}")
                print(f"Robot status: {robot.get_status()}")
                
            elif choice == '2':
                target = int(input("Enter target distance: "))
                result = controller.navigate_with_sensors(target)
                print(f"Navigation result: {result}")
                
            elif choice == '3':
                result = controller.emergency_stop()
                print(f"Emergency stop result: {result}")
                
            elif choice == '4':
                pattern = input("Enter pattern (square/circle): ")
                result = controller.complex_maneuver(pattern)
                print(f"Maneuver completed with {result} movements")
                
            elif choice == '5':
                print(f"Robot: {robot.get_status()}")
                print(f"TTS messages: {tts.get_message_history()}")
                print(f"Sensor readings: {sensor.readings}")
                
            elif choice == '6':
                print("🧩 Exiting interactive testing...")
                break
                
            else:
                print("⚠️ Invalid choice. Please select 1-6.")
        
        except Exception as e:
            print(f"❌ Test error: {e}")


def unit_testing_tutorial():
    """Tutorial on unit testing concepts"""
    print("📚 Unit Testing Tutorial")
    print("Learn effective unit testing practices!")
    
    tutorials = [
        {
            "title": "Test Structure (Arrange-Act-Assert)",
            "description": """
Unit tests follow the Arrange-Act-Assert pattern:

1. ARRANGE: Set up test data and conditions
   robot = MockRobot()
   controller = RobotController(robot)

2. ACT: Execute the function being tested
   result = controller.move_forward(50)

3. ASSERT: Verify the expected outcome
   self.assertTrue(result)
   self.assertEqual(robot.speed, 50)
            """
        },
        {
            "title": "Mock Objects",
            "description": """
Mock objects simulate real components:

• Isolate the code under test
• Control external dependencies
• Verify interactions occurred
• Simulate error conditions

Example:
   mock_sensor = Mock()
   mock_sensor.read.return_value = 42
   controller = RobotController(sensor=mock_sensor)
            """
        },
        {
            "title": "Test Cases to Include",
            "description": """
Comprehensive unit tests should cover:

• Happy path (normal operation)
• Edge cases (boundary values)
• Error conditions (invalid input)
• State verification (object state changes)
• Interaction verification (method calls)

Example test methods:
   test_normal_movement()
   test_invalid_speed_raises_error()
   test_emergency_stop_called()
            """
        },
        {
            "title": "Test-Driven Development (TDD)",
            "description": """
TDD process:

1. RED: Write a failing test first
2. GREEN: Write minimal code to pass
3. REFACTOR: Improve code while keeping tests green

Benefits:
• Better design through testability
• Higher code coverage
• Living documentation
• Regression protection
            """
        }
    ]
    
    for i, tutorial in enumerate(tutorials, 1):
        print(f"\n📖 Tutorial {i}: {tutorial['title']}")
        print("=" * 40)
        print(tutorial['description'])
        
        if i < len(tutorials):
            input("\nPress Enter to continue...")


def main():
    """Main function with unit testing options"""
    print("🧩 PiCar-X Unit Testing Suite")
    print("Component-level validation and testing!")
    print("=" * 50)
    
    explain_unit_testing()
    
    while True:
        print("\nChoose your unit testing approach:")
        print("1. 🧩 Run unit test suite")
        print("2. 🔧 Interactive unit testing")
        print("3. 📚 Unit testing tutorial")
        print("4. ❓ Explain unit testing")
        print("5. 🚪 Exit")
        
        try:
            choice = input("\nEnter choice (1-5): ").strip()
            
            if choice == '1':
                run_unit_test_suite()
            elif choice == '2':
                interactive_unit_testing()
            elif choice == '3':
                unit_testing_tutorial()
            elif choice == '4':
                explain_unit_testing()
            elif choice == '5':
                print("👋 Keep your code well-tested!")
                break
            else:
                print("⚠️ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Unit testing interrupted!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Unit testing helps ensure:")
        print("   - Individual components work correctly")
        print("   - Code quality and maintainability")
        print("   - Confidence in refactoring")
    
    print("\n🧩 Unit testing complete!")