class PCS:
    def __init__(self, maxPower=500000):
        self.nominalPower = maxPower
    
    def updateVals(self):
        self.setDCVoltage = 750
        self.setDCCurrent = 400
    
    def getVals(self):
        return {
            "set_Voltage": self.setDCVoltage,
            "set_Current": self.setDCCurrent
        }