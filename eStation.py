import time

import random
from statistics import mean
import numpy as np

from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
import uuid


def load_avro_schema_from_file(schema_file):
    key_schema_string = """
    {"type": "string"}
    """

    key_schema = avro.loads(key_schema_string)
    value_schema = avro.load(schema_file)

    return key_schema, value_schema

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

class eStation:
    def __init__(self, ID, schemaRegistry, schemaPath, kafkaServer='192.168.188.54:9092', nEVSEs=4, nBESS=1, nPWCEV=1, nPWCATL=1, nPCS=1):
        self.ID = ID
        self.msgID = 0
        self.status = 'running'
        self.QMT = PWC(8)
        self.mainTrafo = transfo()
        self.PCS = [PCS()]*nPCS
        self.PWCATL = [PWC(6)]*nPWCATL
        self.PWCEV = [PWC(6)]*nPWCEV
        self.BESS = [rack()]*nBESS
        self.EVSEs = [EVSE()]*nEVSEs

        key_schema, value_schema = load_avro_schema_from_file(schemaPath)
        self.producer = AvroProducer({"bootstrap.servers": kafkaServer, "schema.registry.url": schemaRegistry}, default_key_schema=key_schema, default_value_schema=value_schema)
    
    def update(self):
        self.QMT.updateVals()
        self.mainTrafo.updateVals()
        self.msgID += 1

        for c in [self.PCS, self.PWCATL, self.PWCEV, self.BESS, self.EVSEs]:
            for u in c:
                u.updateVals()
    
    def getVals(self):
        self.update()
        return {
            "Station_ID": self.ID,
            "MsgID": self.msgID,
            'status': self.status,
            "timeStamp": time.time()*1000,
            "QMT": self.QMT.getVals(),
            "Transformator": self.mainTrafo.getVals(),
            "PCSs": {f"PCS{n}": x.getVals() for n, x in enumerate(self.PCS)},
            "PWCATLs": {f"PWC{n}": x.getVals() for n, x in enumerate(self.PWCATL)},
            "PWCEVs": {f"PWC{n}": x.getVals() for n, x in enumerate(self.PWCEV)},
            "BESSs": {f"Rack{n}": x.getVals() for n, x in enumerate(self.BESS)},
            "EVSEs": {f"EVSE{n}": x.getVals() for n, x in enumerate(self.EVSEs)},
        }
    
    def run(self, maxIter=False, delay=0.05, duration=10000, topic=False): #max speed ~500Hz
        myTime = 0
        start = time.time()
        maxIter = maxIter if maxIter else duration/delay + 1
        topic = topic if topic else self.ID
        msgCount = 0
        while start + duration > time.time():
            if myTime + delay < time.time():
                myTime = time.time() if myTime == 0 else myTime+delay
                #self.producer.send(self.ID if not topic else topic, self.getVals())
                self.producer.produce(topic=topic, key=str(uuid.uuid4()), value=self.getVals())
                msgCount +=1
            if msgCount >= maxIter:
                break
        self.producer.flush()
        print(f'Number of msg sent: {msgCount}/{maxIter}')

def parseArguments():
    import argparse

    parser = argparse.ArgumentParser(description='This is a script simulating the data production of the components in an eStation. All values are randomized and do not follow any logic.')

    parser.add_argument('--name', type=str, default="Default",help="Unique identifier of the eStation as it will appear on Kafka")
    parser.add_argument('--schema-registry', type=str, help="URL of schema registry used to store and verify compatibility of serializer")
    parser.add_argument('--schema', type=str, help="Path to schema used to serialize the message")
    parser.add_argument('--bootstrap-server', type=str, help="URL of the kafka or zookeeper server through which we connect to topic as a producer")
    parser.add_argument('--PCS', type=int, default=1, help="Number of PCSs simulated for the eStation")
    parser.add_argument('--PWCATL', type=int, default=1, help="Number of PWCATLs simulated for the eStation")
    parser.add_argument('--PWCEV', type=int, default=1, help="Number of PWCEVs simulated for the eStation")
    parser.add_argument('--BESS', type=int, default=1, help="Number of BESSs simulated for the eStation")
    parser.add_argument('--EVSE', type=int, default=1, help="Number of EVSEs simulated for the eStation")
    parser.add_argument('--duration', type=int, default=60, help="Duration of data production in seconds")
    parser.add_argument('--rate', type=float, default=20, help="Frequency of data production in Hz")
    parser.add_argument('--topic', type=str, help="Frequency of data production in Hz")

    return parser.parse_args()

if __name__ == "__main__":
    args = parseArguments()

    myStation = eStation(
        args.name,#"ATL1", 
        schemaRegistry=args.schema_registry, #"http://192.168.188.54:8081", 
        schemaPath=args.schema,#'eStationAvroSchemaV2.avsc',
        kafkaServer=args.bootstrap_server,#'192.168.188.54:9092', 
        nEVSEs=args.EVSE, nBESS=args.BESS, nPWCEV=args.PWCEV, nPWCATL=args.PWCATL, nPCS=args.PCS)

    #print(myStation.getVals())
    print("starting Data Sim")
    myStation.run(delay=1/args.rate, duration=args.duration, topic=args.topic)
    print("End data sim")