class transfo:
    def __init__(self, maxPower=1000000):
        self.nominalPower = maxPower
    
    def updateVals(self):
        self.setPower = 50000
        self.DCVoltage = 850
    
    def getVals(self):
        return {
            "set_Power": self.setPower,
            "DC_Voltage": self.DCVoltage
        }