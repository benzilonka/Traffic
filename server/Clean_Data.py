import json
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter


def get_array(param):
    ans = [[], []]
    for i in range(0, len(param[1])):
        coordinates = param[1][i]
        ans[0].append(coordinates[0])
        ans[1].append(coordinates[1])
    return ans


def clean_routs(hash_vehicles):
    while hash_vehicles.__len__() > 0:
        array = get_array(hash_vehicles.popitem())
        x = array[0]
        y = array[1]

    return hash_vehicles


def clean_routs_jsons(hash_vehicles, jsons):
    list_index_hash_vehicles = []
    for json in jsons:
        objects = json['objects']
        for i in range(0, len(objects)):
            vehicle = objects[i]
            vehicle_id = int(vehicle['tracking_id'])
            if not list_index_hash_vehicles.__contains__(vehicle_id):
                list_index_hash_vehicles[vehicle_id] = 0
            vehicle_list = hash_vehicles[vehicle_id]
            vehicle_index_count = list_index_hash_vehicles[vehicle_id]
            vehicle['bounding_box'][0] = vehicle_list[vehicle_index_count]['y']
            vehicle['bounding_box'][1] = vehicle_list[vehicle_index_count]['x']
            list_index_hash_vehicles[vehicle_id] += 1
    return jsons


def clean(data):
    jsons = data.replace("'", '"').replace("False", "false").replace("True", "true").split("\n")
    hash_vehicles = {}
    vehiclesSpeed = {}
    # Extract path for each vehicle by collecting location per frame from the current JSON file
    for frame in jsons:
        try:
            json_frame = json.loads(frame)
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            pass
        objects = json_frame['objects']
        # Extract location and speed of each vehicle in the current frame
        for i in range(0, len(objects)):
            vehicle = objects[i]
            vehicle_id = int(vehicle['tracking_id'])
            coordinates = [[], []]
            if not hash_vehicles.__contains__(vehicle_id):
                hash_vehicles[vehicle_id] = list()
            if not vehiclesSpeed.__contains__(vehicle_id):
                vehiclesSpeed[vehicle_id] = list()
            coordinates[0] = vehicle['bounding_box'][0]
            coordinates[1] = vehicle['bounding_box'][1]
            hash_vehicles[vehicle_id].append(coordinates)
            vehiclesSpeed[vehicle_id].append(vehicle['speed'])

    #hash_vehicles = clean_routs(hash_vehicles)
    hash_vehicles, vehiclesSpeed = normalizeData(hash_vehicles, vehiclesSpeed)
    jsons = updateJson(jsons, hash_vehicles, vehiclesSpeed)
    return jsons

def updateJson(jsonFile, vehiclesPath, vehiclesSpeed):
    # Pass through all the frames in order to update them
    json_to_ret = []
    for frame in jsonFile:
        try:
            jsonFrame = json.loads(frame)
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            pass
        objects = jsonFrame['objects']
        # Update location and speed of each vehicle in the current frame
        vehicles = []
        for i in range(0, len(objects)):
            vehicle = objects[i]
            vehicle_id = int(vehicle['tracking_id'])
            currentVehiclePath = vehiclesPath[vehicle_id]
            currentVehicleSpeeds = vehiclesSpeed[vehicle_id]
            if currentVehiclePath != None:
                modifiedLocation = currentVehiclePath.pop(0)
                vehicle['bounding_box'][0] = modifiedLocation[0]
                vehicle['bounding_box'][1] = modifiedLocation[1]
            if currentVehicleSpeeds != None:
                modifiedSpeed = currentVehicleSpeeds.pop(0)
                vehicle['speed'] = modifiedSpeed
            vehicles.append(vehicle)
        jsonFrame['objects'] = vehicles
        json_to_ret.append(jsonFrame)

    return json_to_ret

def normalizeData(vehiclesPath, vehiclesSpeed):
    # Fix and handle locations of vehicles from given data
    for path in vehiclesPath:
        start_location = vehiclesPath[path][0]
        end_location = vehiclesPath[path][len(vehiclesPath[path])-1]

        # First Stage:
        #   We'll check that every location is in the range in x axis and in y axis
        #   between the start and end location and then change locations that doesn't satisfies that
        #   We'll change these locations to the boundaries. Which means: to max value if bigger or to
        #   min value if smaller. Do it whether in x/y axis or in both axes
        for location in vehiclesPath[path]:
            location[0] = checkInRangeAndFit(start_location[0], end_location[0], location[0])
            location[1] = checkInRangeAndFit(start_location[1], end_location[1], location[1])

        # Second Stage:
        #   We'll check(and fix if needed) that the vehicle movement is linear. Which means that if in x/y axis we start
        #   in high number and end in lower number, the numbers should be going down all the way or vice versa.
        vehiclesPath[path] = linearMovement(start_location, end_location, vehiclesPath[path])

        # Third Stage:
        #   Smooth the locations in current path
        vehiclesPath[path] = smoothData(vehiclesPath[path])

    # Fix and handle speeds of vehicles from given data
        #for vehicle in vehiclesSpeed:
        # Fourth Stage:
        #   We'll fix logically impossible high sampled speeds.
        index = 0
        for speed in vehiclesSpeed[path]:
            normalizedSpeed = checkForLegalSpeedAndFit(speed)
            vehiclesSpeed[path][index] = normalizedSpeed
            index += 1

        # Fifth Stage:
        #   We'll check that the difference in speed between two consecutive frames is logical and fix if needed
        vehiclesSpeed[path] = checkForLegalDifferSpeed(vehiclesSpeed[path], vehiclesPath[path])
    return vehiclesPath, vehiclesSpeed

