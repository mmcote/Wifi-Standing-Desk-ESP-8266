import usocket as socket
import ure
from config import Config
from ultrasonicDeskHeightSensor import UltrasonicSensor
from desk import Desk


def sendResponse(statusCode, responseDict):
    conn.send('HTTP/1.1 {} \n'.format(statusCode))
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    for attribute in responseDict.keys():
        conn.send(str(attribute) + ': ' + str(responseDict[attribute]))
    conn.close()

config = Config()
sensor = UltrasonicSensor(config.sensorConfig)
desk = Desk(config.deskConfig, sensor)
desk.stop()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5) # Number of queued connections

while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))

    byteRequest = conn.recv(1024)
    request = byteRequest.decode('utf-16')

    getHeightRequest = request.find('/height')
    toHeightRequest = request.find('/?height')

    statusCode = 200
    responseDict = {}
    if getHeightRequest >= 0:
        responseDict["height"] = str(desk.getCurrentHeight())
    elif toHeightRequest >= 0:
        desk.stop()

        regex = ure.compile("^GET.\/\?height=([0-9]*)")
        matches = regex.match(request)
        if matches is not None:
            height = int(regex.match(request).group(1))
            responseDict["height"] = desk.updateTargetHeight(height)
        else:
            statusCode = 400
            responseDict["error"] = "Unable to process height value."
    else:
        statusCode = 404
        responseDict["error"] = "No endpoint found"

    sendResponse(statusCode, responseDict)
