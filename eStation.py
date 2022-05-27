import time

from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
import uuid

from eStation.battery import *
from eStation.EVSE import *
from eStation.PCS import *
from eStation.PWC import *
from eStation.trafo import *


def load_avro_schema_from_file(schema_file):
    key_schema_string = """
    {"type": "string"}
    """

    key_schema = avro.loads(key_schema_string)
    value_schema = avro.load(schema_file)

    return key_schema, value_schema


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

    print(myStation.getVals())
    print("starting Data Sim")
    #myStation.run(delay=1/args.rate, duration=args.duration, topic=args.topic)
    print("End data sim")