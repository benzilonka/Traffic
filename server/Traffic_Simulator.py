import random
import numpy as np
from datetime import datetime

e = 2.71828182846


def get_first_frame():
    return {'frame_index': 0, 'objects': []}


def delete_cars(frame, lane):
    vehicle_list = frame['objects']
    index = 0
    while index < len(vehicle_list):
        current_bbox = vehicle_list[index]['bounding_box']
        # yPosition = BBox[1], lane[3]/lane[4] are locations of the end of the lane
        # Delete locations of vehicles that passed the location of the end of the lane
        if current_bbox[1] < lane[3][1]:
            del (vehicle_list[index])
        index += 1
    return frame


def add_car(frame, lane):
    # lane is an object containing four points of the lane
    vehicle_list = frame['objects']
    if len(vehicle_list) > 0:
        new_tracking_id = vehicle_list[len(vehicle_list) - 1]['tracking_id'] + 1
    else:
        new_tracking_id = 1
    new_type = gen_type_of_vehicle()
    new_speed = gen_new_speed(new_type)
    new_bbox = gen_bounding_box(lane)
    new_date_and_time = datetime.now()
    fixed_date_and_time = new_date_and_time.strftime('%Y-%m-%d %H:%M:%S.' + str(new_date_and_time.microsecond))
    vehicle_list.append({'speed': new_speed, 'new': True, 'alert_tags': [], 'static': False, 'bounding_box': new_bbox,
                         'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': new_type,
                         'created_at': fixed_date_and_time, 'lost': False, 'tracking_id': new_tracking_id,
                         'counted': False})
    return frame


def stopping_distance_function(speed):
    return ((2.0502645502645 * pow(10, -15) * pow(speed, 10))
            - (1.4605379188712 * pow(10, -12) * pow(speed, 9))
            + (4.56944444444 * pow(10, -10) * pow(speed, 8))
            - (8.25072751322 * pow(10, -8) * pow(speed, 7))
            + (9.499625000000 * pow(10, -6) * pow(speed, 6))
            - (0.000726897 * pow(speed, 5)) + (0.0373303 * pow(speed, 4))
            - (1.26654 * pow(speed, 3)) + (27.081 * speed * speed) - (327.869 * speed) + 1703.8)


# def get_frame(current_frame, lane, light, traffic_density):
#     x = (pow(traffic_density, 3) * pow(e, (-1 * traffic_density))) / 6


def gen_bounding_box(lane_locations):
    # X location will be in the middle of the lane
    x_point = int((lane_locations[0][0] + lane_locations[1][0]) / 2)
    # Y location will be where the lane begin
    y_point = lane_locations[0][1]
    bbox = [x_point, y_point, 0, 0]
    return bbox


def gen_new_speed(type_of_vehicle):
    # Generate vehicle speed in range 10 to 120 km/h with bigger probability to lower speeds (10-70 km/h)
    if type_of_vehicle == 'car':
        threshold = 0.7
    elif type_of_vehicle == 'bus':
        threshold = 0.8
    else:
        threshold = 0.9
    param = random.uniform(0, 1)
    if param <= threshold:
        # Generate speed in range 10-70
        speed = np.random.choice(np.arange(10.0, 70.0))
    else:
        # Generate speed in range 71-120
        speed = np.random.choice(np.arange(71.0, 120.0))
    # Convert speed from km/h to m/s
    speed = speed / 3.6
    return speed


def gen_type_of_vehicle():
    # There is more probability to generate car over bus and truck
    return np.random.choice(['car', 'bus', 'truck'], p=[0.7, 0.2, 0.1])


def extract_vehicles_per_lane(frame, lanes_list):
    vehicleLst = frame['objects']
    vehiclesPerLane = []
    for lane in lanes_list:
        element = {'lane': lane, 'objects': []}
        for vehicle in vehicleLst:
            bbox = vehicle['bounding_box']
            # Check if vehicle is in the range of the x and y coordinates of current lane
            # lane[0][0]- x in start location , lane[3][0]- x in end location
            # lane[0][1]- y in start location , lane[3][1]- y in end location
            if lane[0][0] <= bbox[0] <= lane[1][0]:
                element['objects'].append(vehicle)
        # sort vehicles by their y loactions
        notSorted = element['objects']
        element['objects'] = sorted(notSorted, key=help_sorted)
        vehiclesPerLane.append(element)
    return vehiclesPerLane


def help_sorted(vehicle):
    # Compare by y locations
    return vehicle['bounding_box'][1]


def get_ratio(gui_dimensions, lane_dimensions):
    return np.amax(gui_dimensions, axis=0)[1] / lane_dimensions[1]


