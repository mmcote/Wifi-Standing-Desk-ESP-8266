from ujson import load


class Config(object):
    def __init__(self):
        super().__init__()

        with open("./../config.json") as configFile:
            configMap = load(configFile)

        self.wifiConfig = WifiConfig(configMap["wifi"])
        self.deskIpConfig = DeskIpConfig(configMap["deskIp"])
        self.deskConfig = DeskConfig(configMap["desk"])
        self.sensorConfig = SensorConfig(configMap["sensor"])

class WifiConfig(object):
    def __init__(self, wifiConfigMap):
        super().__init__()

        self.ssid = wifiConfigMap["ssid"]
        self.password = wifiConfigMap["password"]

    def getSSID(self):
        return self.ssid

    def getPassword(self):
        return self.password

class DeskIpConfig(object):
    def __init__(self, deskIpConfigMap):
        super().__init__()

        self.ip = deskIpConfigMap["ip"]
        self.gateway = deskIpConfigMap["gateway"]

    def getIp(self):
        return self.ip

    def getGateway(self):
        return self.gateway

class DeskConfig(object):
    def __init__(self, deskConfigMap):
        super().__init__()

        self.upPin = deskConfigMap["upPin"]
        self.downPin = deskConfigMap["downPin"]
        self.invertedPins = str(deskConfigMap["invertedPins"]).lower() == "true"

        self.rollingWindowSize = deskConfigMap["rollingWindowSize"]
        self.allowableErrorInCentimeters = deskConfigMap["allowableErrorInCentimeters"]
        self.allowableMeasurementErrorRatio = deskConfigMap["allowableMeasurementErrorRatio"]
        self.consecutiveErrorsUntilRestart = deskConfigMap["consecutiveErrorsUntilRestart"]
        self.measurementDeltaInMicroseconds = deskConfigMap["measurementDeltaInMicroseconds"]
        self.numHeightChecksRequired = deskConfigMap["numHeightChecksRequired"]

    def getUpPin(self):
        return self.upPin

    def getDownPin(self):
        return self.downPin

    def isInvertedPins(self):
        return self.invertedPins

    def getRollingWindowSize(self):
        return self.rollingWindowSize

    def getAllowableErrorInCentimeters(self):
        return self.allowableErrorInCentimeters

    def getAllowableMeasurementErrorRatio(self):
        return self.allowableMeasurementErrorRatio

    def getConsecutiveErrorsUntilRestart(self):
        return self.consecutiveErrorsUntilRestart

    def getMeasurementDeltaInMicroseconds(self):
        return self.measurementDeltaInMicroseconds

    def getNumHeightChecksRequired(self):
        return self.numHeightChecksRequired

class SensorConfig(object):
    def __init__(self, sensorConfigMap):
        super().__init__()

        self.triggerPin = sensorConfigMap["triggerPin"]
        self.echoPin = sensorConfigMap["echoPin"]

    def getTriggerPin(self):
        return self.triggerPin

    def getEchoPin(self):
        return self.echoPin

class MeasurementConfig(object):
    def __init__(self, measurementConfigMap):
        super().__init__()
