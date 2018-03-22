import math
import random
import numpy
from datetime import datetime

e = 2.71828182846
def get_first_frame():
    return {'frame_index': 0, 'objects': []}

def deleteCars(frame, lane):
    vehicleList = frame['objects']
    index = 0
    while index < len(vehicleList):
        currentBBox = vehicleList[index]['bounding_box']
        # yPosition = BBox[1], lane[3]/lane[4] are locations of the end of the lane
        # Delete locations of vehicles that passed the location of the end of the lane
        if currentBBox[1] < lane[3][1]:
            del(vehicleList[index])
        index += 1
    return frame

def add_car(frame, lane):
    # lane is an object containing four points of the lane
    vehicleList = frame['objects']
    if len(vehicleList) > 0:
        biggestTrackingID = vehicleList[len(vehicleList) - 1]['tracking_id']
        newTrackingID = biggestTrackingID + 1
    else:
        newTrackingID = 1
    newType = genTypeOfVehicle()
    newSpeed = genNewSpeed(newType)
    newBBox = genBoundingBox(lane)
    newDateAndTime = datetime.now()
    fixedDateAndTime = newDateAndTime.strftime('%Y-%m-%d %H:%M:%S.' + str(newDateAndTime.microsecond))

    vehicleList.append({'speed': newSpeed, 'new': True, 'alert_tags': [], 'static': False, \
                                     'bounding_box': newBBox, 'confidence': 1.0, \
                                     'times_lost_by_convnet': 0, 'type': newType, \
                                     'created_at': fixedDateAndTime, 'lost': False, \
                                     'tracking_id': newTrackingID, 'counted': False})
    return frame

def genBoundingBox(laneLocations):
    # X location will be in the middle of the lane
    xPoint = int((laneLocations[0][0] + laneLocations[1][0]) / 2)
    # Y location will be where the lane begin
    yPoint = laneLocations[0][1]
    bbox = [xPoint, yPoint, 0, 0]
    return bbox

def genNewSpeed(typeOfVehicle):
    # Generate vehicle speed in range 10 to 120 km/h with bigger probability to lower speeds (10-70 km/h)
    speed = 0.0
    threshold = 0.0
    if typeOfVehicle == 'car':
        threshold = 0.7
    elif typeOfVehicle == 'bus':
        threshold = 0.8
    else:
        threshold = 0.9
    param = random.uniform(0, 1)
    if param <= threshold:
        # Generate speed in range 10-70
        speed = numpy.random.choice(numpy.arange(10.0, 70.0))
    else:
        # Generate speed in range 71-120
        speed = numpy.random.choice(numpy.arange(71.0, 120.0))
    # Convert speed from km/h to m/s
    speed = speed/3.6
    return speed

def genTypeOfVehicle():
    # There is more probability to generate car over bus and truck
    type = numpy.random.choice(['car', 'bus', 'truck'], p = [0.7, 0.2, 0.1])
    return type

def extractVehiclesPerLane(frame, lanesLst):
    vehicleLst = frame['objects']
    vehiclesPerLane = []
    for lane in lanesLst:
        element = {'lane': lane, 'objects': []}
        for vehicle in vehicleLst:
            bbox = vehicle['bounding_box']
            # Check if vehicle is in the range of the x and y coordinates of current lane
            # lane[0][0]- x in start location , lane[3][0]- x in end location
            # lane[0][1]- y in start location , lane[3][1]- y in end location
            if lane[0][0] <= bbox[0] <= lane[3][0] and lane[3][1] <= bbox[1] <= lane[0][1]:
                element['objects'].append(vehicle)
        #sort vehicles by their y loactions
        notSorted = element['objects']
        element['objects'] = sorted(notSorted, key=helpSorted)
        vehiclesPerLane.append(element)
    return vehiclesPerLane

def helpSorted(vehicle):
    # Compare by y locations
    return vehicle['bounding_box'][1]

def get_frame(current_frame, lanesList, light, traffic_density):
    # x = (pow(traffic_density, 3) * pow(e, (-1 * traffic_density)))/6
    x = random.uniform(0, 1)
    frame_index = current_frame['frame_index']
    frame_index += 1
    ans = {'frame_index': frame_index, 'objects': []}
    if x >= traffic_density:
        ans = add_car(ans, lanesList[int(random.uniform(0, len(lanesList)))])
    ans = deleteCars(ans, lanesList)
    vehiclesInLanesArr = extractVehiclesPerLane(ans, lanesList)
    return ans


"""frame = {'frame_index': 0, 'objects': [{'speed': 21.2, 'new': True, 'alert_tags': [], 'static': False, \
                                     'bounding_box': [400,8,0,0], 'confidence': 1.0, \
                                     'times_lost_by_convnet': 0, 'type': 'car', \
                                     'created_at': '2017-12-25 16:05:01.223143', 'lost': False, \
                                     'tracking_id': 1, 'counted': False}, \
                                      {'speed': 10.2, 'new': True, 'alert_tags': [], 'static': False, \
                                      'bounding_box': [250, 8, 0, 0], 'confidence': 1.0, \
                                      'times_lost_by_convnet': 0, 'type': 'car', \
                                      'created_at': '2017-12-25 16:05:01.223143', 'lost': False, \
                                      'tracking_id': 2, 'counted': False}, \
                                       {'speed': 33.3, 'new': True, 'alert_tags': [], 'static': False, \
                                       'bounding_box': [120, 100, 0, 0], 'confidence': 1.0, \
                                       'times_lost_by_convnet': 0, 'type': 'car', \
                                       'created_at': '2017-12-25 16:05:01.223143', 'lost': False, \
                                       'tracking_id': 4, 'counted': False}, \
                                       {'speed': 9.3, 'new': True, 'alert_tags': [], 'static': False, \
                                       'bounding_box': [101, 132, 0, 0], 'confidence': 1.0, \
                                       'times_lost_by_convnet': 0, 'type': 'car', \
                                       'created_at': '2017-12-25 16:05:01.223143', 'lost': False, \
                                       'tracking_id': 3, 'counted': False}, \
                                       ]}"""

lanesArray = [[[500,250], [600,250], [500,10], [600,10]], \
              [[356, 250], [499, 250], [356, 5], [499, 5]], \
              [[200, 100], [350, 100], [200, 0], [350, 0]], \
              [[100, 200], [199, 200], [100, 100], [199, 100]]]

get_frame({'frame_index': 0, 'objects': []}, lanesArray, 0, 0)
#extractVehiclesPerLane(frame, lanesArray)
