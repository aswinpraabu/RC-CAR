from CCM_Submodules.global_data import hw_drivers_data, rf_comms_data, controls_data
from time import ticks_ms, ticks_diff

class POWER_MODES:
    Normal = 0
    Prepare_Shutdown = 1
    Shutdown = 2

Prepare_Shutdown_start_time = 0  # Time when Prepare_Shutdown mode started
Prepare_Shutdown_duration_ms = 5000  # Duration to stay in Prepare_Shutdown mode

def initialize():
    pass


def motor_control():
    if rf_comms_data.rx_validity and controls_data.power_mode == POWER_MODES.Normal:
        # Update car throttle and turn angle based on received data
        controls_data.car_throttle = rf_comms_data.rx_throttle
        controls_data.car_turn_angle = rf_comms_data.rx_turn_angle
    else:
        # If data is invalid or not in Normal mode, stop the car
        controls_data.car_throttle = 0
        controls_data.car_turn_angle = 0
        


def power_control():
    global Prepare_Shutdown_start_time
    
    if controls_data.power_mode == POWER_MODES.Normal and rf_comms_data.shutdown_request_confirmed:
        # Transition to Prepare_Shutdown mode
        controls_data.power_mode = POWER_MODES.Prepare_Shutdown
        
        Prepare_Shutdown_start_time = ticks_ms()
        print("Transitioning to Prepare_Shutdown mode")

    elif controls_data.power_mode == POWER_MODES.Prepare_Shutdown:
        elapsed_time = ticks_diff(ticks_ms(), Prepare_Shutdown_start_time)
        if elapsed_time >= Prepare_Shutdown_duration_ms:
            # Transition to Shutdown mode after the duration
            controls_data.power_mode = POWER_MODES.Shutdown
            print("Transitioning to Shutdown mode")

def warning_lights_control():
    controls_data.led2_loc_rcm = rf_comms_data.LOC_with_RCM





def task_005ms():
    # Update motor control based on received data
    motor_control()
    


def task_010ms():
    # Update power control if needed
    power_control()


def task_100ms():
    # Update warning lights based on communication status
    warning_lights_control()
    
