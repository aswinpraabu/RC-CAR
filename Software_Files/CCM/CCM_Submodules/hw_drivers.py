from CCM_Submodules.global_data import hw_drivers_data, rf_comms_data
from machine import SPI, Pin,PWM

# region RFM69
# Define pin numbers for RFM69 module
RFM69_MOSI_PIN = 19
RFM69_MISO_PIN = 16
RFM69_SCK_PIN = 18
RFM69_CS_PIN = 17
RFM69_RESET_PIN = 20
a = PWM(Pin(RFM69_MOSI_PIN), freq=1000000)  # Example PWM initialization, adjust as needed
a.duty_ns()

# endregion
SERVO_PIN = 21


class Servo:
    def __init__(self):
        pass

    def configure_pin(self, pin):

        # Initialize the parameters for the SG90 servo motor
        self.pin = Pin(pin, Pin.OUT)
        self.angle = 0  # Initialize angle to 0 degrees
        self.min_angle = -90.0  # Minimum angle
        self.max_angle = 90.0 # Maximum angle
        self.min_duty_ns = 1.0e6 # (1ms) Minimum duty cycle in nanoseconds
        self.max_duty_ns = 2.0e6 # (2ms)Maximum duty cycle in nanoseconds
        self.freq = 50

        self.min_duty_offset_ms = -0.5344 # Offset for minimum duty cycle
        self.max_duty_offset_ms = 0.57 # Offset for maximum duty cycle
        self.min_duty_ns += int(self.min_duty_offset_ms * 1e6)  # Convert ms to ns
        self.max_duty_ns += int(self.max_duty_offset_ms * 1e6)  # Convert ms to ns
        
        self.pwm = PWM(self.pin, freq=self.freq)


    def set_angle(self, angle):
        if self.min_angle <= angle <= self.max_angle:
            self.angle = angle
            
            duty_ns = self._angle_to_duty_ns(angle)
            self.pwm.duty_ns(duty_ns)

    def _angle_to_duty_ns(self, angle: float) -> int:
        '''
        Convert angle to duty cycle in ns
        '''
        duty_ns:int = 0
        if angle < self.min_angle or angle > self.max_angle:
            print(f"Angle must be between {self.min_angle} and {self.max_angle} degrees")
            duty_ns = int(( self.max_duty_ns + self.min_duty_ns)/2)
        else:    
            factor = (self.max_duty_ns - self.min_duty_ns)/(self.max_angle - self.min_angle)
            duty_ns = int((angle - self.min_angle) * factor + self.min_duty_ns)
        #print(f"Setting servo angle to {angle} degrees, duty_ns: {duty_ns}")
        return duty_ns

steering_servo = Servo()

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

    steering_servo.configure_pin(SERVO_PIN)

def task_005ms():
    '''
    This function is called every 5ms to update the servo position based on the received data.
    '''
    # Get the received data
    _, turn_angle, decode_result = rf_comms_data.get_rx_data()

    # If the packet is valid, set the servo angle
    if decode_result:
        steering_servo.set_angle(turn_angle)
    pass

