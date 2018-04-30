import math
import random
import sys

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
x_test_1 = {'frame_index': 0, 'objects': []}
    # {'speed': 0, 'new': True, 'alert_tags': [], 'static': False, 'bounding_box': [35, 26.45918013036104, 0, 0],
    #  'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': 'car', 'created_at': '2018-04-07 18:40:45.246162',
    #  'lost': False, 'tracking_id': 36, 'counted': False},
    # {'speed': 0, 'new': True, 'alert_tags': [], 'static': False, 'bounding_box': [35, 26.54151462533078, 0, 0],
    #  'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': 'car', 'created_at': '2018-04-07 18:40:45.254163',
    #  'lost': False, 'tracking_id': 37, 'counted': False},
    # {'speed': 0, 'new': True, 'alert_tags': [], 'static': False, 'bounding_box': [35, 11.134611351746441, 0, 0],
    #  'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': 'car', 'created_at': '2018-04-07 18:40:45.264163',
    #  'lost': False, 'tracking_id': 40, 'counted': False},
    # {'speed': 0, 'new': True, 'alert_tags': [], 'static': False, 'bounding_box': [35, 10.90329295277763, 0, 0],
    #  'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': 'bus', 'created_at': '2018-04-07 18:40:45.297165',
    #  'lost': False, 'tracking_id': 41, 'counted': False},
    # {'speed': 0, 'new': True, 'alert_tags': [], 'static': False, 'bounding_box': [35, 10.230768867451836, 0, 0],
    #  'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': 'bus', 'created_at': '2018-04-07 18:40:45.358169',
    #  'lost': False, 'tracking_id': 43, 'counted': False}]}

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
                                           'bounding_box': [35, 1, 0, 0], 'new': False, 'times_lost_by_convnet': 0,
                                           'tracking_id': 1, 'static': True, 'type': 'car', 'lost': False,
                                           'counted': False,
                                           'speed': 0, 'created_at': '2017-12-22 10:29:13.857687'},
                                          {'confidence': 1.0, 'alert_tags': [],
                                           'bounding_box': [11, 0.87, 0, 0], 'new': False, 'times_lost_by_convnet': 0,
                                           'tracking_id': 2, 'static': True, 'type': 'car', 'lost': False,
                                           'counted': False,
                                           'speed': 0, 'created_at': '2017-12-22 10:29:13.857687'},
                                          {'confidence': 1.0, 'alert_tags': [],
                                           'bounding_box': [58, 0, 0, 0], 'new': False, 'times_lost_by_convnet': 0,
                                           'tracking_id': 2, 'static': True, 'type': 'car', 'lost': False,
                                           'counted': False,
                                           'speed': 0, 'created_at': '2017-12-22 10:29:13.857687'}]}

# return the length of the lane
def get_max_y(gui_dimensions):
    max_point = 0
    for point in gui_dimensions.keys():
        if max_point < gui_dimensions[point][1]:
            max_point = gui_dimensions[point][1]
    return max_point


# calculates the ratio between the actual lane length and the GUI length.
# e.g if the real length is 200 and the GUI length is 700 3.5  pixels are 1 meter and the function will return 3.5
def get_ratio(cars_lane, lane_length):
    max_y = get_max_y(cars_lane)
    return max_y / lane_length


# calculates the car new position according to the speed
def get_new_position(car_info, cars_lane, lane_dimension):
    speed_per_frame = float(car_info['speed'] / 15)
    vehicle_advanced = float(speed_per_frame * float(get_ratio(cars_lane, lane_dimension[1])))
    return car_info['bounding_box'][1] + vehicle_advanced


# returns true if the car cross the end of the lane
def is_car_finished(car_info, lanes_array):
    lane = get_car_lane(car_info, lanes_array)
    max_y = get_max_y(lane)
    return max_y < car_info['bounding_box'][1]


