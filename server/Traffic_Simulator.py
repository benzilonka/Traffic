import random
import numpy as np
from datetime import datetime

# e = 2.71828182846
#
#
# def get_first_frame():
#     return {'frame_index': 0, 'objects': []}
#
#
# # def delete_cars(cars_and_lanes):
# #     vehicle_list = frame['objects']
# #     index = 0
# #     while index < len(vehicle_list):
# #         current_bbox = vehicle_list[index]['bounding_box']
# #         # yPosition = BBox[1], lane[3]/lane[4] are locations of the end of the lane
# #         # Delete locations of vehicles that passed the location of the end of the lane
# #         if current_bbox[1] < lane[3][1]:
# #             del (vehicle_list[index])
# #         index += 1
# #     return frame
#
#
# def add_car(frame, lane):
#     # lane is an object containing four points of the lane
#     vehicle_list = frame['objects']
#     if len(vehicle_list) > 0:
#         new_tracking_id = vehicle_list[len(vehicle_list) - 1]['tracking_id'] + 1
#     else:
#         new_tracking_id = 1
#     new_type = gen_type_of_vehicle()
#     new_speed = gen_new_speed(new_type)
#     new_bbox = gen_bounding_box(lane)
#     new_date_and_time = datetime.now()
#     fixed_date_and_time = new_date_and_time.strftime('%Y-%m-%d %H:%M:%S.' + str(new_date_and_time.microsecond))
#     vehicle_list.append({'speed': new_speed, 'new': True, 'alert_tags': [], 'static': False, 'bounding_box': new_bbox,
#                          'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': new_type,
#                          'created_at': fixed_date_and_time, 'lost': False, 'tracking_id': new_tracking_id,
#                          'counted': False})
#     return frame
#
#
# def stopping_distance_function(speed):
#     return ((2.0502645502645 * pow(10, -15) * pow(speed, 10))
#             - (1.4605379188712 * pow(10, -12) * pow(speed, 9))
#             + (4.56944444444 * pow(10, -10) * pow(speed, 8))
#             - (8.25072751322 * pow(10, -8) * pow(speed, 7))
#             + (9.499625000000 * pow(10, -6) * pow(speed, 6))
#             - (0.000726897 * pow(speed, 5)) + (0.0373303 * pow(speed, 4))
#             - (1.26654 * pow(speed, 3)) + (27.081 * speed * speed) - (327.869 * speed) + 1703.8)
#
#
# # def get_frame(current_frame, lane, light, traffic_density):
# #     x = (pow(traffic_density, 3) * pow(e, (-1 * traffic_density))) / 6
#
#
# def gen_bounding_box(lane_locations):
#     # X location will be in the middle of the lane
#     #print(lane_locations)
#     x_point = int((lane_locations[0][0] + lane_locations[1][0]) / 2)
#     # Y location will be where the lane begin
#     y_point = lane_locations[0][1]
#     bbox = [x_point, y_point, 0, 0]
#     return bbox
#
#
# def gen_new_speed(type_of_vehicle):
#     # Generate vehicle speed in range 10 to 120 km/h with bigger probability to lower speeds (10-70 km/h)
#     if type_of_vehicle == 'car':
#         threshold = 0.7
#     elif type_of_vehicle == 'bus':
#         threshold = 0.8
#     else:
#         threshold = 0.9
#     param = random.uniform(0, 1)
#     if param <= threshold:
#         # Generate speed in range 10-70
#         speed = np.random.choice(np.arange(10.0, 70.0))
#     else:
#         # Generate speed in range 71-120
#         speed = np.random.choice(np.arange(71.0, 120.0))
#     # Convert speed from km/h to m/s
#     speed = speed / 3.6
#     return speed
#
#
# def gen_type_of_vehicle():
#     # There is more probability to generate car over bus and truck
#     return np.random.choice(['car', 'bus', 'truck'], p=[0.7, 0.2, 0.1])
#
#
# def extract_vehicles_per_lane(frame, lanes_list):
#     vehicleLst = frame['objects']
#     vehiclesPerLane = []
#     for lane in lanes_list:
#         element = {'lane': lane, 'objects': []}
#         for vehicle in vehicleLst:
#             bbox = vehicle['bounding_box']
#             #print(bbox)
#             # Check if vehicle is in the range of the x and y coordinates of current lane
#             # lane[0][0]- x in start location , lane[3][0]- x in end location
#             # lane[0][1]- y in start location , lane[3][1]- y in end location
#             if lane[0][0] <= bbox[0] <= lane[1][0]:
#                 element['objects'].append(vehicle)
#         # sort vehicles by their y loactions
#         notSorted = element['objects']
#         element['objects'] = sorted(notSorted, key=help_sorted)
#         vehiclesPerLane.append(element)
#     return vehiclesPerLane
#
#
# def help_sorted(vehicle):
#     # Compare by y locations
#     return vehicle['bounding_box'][1]
#
#
# def get_ratio(gui_dimensions, lane_dimensions):
#     return np.amax(gui_dimensions, axis=0)[1] / lane_dimensions[1]
#
#
# def advance_cars(cars_and_lanes, lane_dimension):
#     ans = []
#     ans_index = -1
#     #print(cars_and_lanes)
#     for cars_lane in cars_and_lanes:
#         ans_index += 1
#         ans.append({'lane': cars_lane['lane'], 'objects': []})
#         for car in cars_lane['objects']:
#             speed_per_frame = float(car['speed'] / 15)
#             vehicle_advanced = float(speed_per_frame * get_ratio(cars_lane['lane'], lane_dimension))
#             car['bounding_box'][1] += vehicle_advanced
#             #print(np.amax(cars_lane['lane'], axis=0))
#             if car['bounding_box'][1] < 700:
#                 ans[ans_index]['objects'].append(car)
#     return ans
#
#
# def adjust_speed(cars_and_lanes, light):
#     for cars_in_lane in cars_and_lanes:
#         last_car_y_coordinate = cars_in_lane['lane'][2][1]
#         for car in cars_in_lane['objects']:
#             dis = last_car_y_coordinate - car['bounding_box'][1]
#             ttc = float(dis / car['speed'])
#     return cars_and_lanes
#
#
# def get_frame(current_frame, lanes_list, lane_dimensions, light, traffic_density):
#     frame_index = current_frame['frame_index']
#     frame_index += 1
#     #print(current_frame)
#     cars_and_lanes = advance_cars(extract_vehicles_per_lane(current_frame, lanes_list), lane_dimensions)
#     #cars_and_lanes = adjust_speed(cars_and_lanes, light)
#     cars = []
#     print(cars_and_lanes)
#     for car_lane in cars_and_lanes:
#         for car in car_lane['objects']:
#             cars.append(car)
#     ans = {'frame_index': frame_index, 'objects': cars}
#     if random.uniform(0, 1) >= traffic_density:
#         ans = add_car(ans, lanes_list[int(random.uniform(0, len(lanes_list)))])
#     # print(current_frame)
#     # print (cars_in_lanes)
#     # for cars_in_lane in cars_in_lanes:
#     #     for i in range(0, len(cars_in_lane['objects'])):
#     #         if i == 0:
#     #             if light == "green":
#     #                 cars_in_lane['objects'][i]['speed'] += random.uniform(-4.5, 4.5)*((34 - cars_in_lane['objects'][i]['speed']) / 34)
#     #             elif light == "orange":
#     #                   dis = cars_in_lane['objects'][i + 1]['bounding_box'][1] - cars_in_lane['objects'][i]['bounding_box'][1]
#     #                   dis *= 5  # the ratio between real distance and pixels on the screen
#     #                   if cars_in_lane[i]['speed']*3 < dis:
#     #                       cars_in_lane['objects'][i]['speed'] += random.uniform(-4.5, 4.5) * ((34 - cars_in_lane['objects'][i]['speed']) / 34)
#     #                   else:
#     #                       cars_in_lane['objects'][i]['speed'] += random.uniform(-4.5, 0) * ((34 - cars_in_lane['objects'][i]['speed']) / 34)
#     #             else:
#     #                 # dis = cars_in_lane[i + 1]['bounding_box'][1] - cars_in_lane[i]['bounding_box'][1]
#     #                 # dis *= 5  # the ratio between real distance and pixels on the screen
#     #                 # sd = stopping_distences(cars_in_lane[i]['speed'] * 3.6)
#     #                 # if dis < sd:
#     #                 #     cars_in_lane[i]['speed'] += random.uniform(-4.5, -1)
#     #                 # else:
#     #                 cars_in_lane['objects'][i]['speed'] += random.uniform(-4.5, 0)
#     #         else:
#     #             dis = cars_in_lane['objects'][i + 1]['bounding_box'][1] - cars_in_lane['objects'][i]['bounding_box'][1]
#     #             dis *= 5  # the ratio between real distance and pixels on the screen
#     #             ttc = dis / cars_in_lane['objects'][i]['speed']
#     #             if ttc > 2:
#     #                 cars_in_lane['objects'][i]['speed'] += random.uniform(-2, 4.5) * ((34 - cars_in_lane['objects'][i]['speed']) / 34)
#     #             elif 1 < ttc < 2:
#     #                 cars_in_lane['objects'][i]['speed'] += random.uniform(-2.5, 2.5) * ((34 - cars_in_lane['objects'][i]['speed']) / 34)
#     #             else:
#     #                 cars_in_lane['objects'][i]['speed'] += random.uniform(-4.5, -1)
#     #          # else:
#     # #print(stopping_distences(120))
#     #
#     # #ans = deleteCars(ans, lanesList)
#     # vehiclesInLanesArr = extract_vehicles_per_lane(ans, lanesList)
#     return ans


