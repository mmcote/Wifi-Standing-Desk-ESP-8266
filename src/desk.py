from machine import Pin
from utime import sleep_us
from rollingAverageState import RollingAverageState


class Desk(object):
    def __init__(self, config, sensor):
        super().__init__()

        self.upGPIO = Pin(config.getUpPin(), Pin.OUT)
        self.downGPIO = Pin(config.getDownPin(), Pin.OUT)
        self.inverted = config.isInvertedPins()

        self.sensor = sensor

        self.state = RollingAverageState(config.getRollingWindowSize(), config.getAllowableMeasurementErrorRatio(), config.getConsecutiveErrorsUntilRestart())

        self.measurementDeltaInMicroseconds = config.getMeasurementDeltaInMicroseconds()
        self.errorInCentimeters = config.getAllowableErrorInCentimeters()
        self.numChecksRequired = config.getNumHeightChecksRequired()

        self.checksRemaining = 0

    def adjust(self):
        if self.checksRemaining <= 0:
            return

        measurement = self.sensor.getCurrentCentimeters()
        sleep_us(int(self.measurementDeltaInMicroseconds/6))
        if measurement != -1:
            self.state.addMeasurement(measurement)

        if self.state.isFull():
            currentValue = self.state.getCurrentRollingAverage()
            if currentValue <= self.targetHeight + self.errorInCentimeters and currentValue > self.targetHeight - self.errorInCentimeters:
                self.stop()
                self.state.reset()
                self.checksCompleted -= 1
            elif currentValue < self.targetHeight - self.errorInCentimeters:
                self.up()
            elif currentValue > self.targetHeight + self.errorInCentimeters:
                self.down()

    def getHeight(self):
        while True:
            measurement = self.sensor.getCurrentCentimeters()
            if measurement != -1:
                self.state.addMeasurement(measurement)

            if self.state.isFull():
                return self.state.getCurrentRollingAverage()

            sleep_us(self.measurementDeltaInMicroseconds)

    def setTargetHeight(self, height):
        self.checksRemaining = self.numChecksRequired
        self.state.reset()

        self.targetHeight = height

    def cancel(self):
        self.stop()
        self.checksRemaining = 0

    def down(self):
        self.setUpDownGPIOs(1 - int(self.inverted), int(self.inverted))

    def stop(self):
        self.setUpDownGPIOs(1 - int(self.inverted), 1 - int(self.inverted))

    def up(self):
        self.setUpDownGPIOs(int(self.inverted), 1 - int(self.inverted))

    def setUpDownGPIOs(self, upBit, downBit):
        self.upGPIO.value(upBit)
        self.downGPIO.value(downBit)