def smoothData(path):
    points = np.array(path)
    numOfPoints = len(path)
    threshold = 15
    polynomialDeg = 4

    # get x and y vectors
    x = points[:, 0]
    y = points[:, 1]
    # Number of points is big enough so the filter affect will be seen while using 4th deg polynomial
    if numOfPoints > threshold:
        numOfPoints = int(numOfPoints/2)
    # this param in savgol_filter has to be a positive odd number
    if numOfPoints % 2 == 0:
        numOfPoints -= 1

    # smooth the path using Savitzky–Golay filter using 4th degree polynomial
    x_new = savgol_filter(x, numOfPoints, polynomialDeg)
    y_new = savgol_filter(y, numOfPoints, polynomialDeg)

    """plt.subplot(211)
    plt.plot(x, 'o', x_new)
    plt.title('Polynomial Fit X with Matplotlib')

    plt.subplot(212)
    plt.plot(y, 'o', y_new)
    plt.title('Polynomial Fit Y with Matplotlib')

    plt.show()"""
    result = []
    for i in range(0, len(x_new)):
        result.append([x_new[i], y_new[i]])
    return result

# Calculate the distance between two locations using Pythagorean Theorem
def calcDistance(startLocation, endLocation):
    xDistance = abs(endLocation[0] - startLocation[0])
    yDistance = abs(endLocation[1] - startLocation[1])
    return math.sqrt(xDistance**2 + yDistance**2)

def checkForLegalDifferSpeed(vehicleSpeedList, vehiclePath):
    # delta(time) = 1/15 second = 66.66666666666667 milliseconds (according to 15 fps)
    deltaTime = 1/15
    index = 0
    while index < len(vehiclePath)-1:
        distance = calcDistance(vehiclePath[index], vehiclePath[index+1])
        suggestedVelocity = distance/deltaTime
        fittedVelocity = checkForLegalSpeedAndFit(suggestedVelocity)
        vehicleSpeedList[index] = fittedVelocity
        index += 1
    return vehicleSpeedList

def checkForLegalSpeedAndFit(currentSpeed):
    # max speed is in km/h
    maxSpeed = 120.0
    # max legal speed is in m/s
    maxLegalSpeedPerSec = maxSpeed/3.6
    if currentSpeed > maxLegalSpeedPerSec:
        currentSpeed = maxLegalSpeedPerSec
    return currentSpeed

def checkInRangeAndFit(start, end, currentLocation):
    # check x/y axis
    newLocation = currentLocation
    if not (start <= currentLocation <= end or end <= currentLocation <= start):
        # anomaly detected
        if currentLocation > start:
            if end > start:
                newLocation = end
            else:
                newLocation = start
        else:
            if end > start:
                newLocation = start
            else:
                newLocation = end
    return newLocation

def linearMovement(start, end, path):
    index = 1
    if len(path) < 2:
        return path
    # check if the movement is from higher to lower numbers or vice versa
    directionX = checkForDirection(start, end, 0)
    directionY = checkForDirection(start, end, 1)
    if directionX == "unknown" or directionY == "unknown":
        if directionX == "unknown" and directionY == "unknown":
            for i in range(index, len(path)-1):
                path[i] = path[i-1]
        elif directionX == "unknown" and not (directionY == "unknown"):
            for i in range(index, len(path)-1):
                path[i][0] = path[i-1][0]
        else:
            for i in range(index, len(path)-1):
                path[i][1] = path[i-1][1]
    else:
        path = linearMovementHelper(directionX, directionY, path, index)
    return path

def linearMovementHelper(directionX, directionY, path, index):
    # No need to change start and end locations
    while index < len(path)-1:
        # if isOK = True, move to the next index else 'fix' the location in index+1
        isOkX = checkIfLinear(path[index], path[index+1], directionX, 0)
        if not isOkX:
            path[index+1][0] =  path[index][0]
        isOkY = checkIfLinear(path[index], path[index+1], directionY, 1)
        if not isOkY:
            path[index+1][1] =  path[index][1]
        index += 1
    return path

def checkForDirection(locFrom, locTo, xORy):
    direction = "unknown"
    if locFrom[xORy] > locTo[xORy]:
        direction = "down"
    elif locFrom[xORy] < locTo[xORy]:
        direction = "up"
    # else there is no difference between the locations
    return direction

def checkIfLinear(locFrom, locTo, direction, xORy):
    ans = True
    if direction == "up":
        if locFrom[xORy] > locTo[xORy]:
            ans = False
    else: # direction = down
        if locTo[xORy] > locFrom[xORy]:
            ans = False
    return ans