lanes_array_test = [{'A': [0, 0], 'B': [23, 0], 'C': [0, 700], 'D': [23, 700]},
                    {'A': [23, 0], 'B': [47, 0], 'C': [23, 700], 'D': [47, 700]},
                    {'A': [47, 0], 'B': [70, 0], 'C': [47, 700], 'D': [70, 700]}]
lane_dimentions_test = [4.6, 200]
# print(int(random.uniform(0, len(lanes_array))))
x_test_1 = {'frame_index': 0, 'objects': []}

x_test_2 = {'frame_index': 0, 'objects': [{'confidence': 1.0, 'alert_tags': [],
                                           'bounding_box': [11, 0, 0, 0], 'new': False, 'times_lost_by_convnet': 0,
                                           'tracking_id': 2, 'static': True, 'type': 'car', 'lost': False,
                                           'counted': False,
                                           'speed': 21.2, 'created_at': '2017-12-22 10:29:13.857687'}]}

x_test_3 = {'frame_index': 0, 'objects': [{'confidence': 1.0, 'alert_tags': [],
                                           'bounding_box': [23, 0, 0, 0], 'new': False, 'times_lost_by_convnet': 0,
                                           'tracking_id': 1, 'static': True, 'type': 'car', 'lost': False,
                                           'counted': False,
                                           'speed': 13.124, 'created_at': '2017-12-22 10:29:13.857687'},
                                          {'confidence': 1.0, 'alert_tags': [],
                                           'bounding_box': [11, 0, 0, 0], 'new': False, 'times_lost_by_convnet': 0,
                                           'tracking_id': 2, 'static': True, 'type': 'car', 'lost': False,
                                           'counted': False,
                                           'speed': 21.2, 'created_at': '2017-12-22 10:29:13.857687'}]}

