import os
import sys
from datetime import datetime
from xml.dom import minidom
from subprocess import call

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    randomTripsPath = os.path.join(os.environ['SUMO_HOME'], 'tools\\randomTrips.py')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

def create_frames(time_step, out_file_name, gui_boundaries, sumo_boundaries):
    index = 0
    with open(out_file_name, 'w') as output:
        for step in time_step:
            frame = {'frame_index': index, 'objects': []}
            add_vehicles_to_frame(step, frame, gui_boundaries, sumo_boundaries)
            output.write(str(frame) + "\n")
            index += 1


def get_bbox(x_coordinate, y_coordinate, angle, gui_boundaries, sumo_boundaries):
    ans = []
    gui_x_len = gui_boundaries[angle][0][1] - gui_boundaries[angle][0][0]
    gui_y_len = gui_boundaries[angle][1][1] - gui_boundaries[angle][1][0]
    sumo_x_len = sumo_boundaries[angle][0][1] - sumo_boundaries[angle][0][0]
    sumo_y_len = sumo_boundaries[angle][1][1] - sumo_boundaries[angle][1][0]
    x_coordinate -= sumo_boundaries[angle][0][0]
    y_coordinate -= sumo_boundaries[angle][1][0]
    print(gui_x_len, gui_y_len, sumo_x_len, sumo_y_len)
    x_ratio = gui_x_len / sumo_x_len
    y_ratio = gui_y_len / sumo_y_len
    ans.append(x_ratio * x_coordinate)
    ans.append(y_ratio * y_coordinate)
    ans.append(0)
    ans.append(0)
    return ans


def add_vehicles_to_frame(step, frame, gui_boundaries, sumo_boundaries):
    for vehicle in step.childNodes:
        if vehicle.attributes is not None:
            print(vehicle.attributes['id'].value)
            vehicle_type = vehicle.attributes['type'].value
            speed = float(vehicle.attributes['speed'].value)
            bbox = get_bbox(float(vehicle.attributes['x'].value), float(vehicle.attributes['y'].value),
                            int(float(vehicle.attributes['angle'].value)), gui_boundaries, sumo_boundaries)
            new_date_and_time = datetime.now()
            fixed_date_and_time = new_date_and_time.strftime('%Y-%m-%d %H:%M:%S.' + str(new_date_and_time.microsecond))
            tracking_id = int(vehicle.attributes['id'].value.split('_')[1])
            frame['objects'].append(
                {'speed': speed, 'new': True, 'alert_tags': [], 'static': False, 'bounding_box': bbox,
                 'confidence': 1.0, 'times_lost_by_convnet': 0, 'type': vehicle_type,
                 'created_at': fixed_date_and_time, 'lost': False, 'tracking_id': tracking_id,
                 'counted': False})


def sumo_parse(in_file_name, out_file_name, gui_boundaries, sumo_boundaries):
    file = minidom.parse(in_file_name)
    time_step = file.getElementsByTagName('timestep')
    create_frames(time_step, out_file_name, gui_boundaries, sumo_boundaries)


sumo_coordinates = {0: [[510.05, 513.25], [0, 1020]], 90: [[0, 1020], [506.75, 509.95]],
                    180: [[506.75, 509.95], [0, 1020]], 270: [[0, 1020], [510.05, 513.25]]}
gui_coordinates = {0: [[0, 1470], [0, 70]], 90: [[0, 1470], [0, 70]],
                   180: [[0, 1470], [0, 70]], 270: [[0, 1470], [0, 70]]}

import traci
def get_simulation():
    sumoCmd =[randomTripsPath, '-n', 3600]
    traci.start(sumoCmd)
    step = 0
    while step < 1000:
        traci.simulationStep()
        if traci.inductionloop.getLastStepVehicleNumber("0") > 0:
            traci.trafficlight.setRedYellowGreenState("0", "GrGr")
        step += 1

    traci.close()

get_simulation()