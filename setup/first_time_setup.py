#!/usr/bin/env python3
"""
🚀 PiCar-X First Time Setup Wizard
==================================

Interactive setup wizard for first-time PiCar-X configuration.
This script guides you through all necessary calibration steps.

Run with: python3 first_time_setup.py
"""

import os
import sys
import time
import subprocess
from typing import Dict, List, Tuple, Optional
from pathlib import Path

# Add parent directory to path for picarx import
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from picarx import Picarx
except ImportError:
    print("❌ Error: Could not import picarx module")
    print("Please ensure you're in the correct directory and picarx is installed")
    sys.exit(1)


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class SetupWizard:
    """Interactive setup wizard for PiCar-X first-time configuration"""
    
    def __init__(self):
        self.setup_dir = Path(__file__).parent
        self.calibration_dir = self.setup_dir / "calibration"
        self.diagnostics_dir = self.setup_dir / "diagnostics"
        self.px: Optional[Picarx] = None
        
    def print_header(self, title: str, emoji: str = "🔧") -> None:
        """Print a formatted header"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.END}")
        print(f"{Colors.HEADER}{Colors.BOLD}{emoji} {title}{Colors.END}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.END}\n")
    
    def print_step(self, step: int, total: int, description: str) -> None:
        """Print step information"""
        print(f"{Colors.CYAN}{Colors.BOLD}[Step {step}/{total}] {description}{Colors.END}")
    
    def print_success(self, message: str) -> None:
        """Print success message"""
        print(f"{Colors.GREEN}✅ {message}{Colors.END}")
    
    def print_warning(self, message: str) -> None:
        """Print warning message"""
        print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")
    
    def print_error(self, message: str) -> None:
        """Print error message"""
        print(f"{Colors.RED}❌ {message}{Colors.END}")
    
    def wait_for_user(self, message: str = "Press Enter to continue...") -> None:
        """Wait for user input"""
        input(f"{Colors.BLUE}{message}{Colors.END}")
    
    def ask_yes_no(self, question: str, default: bool = True) -> bool:
        """Ask yes/no question"""
        default_str = "Y/n" if default else "y/N"
        while True:
            response = input(f"{Colors.BLUE}{question} ({default_str}): {Colors.END}").strip().lower()
            if response == "":
                return default
            elif response in ["y", "yes"]:
                return True
            elif response in ["n", "no"]:
                return False
            else:
                print("Please answer 'y' or 'n'")
    
    def run_script(self, script_path: Path, description: str) -> bool:
        """Run a calibration script"""
        try:
            print(f"\n{Colors.YELLOW}🔄 Running: {description}{Colors.END}")
            result = subprocess.run([sys.executable, str(script_path)], 
                                  capture_output=False, 
                                  text=True, 
                                  cwd=script_path.parent)
            
            if result.returncode == 0:
                self.print_success(f"Completed: {description}")
                return True
            else:
                self.print_error(f"Failed: {description}")
                return False
        except Exception as e:
            self.print_error(f"Error running {description}: {e}")
            return False
    
    def check_prerequisites(self) -> bool:
        """Check if system is ready for setup"""
        self.print_step(1, 7, "Checking Prerequisites")
        
        checks = [
            ("Python version", sys.version_info >= (3, 6)),
            ("Running as user", os.getuid() != 0),  # Should NOT run as root
            ("Setup directory", self.setup_dir.exists()),
            ("PiCar-X module", True),  # Already checked in import
        ]
        
        all_passed = True
        for check_name, passed in checks:
            if passed:
                self.print_success(f"{check_name}: OK")
            else:
                self.print_error(f"{check_name}: FAILED")
                all_passed = False
        
        if not all_passed:
            print(f"\n{Colors.RED}❌ Prerequisites check failed. Please fix the issues above.{Colors.END}")
            return False
        
        self.print_success("All prerequisites satisfied!")
        return True
    
    def hardware_connection_check(self) -> bool:
        """Verify hardware connections"""
        self.print_step(2, 7, "Hardware Connection Check")
        
        print("🔌 Checking basic hardware connections...")
        print("\nPlease verify your PiCar-X has:")
        print("  • Power connected and LED indicators on")
        print("  • Servo motors connected to servo board")
        print("  • Motors connected to motor driver")
        print("  • All sensor modules properly seated")
        
        if not self.ask_yes_no("Are all hardware connections secure?"):
            self.print_warning("Please check your connections before continuing")
            return False
        
        # Try to initialize Picarx
        try:
            self.px = Picarx()
            self.print_success("PiCar-X initialized successfully!")
            return True
        except Exception as e:
            self.print_error(f"Failed to initialize PiCar-X: {e}")
            self.print_warning("Check connections and try again")
            return False
    
    def servo_calibration(self) -> bool:
        """Run servo calibration"""
        self.print_step(3, 7, "Servo Calibration")
        
        print("🎯 This will calibrate your steering and camera servos")
        print("You'll be able to adjust servo angles using keyboard controls")
        
        if not self.ask_yes_no("Ready to calibrate servos?"):
            return False
        
        # Note: In real implementation, these scripts would need to be created
        servo_script = self.calibration_dir / "servo_calibration.py"
        if servo_script.exists():
            return self.run_script(servo_script, "Servo Calibration")
        else:
            print("📝 Manual servo calibration:")
            print("  1. Use 'W/S' keys to adjust direction servo")
            print("  2. Use 'A/D' keys to adjust camera pan")
            print("  3. Use 'Q/E' keys to adjust camera tilt")
            print("  4. Press 'Space' to save when servos are centered")
            self.wait_for_user("Complete manual calibration, then press Enter")
            return True
    
    def motor_calibration(self) -> bool:
        """Run motor calibration"""
        self.print_step(4, 7, "Motor Calibration")
        
        print("🚗 This will calibrate your drive motors")
        print("You'll test forward/backward movement and adjust directions")
        
        if not self.ask_yes_no("Ready to calibrate motors?"):
            return False
        
        motor_script = self.calibration_dir / "motor_calibration.py"
        if motor_script.exists():
            return self.run_script(motor_script, "Motor Calibration")
        else:
            print("📝 Manual motor calibration:")
            print("  1. Test forward movement - should move forward")
            print("  2. If backwards, use 'Q' to flip motor direction")
            print("  3. Adjust speed balance if turning while moving straight")
            self.wait_for_user("Complete manual calibration, then press Enter")
            return True
    
    def sensor_calibration(self) -> bool:
        """Run sensor calibration"""
        self.print_step(5, 7, "Sensor Calibration")
        
        print("📡 This will calibrate your sensors")
        print("Including grayscale sensors for line following")
        
        if not self.ask_yes_no("Ready to calibrate sensors?"):
            return False
        
        sensor_script = self.calibration_dir / "sensor_calibration.py"
        if sensor_script.exists():
            return self.run_script(sensor_script, "Sensor Calibration")
        else:
            print("📝 Manual sensor calibration:")
            print("  1. Place robot on white surface for baseline")
            print("  2. Place robot on black line for contrast")
            print("  3. Test cliff detection near table edge")
            self.wait_for_user("Complete manual calibration, then press Enter")
            return True
    
    def run_verification(self) -> bool:
        """Run verification tests"""
        self.print_step(6, 7, "Verification Tests")
        
        print("✅ Running final verification tests...")
        
        verification_script = self.diagnostics_dir / "hardware_check.py"
        if verification_script.exists():
            return self.run_script(verification_script, "Hardware Verification")
        else:
            # Manual verification
            print("📝 Manual verification tests:")
            
            tests = [
                "Servo movement (steering left/right)",
                "Camera pan/tilt movement",
                "Forward/backward movement",
                "Sensor readings (light/dark detection)",
            ]
            
            all_passed = True
            for test in tests:
                if self.ask_yes_no(f"✓ {test} working correctly?"):
                    self.print_success(f"PASS: {test}")
                else:
                    self.print_error(f"FAIL: {test}")
                    all_passed = False
            
            return all_passed
    
    def setup_complete(self) -> None:
        """Show completion message and next steps"""
        self.print_step(7, 7, "Setup Complete!")
        
        self.print_header("🎉 Congratulations! Setup Complete!", "🎉")
        
        print(f"{Colors.GREEN}Your PiCar-X is now ready to use!{Colors.END}\n")
        
        print("🚀 Next Steps:")
        print(f"  {Colors.CYAN}1. Try basic examples:{Colors.END}")
        print("     cd ../examples_new/01_basics")
        print("     python3 hello_world.py")
        print()
        print(f"  {Colors.CYAN}2. Learn with tutorials:{Colors.END}")
        print("     cd ../examples_new/02_movement")
        print("     python3 basic_movement.py")
        print()
        print(f"  {Colors.CYAN}3. Explore advanced features:{Colors.END}")
        print("     cd ../examples_new/04_vision")
        print("     python3 camera_preview.py")
        print()
        
        print(f"{Colors.YELLOW}📚 Documentation:{Colors.END}")
        print("  • Setup guide: setup/README.md")
        print("  • Examples guide: examples_new/README.md")
        print("  • API reference: Check the code documentation")
        print()
        
        print(f"{Colors.BLUE}🆘 Need help?{Colors.END}")
        print("  • Run diagnostics: python3 setup/diagnostics/hardware_check.py")
        print("  • Recalibrate: python3 setup/calibration/hardware_calibration.py")
        print("  • Factory reset: python3 setup/tools/factory_reset.py")
    
    def cleanup(self) -> None:
        """Clean up resources"""
        if self.px:
            try:
                # Clean shutdown of PiCar-X
                del self.px
                self.px = None
            except:
                pass
    
    def run(self) -> bool:
        """Run the complete setup wizard"""
        try:
            self.print_header("PiCar-X First Time Setup Wizard", "🚀")
            
            print(f"{Colors.BLUE}Welcome to PiCar-X!{Colors.END}")
            print("This wizard will guide you through the initial setup and calibration.")
            print("The process takes about 10-15 minutes.\n")
            
            if not self.ask_yes_no("Ready to begin setup?"):
                print("Setup cancelled.")
                return False
            
            # Run setup steps
            steps = [
                ("Prerequisites", self.check_prerequisites),
                ("Hardware Check", self.hardware_connection_check),
                ("Servo Calibration", self.servo_calibration),
                ("Motor Calibration", self.motor_calibration),
                ("Sensor Calibration", self.sensor_calibration),
                ("Verification", self.run_verification),
            ]
            
            for step_name, step_func in steps:
                if not step_func():
                    self.print_error(f"Setup failed at: {step_name}")
                    print("\nYou can:")
                    print("  • Fix the issue and run setup again")
                    print("  • Skip to manual calibration")
                    print("  • Check the setup/README.md for troubleshooting")
                    return False
                
                print()  # Add spacing between steps
            
            self.setup_complete()
            return True
            
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Setup interrupted by user{Colors.END}")
            return False
        except Exception as e:
            self.print_error(f"Unexpected error during setup: {e}")
            return False
        finally:
            self.cleanup()


def main():
    """Main entry point"""
    wizard = SetupWizard()
    
    try:
        success = wizard.run()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"{Colors.RED}Fatal error: {e}{Colors.END}")
        sys.exit(1)


if __name__ == "__main__":
    main()