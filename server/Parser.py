import json
from typing import List

import Clean_Data
import Calibration_1
import Data_Analysis

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
    for frame in jsons:
        if frame:
            frame = strip_json(frame)
            frames.append(frame)
    transformation_matrix = Calibration_1.calibrate(info['tracking_params']['lanes'])
    for frame in frames:
        fixed_frame = Calibration_1.wrap(frame, transformation_matrix)
        fixed_frame = Data_Analysis.add_pre_alerts(fixed_frame, lane_ratio)
        fixed_frames.append(fixed_frame)
    Data_Analysis.add_post_alerts(fixed_frames, REACT_DIRECTION, 0)
    return fixed_frames


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
