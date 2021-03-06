import usocket as socket
import ure
import uselect
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

def handle(conn):
    byteRequest = conn.recv(1024)
    request = byteRequest.decode('utf-16')

    getHeightRequest = request.find('/height')
    setHeightRequest = request.find('?height')
    cancelRequest = request.find('/cancel')

    statusCode = 200
    responseDict = {}
    if getHeightRequest >= 0:
        responseDict["height"] = str(desk.getHeight())
    elif cancelRequest >= 0:
        responseDict["msg"] = "Adjustment Cancelled"
        desk.cancel()
    elif setHeightRequest >= 0:
        desk.stop()

        regex = ure.compile("^GET.\/\?height=([0-9]*)")
        matches = regex.match(request)
        if matches is not None:
            height = int(regex.match(request).group(1))
            responseDict["height"] = height
            desk.setTargetHeight(height)
        else:
            statusCode = 400
            responseDict["error"] = "Unable to process height value."
    else:
        statusCode = 404
        responseDict["error"] = "No endpoint found"

    return statusCode, responseDict

def main():
    config = Config()
    sensor = UltrasonicSensor(config.sensorConfig)
    desk = Desk(config.deskConfig, sensor)
    desk.stop()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    sPoller = uselect.poll()
    sPoller.register(s, uselect.POLLIN)

    while True:
        # Poll every 10 milliseconds for a connection
        res = sPoller.poll(10)
        if res:
            conn, addr = s.accept()
            # print('Got a connection from %s' % str(addr))
            statusCode, response = handle(conn)
            sendResponse(statusCode, response)
        else:
            desk.adjust()

main()