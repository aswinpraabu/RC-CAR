from CCM_Submodules.global_data import hw_drivers_data
from machine import SPI, Pin

# region RFM69
# Define pin numbers for RFM69 module
RFM69_MOSI_PIN = 19
RFM69_MISO_PIN = 16
RFM69_SCK_PIN = 18
RFM69_CS_PIN = 17
RFM69_RESET_PIN = 20

# endregion

def initialize():
    print("Initializing hardware drivers...")
    hw_drivers_data.rfm69_SPI = SPI(
                                    0,
                                    baudrate=500_000,
                                    polarity=0,
                                    phase=0,
                                    bits=8,
                                    firstbit=SPI.MSB,
                                    sck=Pin(RFM69_SCK_PIN),# type: ignore
                                    mosi=Pin(RFM69_MOSI_PIN),# type: ignore
                                    miso=Pin(RFM69_MISO_PIN)# type: ignore
                                    )
    hw_drivers_data.rfm69_CS = Pin(RFM69_CS_PIN, Pin.OUT)
    hw_drivers_data.rfm69_RESET = Pin(RFM69_RESET_PIN, Pin.OUT)


def task_005ms():
    pass