x_test_4 = {'frame_index': 0, 'objects': [{'confidence': 1.0, 'alert_tags': [],
                                           'bounding_box': [23, 0, 0, 0], 'new': False, 'times_lost_by_convnet': 0,
                                           'tracking_id': 1, 'static': True, 'type': 'car', 'lost': False,
                                           'counted': False,
                                           'speed': 13.124, 'created_at': '2017-12-22 10:29:13.857687'},
                                          {'confidence': 1.0, 'alert_tags': [],
                                           'bounding_box': [11, 0, 0, 0], 'new': False, 'times_lost_by_convnet': 0,
                                           'tracking_id': 2, 'static': True, 'type': 'car', 'lost': False,
                                           'counted': False,
                                           'speed': 21.2, 'created_at': '2017-12-22 10:29:13.857687'},
                                          {'confidence': 1.0, 'alert_tags': [],
                                           'bounding_box': [47, 0, 0, 0], 'new': False, 'times_lost_by_convnet': 0,
                                           'tracking_id': 2, 'static': True, 'type': 'car', 'lost': False,
                                           'counted': False,
                                           'speed': 7.2, 'created_at': '2017-12-22 10:29:13.857687'}]}


# print(get_ratio(lanes_array[0], lane_dimentions))


def get_max_y(gui_dimensions):
    max_point = 0
    for point in gui_dimensions.keys():
        if max_point < gui_dimensions[point][1]:
            max_point = gui_dimensions[point][1]
    return max_point


def get_ratio(cars_lane, lane_length):
    max_y = get_max_y(cars_lane)
    return max_y / lane_length


def get_new_position(car, cars_lane, lane_dimension):
    speed_per_frame = float(car['speed'] / 15)
    vehicle_advanced = float(speed_per_frame * float(get_ratio(cars_lane, lane_dimension[1])))
    return car['bounding_box'][1] + vehicle_advanced


def is_car_finished(car, lanes_array):
    lane = get_car_lane(car, lanes_array)
    max_y = get_max_y(lane)
    return max_y < car['bounding_box'][1]


def get_car_lane(car, lanes_array):
    new_lane = None
    for lane in lanes_array:
        if lane['A'][0] <= car['bounding_box'][0] <= lane['B'][0]:
            new_lane = lane
    return new_lane


