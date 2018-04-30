import Parser


def add_pre_alerts(frame, lane_ratio):
    return addTTC(frame, lane_ratio)


def add_post_alerts(frames, direction, per_or_hor):
    add_zigzag_count(frames, direction, per_or_hor)


def addTTC(frame, lane_ratio):
    vehicles = frame['objects']
    i = 0
    for vehicle in vehicles:
        frame['objects'][i]['distance'] = getDistance(vehicle, vehicles)
        frame['objects'][i]['ttc'] = calcTTC(vehicle, vehicles, lane_ratio)
        i = i + 1
    return frame


def add_fields(frames):
    for frame in frames:
        vehicles = frame['objects']
        for vehicle in vehicles:
            vehicle["change_lane_count"] = 0
            vehicle["against_direction_flag"] = False


def add_zigzag_count(frames, direction, per_or_hor):
    add_fields(frames)
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


def calcTTC(vehicle, vehicles, lane_ratio):
    if vehicle['speed'] == 0:
        return -1
    distance_and_speed = get_distance_and_speed(vehicle, vehicles)
    if distance_and_speed[0] <= 0:
        return -1
    if vehicle['speed'] == 0 or vehicle['speed'] == distance_and_speed[1]:
        return -1
    else:
        ttc = float(distance_and_speed[0] / ((distance_and_speed[1] * lane_ratio) - (vehicle['speed'] * lane_ratio)))
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


def get_distance_and_speed(vehicle, vehicles):
    y = Parser.RECT_HEIGHT
    speed = 0
    for v in vehicles:
        if v['bounding_box'] != vehicle['bounding_box']:
            if areInSameLane(vehicle['bounding_box'][0], v['bounding_box'][0]):
                if y > v['bounding_box'][1] > vehicle['bounding_box'][1]:
                    y = v['bounding_box'][1]
                    speed = v['speed']
    if y == Parser.RECT_HEIGHT:
        return [0, speed]
    return [(y - vehicle['bounding_box'][1]) / Parser.PIXEL_PER_METER, speed]


def areInSameLane(x1, x2):
    return int(int(x1) / Parser.LANE_WIDTH) == int(int(x2) / Parser.LANE_WIDTH)
