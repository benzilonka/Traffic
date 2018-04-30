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

# TODO: Need to add list of lanes as an argument
def getVehicleLane(vehicle):
    lane = ""
    x_loc = vehicle['bounding_box'][0]
    if 49 <= x_loc <= 60:
        lane = "right"
    elif 38 <= x_loc < 49:
        lane = "forward"
    elif 27 <= x_loc < 38:
        lane = "left"
    return lane

# TODO: Need to add list of lanes as an argument
def isVehiclePassedInRedLight(frames, stopLine):
    for frameIdx, frame in enumerate(frames):
        vehicles = frame['objects']
        for idx, current_vehicle in enumerate(vehicles):
            vehicles[idx]['passedInRedLight'] = False
            y_loc = current_vehicle['bounding_box'][1]
            vehicleLane = getVehicleLane(current_vehicle)
            if frame['light_status'][vehicleLane] == "red" and stopLine < y_loc:
                # We don't have any info before the first frame and before there was data on the current vehicle
                if frameIdx >= 1 and idx < len(frames[frameIdx-1]['objects']):
                    # If in the frame before (~0.06 sec before) the light was red too and the vehicle located before
                    # the stop line, then the vehicle passed in red light and we'll mark it
                    prev_y_loc = frames[frameIdx-1]['objects'][idx]['bounding_box'][1]
                    if frames[frameIdx-1]['light_status'][vehicleLane] == "red" and stopLine >= prev_y_loc:
                        vehicles[idx]['passedInRedLight'] = True
    return frames


def searchRedLight(frames):
    lst = []
    for idx, frame in enumerate(frames):
        vehicles = frame['objects']
        for current_vehicle in vehicles:
            if current_vehicle['passedInRedLight'] == True:
                lst.append([idx, current_vehicle['tracking_id']])
    return lst



"""frames = [{"frame_index": 0, "light_status": {"right": "red", "forward": "red", "left": "red"}, "objects": []} \
    ,{"frame_index": 1, "light_status": {"right": "red", "forward": "red", "left": "red"}, "objects": []} \
    ,{"frame_index": 2, "light_status": {"right": "red", "forward": "red", "left": "red"}, "objects": [{"speed": 0.0, "alert_tags": [], "bounding_box": [53.875, 737.55, 0, 0], "confidence": 1.0, "times_lost_by_convnet": 0, "type": "DEFAULT_VEHTYPE", "created_at": "2018-04-29 18:01:26.250089", "tracking_id": 1}]} \
    ,{"frame_index": 3, "light_status": {"right": "red", "forward": "red", "left": "red"}, "objects": [{"speed": 2.54, "alert_tags": [], "bounding_box": [52.32500000000016, 749.5242857142857, 0, 0], "confidence": 1.0, "times_lost_by_convnet": 0, "type": "DEFAULT_VEHTYPE", "created_at": "2018-04-29 18:01:26.250089", "tracking_id": 1}]} \
    ,{"frame_index": 4, "light_status": {"right": "red", "forward": "red", "left": "red"}, "objects": [{"speed": 4.37, "alert_tags": [], "bounding_box": [52.32500000000016, 770.1257142857144, 0, 0], "confidence": 1.0, "times_lost_by_convnet": 0, "type": "DEFAULT_VEHTYPE", "created_at": "2018-04-29 18:01:26.250089", "tracking_id": 1}, {"speed": 0.0, "alert_tags": [], "bounding_box": [53.875, 1296.9, 0, 0], "confidence": 1.0, "times_lost_by_convnet": 0, "type": "DEFAULT_VEHTYPE", "created_at": "2018-04-29 18:01:26.250089", "tracking_id": 2}]} \
    ,{"frame_index": 5, "light_status": {"right": "red", "forward": "red", "left": "red"}, "objects": [{"speed": 6.65, "alert_tags": [], "bounding_box": [40.77499999999992, 801.522857142857, 0, 0], "confidence": 1.0, "times_lost_by_convnet": 0, "type": "DEFAULT_VEHTYPE", "created_at": "2018-04-29 18:01:26.250089", "tracking_id": 1}, {"speed": 1.63, "alert_tags": [], "bounding_box": [52.32500000000016, 1304.584285714286, 0, 0], "confidence": 1.0, "times_lost_by_convnet": 0, "type": "DEFAULT_VEHTYPE", "created_at": "2018-04-29 18:01:26.250089", "tracking_id": 2}]} \
    ,{"frame_index": 6, "light_status": {"right": "red", "forward": "red", "left": "red"}, "objects": [{"speed": 8.28, "alert_tags": [], "bounding_box": [40.77499999999992, 840.5571428571429, 0, 0], "confidence": 1.0, "times_lost_by_convnet": 0, "type": "DEFAULT_VEHTYPE", "created_at": "2018-04-29 18:01:26.251089", "tracking_id": 1}, {"speed": 3.26, "alert_tags": [], "bounding_box": [40.77499999999992, 1319.9528571428573, 0, 0], "confidence": 1.0, "times_lost_by_convnet": 0, "type": "DEFAULT_VEHTYPE", "created_at": "2018-04-29 18:01:26.251089", "tracking_id": 2}]} \
    ,{"frame_index": 7, "light_status": {"right": "red", "forward": "red", "left": "red"}, "objects": [{"speed": 10.3, "alert_tags": [], "bounding_box": [40.77499999999992, 889.1142857142859, 0, 0], "confidence": 1.0, "times_lost_by_convnet": 0, "type": "DEFAULT_VEHTYPE", "created_at": "2018-04-29 18:01:26.251089", "tracking_id": 1}]} \
    ,{"frame_index": 8, "light_status": {"right": "red", "forward": "red", "left": "red"}, "objects": [{"speed": 9.97, "alert_tags": [], "bounding_box": [40.77499999999992, 936.1157142857143, 0, 0], "confidence": 1.0, "times_lost_by_convnet": 0, "type": "DEFAULT_VEHTYPE", "created_at": "2018-04-29 18:01:26.251089", "tracking_id": 1}, {"speed": 0.0, "alert_tags": [], "bounding_box": [53.875, 24.0428571428572, 0, 0], "confidence": 1.0, "times_lost_by_convnet": 0, "type": "DEFAULT_VEHTYPE", "created_at": "2018-04-29 18:01:26.252089", "tracking_id": 4}]} \
    ,{"frame_index": 9, "light_status": {"right": "red", "forward": "red", "left": "red"}, "objects": [{"speed": 10.71, "alert_tags": [], "bounding_box": [40.77499999999992, 986.6057142857142, 0, 0], "confidence": 1.0, "times_lost_by_convnet": 0, "type": "DEFAULT_VEHTYPE", "created_at": "2018-04-29 18:01:26.252089", "tracking_id": 1}, {"speed": 2.54, "alert_tags": [], "bounding_box": [53.875, 36.017142857142744, 0, 0], "confidence": 1.0, "times_lost_by_convnet": 0, "type": "DEFAULT_VEHTYPE", "created_at": "2018-04-29 18:01:26.252089", "tracking_id": 4}]}]

frames = isVehiclePassedInRedLight(frames, 900)

print(searchRedLight(frames))"""

