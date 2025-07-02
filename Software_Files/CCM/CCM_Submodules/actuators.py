from CCM_Submodules.global_data import hw_drivers_data, rf_comms_data

def task_005ms():
    '''
    This function is called every 5ms to update the servo position based on the received data.
    '''
    # Get the received data
    _, turn_angle, decode_result = rf_comms_data.get_rx_data()

    # If the packet is valid, set the servo angle
    if decode_result:
        hw_drivers_data.servo_pin.set_angle(turn_angle)


    