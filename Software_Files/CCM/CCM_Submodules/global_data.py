from micropython import const
from machine import SPI, Pin
from time import ticks_ms, ticks_diff

class POWER_MODES:
    Normal = const(0)
    Prepare_Shutdown = const(1)
    Shutdown = const(2)

class DIAG_STATUS:
    Not_Tested = const(-1)
    OK = const(1)
    FAIL = const(2)
class diagnostics_class:
    _id = 0
    _name = ""
    _diag_status = -1 # Possible values: "-1 Not Tested", "1 OK", "2 FAIL"
    _last_test_fail = False
    _test_fail_start_time = 0
    _test_pass_start_time = 0

    _mature_time_ms = 0
    _demature_time_ms = 0
    def __init__(self, id:int, name:str, mature_time:int, demature_time:int):
        self._id = id
        self._name = name
        self._mature_time_ms = mature_time
        self._demature_time_ms = demature_time
        self._test_fail_start_time = 0
        self._test_pass_start_time = 0
        self._diag_status = DIAG_STATUS.Not_Tested
        self._last_test_fail = False

    def test_fail(self):
        current_time = ticks_ms()
        if not self._last_test_fail:
            # if last test was not a fail, set the flag & start the timer
            self._test_fail_start_time = current_time
            self._last_test_fail = True
        elif self._last_test_fail and self._diag_status != 2:
            # if last test was a fail, check if mature time has passed
            elapsed_time = ticks_diff(current_time, self._test_fail_start_time)
            if elapsed_time >= self._mature_time_ms:
                self._diag_status = 2
                print(f"Diag {self._name} (ID: {self._id}) diagnostic status changed to FAIL")
    
    def test_pass(self):
        current_time = ticks_ms()
        if self._last_test_fail:
            # if last test was a fail, set the flag & start the timer
            self._test_pass_start_time = current_time
            self._last_test_fail = False
        elif not self._last_test_fail and self._diag_status != 1:
            # if last test was a pass, check if demature time has passed
            elapsed_time = ticks_diff(current_time, self._test_pass_start_time)
            if elapsed_time >= self._demature_time_ms:
                self._diag_status = 1
                print(f"Diag {self._name} (ID: {self._id}) diagnostic status changed to OK")
    def reset_status(self):
        self._diag_status = -1
        self._last_test_fail = False
        self._test_fail_start_time = 0
        self._test_pass_start_time = 0
    def get_status(self):
        return self._diag_status

class hw_drivers_data_class:
    
    rfm69_SPI:SPI = None #type: ignore
    rfm69_CS:Pin = None #type: ignore
    rfm69_RESET:Pin = None #type: ignore

    battery_voltage = 0.0  # Battery voltage in volts
    battery_voltage_validity = False  # Flag indicating if battery voltage reading is valid
    battery_current = 0.0  # Battery current in milliamps
    battery_current_validity = False  # Flag indicating if battery current reading is valid

    battery_voltage_low_warn = False  # Flag indicating if battery voltage is low (warning level)
    battery_voltage_low_critical = False  # Flag indicating if battery voltage is critically low
    battery_voltage_low_warn_diag:diagnostics_class = None #type: ignore
    battery_voltage_low_critical_diag:diagnostics_class = None #type: ignore


    def get_rfm69_info(self):
        '''
        Returns the SPI, CS, and RESET pin objects for the RFM69 module.\n
        -> (SPI, CS, RESET)
        '''
        return self.rfm69_SPI, self.rfm69_CS, self.rfm69_RESET
    
class rf_comms_data_class:
    rx_throttle = 0
    rx_turn_angle = 0
    rx_validity = False

    LOC_with_RCM = False #Flag to indicate if CCM has lost communication with RCM

    shutdown_request_confirmed = False # Flag to indicate if Shutdown message has been received and confirmed
    LOC_with_RCM_diag:diagnostics_class = None #type: ignore
    def get_rx_PropulsionCtrl_data(self):
        '''
        Returns the received throttle and turn angle data.\n
        -> (throttle, turn_angle, decode_result)
        '''
        return self.rx_throttle, self.rx_turn_angle, self.rx_validity
    
class controls_data_class:
    car_throttle = 0
    car_turn_angle = 0

    led1_bat_low = False  # LED1 indicates battery is low
    led2_loc_rcm = False  # LED2 indicates CCM has lost communication with RCM

    power_mode = POWER_MODES.Normal
    
# Initialize global data instances    
hw_drivers_data = hw_drivers_data_class()
rf_comms_data = rf_comms_data_class()
controls_data = controls_data_class()