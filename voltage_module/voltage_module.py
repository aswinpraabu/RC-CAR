from typing import NamedTuple
from enum import Enum

class fault_level(Enum):
    NO_ERROR = 0
    WARNING = 1
    ERROR = 2


class voltages_struct(NamedTuple):
    pack_voltage : float #  (V2 - V1) Voltage of the battery pack
    bus_voltage : float # (V4 - V2) Voltage after the main relays
    fuse2_voltage : float # (V4 - V9) Voltage between after main positive relay and after fuse2
    dc_charge_voltage: float # (V6 - V5) Voltage across of the DC charger
    ecu_supply_voltage: float # (V8 - V9) Voltage across pthe ECU's supply terminals

class diagnostic_thresholds_struct(NamedTuple):
    # UV = Under Voltage
    # OV = Over Voltage
    pack_UV_OV_warn_thresholds : tuple[float, float] # Pack UV warning threshold , OV warning threshold
    pack_UV_OV_error_thresholds : tuple[float, float] # Pack UV error threshold, OV error threshold
    dc_charge_UV_OV_warn_thresholds : tuple[float, float] # DC Charging UV warning threshold, OV warning threshold
    dc_charge_UV_OV_error_thresholds : tuple[float, float] # DC Charging UV error threshold, OV error threshold
    ecu_supply_UV_OV_warn_thresholds : tuple[float, float] # ECU Supply UV warning threshold, OV warning threshold
    ecu_supply_UV_OV_error_thresholds : tuple[float, float] # ECU Supply UV error threshold, OV error threshold

# probably will move this to a common library and use it in other places
class dtc_description(NamedTuple):
    Name : str
    Description : str
    DTC_code : int
    threshold : float
    maturation_time : float
    dematuration_time : float
    fault_cat : int
    

class diagnostic_results_struct(NamedTuple):
    # True = fault is present
    # False = fault is not present
    # UV = Under Voltage
    # OV = Over Voltage
    pack_UV_OV : tuple[fault_level, fault_level]  = (fault_level.NO_ERROR,fault_level.NO_ERROR) # Pack Voltage faults
    dc_charge_UV_OV : tuple[fault_level, fault_level]  = (fault_level.NO_ERROR,fault_level.NO_ERROR) # DC Charging Voltage faults
    ecu_supply_UV_OV : tuple[fault_level, fault_level]  = (fault_level.NO_ERROR,fault_level.NO_ERROR) # ECU Supply Voltage faults


class voltage_mod:
    _diagnostic_thresholds:diagnostic_thresholds_struct
    _diagnostic_results:diagnostic_results_struct
    def __init__(self):
        
        pass
    def load_calibrations(self, calibration_file_path):

        #TODO remove this later; Temporarily here until file read is implemented
        thresholds = diagnostic_thresholds_struct(
        (9.5,11.5),
        (9.2,12.2),
        (11,12.4),
        (10.5,12.6),
        (9.5,11.5),
        (9,12.5)
        )
        diagnostic_thresholds = thresholds
    def main(self):
        self.diagnostics()
        pass

    def diagnostics(self):
        pack_OV = 0 # 1 = warning, 2 = error
        pass


if __name__ == '__main__':
    voltages = voltages_struct(1,2,3,4,5)
    thresholds = diagnostic_thresholds_struct(
        (9.5,11.5),
        (9.2,12.2),
        (11,12.4),
        (10.5,12.6),
        (9.5,11.5),
        (9,12.5)
    )
    v = voltage_mod()
    