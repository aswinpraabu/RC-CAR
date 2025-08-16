from CCM_Submodules.global_data import hw_drivers_data, rf_comms_data, controls_data

def initialize():
    pass


def motor_control():
    if rf_comms_data.rx_validity:
        # Update car throttle and turn angle based on received data
        controls_data.car_throttle = rf_comms_data.rx_throttle
        controls_data.car_turn_angle = rf_comms_data.rx_turn_angle
        


def power_control():
    pass

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
    
