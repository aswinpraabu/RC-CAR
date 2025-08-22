# CAL + _ + submodule name + _ + unit + _ + name 

# f = frequency
# a = angle
# p = percentage
# t = time

from micropython import const

# This unnecessarily creates classes, but it helps with organization and clarity
# If more efficiency is needed, these can be converted global constants instead

class HW_DRIVERS_Class:
    # Servo calibration parameters
    CAL_f_servo_freq = 50  # Frequency for servo PWM in Hz
    CAL_a_servo_min_angle = -90  # Minimum angle for servo in degrees
    CAL_t_servo_min_duty_offset_ms = -0.5344   # Offset for minimum duty cycle in milliseconds
    CAL_t_servo_max_duty_offset_ms = 0.57  # Offset for maximum duty cycle in milliseconds

    # DC Motor calibration parameters
    CAL_f_dc_motor_freq = 1000  # Frequency for DC motor PWM in Hz
    CAL_P_dc_motor_min_power = -100  # Minimum power for DC motor in percentage
    CAL_P_dc_motor_max_power = 100  # Maximum power for DC motor in percentage
    CAL_p_dc_motor_reverse_factor = 50  # Minimum speed for DC motor in RPM

class CONTROLS_Class:
    CAL_t_Prepare_Shutdown_duration_ms = 5000  # Duration to stay in Prepare_Shutdown mode

class RF_COMMS_Class:
    CAL_f_rf_comms_freq = 1000  # Frequency for RF communications in Hz
    CAL_t_shutdown_timeout_ms = 100  # Timeout for reseting the shutdown request in milliseconds

HW_DRIVERS_Calibrations = HW_DRIVERS_Class()
CONTROLS_Calibrations = CONTROLS_Class()
