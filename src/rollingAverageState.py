from collections import deque


class RollingAverageState(object):
    def __init__(self, maxRollingAverageSize, percentError, maxConsecutiveErrors):
        super().__init__()
        self.maxRollingAverageSize = maxRollingAverageSize
        self.percentError = percentError
        self.maxConsecutiveErrors = maxConsecutiveErrors

        self.resetState()

    def getCurrentRollingAverage(self):
        valuesSize = len(self.values)
        if valuesSize == 0:
            return None

        return self.rollingAverageSum/valuesSize

    def resetState(self):
        self.values = deque((), self.maxRollingAverageSize)
        self.rollingAverageSum = 0
        self.consecutiveUnstableValues = 0

    def addMeasurement(self, value):
        if not self.withinErrorDelta(value):
            self.recordError()
            return
        self.clearErrors()

        if len(self.values) >= self.maxRollingAverageSize:
            self.rollingAverageSum -= self.values.popleft()

        self.values.append(value)
        self.rollingAverageSum += value

    def isFull(self):
        return len(self.values) == self.maxRollingAverageSize

    def withinErrorDelta(self, value):
        rollingAverage = self.getCurrentRollingAverage()
        if rollingAverage is None:
            return True
        return abs(value - rollingAverage) <= self.getErrorDelta()

    def recordError(self):
        self.consecutiveUnstableValues += 1

        if self.consecutiveUnstableValues > self.maxConsecutiveErrors:
            self.resetState()

    def clearErrors(self):
        self.consecutiveUnstableValues = 0

    def getErrorDelta(self):
        value = self.getCurrentRollingAverage()
        if value is not None:
            return value*self.percentError

        return None