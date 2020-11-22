from machine import Pin
from utime import sleep_us, ticks_us
from deskHeightSensor import DeskHeightSensor


class UltrasonicDeskHeightSensor(DeskHeightSensor):
    TRIGGER_ON_DURATION_IN_MS = 10
    TRIGGER_OFF_DURATION_IN_MS = 2
    RETRY_COUNT = 100

    def __init__(self, sensorConfig):
        super().__init__()

        self.triggerPin = Pin(sensorConfig.getTriggerPin(), Pin.OUT)
        self.echoPin = Pin(sensorConfig.getEchoPin(), Pin.IN)

    def getCurrentCentimeters(self):
        self.triggerPin.off()

        sleep_us(self.TRIGGER_OFF_DURATION_IN_MS)
        self.triggerPin.on()

        sleep_us(self.TRIGGER_ON_DURATION_IN_MS)
        self.triggerPin.off()

        retryCount = 0
        while self.echoPin.value() == 0:
            if retryCount >= self.RETRY_COUNT:
                return -1
            retryCount += 1

        retryCount = 0
        t1 = ticks_us()
        while self.echoPin.value() == 1:
            if retryCount >= self.RETRY_COUNT:
                return -1
            retryCount += 1

        t2 = ticks_us()
        return UltrasonicDeskHeightSensor.getMicrosecondsInCentimeters(t2 - t1)

    '''
    Sound travels at 343 m/s --> 29 microseconds/cm
    Multiplied by two as the sound travel downward then upward
    '''
    @staticmethod
    def getMicrosecondsInCentimeters(microseconds):
        return microseconds / 58
