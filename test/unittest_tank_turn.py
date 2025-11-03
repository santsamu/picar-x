#!/usr/bin/env python3
"""
Unit tests for PiCar-X tank_turn function
Uses Python unittest framework for automated testing
"""

import unittest
import time
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path to import picarx
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from picarx import Picarx

class TestTankTurn(unittest.TestCase):
    """Unit tests for tank_turn functionality"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        # Mock the hardware dependencies to allow testing without actual hardware
        with patch('picarx.picarx.utils.reset_mcu'), \
             patch('picarx.picarx.fileDB'), \
             patch('picarx.picarx.Servo'), \
             patch('picarx.picarx.Pin'), \
             patch('picarx.picarx.PWM'), \
             patch('picarx.picarx.ADC'), \
             patch('picarx.picarx.Grayscale_Module'), \
             patch('picarx.picarx.Ultrasonic'):
            
            self.picar = Picarx()
            
            # Mock the motor control methods
            self.picar.set_motor_speed = Mock()
    
    def test_tank_turn_left_string(self):
        """Test tank turn left with string parameter"""
        self.picar.tank_turn('left', 50)
        
        # Verify that motors are called with correct parameters
        # Left motor should go backward (-50), right motor forward (+50)
        calls = self.picar.set_motor_speed.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0][0], (1, -50))  # Left motor backward
        self.assertEqual(calls[1][0], (2, 50))   # Right motor forward
    
    def test_tank_turn_right_string(self):
        """Test tank turn right with string parameter"""
        self.picar.tank_turn('right', 60)
        
        # Verify that motors are called with correct parameters
        # Left motor should go forward (+60), right motor backward (-60)
        calls = self.picar.set_motor_speed.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0][0], (1, 60))   # Left motor forward
        self.assertEqual(calls[1][0], (2, -60))  # Right motor backward
    
    def test_tank_turn_left_numeric(self):
        """Test tank turn left with numeric parameter (-1)"""
        self.picar.tank_turn(-1, 40)
        
        calls = self.picar.set_motor_speed.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0][0], (1, -40))  # Left motor backward
        self.assertEqual(calls[1][0], (2, 40))   # Right motor forward
    
    def test_tank_turn_right_numeric(self):
        """Test tank turn right with numeric parameter (1)"""
        self.picar.tank_turn(1, 70)
        
        calls = self.picar.set_motor_speed.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0][0], (1, 70))   # Left motor forward
        self.assertEqual(calls[1][0], (2, -70))  # Right motor backward
    
    def test_speed_constraint_high(self):
        """Test that speed is constrained to maximum value"""
        self.picar.tank_turn('left', 150)  # Over 100
        
        calls = self.picar.set_motor_speed.call_args_list
        # Speed should be constrained to 100
        self.assertEqual(calls[0][0], (1, -100))
        self.assertEqual(calls[1][0], (2, 100))
    
    def test_speed_constraint_low(self):
        """Test that speed is constrained to minimum value"""
        self.picar.tank_turn('right', -10)  # Negative
        
        calls = self.picar.set_motor_speed.call_args_list
        # Speed should be constrained to 0
        self.assertEqual(calls[0][0], (1, 0))
        self.assertEqual(calls[1][0], (2, 0))
    
    def test_invalid_direction_string(self):
        """Test that invalid string direction raises ValueError"""
        with self.assertRaises(ValueError):
            self.picar.tank_turn('invalid', 50)
    
    def test_invalid_direction_numeric(self):
        """Test that invalid numeric direction raises ValueError"""
        with self.assertRaises(ValueError):
            self.picar.tank_turn(2, 50)  # Only -1 and 1 are valid
        
        with self.assertRaises(ValueError):
            self.picar.tank_turn(0, 50)  # 0 is not valid
    
    def test_zero_speed(self):
        """Test tank turn with zero speed"""
        self.picar.tank_turn('left', 0)
        
        calls = self.picar.set_motor_speed.call_args_list
        self.assertEqual(calls[0][0], (1, 0))
        self.assertEqual(calls[1][0], (2, 0))

class TestTankTurnIntegration(unittest.TestCase):
    """Integration tests that require actual hardware (run with --integration flag)"""
    
    @unittest.skipUnless('--integration' in sys.argv, "Integration test - requires hardware")
    def test_actual_tank_turn(self):
        """Test actual tank turn on hardware"""
        picar = Picarx()
        
        try:
            # Perform a short tank turn
            picar.tank_turn('left', 30)
            time.sleep(0.5)
            picar.stop()
            
            # If we get here without exception, test passed
            self.assertTrue(True)
            
        except Exception as e:
            self.fail(f"Tank turn failed on actual hardware: {e}")
        finally:
            picar.stop()

def run_hardware_test():
    """Quick hardware test function"""
    print("Running hardware test for tank_turn function...")
    
    try:
        px = Picarx()
        
        print("Testing left tank turn...")
        px.tank_turn('left', 40)
        time.sleep(1.0)
        px.stop()
        
        time.sleep(0.5)
        
        print("Testing right tank turn...")
        px.tank_turn('right', 40)
        time.sleep(1.0)
        px.stop()
        
        print("✓ Hardware test completed successfully")
        
    except Exception as e:
        print(f"✗ Hardware test failed: {e}")
    finally:
        px.stop()

if __name__ == '__main__':
    if '--hardware' in sys.argv:
        # Remove the flag so unittest doesn't see it
        sys.argv.remove('--hardware')
        run_hardware_test()
    else:
        # Run unit tests
        unittest.main()