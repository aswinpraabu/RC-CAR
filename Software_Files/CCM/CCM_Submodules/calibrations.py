# CAL + _ + submodule name + _ + unit + _ + name 

# f = frequency
# a = angle
# p = percentage
# t = time

from micropython import const
from CCM_Libraries.ina260 import AveragingCount, ConversionTime

# This unnecessarily creates classes, but it helps with organization and clarity
# If more efficiency is needed, these can be converted global constants instead

class HW_DRIVERS_Class:
    # Servo calibration parameters
    CAL_f_servo_freq = const(50)  # Frequency for servo PWM in Hz
    CAL_a_servo_min_angle = const(-90)  # Minimum angle for servo in degrees
    CAL_t_servo_min_duty_offset_ms = const(-0.5344)   # Offset for minimum duty cycle in milliseconds
    CAL_t_servo_max_duty_offset_ms = const(0.57)  # Offset for maximum duty cycle in milliseconds

    # DC Motor calibration parameters
    CAL_f_dc_motor_freq = const(1000)  # Frequency for DC motor PWM in Hz
    CAL_P_dc_motor_min_power = const(-100)  # Minimum power for DC motor in percentage
    CAL_P_dc_motor_max_power = const(100)  # Maximum power for DC motor in percentage
    CAL_p_dc_motor_reverse_factor = const(50)  # Minimum speed for DC motor in RPM

    # INA260 calibration parameters
    CAL_t_ina260_voltage_conversion_time = ConversionTime.TIME_8_244_ms  # Voltage conversion time in ms
    CAL_t_ina260_current_conversion_time = ConversionTime.TIME_1_1_ms # Current conversion time in ms
    CAL_n_ina260_averaging_count = AveragingCount.COUNT_4  # Number of samples to average

class CONTROLS_Class:
    CAL_t_Prepare_Shutdown_duration_ms = const(5000)  # Duration to stay in Prepare_Shutdown mode

class RF_COMMS_Class:
    CAL_f_rf_comms_freq = const(1000)  # Frequency for RF communications in Hz
    CAL_t_shutdown_timeout_ms = const(100)  # Timeout for reseting the shutdown request in milliseconds

HW_DRIVERS_Calibrations = HW_DRIVERS_Class()
CONTROLS_Calibrations = CONTROLS_Class()
