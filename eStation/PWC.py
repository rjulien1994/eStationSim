import random

class PWCconnection:
    def __init__(self):
        self.ID = 0
    
    def updateVals(self):
        self.current = random.randint(0, 180)
    
    def getVals(self):
        return {'current': self.current}

class PWC:
    def __init__(self, nConns=6):
        self.name = "PWC"
        self.conns = [PWCconnection() for c in range(nConns)]
    
    def updateVals(self):
        for c in self.conns:
            c.updateVals()
        self.voltage = random.randint(150, 850)
        self.temperature = random.randint(15, 35)
    
    def getVals(self):
        return {
            "Voltage": self.voltage,
            "Temperature": self.temperature,
            "Connections": {"conn"+str(n): c.getVals() for n, c in enumerate(self.conns)}
        }