
class hw_drivers_data_class:
    
    rfm69_SPI = None
    rfm69_CS = None
    rfm69_RESET = None


    def get_rfm69_info(self):
        '''
        Returns the SPI, CS, and RESET pin objects for the RFM69 module.
        -> (SPI, CS, RESET)
        '''
        return self.rfm69_SPI, self.rfm69_CS, self.rfm69_RESET
    

hw_drivers_data = hw_drivers_data_class()