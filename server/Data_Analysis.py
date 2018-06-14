import json
import sys

import Parser


def add_alerts(frame, prev_frame, lane_ratio, direction, ver_or_hor, stop_line, lanes, sumo_flag):
    add_ttc_tti(frame, lane_ratio, stop_line)
    add_zigzag_count(frame, prev_frame, direction, ver_or_hor)
    if sumo_flag:
        is_vehicle_passed_in_red_light(frame, prev_frame, stop_line, lanes)


def calc_tti(vehicle, stop_line, lane_ratio):
    if vehicle['bounding_box'][1] > stop_line or vehicle['speed'] == 0:
        return -1
    return (stop_line - vehicle['bounding_box'][1]) / (vehicle['speed'] * lane_ratio)


def add_ttc_tti(frame, lane_ratio, stop_line):
    vehicles = frame['objects']
    i = 0
    for vehicle in vehicles:
        frame['objects'][i]['distance'] = get_distance(vehicle, vehicles)
        frame['objects'][i]['ttc'] = calc_ttc(vehicle, vehicles, lane_ratio)
        frame['objects'][i]['tti'] = calc_tti(vehicle, stop_line, lane_ratio)
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


def get_vehicle_by_id(frame):
    vehicles = frame['objects']
    ans = {}
    for vehicle in vehicles:
        ans[vehicle['tracking_id']] = vehicle
    return ans


def is_vehicle_passed_in_red_light(frame, prev_frame, stop_line, lanes):
    prev_vehicles = {}
    vehicles = get_vehicle_by_id(frame)
    if prev_frame is not None:
        prev_vehicles = get_vehicle_by_id(prev_frame)
    for idx in vehicles.keys():
        vehicles[idx]['passed_in_red'] = False
        current_vehicle = vehicles[idx]
        y_loc = current_vehicle['bounding_box'][1]
        vehicleLane = get_vehicle_lane(current_vehicle, lanes)
        if vehicleLane != "" and frame["light_status"][vehicleLane] == "red" and stop_line < y_loc:
            # We don't have any info before the first frame and before there was data on the current vehicle
            if prev_frame is not None and idx in prev_vehicles.keys():
                # If in the frame before (~0.06 sec before) the light was red too and the vehicle located before
                # the stop line, then the vehicle passed in red light and we'll mark it
                prev_y_loc = prev_vehicles[idx]['bounding_box'][1]
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


def get_final_report(vehicle_info, report, car_count, bus_count, truck_count, length):
    vehicle_num = len(vehicle_info)
    report['num_of_cars'] = vehicle_num
    report['car_distribution'] = car_count / vehicle_num
    report['bus_distribution'] = bus_count / vehicle_num
    report['truck_distribution'] = truck_count / vehicle_num
    speed_sum = 0
    ttc_sum = 0
    ttc_count = 0
    zigzag_sum = 0
    for vid in vehicle_info.keys():
        speed_sum += vehicle_info[vid]['average_speed']
        zigzag_sum += vehicle_info[vid]['zigzag_count']
        if vehicle_info[vid]['average_ttc'] != 0:
            ttc_sum += vehicle_info[vid]['average_ttc']
            ttc_count += 1
    report['average_speed'] = speed_sum / vehicle_num
    if ttc_count == 0:
        report['average_ttc'] = None
    else:
        report['average_ttc'] = ttc_sum / ttc_count
    report['ttc_count'] = ttc_count
    report['average_zigzag'] = zigzag_sum / vehicle_num
    report['zigzag_per_second'] = zigzag_sum / length
    report['car_pre_second'] = vehicle_num / length
    report['vehicle_info'] = vehicle_info
    return report


def get_statistic_report(frames):
    vehicle_info = {}
    report = {'num_of_cars': 0, 'car_pre_second': 0, 'max_speed': -sys.maxsize, 'min_ttc': sys.maxsize, 'ttc_count': 0,
              'average_speed': 0, 'average_ttc': 0, "average_zigzag": 0, 'max_zigzag': 0, 'zigzag_per_second': 0,
              'red_cross_count': None, 'against_direction_count': 0, 'car_distribution': 0, 'bus_distribution': 0,
              'truck_distribution': 0, 'vehicle_info': []}
    car_count = 0
    bus_count = 0
    truck_count = 0
    red_cross_count = -1
    against_direction_count = 0
    vehicle_map = {"car": -1, "bus": 0, "truck": 1}
    for frame in frames:
        for vehicle in frame['objects']:
            report['max_speed'] = max(vehicle['speed'], report['max_speed'])
            ttc = 0
            ttc_holder = sys.maxsize
            ttc_count = 0
            if vehicle['ttc'] != -1:
                ttc_holder = vehicle['ttc']
                ttc = ttc_holder
                ttc_count = 1
            report['min_ttc'] = min(ttc_holder, report['min_ttc'])
            report['max_zigzag'] = max(vehicle['change_lane_count'], report['max_zigzag'])
            vid = vehicle['tracking_id']
            if vid not in vehicle_info.keys():
                vehicle_info[vid] = {'vehicle_id': vid, 'average_speed': vehicle['speed'], 'appearances': 1,
                                     'average_ttc': ttc, 'ttc_count': ttc_count, 'zigzag_count': 0}
                vehicle_type = vehicle_map[vehicle['type']]
                car_count += (0.5 * ((vehicle_type ** 2) - vehicle_type))
                bus_count += (-(vehicle_type ** 2) + 1)
                truck_count += (0.5 * ((vehicle_type ** 2) + vehicle_type))
            else:
                average_ttc = vehicle_info[vid]['average_ttc'] * vehicle_info[vid]['ttc_count']
                average_ttc += ttc
                vehicle_info[vid]['ttc_count'] += ttc_count
                vehicle_info[vid]['average_ttc'] = average_ttc / max(vehicle_info[vid]['ttc_count'], 1)
                average_speed = vehicle_info[vid]['average_speed'] * vehicle_info[vid]['appearances']
                average_speed += vehicle['speed']
                vehicle_info[vid]['appearances'] += 1
                vehicle_info[vid]['average_speed'] = average_speed / vehicle_info[vid]['appearances']
                vehicle_info[vid]['zigzag_count'] = vehicle['change_lane_count']
                if 'passed_in_red' in vehicle.keys() and vehicle['passed_in_red']:
                    if red_cross_count == -1:
                        red_cross_count = 0
                    red_cross_count += 1
                if 'against_direction_flag' in vehicle.keys() and vehicle['against_direction_flag']:
                    against_direction_count += 1
    if red_cross_count != -1:
        report['red_cross_count'] = red_cross_count
    report['against_direction_count'] = against_direction_count
    return get_final_report(vehicle_info, report, car_count, bus_count, truck_count, len(frames))



# with open("dataset_0.json", 'r') as input:
#    print(get_statistic_report(json.loads(input.read().replace("'", '"').replace("False", "false").replace("True", "true"))))