def advance_cars(cars_and_lanes, lane_dimension):
    for cars_lane in cars_and_lanes:
        for car in cars_lane['objects']:
            speed_per_frame = float(car['speed'] / 15)
            vehicle_advanced = float(speed_per_frame * get_ratio(cars_lane['lane'], lane_dimension))
            car['bounding_box'][1] += vehicle_advanced
    return cars_and_lanes


def adjust_speed(cars_and_lanes, light):
    for cars_in_lane in cars_and_lanes:
        last_car_y_coordinate = cars_in_lane['lane'][2][1]
        for car in cars_in_lane['objects']:
            dis = last_car_y_coordinate - car['bounding_box'][1]
            ttc = float(dis / car['speed'])
    return cars_and_lanes


def get_frame(current_frame, lanes_list, lane_dimensions, light, traffic_density):
    frame_index = current_frame['frame_index']
    frame_index += 1
    print(current_frame)
    cars_and_lanes = advance_cars(extract_vehicles_per_lane(current_frame, lanes_list), lane_dimensions)
    cars_and_lanes = adjust_speed(cars_and_lanes, light)
    cars = []
    for car_lane in cars_and_lanes:
        for car in car_lane['objects']:
            cars.append(car[i])
    ans = {'frame_index': frame_index, 'objects': cars}
    if random.uniform(0, 1) >= traffic_density:
        ans = add_car(ans, lanes_list[int(random.uniform(0, len(lanes_list)))])

    # print(current_frame)
    # print (cars_in_lanes)

    # for cars_in_lane in cars_in_lanes:
    #     for i in range(0, len(cars_in_lane['objects'])):
    #         if i == 0:
    #             if light == "green":
    #                 cars_in_lane['objects'][i]['speed'] += random.uniform(-4.5, 4.5)*((34 - cars_in_lane['objects'][i]['speed']) / 34)
    #             elif light == "orange":
    #                   dis = cars_in_lane['objects'][i + 1]['bounding_box'][1] - cars_in_lane['objects'][i]['bounding_box'][1]
    #                   dis *= 5  # the ratio between real distance and pixels on the screen
    #                   if cars_in_lane[i]['speed']*3 < dis:
    #                       cars_in_lane['objects'][i]['speed'] += random.uniform(-4.5, 4.5) * ((34 - cars_in_lane['objects'][i]['speed']) / 34)
    #                   else:
    #                       cars_in_lane['objects'][i]['speed'] += random.uniform(-4.5, 0) * ((34 - cars_in_lane['objects'][i]['speed']) / 34)
    #             else:
    #                 # dis = cars_in_lane[i + 1]['bounding_box'][1] - cars_in_lane[i]['bounding_box'][1]
    #                 # dis *= 5  # the ratio between real distance and pixels on the screen
    #                 # sd = stopping_distences(cars_in_lane[i]['speed'] * 3.6)
    #                 # if dis < sd:
    #                 #     cars_in_lane[i]['speed'] += random.uniform(-4.5, -1)
    #                 # else:
    #                 cars_in_lane['objects'][i]['speed'] += random.uniform(-4.5, 0)
    #         else:
    #             dis = cars_in_lane['objects'][i + 1]['bounding_box'][1] - cars_in_lane['objects'][i]['bounding_box'][1]
    #             dis *= 5  # the ratio between real distance and pixels on the screen
    #             ttc = dis / cars_in_lane['objects'][i]['speed']
    #             if ttc > 2:
    #                 cars_in_lane['objects'][i]['speed'] += random.uniform(-2, 4.5) * ((34 - cars_in_lane['objects'][i]['speed']) / 34)
    #             elif 1 < ttc < 2:
    #                 cars_in_lane['objects'][i]['speed'] += random.uniform(-2.5, 2.5) * ((34 - cars_in_lane['objects'][i]['speed']) / 34)
    #             else:
    #                 cars_in_lane['objects'][i]['speed'] += random.uniform(-4.5, -1)
    #          # else:
    # #print(stopping_distences(120))
    #
    # #ans = deleteCars(ans, lanesList)
    # vehiclesInLanesArr = extract_vehicles_per_lane(ans, lanesList)
    return ans


lanes_array = [[[0, 0], [23, 0], [0, 700], [23, 700]], [[23, 0], [47, 0], [23, 700], [47, 700]],
               [[47, 0], [70, 0], [47, 700], [70, 700]]]
lane_dimentions = [4.6, 200]
x = {'frame_index': 0, 'objects': []}
# print(get_ratio(lanes_array[0], lane_dimentions))
with open("new_data.meta", 'w') as output:
    for i in range(0, 100):
        x = get_frame(x, lanes_array, lane_dimentions, "green", 0.25)
        output.write(str(x) + "\n")
# extractVehiclesPerLane(frame, lanesArray)