# returns the lane that the car is in.
def get_car_lane(car_info, lanes_array):
    new_lane = None
    for lane in lanes_array:
        if lane['A'][0] <= car_info['bounding_box'][0] <= lane['B'][0]:
            new_lane = lane
    return new_lane


# returns the distance of a car from the closest car that is in front of it.
def front_car_distance(current_car, current_frame):
    car_position = 0
    distanceToReturn = 0
    front_car = None
    for car in current_frame['objects']:
        if current_car['bounding_box'][0] == car['bounding_box'][0] and \
                current_car['bounding_box'][1] < car['bounding_box'][1] < car_position:
            car_position = car['bounding_box'][1]
            front_car = car
    if car_position > 0:
        distanceToReturn = car_position - current_car['bounding_box'][1]
    return distanceToReturn, front_car


# returns the car in front of current_car.
def get_front_car(current_car, current_frame):
    front_car = None
    car_position = 700
    for car_info in current_frame['objects']:
        if current_car['bounding_box'][0] == car_info['bounding_box'][0] and \
                current_car['bounding_box'][1] < car_info['bounding_box'][1] < car_position:
            car_position = car_info['bounding_box'][1]
            front_car = car_info
    return front_car

# returns a new speed of a car according to the distance from the front car and the car speed (ttc)
# uses a random factor of stopping (normal distribution)
def get_new_speed(car_info, current_frame, current_speed, distance_from_front_car, lane_ratio, front_car_speed):
    newSpeed = 0
    if current_speed == 0 or current_speed == front_car_speed:
        ttc = sys.maxsize
    else:
        # ttc calculation is: delta(location) / delta(velocity) = (Xfront - Xcurr) / (Vfront - Vcurr)
        ttc = float(distance_from_front_car / ((front_car_speed * lane_ratio) - (current_speed * lane_ratio)))
    # The current car is all alone and there is no one in front of it
    if front_car_speed == 0 and distance_from_front_car == 0:
        newSpeed = current_speed + 2
    else:
        # We need to change the current car speed (increase\decrease) and check if it's ok before returning it.
        # If the suggested change is not ok we'll try to find a new one.
        acceleration_deceleration = 0
        ttc_treshold = 2.5
        isAcceleration = False
        # if equal or bigger the vehicle can accelerate
        if ttc >= ttc_treshold:
            acceleration_deceleration = 5
            isAcceleration = True
        else:
            # vehicles are too close deceleration is needed
            acceleration_deceleration = -5
        isOK = False
        frontCarCurrentLocation = car_info['bounding_box'][1] + distance_from_front_car
        # The time is in seconds - 15 FPS
        timeInFrame = 1/15
        counter = 0
        # keep looking for vehicle new speed until it's ok or the change won't be successful within 100 attempts
        while not isOK and counter < 100:
            # Convert acceleration_deceleration into velocity => v = v0 + a*t (where t is 1/15 second)
            speedRate = current_speed + acceleration_deceleration * timeInFrame

            # Choose one speed from 1000 samples, 1.55 is Standard deviation (spread or “width”) of the distribution
            # And the mean value is speedRate
            max_change_speed_rate = np.random.choice(np.random.normal(speedRate, 1.55, 1000))
            if isAcceleration > 0:
                # Need to be positive
                min_change_speed_rate = max(1, max_change_speed_rate - ttc)
            else:
                min_change_speed_rate = max_change_speed_rate - ttc
            suggestedSpeed = current_speed + random.uniform(min_change_speed_rate, max_change_speed_rate)
            # X = X0 + [(v+v0)/2]*t (and we're converting the speed from m/s to pixel/s by multiplying it with lane_ratio)
            frontCarNextLocatoion = frontCarCurrentLocation + (front_car_speed*lane_ratio)*timeInFrame
            currentCarNextLocation = car_info['bounding_box'][1] + (((current_speed + suggestedSpeed)/2)*lane_ratio)*timeInFrame
            if currentCarNextLocation < frontCarNextLocatoion:
                isOK = True
                newSpeed = suggestedSpeed
            counter += 1
    return newSpeed


