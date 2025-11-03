#!/usr/bin/env python3
from picarx import Picarx
from time import sleep
import readchar 

manual = '''
--------------- Picar-X Calibration Helper -----------------

    [1]: direction servo            [W/D]: increase servo angle
    [2]: camera pan servo           [S/A]: decrease servo angle
    [3]: camera tilt servo          [R]: servos test

    [4]: left motor                 [Q]: change motor direction
    [5]: right motor                [E]: motors run/stop
    
    [6]: tank turn calibration      [T]: test tank turn 360°
    [7]: pivot turn calibration     [P]: test pivot turn 360°

    [SPACE]: confirm calibration                [Crtl+C]: quit
                                      
'''    

px = Picarx()
px_power = 30
tank_turn_speed = 50  # Default speed for tank turn calibration
pivot_turn_speed = 50  # Default speed for pivot turn calibration

servo_num = 0
motor_num = 0
tank_turn_time = float(px.config_file.get("tank_turn_360_time", default_value=4.0))  # Default 4 seconds for 360°
pivot_turn_time = float(px.config_file.get("pivot_turn_360_time", default_value=8.0))  # Default 8 seconds for 360° (slower than tank turn)
servo_names = ['direction servo', 'camera pan servo', 'camera tilt servo']
motor_names = ['left motor', 'right motor']
servos_cali = [px.dir_cali_val, px.cam_pan_cali_val, px.cam_tilt_cali_val]
motors_cali = px.cali_dir_value
servos_offset = list.copy(servos_cali)
motors_offset = list.copy(motors_cali)

