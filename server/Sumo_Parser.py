import os
import sys
import subprocess
import Data_Analysis

from datetime import datetime
from xml.dom import minidom
import xml.etree.cElementTree as ET

SUMO_DIRECTION = 1


def add_traffic_light_status(frames, angle, traffic_timing):
    for direction in traffic_timing[angle]:
        param_list = traffic_timing[angle][direction]
        light = get_light_from_time(frames[angle]["frame_index"], traffic_timing["total"], param_list[0],
                                    param_list[1], param_list[2])
        frames[angle]["light_status"][direction] = light


def create_frames(time_step, traffic_timing, gui_boundaries, sumo_boundaries):
    index = 0
    out_jsons = [[], [], [], []]
    sumo_y_len = sumo_boundaries[0][1][1] - sumo_boundaries[0][1][0]
    lane_ratio = gui_boundaries[0][1] / sumo_y_len
    prev_frames = {0: None, 90: None, 180: None, 270: None}
    stop_line = 648
    lanes = {"right": [55, 65], "forward": [45, 55], "left": [35, 45]}
    for step in time_step:
        frames = {0: {"frame_index": index, "light_status": {}, "objects": []},
                  90: {"frame_index": index, "light_status": {}, "objects": []},
                  180: {"frame_index": index, "light_status": {}, "objects": []},
                  270: {"frame_index": index, "light_status": {}, "objects": []}}
        add_vehicles_to_frame(step, frames, gui_boundaries, sumo_boundaries)
        for angle in frames.keys():
            add_traffic_light_status(frames, angle, traffic_timing)
        Data_Analysis.add_alerts(frames[0], prev_frames[0], lane_ratio, SUMO_DIRECTION, 0, stop_line, lanes)
        Data_Analysis.add_alerts(frames[90], prev_frames[90], lane_ratio, SUMO_DIRECTION, 0, stop_line, lanes)
        Data_Analysis.add_alerts(frames[180], prev_frames[180], lane_ratio, SUMO_DIRECTION, 0, stop_line, lanes)
        Data_Analysis.add_alerts(frames[270], prev_frames[270], lane_ratio, SUMO_DIRECTION, 0, stop_line, lanes)
        out_jsons[0].append(frames[0])
        out_jsons[1].append(frames[90])
        out_jsons[2].append(frames[180])
        out_jsons[3].append(frames[270])
        prev_frames = frames
        index += 1
    return out_jsons


def get_bbox(x_coordinate, y_coordinate, angle, gui_dimension, sumo_boundaries):
    ans = []
    sumo_x_len = sumo_boundaries[angle][0][1] - sumo_boundaries[angle][0][0]
    sumo_y_len = sumo_boundaries[angle][1][1] - sumo_boundaries[angle][1][0]
    x_coordinate -= sumo_boundaries[angle][0][0]
    y_coordinate -= sumo_boundaries[angle][1][0]
    x_ratio = gui_dimension[angle][0] / sumo_x_len
    y_ratio = gui_dimension[angle][1] / sumo_y_len
    if angle == 0:
        ans.append(x_ratio * x_coordinate)
        ans.append(y_ratio * y_coordinate)
    elif angle == 180:
        ans.append(x_ratio * x_coordinate)
        ans.append(gui_dimension[angle][1] - y_ratio * y_coordinate)
    elif angle == 90:
        ans.append(y_ratio * y_coordinate)
        ans.append((x_ratio * x_coordinate))
    else:
        ans.append(y_ratio * y_coordinate)
        ans.append(gui_dimension[angle][0] - x_ratio * x_coordinate)
    ans.append(0)
    ans.append(0)
    return ans


def add_vehicles_to_frame(step, frame, gui_boundaries, sumo_boundaries):
    for vehicle in step.childNodes:
        if vehicle.attributes is not None:
            vehicle_type = vehicle.attributes['type'].value
            speed = float(vehicle.attributes['speed'].value)
            angle = int(float(vehicle.attributes['angle'].value))
            if angle == 0 or angle == 90 or angle == 180 or angle == 270:
                bbox = get_bbox(float(vehicle.attributes['x'].value), float(vehicle.attributes['y'].value),
                                angle, gui_boundaries, sumo_boundaries)
                new_date_and_time = datetime.now()
                fixed_date_and_time = new_date_and_time.strftime('%Y-%m-%d %H:%M:%S.' +
                                                                 str(new_date_and_time.microsecond))
                tracking_id = int(vehicle.attributes['id'].value)
                frame[angle]["objects"].append(
                    {"speed": speed, "alert_tags": [], "bounding_box": bbox,
                     "confidence": 1.0, "times_lost_by_convnet": 0, "type": vehicle_type,
                     "created_at": fixed_date_and_time, "tracking_id": tracking_id})


def write_jsons_to_files(jsons_ans, output_files):
    index = 0
    for json in jsons_ans:
        with open(output_files[index], 'w') as output:
            index += 1
            output.write("[")
            flag = False
            for frame in json:
                if flag:
                    output.write(",")
                flag = True
                output.write(str(frame).replace("'", "\"") + "\n")
            output.write("]")


