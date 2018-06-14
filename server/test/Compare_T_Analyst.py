import json
import os
import sys

from scipy._lib.six import reduce
from scipy.spatial import distance

RATIO_X = 1.78082
RATIO_Y = 0.78475
PIXEL_PER_METER = 5


def extract_from_data(directory):
    vehicles = {}
    car_index = 1
    frames = 0
    for filename in os.listdir(directory):
        with open(directory + '\\' + filename, 'r') as vehicle:
            vehicle.readline()
            content = vehicle.readlines()
            vehicles[car_index] = []
            i = -1
            for line in content:
                vehicle_data = line.split("\t")
                speed = 0
                frames = max(frames, int(vehicle_data[0]))
                if float(vehicle_data[1]) > 0:
                    x = (float(vehicle_data[1]) * RATIO_X) + 190
                    if i > -1:
                        speed = max(0, (((x - vehicles[car_index][i][1]) / PIXEL_PER_METER) * 15))
                    vehicles[car_index].append([int(vehicle_data[0]),
                                                (272 - float(vehicle_data[2])) * RATIO_Y, x, speed])
                    i += 1
            car_index += 1
    return vehicles, frames


def convert_to_meta_format(data):
    frames = []
    for i in range(data[1]):
        frame = {'frame_index': i, 'objects': []}
        for car_id in data[0].keys():
            first_index = data[0][car_id][0][0]
            if first_index <= i < (len(data[0][car_id]) + first_index):
                car_frame_info = data[0][car_id][i - first_index]
                car = {'type': 'car', 'tracking_id': car_id, 'bounding_box': [car_frame_info[1], car_frame_info[2]],
                       'speed': car_frame_info[3]}
                frame['objects'].append(car)
        frames.append(frame)
    return frames


def write_to_file(frames):
    with open("t_analyst_out.json", 'w') as outfile:
        outfile.write('[')
        first_flag = False
        for frame in frames:
            if first_flag:
                outfile.write(',')
            first_flag = True
            outfile.write(str(frame))
            outfile.write('\n')
        outfile.write(']')


def convert_to_meta(directory):
    return convert_to_meta_format(extract_from_data(directory))


def get_system_data():
    with open('system_out.json', 'r') as system_data:
        return json.loads(system_data.read().replace("'", '"').replace("False", "false").replace("True", "true"))


def get_vehicle(frames, div):
    ans = {}
    i = 0
    div_count = 0
    for frame in frames:
        vehicles = frame['objects']
        if div_count % div == 0:
            for vehicle in vehicles:
                if vehicle['tracking_id'] not in ans.keys():
                    ans[vehicle['tracking_id']] = {}
                ans[vehicle['tracking_id']][i] = [vehicle['bounding_box'][0], vehicle['bounding_box'][1], vehicle['speed']]
            i += 1
        div_count += 1
    return ans


def one_show(vehicle_mapping, v_key):
    id = vehicle_mapping[v_key][0]
    for key in vehicle_mapping.keys():
        for value in vehicle_mapping[key]:
            if key != v_key and value[0] == id[0] and id[1] > value[1]:
                return False
    return True


def no_show(vehicle_mapping, v_key):
    ids = vehicle_mapping[v_key]
    for id in ids:
        for key in vehicle_mapping.keys():
            for value in vehicle_mapping[key]:
                if key != v_key and value[0] == id[0]:
                    return False
    return True


def get_car_mapping(t_analyst_data, system_data):
    vehicles_system = get_vehicle(system_data, 2)
    vehicles_analyst = get_vehicle(t_analyst_data, 3)
    vehicle_mapping = {}
    for key in vehicles_analyst.keys():
        vehicle_frames = list(vehicles_analyst[key])
        first_frame = vehicle_frames[0]
        last_frame = first_frame + len(vehicle_frames) - 1
        over_half_vehicles = []
        for v_key in vehicles_system.keys():
            sys_vehicle_frames = list(vehicles_system[v_key])
            sys_first_frame = sys_vehicle_frames[0]
            sys_last_frame = sys_first_frame + len(sys_vehicle_frames) - 1
            frame_laps = (abs(sys_first_frame - first_frame) + abs(last_frame - sys_last_frame)) / len(vehicle_frames)
            if frame_laps < 0.3:
                over_half_vehicles.append([v_key, frame_laps])
        if over_half_vehicles:
            vehicle_mapping[key] = over_half_vehicles
    final_mapping = {}
    for v_key in vehicle_mapping.keys():
        if len(vehicle_mapping[v_key]) == 1 and one_show(vehicle_mapping, v_key):
            final_mapping[v_key] = vehicle_mapping[v_key]
        elif len(vehicle_mapping[v_key]) > 1 and no_show(vehicle_mapping, v_key):
            final_mapping[v_key] = vehicle_mapping[v_key]
    return final_mapping, vehicles_system, vehicles_analyst


