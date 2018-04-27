import os
import sys
import subprocess
from datetime import datetime
from xml.dom import minidom


def create_frames(time_step, gui_boundaries, sumo_boundaries):
    index = 0
    out_jsons = [[], [], [], []]
    for step in time_step:
        frames = {0: {"frame_index": index, "objects": []}, 90: {"frame_index": index, "objects": []},
                  180: {"frame_index": index, "objects": []}, 270: {"frame_index": index, "objects": []}}
        add_vehicles_to_frame(step, frames, gui_boundaries, sumo_boundaries)
        out_jsons[0].append(frames[0])
        out_jsons[1].append(frames[90])
        out_jsons[2].append(frames[180])
        out_jsons[3].append(frames[270])
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
    '''index = 0
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
            output.write("]")'''



def sumo_parse(in_file_name, gui_boundaries, sumo_boundaries):
    file = minidom.parse(in_file_name)
    time_step = file.getElementsByTagName('timestep')
    jsons_ans = create_frames(time_step, gui_boundaries, sumo_boundaries)
    write_jsons_to_files(jsons_ans, ["data_set_0.json", "data_set_1.json", "data_set_2.json", "data_set_3.json"])
    return jsons_ans


def get_simulation(duration, cars_per_second, max_speed):
    if 'SUMO_HOME' in os.environ:
        sumo = os.path.join(os.environ['SUMO_HOME'], 'bin', 'sumo.exe')
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        randomTripsPath = os.path.join(os.environ['SUMO_HOME'], 'tools\\randomTrips.py')
        sys.path.append(tools)
    else:
        sys.exit("please declare environment variable 'SUMO_HOME'")
    sumo_coordinates = {0: [[500., 520.], [370, 650]], 90: [[370, 650], [500., 520.]],
                        180: [[500., 520.], [370, 650]], 270: [[370, 650], [500., 520.]]}
    gui_coordinates = {0: [70, 1320], 180: [70, 1320], 90: [1320, 70], 270: [1320, 70]}
    sumoCmd = ['py', randomTripsPath, "-n", "cross_1.net.xml", '-o', "cross_1.rou.xml"
        ]
    subprocess.call(sumoCmd)
    sumoCmd = [sumo, "-c", "cross_1.sumocfg", "--fcd-output", "cross_1_trace.xml"]
    subprocess.call(sumoCmd)
    return sumo_parse("cross_1_trace.xml", gui_coordinates, sumo_coordinates)


#print(get_simulation(1, 0.5, 0))
