import Parser


def add_pre_alerts(frame):
    addTTC(frame)


def add_post_alerts(frames, direction, per_or_hor):
    pass


def addTTC(frame):
    vehicles = frame['objects']
    i = 0
    for vehicle in vehicles:
        frame['objects'][i]['distance'] = getDistance(vehicle, vehicles)
        frame['objects'][i]['ttc'] = calcTTC(vehicle, vehicles)
        i = i + 1
    return frame


def add_change_lane_count_field(frames):
    for frame in frames:
        vehicles = frame['objects']
        for vehicle in vehicles:
            vehicle["change_lane_count"] = 0
            vehicle["against_direction_flag"] = False


def add_zigzag_count(frames, direction, per_or_hor):
    add_change_lane_count_field(frames)
    for i in range(1, len(frames)):
        for current_vehicle in frames[i]['objects']:
            for prev_vehicle in frames[i - 1]['objects']:
                if current_vehicle['tracking_id'] == prev_vehicle['tracking_id']:
                    current_vehicle["change_lane_count"] = prev_vehicle["change_lane_count"]
                    curr_pos = current_vehicle['bounding_box'][per_or_hor]
                    prev_pos = prev_vehicle['bounding_box'][per_or_hor]
                    if curr_pos != prev_pos:
                        current_vehicle["change_lane_count"] += 1
                    curr_pos = current_vehicle['bounding_box'][1-per_or_hor]
                    prev_pos = prev_vehicle['bounding_box'][1-per_or_hor]
                    if curr_pos * direction < prev_pos * direction:
                        current_vehicle["against_direction_flag"] = True


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
