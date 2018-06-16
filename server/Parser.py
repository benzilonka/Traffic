import json
from server import Clean_Data
from server import Calibration_1
from server import Data_Analysis

RECT_WIDTH = 35
RECT_HEIGHT = 690
REACT_DIRECTION = 1
PIXEL_PER_METER = 5
MAX_TTC = 3
LANE_WIDTH = 23


def fix_file(data, info):
    jsons = Clean_Data.clean(data)
    frames = []
    fixed_frames = []
    # need to fix and get the ratio from the data
    lane_ratio = 5
    lane_stop = 650
    react_lanes = {"right": [0, 11.66], "forward": [11.66, 23.33], "left": [23.33, 35]}
    for frame in jsons:
        if frame:
            frame = strip_json(frame)
            frames.append(frame)
    transformation_matrix = Calibration_1.calibrate(info['tracking_params']['lanes'])
    prev_frame = None
    for frame in frames:
        fixed_frame = Calibration_1.wrap(frame, transformation_matrix)
        Data_Analysis.add_alerts(fixed_frame, prev_frame, lane_ratio, REACT_DIRECTION, 0, lane_stop, react_lanes,
                                 react_lanes, False)
        fixed_frames.append(fixed_frame)
        prev_frame = fixed_frame
    return {
        'frames': fixed_frames, 
        'statistics': Data_Analysis.get_statistic_report(fixed_frames)
    }


def strip_json(js_file):
    data = []
    for objc in js_file['objects']:
        updatedObj = {"type": objc['type'], "created_at": objc['created_at'], "tracking_id": objc['tracking_id'],
                      "bounding_box": objc['bounding_box'], "speed": objc['speed'], }
        data.append(updatedObj)
    js_file['objects'] = data
    return js_file


def get_vehicles(frame):
    points = []
    for vehicle in frame['objects']:
        box = vehicle['bounding_box']
        if len(box) == 4:
            x = box[0] + ((box[2] * 2) / 3)
            y = box[1] + ((box[3] * 4) / 5)
        else:
            x = box[0]
            y = box[1]
        points.append([x, y])
    return points



