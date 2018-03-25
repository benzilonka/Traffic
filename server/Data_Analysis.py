import Parser


def addTTC(frame):
    vehicles = frame['objects']

    i = 0
    for vehicle in vehicles:
        frame['objects'][i]['distance'] = getDistance(vehicle, vehicles)
        frame['objects'][i]['ttc'] = calcTTC(vehicle, vehicles)
        i = i + 1

    return frame

def calcTTC(vehicle, vehicles):
    if vehicle['speed'] == 0:
        return -1
    distance = getDistance(vehicle, vehicles)
    if distance <= 0:
        return -1
    ttc = distance / vehicle['speed']
    if ttc > Parser.MAX_TTC:
        return -1
    return ttc

def getDistance(vehicle, vehicles):
    y = Parser.RECT_HEIGHT
    for v in vehicles:
        if v['bounding_box'] != vehicle['bounding_box']:
            if areInSameLane(vehicle['bounding_box'][0], v['bounding_box'][0]):
                if y > v['bounding_box'][1] and vehicle['bounding_box'][1] < v['bounding_box'][1]:
                    y = v['bounding_box'][1]
    if y == Parser.RECT_HEIGHT:
        return 0
    return (y - vehicle['bounding_box'][1]) / Parser.PIXEL_PER_METER


def areInSameLane(x1, x2):
    return int(int(x1) / Parser.LANE_WIDTH) == int(int(x2) / Parser.LANE_WIDTH)