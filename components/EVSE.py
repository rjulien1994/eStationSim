import random

class EVSEConn:
    def __init__(self):
        self.ID = 0
        self.EVSEexportEnergy = 0
        self.EVSEimportEnergy = 0

    def updateVals(self):
        self.gridPower = random.randint(0, 50000)
        self.EVvoltage = random.randint(250, 900)
        self.EVcurrent = random.randint(0, 2000)/10
        self.EVSOC = random.randint(0,100)
        self.EVbattCapacity = 63800

        energy = random.randint(-100, 100)/10
        self.EVSEexportEnergy += max(0, energy)
        self.EVSEimportEnergy -= min(0, energy)

        self.ChargeTime = random.randint(0, 2000)
        self.RemainingChargeTime = random.randint(0, 2000)

        self.OCPPStatus = random.randint(0,5)
        self.EVstatus = random.randint(0,1)
        self.CPstatus = random.randint(0,1)

        self.EVcommState = random.randint(0,5)
        self.EVSEcontrolState = random.randint(0,5)

        self.EVmaxSOC = 100
        self.EVmaxChargeCurrent = 250
        self.EVmaxVoltage = 700
        self.EVmaxPower = 25000

        self.EVrequestVoltage = random.randint(300, self.EVmaxVoltage)
        self.EVrequestCurrent = random.randint(25, self.EVmaxChargeCurrent)
    
    def getVals(self):
        return {
            "Grid_Power": self.gridPower,
            "EV_voltage": self.EVvoltage,
            "EV_Current": self.EVcurrent,
            "EV_SOC": self.EVSOC,
            "EV_Battery": self.EVbattCapacity,

            "EV_Eexport": self.EVSEexportEnergy,
            "EV_Eimport": self.EVSEimportEnergy,

            "EV_charge_time": self.ChargeTime,
            "EV_est_charge_time_left": self.RemainingChargeTime,

            "OCPP_Status": self.OCPPStatus,
            "EV_status": self.EVstatus,
            "CP_status": self.CPstatus,

            "EV_Com_State": self.EVcommState,
            "EV_control_State": self.EVSEcontrolState,

            "EV_max_SOC": self.EVmaxSOC,
            "EV_max_Current": self.EVmaxChargeCurrent,
            "EV_max_Voltage": self.EVmaxVoltage,
            "EV_max_Power": self.EVmaxPower,

            "EV_request_Voltage": self.EVrequestVoltage,
            "EV_request_Current": self.EVrequestCurrent,
        }

class EVSE:
    def __init__(self, nConnectors=2):
        self.conns = [EVSEConn() for c in range(nConnectors)]
    
    def updateVals(self):
        for c in self.conns:
            c.updateVals()
        self.SW = "Beta 1.0.0"
        self.gridPower = random.randint(0, 50000)
        self.temperature = random.randint(15, 35)
        self.fault1 = random.randint(0, 10)
        self.fault2 = random.randint(0, 10)
        self.Nfault1 = random.randint(0, 10)
        self.Nfault2 = random.randint(0, 10)

    def getVals(self):
        return {
            "SW_version": self.SW,
            "Grid_power": self.gridPower,
            "Temperature": self.temperature,
            "Fault_1": self.fault1,
            "Fault_2": self.fault2,
            "Non_recoverable_Fault_1": self.Nfault1,
            "Non_recoverable_Fault_2": self.Nfault2,
            "Connectors": {f'conn{n}': c.getVals() for n, c in enumerate(self.conns)}
        }