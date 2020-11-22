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

        self.checksCompleted = 0
        self.state = RollingAverageState(config.getRollingWindowSize(), config.getAllowableMeasurementErrorRatio(), config.getConsecutiveErrorsUntilRestart())

        self.measurementDeltaInMicroseconds = config.getMeasurementDeltaInMicroseconds()
        self.errorInCentimeters = config.getAllowableErrorInCentimeters()
        self.numChecksRequired = config.getNumHeightChecksRequired()

        self.targetHeight = -1

    # Refactor just to return the current height, best guess
    def getCurrentHeight(self):
        while True:
            measurement = self.sensor.getCurrentCentimeters()
            if measurement != -1:
                self.state.addMeasurement(measurement)

            if self.state.isFull():
                return self.state.getCurrentRollingAverage()

            sleep_us(self.measurementDeltaInMicroseconds)

    def updateTargetHeight(self, height):

        # This should be moved to be set together
        self.checksCompleted = 0
        self.state.reset()

        while True:
            val = self.adjust(height)
            if val != -1:
                return val

    def adjust(self, height):
        measurement = self.sensor.getCurrentCentimeters()
        sleep_us(int(self.measurementDeltaInMicroseconds/6))
        if measurement != -1:
            self.state.addMeasurement(measurement)

        if self.state.isFull():
            print("Here1")
            currentValue = self.state.getCurrentRollingAverage()
            if currentValue <= height + self.errorInCentimeters and currentValue > height - self.errorInCentimeters:
                print("Here1.1")
                self.stop()
                self.state.reset()

                self.checksCompleted += 1
                print(self.checksCompleted)
                print(self.numChecksRequired)
                if self.checksCompleted == self.numChecksRequired:
                    return currentValue
            elif currentValue < height - self.errorInCentimeters:
                print("Here2")
                self.up()
            elif currentValue > height + self.errorInCentimeters:
                print("Here3")
                self.down()

        return -1

    def down(self):
        self.setUpDownGPIOs(1 - int(self.inverted), int(self.inverted))

    def stop(self):
        self.setUpDownGPIOs(1 - int(self.inverted), 1 - int(self.inverted))

    def up(self):
        self.setUpDownGPIOs(int(self.inverted), 1 - int(self.inverted))

    def setUpDownGPIOs(self, upBit, downBit):
        self.upGPIO.value(upBit)
        self.downGPIO.value(downBit)
