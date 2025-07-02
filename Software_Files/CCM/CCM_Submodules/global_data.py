from machine import SPI, Pin
from hw_drivers import Servo

class hw_drivers_data_class:
    
    rfm69_SPI:SPI = None #type: ignore
    rfm69_CS:Pin = None #type: ignore
    rfm69_RESET:Pin = None #type: ignore
    servo_pin:Servo = None #type: ignore

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

    def get_rx_data(self):
        '''
        Returns the received throttle and turn angle data.\n
        -> (throttle, turn_angle, decode_result)
        '''
        return self.rx_throttle, self.rx_turn_angle, self.rx_validity
    
# Initialize global data instances    
hw_drivers_data = hw_drivers_data_class()
rf_comms_data = rf_comms_data_class()