def tank_turn_calibration():
    """Interactive tank turn calibration to measure 360° turn time"""
    import time
    global tank_turn_time
    
    print("\n=== Tank Turn Calibration ===")
    print("This will help calibrate how long it takes to make a 360° turn")
    print(f"Current speed: {tank_turn_speed}")
    print(f"Current 360° time: {tank_turn_time:.2f} seconds")
    print("\nInstructions:")
    print("1. Place a marker (tape, pen) pointing forward from the car")
    print("2. Press ENTER to start calibration turn")
    print("3. Watch the marker and press ENTER when it completes 360°")
    print("4. The time will be automatically measured and saved")
    print("\nPress ENTER to start, or 'c' to cancel...")
    
    key = input().lower()
    if key == 'c':
        return
    
    print("Starting 360° calibration turn in 3 seconds...")
    time.sleep(1)
    print("3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    print("GO! Press ENTER when the marker completes 360°")
    
    # Start tank turn and timer
    start_time = time.time()
    px.tank_turn('right', tank_turn_speed)
    
    # Wait for user to press enter when 360° is complete
    input()
    px.stop()
    
    # Calculate the time
    measured_time = time.time() - start_time
    
    print(f"\nMeasured time for 360° turn: {measured_time:.2f} seconds")
    print(f"Speed used: {tank_turn_speed}")
    
    # Ask if user wants to save this calibration
    save = input("Save this calibration? (y/n): ").lower()
    if save == 'y':
        tank_turn_time = measured_time
        px.config_file.set("tank_turn_360_time", tank_turn_time)
        px.config_file.set("tank_turn_calibration_speed", tank_turn_speed)
        print(f"✓ Saved: 360° turn takes {tank_turn_time:.2f}s at speed {tank_turn_speed}")
    else:
        print("Calibration not saved")

def test_tank_turn_360():
    """Test a 360° turn using current calibration"""
    import time
    
    print(f"\nTesting 360° turn using calibrated time: {tank_turn_time:.2f}s at speed {tank_turn_speed}")
    print("Starting in 3 seconds...")
    time.sleep(3)
    
    px.tank_turn('right', tank_turn_speed)
    time.sleep(tank_turn_time)
    px.stop()
    
    print("360° turn complete! Check if the car returned to its original orientation.")

def pivot_turn_calibration():
    """Interactive pivot turn calibration to measure 360° turn time"""
    global pivot_turn_time
    import time
    
    print("\n=== Pivot Turn Calibration ===")
    print("This will help calibrate how long it takes for a 360° pivot turn.")
    print("Make sure you have enough space around the car.")
    print(f"Current speed setting: {pivot_turn_speed}")
    print("\nThe car will pivot using one stationary wheel.")
    
    # User interaction
    input("Position the car and press Enter when ready...")
    
    print("Starting 360° pivot turn in 3 seconds...")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    start_time = time.time()
    px.pivot_turn('right', pivot_turn_speed)
    
    print("Pivot turning... Press Enter when the car completes 360° and returns to start position")
    input()  # Wait for user input
    
    px.stop()
    measured_time = time.time() - start_time
    
    print(f"\nMeasured time for 360° pivot turn: {measured_time:.2f} seconds")
    print(f"Speed used: {pivot_turn_speed}")
    
    # Ask if user wants to save this calibration
    save = input("Save this calibration? (y/n): ").lower()
    if save == 'y':
        pivot_turn_time = measured_time
        px.config_file.set("pivot_turn_360_time", pivot_turn_time)
        px.config_file.set("pivot_turn_calibration_speed", pivot_turn_speed)
        print(f"✓ Saved: 360° pivot turn takes {pivot_turn_time:.2f}s at speed {pivot_turn_speed}")
    else:
        print("Calibration not saved")

def test_pivot_turn_360():
    """Test a 360° pivot turn using current calibration"""
    import time
    
    print(f"\nTesting 360° pivot turn using calibrated time: {pivot_turn_time:.2f}s at speed {pivot_turn_speed}")
    print("Starting in 3 seconds...")
    time.sleep(3)
    
    px.pivot_turn('right', pivot_turn_speed)
    time.sleep(pivot_turn_time)
    px.stop()
    
    print("360° pivot turn complete! Check if the car returned to its original orientation.")

def servos_test():
    px.set_dir_servo_angle(-30)
    sleep(0.5)
    px.set_dir_servo_angle(30)
    sleep(0.5)
    px.set_dir_servo_angle(0)
    sleep(0.5)
    px.set_cam_pan_angle(-30)
    sleep(0.5)
    px.set_cam_pan_angle(30)
    sleep(0.5)
    px.set_cam_pan_angle(0)
    sleep(0.5)
    px.set_cam_tilt_angle(-30)
    sleep(0.5)
    px.set_cam_tilt_angle(30)
    sleep(0.5)
    px.set_cam_tilt_angle(0)
    sleep(0.5)

def servos_move(servo_num, value):
    if servo_num == 0:
        px.set_dir_servo_angle(value)
    elif servo_num == 1:
        px.set_cam_pan_angle(value)
    elif servo_num == 2:
        px.set_cam_tilt_angle(value)
    sleep(0.2)

def set_servos_offset(servo_num, value):
    if servo_num == 0:
        px.dir_cali_val = value
    elif servo_num == 1:
        px.cam_pan_cali_val = value
    elif servo_num == 2:
        px.cam_tilt_cali_val  = value  

def servos_reset():
    for i in range(3):
        servos_move(i,0)

def show_info():
    print("\033[H\033[J", end='')  # clear terminal windows
    print(manual)
    print('[ %s ] [ %s ]'%(servo_names[servo_num], motor_names[motor_num])) 
    print('offset: %s, %s'%(servos_offset, motors_offset))
    print(f'tank turn 360° time: {tank_turn_time:.2f}s @ speed {tank_turn_speed}')
    print(f'pivot turn 360° time: {pivot_turn_time:.2f}s @ speed {pivot_turn_speed}')


def cali_helper(): 
    global servo_num, motor_num
    global servos_cali, motors_cali, servos_offset, motors_offset
    motor_run = False
    step = 0.4
    # step = (180 / 2000) * (20000 / 4095)  # actual precision of steering gear

    # reset
    servos_reset()
    # show_info 
    show_info()

    # key control
    while True:
        # readkey
        key = readchar.readkey()
        key = key.lower()
        if key in ('1234567'):
            if key in ('123'):
                servo_num = int(key)-1
                show_info()
            elif key == '4' or key == '5':
                motor_num = int(key)-4
                show_info()
            elif key == '6':
                tank_turn_calibration()
                show_info()
            elif key == '7':
                pivot_turn_calibration()
                show_info()
        # servos move
        elif key == 'r':
            servos_test()
        elif key == 't':
            test_tank_turn_360()
            show_info()
        elif key == 'p':
            test_pivot_turn_360()
            show_info()
        elif key == 'w' or key == 'd':
            servos_offset[servo_num] += step
            if servos_offset[servo_num] > 20:
                servos_offset[servo_num] =20
            servos_offset[servo_num] = round(servos_offset[servo_num], 2) 
            show_info()
            set_servos_offset(servo_num, servos_offset[servo_num])
            servos_move(servo_num, 0)
        elif key == 's' or key == 'a':
            servos_offset[servo_num] -= step
            if servos_offset[servo_num] < -20:
                servos_offset[servo_num] = -20
            servos_offset[servo_num] = round(servos_offset[servo_num], 2) 
            show_info()
            set_servos_offset(servo_num, servos_offset[servo_num])
            servos_move(servo_num, 0)
        # motors move
        elif key == 'q': 
            motors_offset[motor_num] = -1 * motors_offset[motor_num]
            px.cali_dir_value = list.copy(motors_offset)
            motor_run = True
            px.forward(px_power)
            show_info()
        elif key == 'e':
            if motor_run == False:
                motor_run = True
                px.forward(px_power)
            else:
                motor_run = False
                px.stop()
        # save
        elif key == readchar.key.SPACE:
            print('Confirm save ?(y/n)')
            while True:
                key = readchar.readkey()
                key = key.lower()
                if key == 'y':
                    px.dir_servo_calibrate(servos_offset[0])
                    px.cam_pan_servo_calibrate(servos_offset[1])
                    px.cam_tilt_servo_calibrate(servos_offset[2])
                    px.motor_direction_calibrate(motor_num +1 , motors_offset[motor_num])
                    # Save turn calibration values
                    px.config_file.set("tank_turn_360_time", tank_turn_time)
                    px.config_file.set("tank_turn_calibration_speed", tank_turn_speed)
                    px.config_file.set("pivot_turn_360_time", pivot_turn_time)
                    px.config_file.set("pivot_turn_calibration_speed", pivot_turn_speed)
                    sleep(0.2)
                    servos_offset = [px.dir_cali_val, px.cam_pan_cali_val, px.cam_tilt_cali_val]
                    show_info()
                    print('The calibration value has been saved.')
                    print(f'Turn calibrations saved: Tank 360°={tank_turn_time:.2f}s, Pivot 360°={pivot_turn_time:.2f}s')
                    break
                elif key == 'n':
                    show_info()
                    break   
                sleep(0.01) 

        # quit
        elif key == readchar.key.CTRL_C or key in readchar.key.ESC:
            print('quit')
            break 

        sleep(0.01)


if __name__ == "__main__":
    try:
        cali_helper()
    except KeyboardInterrupt:
        print('quit')
    except Exception as e:
        print(e)
    finally:
        px.stop()
        sleep(0.1)
