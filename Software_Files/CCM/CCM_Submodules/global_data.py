from machine import SPI, Pin
from controls import POWER_MODES

class hw_drivers_data_class:
    
    rfm69_SPI:SPI = None #type: ignore
    rfm69_CS:Pin = None #type: ignore
    rfm69_RESET:Pin = None #type: ignore


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