# checks if the distance from the front car is far enough (if not the speed will be zero because it's an "accident")
# if not will get a new speed with get_new_speed function
def adjust_speed_to_traffic(car_info, current_frame, light, accident_rate, lane_ratio):
    front_car_speed = 0
    current_speed = car_info['speed']
    light_acceleration_distribution = {'green': [], "orange": [], 'red': []}
    distance_from_front_car, front_car = front_car_distance(car_info, current_frame)
    if front_car is not None:
        front_car_speed = front_car['speed']
    if distance_from_front_car > (lane_ratio / 5) or len(current_frame['objects']) == 1:
        new_speed = get_new_speed(car_info, current_frame, current_speed, distance_from_front_car, lane_ratio, front_car_speed)
    else:
        # An "accident" occurred
        #front_car = get_front_car(car_info, current_frame)
        if front_car is not None:
            front_car['speed'] = 0
        new_speed = 0
    return new_speed


# the main function that generate a new frame from the previous one, take into account the lane length, the light(for
# now not implemented) and accident rate(also not implemented) every car in the frame gets evaluated from the driver
# point of view
def frame_time_lapse(current_frame, lanes_array, lane_dimensions, light, accident_rate):
    cars = []
    ratio = get_ratio(lanes_array[0], lane_dimensions[1])
    for car_info in current_frame['objects']:
        car_lane = get_car_lane(car_info, lanes_array)
        car_new_position = get_new_position(car_info, car_lane, lane_dimensions)
        car_info['speed'] = adjust_speed_to_traffic(car_info, current_frame, light,
                                                    accident_rate, ratio, car_new_position)
        car_info['bounding_box'][1] = car_new_position
        if not is_car_finished(car_info, lanes_array):
            cars.append(car_info)
    frame_index = current_frame['frame_index'] + 1
    return {'frame_index': frame_index, 'objects': cars}


# generates a random speed according to the car type
def get_random_speed(car_type):
    vehicle_speed = {'car': [25, 70, 120], 'bus': [15, 55, 110], 'truck': [10, 45, 110]}
    top_speed = np.random.choice(vehicle_speed[car_type], p=[0.2, 0.6, 0.2])
    return random.uniform(0, top_speed) / 3.6


def get_random_car_type():
    return np.random.choice(['car', 'bus', 'truck'], p=[0.75, 0.15, 0.1])


def add_new_cars(current_frame, cars_position):
    new_cars = []
    new_tracking_id = 0
    seq = [x['tracking_id'] for x in current_frame['objects']]
    if seq != []:
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


# returns the lanes that are vacant from car in the length of buffer_distance e.g if the buffer is size 5
# and there is a car in position 3 than the function will not return this lane, if there isn't any car in the strip
# from 0 to 5(the buffer length) than the function will return it.
def get_available_positions_number(current_frame, lanes_array, buffer_distance):
    ans = []
    lane_checked = []
    occupied_lane = []
    for car_info in current_frame['objects']:
        lane = get_car_lane(car_info, lanes_array)
        if (car_info['bounding_box'][1] <= buffer_distance) and (not (lane in lane_checked)):
            occupied_lane.append(int((lane['A'][0] + lane['B'][0]) / 2))
    for lane in lanes_array:
        lane_center = int((lane['A'][0] + lane['B'][0]) / 2)
        if lane_center not in occupied_lane:
            ans.append([lane_center, 0, 0, 0])
    return ans


# returns a subset of positions from number_of_positions according to the traffic_density.
# uses a poisson distribution to return a reasonable position quantity
def random_car_quantity(traffic_density, number_of_positions):
    ans = []
    lambda_value = traffic_density / (60 * 15)
    for position in number_of_positions:
        if random.uniform(0, 1) <= np.random.poisson(lambda_value, 1):
            ans.append(position)
    return ans


