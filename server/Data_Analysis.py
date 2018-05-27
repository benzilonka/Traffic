from . import Parser


def add_alerts(frame, prev_frame, lane_ratio, direction, ver_or_hor, stop_line, lanes, sumo_flag):
    add_ttc(frame, lane_ratio)
    add_zigzag_count(frame, prev_frame, direction, ver_or_hor)
    if sumo_flag:
        is_vehicle_passed_in_red_light(frame, prev_frame, stop_line, lanes)


def add_ttc(frame, lane_ratio):
    vehicles = frame['objects']
    i = 0
    for vehicle in vehicles:
        frame['objects'][i]['distance'] = get_distance(vehicle, vehicles)
        frame['objects'][i]['ttc'] = calc_ttc(vehicle, vehicles, lane_ratio)
        i = i + 1
    return frame


def add_fields(frame):
    vehicles = frame['objects']
    for vehicle in vehicles:
        vehicle["change_lane_count"] = 0
        vehicle["against_direction_flag"] = False


def add_zigzag_count(frame, prev_frame, direction, per_or_hor):
    add_fields(frame)
    if prev_frame is not None:
        for current_vehicle in frame['objects']:
            for prev_vehicle in prev_frame['objects']:
                if current_vehicle['tracking_id'] == prev_vehicle['tracking_id']:
                    current_vehicle["change_lane_count"] = prev_vehicle["change_lane_count"]
                    curr_pos = current_vehicle['bounding_box'][per_or_hor]
                    prev_pos = prev_vehicle['bounding_box'][per_or_hor]
                    if curr_pos != prev_pos:
                        current_vehicle["change_lane_count"] += 1
                    curr_pos = current_vehicle['bounding_box'][1 - per_or_hor]
                    prev_pos = prev_vehicle['bounding_box'][1 - per_or_hor]
                    if curr_pos * direction < prev_pos * direction:
                        current_vehicle["against_direction_flag"] = True
    return frame


def calc_ttc(vehicle, vehicles, lane_ratio):
    if vehicle['speed'] == 0:
        return -1
    distance_and_speed = get_distance_and_speed(vehicle, vehicles)
    if distance_and_speed[0] <= 0:
        return -1
    if vehicle['speed'] == 0 or vehicle['speed'] <= distance_and_speed[1]:
        return -1
    else:
        ttc = float(distance_and_speed[0] / ((vehicle['speed'] * lane_ratio) - (distance_and_speed[1] * lane_ratio)))
    if ttc > Parser.MAX_TTC:
        return -1
    return ttc


def get_distance(vehicle, vehicles):
    y = Parser.RECT_HEIGHT
    for v in vehicles:
        if v['bounding_box'] != vehicle['bounding_box']:
            if are_in_same_lane(vehicle['bounding_box'][0], v['bounding_box'][0]):
                if y > v['bounding_box'][1] > vehicle['bounding_box'][1]:
                    y = v['bounding_box'][1]
    if y == Parser.RECT_HEIGHT:
        return 0
    return (y - vehicle['bounding_box'][1]) / Parser.PIXEL_PER_METER


def get_distance_and_speed(vehicle, vehicles):
    y = Parser.RECT_HEIGHT
    speed = 0
    for v in vehicles:
        if v['bounding_box'] != vehicle['bounding_box']:
            if are_in_same_lane(vehicle['bounding_box'][0], v['bounding_box'][0]):
                if y > v['bounding_box'][1] > vehicle['bounding_box'][1]:
                    y = v['bounding_box'][1]
                    speed = v['speed']
    if y == Parser.RECT_HEIGHT:
        return [0, speed]
    return [(y - vehicle['bounding_box'][1]) / Parser.PIXEL_PER_METER, speed]


def are_in_same_lane(x1, x2):
    return int(int(x1) / Parser.LANE_WIDTH) == int(int(x2) / Parser.LANE_WIDTH)


def get_vehicle_lane(vehicle, lanes):
    lane = ""
    x_loc = vehicle['bounding_box'][0]
    if lanes["right"][0] <= x_loc <= lanes["right"][1]:
        lane = "right"
    elif lanes["forward"][0] <= x_loc < lanes["forward"][1]:
        lane = "forward"
    elif lanes["left"][0] <= x_loc < lanes["left"][1]:
        lane = "left"
    return lane


def is_vehicle_passed_in_red_light(frame, prev_frame, stop_line, lanes):
    vehicles = frame['objects']
    for idx, current_vehicle in enumerate(vehicles):
        vehicles[idx]['passed_in_red'] = False
        y_loc = current_vehicle['bounding_box'][1]
        vehicleLane = get_vehicle_lane(current_vehicle, lanes)
        if vehicleLane != "" and frame["light_status"][vehicleLane] == "red" and stop_line < y_loc:
            # We don't have any info before the first frame and before there was data on the current vehicle
            if prev_frame is not None and idx < len(prev_frame['objects']):
                # If in the frame before (~0.06 sec before) the light was red too and the vehicle located before
                # the stop line, then the vehicle passed in red light and we'll mark it
                prev_y_loc = prev_frame['objects'][idx]['bounding_box'][1]
                if prev_frame['light_status'][vehicleLane] == "red" and stop_line >= prev_y_loc:
                    vehicles[idx]['passed_in_red'] = True
    return frame


def search_red_light(frames):
    lst = []
    for idx, frame in enumerate(frames):
        vehicles = frame['objects']
        for current_vehicle in vehicles:
            if current_vehicle['passed_in_red']:
                lst.append([idx, current_vehicle['tracking_id']])
    return lst