def get_first_frame(car_1, car_2):
    min_value = sys.maxsize
    first_frame_car_1 = None
    car_2_first_frame = car_2[min(list(car_2.keys()))]
    for frame in car_1.keys():
        new_value = distance.euclidean(tuple(car_2_first_frame), tuple(car_1[frame]))
        if min_value > new_value:
            min_value = new_value
            first_frame_car_1 = frame
    car_1_first_frame = car_1[min(list(car_1.keys()))]
    first_frame_car_2 = min(list(car_2.keys()))
    for frame in car_2.keys():
        new_value = distance.euclidean(car_1_first_frame, car_2[frame])
        if min_value > new_value:
            min_value = new_value
            first_frame_car_1 = min(list(car_1.keys()))
            first_frame_car_2 = frame
    return [first_frame_car_1, first_frame_car_2]


def get_first_frame_2(car_1, car_2):
    min_value = sys.maxsize
    first_frame_car_1 = None
    first_frame_car_2 = None
    for frame_1 in car_1.keys():
        for frame_2 in car_2.keys():
            vector_ans = camper_two_2(car_1, car_2, [frame_1, frame_2])
            vector_average = (vector_ans[0] + vector_ans[1]) / 2
            if 0 < vector_average < min_value and (vector_ans[2] >= len(car_1.keys()) * 0.5 or
                                                   vector_ans[2] >= len(car_2.keys()) * 0.5):
                first_frame_car_1 = frame_1
                first_frame_car_2 = frame_2
                min_value = min(min_value, vector_average)
    return [first_frame_car_1, first_frame_car_2]


def camper_two_2(car_1, car_2, start_frames):
    key_1 = start_frames[0]
    key_2 = start_frames[1]
    frame_counter = 0
    sum_error_x = 0
    sum_error_y = 0
    while key_1 in car_1.keys() and key_2 in car_2.keys():
        frame_counter += 1
        sum_error_x += abs(car_1[key_1][0] - car_2[key_2][0])
        sum_error_y += abs(car_1[key_1][1] - car_2[key_2][1])
        key_1 += 1
        key_2 += 1
    return [sum_error_x / frame_counter, sum_error_y / frame_counter, frame_counter]


def camper_two(car_1, car_2):
    start_frames = get_first_frame_2(car_1, car_2)
    key_1 = start_frames[0]
    key_2 = start_frames[1]
    frame_counter = 0
    sum_error_x = 0
    sum_error_y = 0
    while key_1 in car_1.keys() and key_2 in car_2.keys():
        frame_counter += 1
        sum_error_x += abs(car_1[key_1][0] - car_2[key_2][0])
        sum_error_y += abs(car_1[key_1][1] - car_2[key_2][1])
        key_1 += 1
        key_2 += 1
    return [sum_error_x / frame_counter, sum_error_y / frame_counter, frame_counter]


def compare(data):
    ans = []
    car_mapping = data[0]
    vehicles_system = data[1]
    vehicles_analyst = data[2]
    print(vehicles_analyst)
    for car_key in car_mapping.keys():
        vector_ans = (sys.maxsize, sys.maxsize, sys.maxsize)
        for car_to_map in car_mapping[car_key]:
            vector = camper_two(vehicles_system[car_to_map[0]], vehicles_analyst[car_key])
            if reduce(lambda x, y: x + y, vector_ans) / len(vector_ans) > \
                    reduce(lambda x, y: x + y, vector) / len(vector):
                vector_ans = vector
        ans.append(vector_ans)
    return ans


def compare_data():
    t_analyst_data = convert_to_meta('.\\t-analyst data')
    system_data = get_system_data()
    print(compare(get_car_mapping(t_analyst_data, system_data)))


compare_data()