def get_frame(current_frame, lanes_array, lane_dimensions, light, traffic_density, red_crossing_rate, accident_rate):
    new_frame = frame_time_lapse(current_frame, lanes_array, lane_dimensions, light, red_crossing_rate, accident_rate)
    buffer_distance = float(get_ratio(lanes_array[0], lane_dimensions[1]) / 2)
    number_of_positions = get_available_positions_number(current_frame, lanes_array, buffer_distance)
    new_cars = add_new_cars(new_frame, random_car_quantity(traffic_density, number_of_positions))
    for car_info in new_cars:
        new_frame['objects'].append(car_info)
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
# traffic_density = 60
# buffer = float(get_ratio(lanes_array_test[0], lane_dimentions_test[1]) / 3)
# number_positions = get_available_positions_number(x_test_1, lanes_array_test, buffer)
# print(min(number_positions, random_car_quantity(traffic_density, number_positions)))
# buffer = float(get_ratio(lanes_array_test[0], lane_dimentions_test[1]) / 3)
# number_positions = get_available_positions_number(x_test_2, lanes_array_test, buffer)
# print(min(number_positions, random_car_quantity(traffic_density, number_positions)))
# buffer = float(get_ratio(lanes_array_test[0], lane_dimentions_test[1]) / 3)
# number_positions = get_available_positions_number(x_test_3, lanes_array_test, buffer)
# print(min(number_positions, random_car_quantity(traffic_density, number_positions)))
# buffer = float(get_ratio(lanes_array_test[0], lane_dimentions_test[1]) / 3)
# number_positions = get_available_positions_number(x_test_4, lanes_array_test, buffer)
# print(min(number_positions, random_car_quantity(traffic_density, number_positions)))