def get_light_from_time(n, total, start_g, end_g, end_y):
    n_modulo = n % total
    if start_g <= n_modulo <= end_g:
        return "green"
    elif end_g < n_modulo <= end_y:
        return "yellow"
    else:
        return "red"


def get_light_timing(net_file_name):
    file = minidom.parse(net_file_name)
    raw_input = file.getElementsByTagName('phase')
    if not raw_input:
        return {}
    light_ans = {"total": 0, 0: {"right": [0, 0, 0], "forward": [0, 0, 0], "left": [0, 0, 0]},
                 90: {"right": [0, 0, 0], "forward": [0, 0, 0], "left": [0, 0, 0]},
                 180: {"right": [0, 0, 0], "forward": [0, 0, 0], "left": [0, 0, 0]},
                 270: {"right": [0, 0, 0], "forward": [0, 0, 0], "left": [0, 0, 0]}}
    for phase in raw_input:
        duration = int(phase.attributes['duration'].value)
        state = phase.attributes['state'].value
        s_index = 0
        light_ans["total"] += duration
        for angle in light_ans.keys():
            if angle != "total":
                for direction in light_ans[angle].keys():
                    if state[s_index] == 'g':
                        light_ans[angle][direction][1] += light_ans[angle][direction][0] + duration - 1
                    elif state[s_index] == 'y':
                        light_ans[angle][direction][2] = light_ans[angle][direction][1] + duration
                        if light_ans[angle][direction][1] == 0:
                            light_ans[angle][direction][2] -= 1
                    if light_ans[angle][direction][1] == 0:
                        light_ans[angle][direction][0] += duration
                    s_index += 1
                    if direction == "right":
                        s_index += 1
        s_index += 1
    return light_ans


def sumo_parse(in_file_name, net_file_name, gui_boundaries, sumo_boundaries):
    file = minidom.parse(in_file_name)
    time_step = file.getElementsByTagName('timestep')
    jsons_ans = create_frames(time_step, get_light_timing(net_file_name), gui_boundaries, sumo_boundaries)
    write_jsons_to_files(jsons_ans, ["data_set_0.json", "data_set_1.json", "data_set_2.json", "data_set_3.json"])
    return jsons_ans


def add_vehicle_types(vehicle_info, file_name):
    root = ET.Element("additional")
    v_type_element = ET.SubElement(root, "vTypeDistribution", id="myType")
    for v_type in vehicle_info.keys():
        ET.SubElement(v_type_element, "vType", id=v_type, maxSpeed=str(vehicle_info[v_type][0]),
                      sigma=str(vehicle_info[v_type][1]), accel=str(vehicle_info[v_type][2]),
                      decel=str(vehicle_info[v_type][3]), minGap=str(vehicle_info[v_type][4]),
                      lcStrategic=str(vehicle_info[v_type][5]), jmDriveAfterRedTime=str(vehicle_info[v_type][6]))
    tree = ET.ElementTree(root)
    tree.write(file_name)


# vehicle info example values are: max speed, sigma, acceleration, deceleration, minimum gap between cars,
# lane change policy (1-inf), make red crossing optional (-1 to 0)
# for more info see http://sumo.dlr.de/wiki/Definition_of_Vehicles,_Vehicle_Types,_and_Routes
vehicle_info1 = {"car": [70, 0.8, 2.6, 4.5, 2.5, 10, 0], "bus": [70, 0.2, 2.1, 4.3, 2.5, 1, -1]}

# fix: the configuration file need to be defined in here from scratch
def get_simulation(duration, cars_per_second, vehicle_info):
    if 'SUMO_HOME' in os.environ:
        sumo = os.path.join(os.environ['SUMO_HOME'], 'bin', 'sumo.exe')
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        random_trips_path = os.path.join(os.environ['SUMO_HOME'], 'tools\\randomTrips.py')
        sys.path.append(tools)
    else:
        sys.exit("please declare environment variable 'SUMO_HOME'")
    sumo_coordinates = {0: [[500., 520.], [370, 650]], 90: [[370, 650], [500., 520.]],
                        180: [[500., 520.], [370, 650]], 270: [[370, 650], [500., 520.]]}
    gui_coordinates = {0: [65, 1420], 180: [65, 1420], 90: [1420, 65], 270: [1420, 65]}
    p_value = str(1. / float(cars_per_second))
    sumoCmd = ['py', random_trips_path, "-n", "cross_1.net.xml", '-o', "cross_1.rou.xml",
               "-e", str(duration), "-p", p_value, "--trip-attributes=type=\"myType\""
               ]
    subprocess.call(sumoCmd)
    add_vehicle_types(vehicle_info, "cross_1.add.xml")
    sumoCmd = [sumo, "-c", "cross_1.sumocfg", "-e", str(duration), "--fcd-output", "cross_1_trace.xml"]
    subprocess.call(sumoCmd)
    return sumo_parse("cross_1_trace.xml", "cross_1.net.xml", gui_coordinates, sumo_coordinates)


get_simulation(100, 0.5, vehicle_info1)