def frame_time_lapse(current_frame, lanes_array, lane_dimentions, light):
    cars = []
    for car in current_frame['objects']:
        car_lane = get_car_lane(car, lanes_array)
        car['bounding_box'][1] = get_new_position(car, car_lane, lane_dimentions)
        if not is_car_finished(car, lanes_array):
            cars.append(car)
    frame_index = current_frame['frame_index'] + 1
    return {'frame_index': frame_index, 'objects': cars}



def get_random_speed(car_type):
    vehicle_speed = {'car': [25, 70, 120], 'bus': [15, 55, 110], 'truck': [10, 45, 110]}
    

def get_random_car_type():
    return np.random.choice(['car', 'bus', 'truck'], p=[0.75, 0.15, 0.1])


def add_new_cars(current_frame, cars_position):
    new_cars = []
    seq = [x['tracking_id'] for x in current_frame['objects']]
    new_tracking_id = max(seq)
    for car_position in cars_position:
        new_bbox = car_position
        new_tracking_id += 1
        new_type = get_random_car_type()
        new_speed = get_random_speed(new_type)
        new_date_and_time = datetime.now()
        fixed_date_and_time = new_date_and_time.strftime('%Y-%m-%d %H:%M:%S.' + str(new_date_and_time.microsecond))
        new_cars.append({'speed': new_speed, 'new': True, 'alert_tags': [], 'static': False, 'bounding_box': new_bbox,
                         'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': new_type,
                         'created_at': fixed_date_and_time, 'lost': False, 'tracking_id': new_tracking_id,
                         'counted': False})
    return new_cars


def get_available_positions_number(current_frame, lanes_array, buffer_distance):
    ans = []
    lane_list = []
    for car in current_frame['objects']:
        lane = get_car_lane(car, lanes_array)
        if (car['bounding_box'][1] <= buffer_distance) and (not (lane in lane_list)):
            ans.append([car['bounding_box'][0], 0, 0, 0])
            lane_list.append(lane)
    return ans


def random_car_quantity(traffic_density, number_of_positions):
    lambda_value = traffic_density / (60 * 15)
    ans = []
    for position in number_of_positions:
        if random.uniform(0, 1) <= np.random.poisson(lambda_value, 1):
            ans.append(position)
    return ans


def get_frame(current_frame, lanes_array, lane_dimentions, light, traffic_density):
    new_frame = frame_time_lapse(current_frame, lanes_array, lane_dimentions, light)
    print(new_frame)
    buffer_distance = float(get_ratio(lanes_array[0], lane_dimentions[1]) / 3)
    number_of_positions = get_available_positions_number(current_frame, lanes_array, buffer_distance)
    new_cars = add_new_cars(new_frame, random_car_quantity(traffic_density, number_of_positions))
    for car in new_cars:
        new_frame['objects'].append(car)
    return new_frame


# def test(list):
#     for e in list:
#         print(e)
#
#
# def test2(ls1):
#     ans = []
#     for i in ls1:
#         ans.append(i)
#     return ans
#
#
# lst = []
# lst.append([1, 2, 3])
# lst.append([2, 3, 4])
# lst.append([3, 4, 5])
# a = test2(lst)
# test(a)
traffic_density = 60
buffer = float(get_ratio(lanes_array_test[0], lane_dimentions_test[1]) / 3)
number_positions = get_available_positions_number(x_test_1, lanes_array_test, buffer)
print(min(number_positions, random_car_quantity(traffic_density, number_positions)))
buffer = float(get_ratio(lanes_array_test[0], lane_dimentions_test[1]) / 3)
number_positions = get_available_positions_number(x_test_2, lanes_array_test, buffer)
print(min(number_positions, random_car_quantity(traffic_density, number_positions)))
buffer = float(get_ratio(lanes_array_test[0], lane_dimentions_test[1]) / 3)
number_positions = get_available_positions_number(x_test_3, lanes_array_test, buffer)
print(min(number_positions, random_car_quantity(traffic_density, number_positions)))
buffer = float(get_ratio(lanes_array_test[0], lane_dimentions_test[1]) / 3)
number_positions = get_available_positions_number(x_test_4, lanes_array_test, buffer)
print(min(number_positions, random_car_quantity(traffic_density, number_positions)))

# with open("new_data.meta", 'w') as output:
#     for i in range(0, 200):
#         x_test = get_frame(x_test, lanes_array_test, lane_dimentions_test, "green", 0.25)
#         output.write(str(x_test) + "\n")
# # extractVehiclesPerLane(frame, lanesArray)
