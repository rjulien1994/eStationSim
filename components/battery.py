import random
from statistics import mean
import numpy as np

class cell:
    def __init__(self, capacity=100, minVolt=2.4, maxVolt=4.2):
        self.minVolt = minVolt
        self.maxVolt = maxVolt
        self.capacity = capacity

        self.voltage = random.randint(minVolt*100, maxVolt*100)/100
    
    def updateVals(self):
        self.voltage += random.randint(-5, 5)/100
        self.voltage = max(self.voltage, self.minVolt)
        self.voltage = min(self.voltage, self.maxVolt)

        self.temp = random.randint(1800, 3000)/100
        self.balance = random.randint(0, 1)
    
    def getVals(self):
        return {
            "Voltage": self.voltage,
            "Temperature": self.temp,
            "balancing": self.balance
        }

class module:
    def __init__(self, nCells=20):
        self.cells = [cell() for x in range(nCells)]
        self.capacity = sum([c.capacity for c in self.cells])
    
    def updateVals(self):
        for c in self.cells:
            c.updateVals()

        self.voltage = sum([c.voltage for c in self.cells])
        self.current = random.randint(-2000, 2000)/1000
        self.SOC = random.randint(0, 100)
        self.SOH = random.randint(0, 100)

        self.maxCellVoltage = max([c.voltage for c in self.cells])
        self.minCellVoltage = min([c.voltage for c in self.cells])
        self.meanCellVoltage = mean([c.voltage for c in self.cells])

        self.minCellVoltID = int(np.argmin([c.voltage for c in self.cells]))
        self.maxCellVoltID = int(np.argmax([c.voltage for c in self.cells]))

        self.maxCellTemp = max([c.temp for c in self.cells])
        self.minCellTemp = min([c.temp for c in self.cells])
        self.meanCellTemp = mean([c.temp for c in self.cells])

        self.minCellTempID = int(np.argmin([c.temp for c in self.cells]))
        self.maxCellTempID = int(np.argmax([c.temp for c in self.cells]))

        self.maxChargeCurrent = random.randint(0, 1000)/100
        self.maxDischargeCurrent = random.randint(0, 1000)/100

        self.TMSControl = random.randint(0, 10)
        self.TMSTemp = random.randint(180,300)/10
        self.TMSRealMode = random.randint(0, 10)
        
        self.rackInletTemp = random.randint(180,300)/10
        self.rackOutletTemp = random.randint(200,320)/10

        self.envTemp = random.randint(180,320)/10
        self.TMSpowerDemand = random.randint(0,10000)
        self.TMSFaultCode = random.randint(0, 10)

        self.doorState = random.randint(0, 1)
        self.fanState = random.randint(0, 1)

        self.systemWarning = random.randint(0, 1)
        self.relayStatus = random.randint(0, 1)
        self.balance = random.randint(0, 1)

    def getVals(self):
        return {
            "Voltage": self.voltage,
            "Current": self.current,
            "SOC": self.SOC,
            "SOH": self.SOH,

            "Max_Cell_Voltage": self.maxCellVoltage,
            "Min_Cell_Voltage": self.minCellVoltage,
            "Avg_Cell_Voltage": self.meanCellVoltage,

            "Min_Voltage_Cell_ID": self.minCellVoltID,
            "Max_Voltage_Cell_ID": self.maxCellVoltID,

            "Max_Cell_Temperature": self.maxCellTemp,
            "Min_Cell_Temperature": self.minCellTemp,
            "Avg_Cell_Temperature": self.meanCellTemp,

            "Min_Temp_Cell_ID": self.minCellTempID,
            "Max_Temp_Cell_ID": self.maxCellTempID,

            "Max_Charge_Current": self.maxChargeCurrent,
            "Max_Discharge_current": self.maxDischargeCurrent,

            "TMS_command": self.TMSControl,
            "TMS_temperature": self.TMSTemp,
            "TMS_Real_Mode": self.TMSRealMode,
        
            "Rack_inlet_Temp": self.rackInletTemp,
            "Rack_outlet_Temp": self.rackOutletTemp,

            "Temperature": self.envTemp,
            "TMS_power": self.TMSpowerDemand,
            "TMS_fault": self.TMSFaultCode,

            "Door_State": self.doorState,
            "Fan_State": self.fanState,

            "System_Warning": self.systemWarning,
            "Relay_Status": self.relayStatus,
            "Balancing": self.balance,

            #"Cells": [c.getVals() for c in self.cells]
        }

class rack:
    def __init__(self, nModules=8):
        self.modules = [module() for m in range(nModules)]
    
    def updateVals(self):
        for m in self.modules:
            m.updateVals()
        
        self.systemWarning = sum([m.systemWarning for m in self.modules])
        self.systemStatus = random.randint(0, 2)
        self.voltage = mean([m.voltage for m in self.modules])
        self.current = sum([m.current for m in self.modules])
        self.SOC = mean([m.SOC for m in self.modules])
        self.SOH = mean([m.SOH for m in self.modules])

        self.maxCellVoltage = max([m.maxCellVoltage for m in self.modules])
        self.minCellVoltage = min([m.minCellVoltage for m in self.modules])
        self.avgCellVoltage = mean([m.meanCellVoltage for m in self.modules])

        self.maxCellTemp = max([m.maxCellTemp for m in self.modules])
        self.minCellTemp = min([m.minCellTemp for m in self.modules])
        self.avgCellTemp = mean([m.meanCellTemp for m in self.modules])

        self.maxChargeCurrent = sum([m.maxChargeCurrent for m in self.modules])
        self.maxDischargeCurrent = sum([m.maxDischargeCurrent for m in self.modules])
    
    def getVals(self):
        return {
            "System_Warning": self.systemWarning,
            "System_Status": self.systemStatus,
            "Voltage": self.voltage,
            "Current": self.current,
            "SOC": self.SOC,
            "SOH": self.SOH,

            "Max_Cell_Voltage": self.maxCellVoltage,
            "Min_Cell_Voltage": self.minCellVoltage,
            "Avg_Cell_Voltage": self.avgCellVoltage,

            "Max_Cell_Temperature": self.maxCellTemp,
            "Min_Cell_Temperature": self.minCellTemp,
            "Avg_Cell_Temperature": self.avgCellTemp,

            "Max_Charge_Current": self.maxChargeCurrent,
            "Max_Discharge_Current": self.maxDischargeCurrent,

            "Modules": {f'Module{n}': m.getVals() for n, m in enumerate(self.modules)}
        }