# x_test_1 = {'frame_index': 195, 'objects': [{'speed': 8.630630962187603, 'new': True, 'alert_tags': [], 'static': False,
#                                              'bounding_box': [11, 389.6660809971818, 0, 0], 'confidence': 1.0,
#                                              'times_lost_by_convnet': 0, 'type': 'bus',
#                                              'created_at': '2018-04-05 18:12:50.752424', 'lost': False,
#                                              'tracking_id': 2, 'counted': False},
#                                             {'speed': 8.630630962187603, 'new': True, 'alert_tags': [], 'static': False,
#                                              'bounding_box': [35, 388.6660809971818, 0, 0], 'confidence': 1.0,
#                                              'times_lost_by_convnet': 0, 'type': 'bus',
#                                              'created_at': '2018-04-05 18:12:50.752424', 'lost': False,
#                                              'tracking_id': 2, 'counted': False},
#                                             {'speed': 13.397396485954323, 'new': True, 'alert_tags': [],
#                                              'static': False, 'bounding_box': [11, 584.5730666704749, 0, 0],
#                                              'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': 'car',
#                                              'created_at': '2018-04-05 18:12:50.753424', 'lost': False,
#                                              'tracking_id': 3, 'counted': False},
#                                             {'speed': 0.5527901091091396, 'new': True, 'alert_tags': [],
#                                              'static': False, 'bounding_box': [35, 23.991090735336595, 0, 0],
#                                              'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': 'car',
#                                              'created_at': '2018-04-05 18:12:50.753424', 'lost': False,
#                                              'tracking_id': 4, 'counted': False},
#                                             {'speed': 7.122364886345414, 'new': True, 'alert_tags': [], 'static': False,
#                                              'bounding_box': [11, 305.78686578709636, 0, 0], 'confidence': 1.0,
#                                              'times_lost_by_convnet': 0, 'type': 'bus',
#                                              'created_at': '2018-04-05 18:12:50.755424', 'lost': False,
#                                              'tracking_id': 5, 'counted': False},
#                                             {'speed': 9.606563638906426, 'new': True, 'alert_tags': [], 'static': False,
#                                              'bounding_box': [35, 405.71720434981563, 0, 0], 'confidence': 1.0,
#                                              'times_lost_by_convnet': 0, 'type': 'bus',
#                                              'created_at': '2018-04-05 18:12:50.756424', 'lost': False,
#                                              'tracking_id': 6, 'counted': False},
#                                             {'speed': 9.780434844846907, 'new': True, 'alert_tags': [], 'static': False,
#                                              'bounding_box': [35, 401.6498576283804, 0, 0], 'confidence': 1.0,
#                                              'times_lost_by_convnet': 0, 'type': 'car',
#                                              'created_at': '2018-04-05 18:12:50.758424', 'lost': False,
#                                              'tracking_id': 8, 'counted': False},
#                                             {'speed': 3.7263995984068745, 'new': True, 'alert_tags': [],
#                                              'static': False, 'bounding_box': [35, 150.42233045569066, 0, 0],
#                                              'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': 'car',
#                                              'created_at': '2018-04-05 18:12:50.760424', 'lost': False,
#                                              'tracking_id': 10, 'counted': False},
#                                             {'speed': 5.651536555812757, 'new': True, 'alert_tags': [], 'static': False,
#                                              'bounding_box': [58, 222.85892485088206, 0, 0], 'confidence': 1.0,
#                                              'times_lost_by_convnet': 0, 'type': 'car',
#                                              'created_at': '2018-04-05 18:12:50.762424', 'lost': False,
#                                              'tracking_id': 11, 'counted': False},
#                                             {'speed': 4.11431059238817, 'new': True, 'alert_tags': [], 'static': False,
#                                              'bounding_box': [35, 157.44095200205416, 0, 0], 'confidence': 1.0,
#                                              'times_lost_by_convnet': 0, 'type': 'car',
#                                              'created_at': '2018-04-05 18:12:50.765425', 'lost': False,
#                                              'tracking_id': 12, 'counted': False},
#                                             {'speed': 13.535134647075964, 'new': True, 'alert_tags': [],
#                                              'static': False, 'bounding_box': [58, 517.9444858281082, 0, 0],
#                                              'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': 'car',
#                                              'created_at': '2018-04-05 18:12:50.765425', 'lost': False,
#                                              'tracking_id': 13, 'counted': False},
#                                             {'speed': 11.849621749020772, 'new': True, 'alert_tags': [],
#                                              'static': False, 'bounding_box': [35, 442.38587863010963, 0, 0],
#                                              'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': 'car',
#                                              'created_at': '2018-04-05 18:12:50.768425', 'lost': False,
#                                              'tracking_id': 14, 'counted': False},
#                                             {'speed': 18.58520937311935, 'new': True, 'alert_tags': [], 'static': False,
#                                              'bounding_box': [11, 685.1747188890005, 0, 0], 'confidence': 1.0,
#                                              'times_lost_by_convnet': 0, 'type': 'car',
#                                              'created_at': '2018-04-05 18:12:50.769425', 'lost': False,
#                                              'tracking_id': 15, 'counted': False},
#                                             {'speed': 8.249057967784044, 'new': True, 'alert_tags': [], 'static': False,
#                                              'bounding_box': [35, 296.41614964237425, 0, 0], 'confidence': 1.0,
#                                              'times_lost_by_convnet': 0, 'type': 'car',
#                                              'created_at': '2018-04-05 18:12:50.772425', 'lost': False,
#                                              'tracking_id': 16, 'counted': False},
#                                             {'speed': 8.840166404022945, 'new': True, 'alert_tags': [], 'static': False,
#                                              'bounding_box': [35, 303.21770765798675, 0, 0], 'confidence': 1.0,
#                                              'times_lost_by_convnet': 0, 'type': 'car',
#                                              'created_at': '2018-04-05 18:12:50.780425', 'lost': False,
#                                              'tracking_id': 18, 'counted': False},
#                                             {'speed': 1.6970660538996345, 'new': True, 'alert_tags': [],
#                                              'static': False, 'bounding_box': [58, 57.021419411027594, 0, 0],
#                                              'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': 'bus',
#                                              'created_at': '2018-04-05 18:12:50.783426', 'lost': False,
#                                              'tracking_id': 20, 'counted': False},
#                                             {'speed': 9.357235024768581, 'new': True, 'alert_tags': [], 'static': False,
#                                              'bounding_box': [58, 296.93625811932276, 0, 0], 'confidence': 1.0,
#                                              'times_lost_by_convnet': 0, 'type': 'bus',
#                                              'created_at': '2018-04-05 18:12:50.801427', 'lost': False,
#                                              'tracking_id': 21, 'counted': False},
#                                             {'speed': 3.6096339439440968, 'new': True, 'alert_tags': [],
#                                              'static': False, 'bounding_box': [11, 112.01897339373193, 0, 0],
#                                              'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': 'car',
#                                              'created_at': '2018-04-05 18:12:50.814427', 'lost': False,
#                                              'tracking_id': 22, 'counted': False},
#                                             {'speed': 11.633285343811417, 'new': True, 'alert_tags': [],
#                                              'static': False, 'bounding_box': [58, 361.0196218362808, 0, 0],
#                                              'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': 'car',
#                                              'created_at': '2018-04-05 18:12:50.814427', 'lost': False,
#                                              'tracking_id': 23, 'counted': False},
#                                             {'speed': 16.446534449453114, 'new': True, 'alert_tags': [],
#                                              'static': False, 'bounding_box': [58, 502.7157363382849, 0, 0],
#                                              'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': 'car',
#                                              'created_at': '2018-04-05 18:12:50.826428', 'lost': False,
#                                              'tracking_id': 24, 'counted': False},
#                                             {'speed': 9.601837824628609, 'new': True, 'alert_tags': [], 'static': False,
#                                              'bounding_box': [58, 277.81317439258777, 0, 0], 'confidence': 1.0,
#                                              'times_lost_by_convnet': 0, 'type': 'car',
#                                              'created_at': '2018-04-05 18:12:50.869431', 'lost': False,
#                                              'tracking_id': 25, 'counted': False},
#                                             {'speed': 2.6048588509871116, 'new': True, 'alert_tags': [],
#                                              'static': False, 'bounding_box': [35, 74.15164862476642, 0, 0],
#                                              'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': 'bus',
#                                              'created_at': '2018-04-05 18:12:50.880431', 'lost': False,
#                                              'tracking_id': 26, 'counted': False},
#                                             {'speed': 3.2002121345387375, 'new': True, 'alert_tags': [],
#                                              'static': False, 'bounding_box': [11, 88.85922360235908, 0, 0],
#                                              'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': 'car',
#                                              'created_at': '2018-04-05 18:12:50.898432', 'lost': False,
#                                              'tracking_id': 27, 'counted': False},
#                                             {'speed': 3.425314261564256, 'new': True, 'alert_tags': [], 'static': False,
#                                              'bounding_box': [58, 93.51107934070436, 0, 0], 'confidence': 1.0,
#                                              'times_lost_by_convnet': 0, 'type': 'car',
#                                              'created_at': '2018-04-05 18:12:50.910433', 'lost': False,
#                                              'tracking_id': 28, 'counted': False},
#                                             {'speed': 18.752673964000238, 'new': True, 'alert_tags': [],
#                                              'static': False, 'bounding_box': [58, 481.3186317426731, 0, 0],
#                                              'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': 'car',
#                                              'created_at': '2018-04-05 18:12:50.952435', 'lost': False,
#                                              'tracking_id': 29, 'counted': False},
#                                             {'speed': 3.271872495004087, 'new': True, 'alert_tags': [], 'static': False,
#                                              'bounding_box': [58, 78.63400229659808, 0, 0], 'confidence': 1.0,
#                                              'times_lost_by_convnet': 0, 'type': 'truck',
#                                              'created_at': '2018-04-05 18:12:50.978437', 'lost': False,
#                                              'tracking_id': 30, 'counted': False},
#                                             {'speed': 18.68251576394835, 'new': True, 'alert_tags': [], 'static': False,
#                                              'bounding_box': [35, 435.9253678254617, 0, 0], 'confidence': 1.0,
#                                              'times_lost_by_convnet': 0, 'type': 'car',
#                                              'created_at': '2018-04-05 18:12:50.984437', 'lost': False,
#                                              'tracking_id': 31, 'counted': False},
#                                             {'speed': 0.3074951983260703, 'new': True, 'alert_tags': [],
#                                              'static': False, 'bounding_box': [11, 6.887892442503988, 0, 0],
#                                              'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': 'car',
#                                              'created_at': '2018-04-05 18:12:50.992438', 'lost': False,
#                                              'tracking_id': 32, 'counted': False},
#                                             {'speed': 17.85104437647752, 'new': True, 'alert_tags': [], 'static': False,
#                                              'bounding_box': [35, 391.5329066574066, 0, 0], 'confidence': 1.0,
#                                              'times_lost_by_convnet': 0, 'type': 'bus',
#                                              'created_at': '2018-04-05 18:12:50.996438', 'lost': False,
#                                              'tracking_id': 33, 'counted': False},
#                                             {'speed': 5.012198235388051, 'new': True, 'alert_tags': [], 'static': False,
#                                              'bounding_box': [11, 97.06957249201506, 0, 0], 'confidence': 1.0,
#                                              'times_lost_by_convnet': 0, 'type': 'bus',
#                                              'created_at': '2018-04-05 18:12:51.30440', 'lost': False,
#                                              'tracking_id': 34, 'counted': False},
#                                             {'speed': 1.5850912192621536, 'new': True, 'alert_tags': [],
#                                              'static': False, 'bounding_box': [35, 28.478805572743386, 0, 0],
#                                              'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': 'car',
#                                              'created_at': '2018-04-05 18:12:51.62442', 'lost': False,
#                                              'tracking_id': 35, 'counted': False},
#                                             {'speed': 12.380479965851624, 'new': True, 'alert_tags': [],
#                                              'static': False, 'bounding_box': [11, 219.54717806110256, 0, 0],
#                                              'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': 'car',
#                                              'created_at': '2018-04-05 18:12:51.68442', 'lost': False,
#                                              'tracking_id': 36, 'counted': False},
#                                             {'speed': 13.233936250853418, 'new': True, 'alert_tags': [],
#                                              'static': False, 'bounding_box': [58, 219.2422105558053, 0, 0],
#                                              'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': 'bus',
#                                              'created_at': '2018-04-05 18:12:51.98444', 'lost': False,
#                                              'tracking_id': 37, 'counted': False},
#                                             {'speed': 17.002980958664658, 'new': True, 'alert_tags': [],
#                                              'static': False, 'bounding_box': [35, 265.813268987124, 0, 0],
#                                              'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': 'car',
#                                              'created_at': '2018-04-05 18:12:51.122445', 'lost': False,
#                                              'tracking_id': 38, 'counted': False},
#                                             {'speed': 22.47520689433308, 'new': True, 'alert_tags': [], 'static': False,
#                                              'bounding_box': [11, 319.89711146267416, 0, 0], 'confidence': 1.0,
#                                              'times_lost_by_convnet': 0, 'type': 'car',
#                                              'created_at': '2018-04-05 18:12:51.164447', 'lost': False,
#                                              'tracking_id': 39, 'counted': False},
#                                             {'speed': 9.694485049459766, 'new': True, 'alert_tags': [], 'static': False,
#                                              'bounding_box': [11, 115.36437208857132, 0, 0], 'confidence': 1.0,
#                                              'times_lost_by_convnet': 0, 'type': 'truck',
#                                              'created_at': '2018-04-05 18:12:51.219451', 'lost': False,
#                                              'tracking_id': 40, 'counted': False},
#                                             {'speed': 6.773509143258638, 'new': True, 'alert_tags': [], 'static': False,
#                                              'bounding_box': [35, 69.54136053745538, 0, 0], 'confidence': 1.0,
#                                              'times_lost_by_convnet': 0, 'type': 'truck',
#                                              'created_at': '2018-04-05 18:12:51.257453', 'lost': False,
#                                              'tracking_id': 41, 'counted': False},
#                                             {'speed': 4.314464832600776, 'new': True, 'alert_tags': [], 'static': False,
#                                              'bounding_box': [58, 39.26162997666708, 0, 0], 'confidence': 1.0,
#                                              'times_lost_by_convnet': 0, 'type': 'car',
#                                              'created_at': '2018-04-05 18:12:51.287454', 'lost': False,
#                                              'tracking_id': 42, 'counted': False},
#                                             {'speed': 13.974681558640015, 'new': True, 'alert_tags': [],
#                                              'static': False, 'bounding_box': [58, 107.60504800152805, 0, 0],
#                                              'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': 'car',
#                                              'created_at': '2018-04-05 18:12:51.323457', 'lost': False,
#                                              'tracking_id': 43, 'counted': False},
#                                             {'speed': 12.881173772108871, 'new': True, 'alert_tags': [],
#                                              'static': False, 'bounding_box': [35, 93.17382361825416, 0, 0],
#                                              'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': 'car',
#                                              'created_at': '2018-04-05 18:12:51.335457', 'lost': False,
#                                              'tracking_id': 44, 'counted': False},
#                                             {'speed': 10.123970363296818, 'new': True, 'alert_tags': [],
#                                              'static': False, 'bounding_box': [58, 70.8677925430777, 0, 0],
#                                              'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': 'car',
#                                              'created_at': '2018-04-05 18:12:51.341458', 'lost': False,
#                                              'tracking_id': 45, 'counted': False},
#                                             {'speed': 27.259951383336684, 'new': True, 'alert_tags': [],
#                                              'static': False, 'bounding_box': [35, 165.37703839224258, 0, 0],
#                                              'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': 'bus',
#                                              'created_at': '2018-04-05 18:12:51.366459', 'lost': False,
#                                              'tracking_id': 46, 'counted': False},
#                                             {'speed': 13.21835269590198, 'new': True, 'alert_tags': [], 'static': False,
#                                              'bounding_box': [58, 58.60136361849881, 0, 0], 'confidence': 1.0,
#                                              'times_lost_by_convnet': 0, 'type': 'car',
#                                              'created_at': '2018-04-05 18:12:51.381460', 'lost': False,
#                                              'tracking_id': 47, 'counted': False},
#                                             {'speed': 1.3050694084056036, 'new': True, 'alert_tags': [],
#                                              'static': False, 'bounding_box': [58, 5.481291515303534, 0, 0],
#                                              'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': 'car',
#                                              'created_at': '2018-04-05 18:12:51.384460', 'lost': False,
#                                              'tracking_id': 48, 'counted': False}]}
# car = {'speed': 8.630630962187603, 'new': True, 'alert_tags': [], 'static': False,
#        'bounding_box': [35, 388.6660809971818, 0, 0], 'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': 'bus',
#        'created_at': '2018-04-05 18:12:50.752424', 'lost': False, 'tracking_id': 2, 'counted': False}

with open("new_data.meta", 'w') as output:
    for i in range(0, 1000):
        x_test_1 = get_frame(x_test_1, lanes_array_test, lane_dimentions_test, "green", 20, 0, 1)
        output.write(str(x_test_1) + "\n")
# # extractVehiclesPerLane(frame, lanesArray)
