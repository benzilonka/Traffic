import math
import random
import numpy

e = 2.71828182846
def get_first_frame():
    return {'frame_index': 0, 'objects': []}


def add_car(frame, lane):
    """object = {'speed': 0, 'new': False, 'alert_tags': [], 'static': False, 'bounding_box': [0, 0, 0, 0], 'confidence': 1.0,
              'times_lost_by_convnet': 0, 'type': 'car', 'created_at': '2017-12-25 16:05:01.223143', 'lost': False,
              'tracking_id': 10000, 'counted': False}

              lane is an object containing four points of the lane
              """
    vehicleList = frame['objects']
    if len(vehicleList) > 0:
        biggestTrackingID = vehicleList[len(vehicleList) - 1]['tracking_id']
        newTrackingID = biggestTrackingID + 1
    else:
        newTrackingID = 1
    newType = genTypeOfVehicle()
    newSpeed = genNewSpeed(newType)
    newBBox = genBoundingBox(lane)

    vehicleList.append({'speed': newSpeed, 'new': True, 'alert_tags': [], 'static': False, \
                                     'bounding_box': newBBox, 'confidence': 1.0, \
                                     'times_lost_by_convnet': 0, 'type': newType, \
                                     'created_at': '2017-12-25 16:05:01.223143', 'lost': False, \
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

def get_frame(current_frame, lane, light, traffic_density):
    # x = (pow(traffic_density, 3) * pow(e, (-1 * traffic_density)))/6
    x = random.uniform(0, 1)
    frame_index = current_frame['frame_index']
    frame_index += 1
    ans = {'frame_index': frame_index, 'objects': []}
    if x >= traffic_density:
        #ans = add_car(ans, lane[int(random.uniform(0, len(lane)))])
        ans = add_car(ans, lane)
    return ans

get_frame({'frame_index': 0, 'objects': []}, [[500,250], [600,250], [400,0], [500,0]], 0, 0)