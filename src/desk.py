from machine import Pin
from utime import sleep_us
from rollingAverageState import RollingAverageState


class Desk(object):
    def __init__(self, deskConfig, deskHeightSensor):
        super().__init__()

        self.upGPIO = Pin(deskConfig.getUpPin(), Pin.OUT)
        self.downGPIO = Pin(deskConfig.getDownPin(), Pin.OUT)
        self.inverted = deskConfig.isInvertedPins()

        self.sensor = deskHeightSensor

        self.rollingWindowSize = deskConfig.getRollingWindowSize()
        self.measurementErrorRatio = deskConfig.getAllowableMeasurementErrorRatio()
        self.consecutiveErrorsUntilRestart = deskConfig.getConsecutiveErrorsUntilRestart()
        self.measurementDeltaInMicroseconds = deskConfig.getMeasurementDeltaInMicroseconds()
        self.errorInCentimeters = deskConfig.getAllowableErrorInCentimeters()
        self.numChecksRequired = deskConfig.getNumHeightChecksRequired()

    def getCurrentHeight(self):
        state = RollingAverageState(self.rollingWindowSize, self.measurementErrorRatio, self.consecutiveErrorsUntilRestart)

        while True:
            measurement = self.sensor.getCurrentCentimeters()
            if measurement != -1:
                state.addMeasurement(measurement)

            if state.isFull():
                return state.getCurrentRollingAverage()

            sleep_us(self.measurementDeltaInMicroseconds)

    def adjustToHeight(self, height):
        checksCompleted = 0
      
        state = RollingAverageState(self.rollingWindowSize, self.measurementErrorRatio, self.consecutiveErrorsUntilRestart)
        while True:
            measurement = self.sensor.getCurrentCentimeters()
            sleep_us(int(self.measurementDeltaInMicroseconds/6))
            if measurement != -1:
                state.addMeasurement(measurement)

            if state.isFull():
                currentValue = state.getCurrentRollingAverage()
                if currentValue <= height + self.errorInCentimeters and currentValue > height - self.errorInCentimeters:
                    self.stop()
                    state = RollingAverageState(self.rollingWindowSize, self.measurementErrorRatio, self.consecutiveErrorsUntilRestart)

                    checksCompleted += 1
                    if checksCompleted == self.numChecksRequired:
                        return currentValue
                elif currentValue < height - self.errorInCentimeters:
                    self.up()
                elif currentValue > height + self.errorInCentimeters:
                    self.down()

    def down(self):
        self.setUpDownGPIOs(1 - int(self.inverted), int(self.inverted))

    def stop(self):
        self.setUpDownGPIOs(1 - int(self.inverted), 1 - int(self.inverted))

    def up(self):
        self.setUpDownGPIOs(int(self.inverted), 1 - int(self.inverted))

    def setUpDownGPIOs(self, upBit, downBit):
        self.upGPIO.value(upBit)
        self.downGPIO.value(downBit)
