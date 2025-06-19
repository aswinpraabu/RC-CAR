
class hw_drivers_data_class:
    
    rfm69_SPI = None
    rfm69_CS = None
    rfm69_RESET = None


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