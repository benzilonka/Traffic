import json
import Calibration
import Clean_Data
import Knowledge_Base
import transform


def fix_file(data,info):
    jsons = Clean_Data.clean(data)
    frames = []
    fixed_frames = []
    i = 0
    for frame in jsons:
        if frame:
            frame = strip_json(frame)
            frames.append(frame)
    
    transformationMatrix = transform.getTransformation(info['tracking_params']['lanes'])
    for frame in frames:
        fixed_frame = transform.wrap(frame, transformationMatrix)
        fixed_frames.append(fixed_frame)

    return fixed_frames


def strip_json(json_file):
    data = []
    jsFile = json.loads(json_file)
    for objc in jsFile['objects']:
        updatedObj = {"type": objc['type'], "created_at": objc['created_at'], "tracking_id": objc['tracking_id'],
                      "bounding_box": objc['bounding_box']}
        data.append(updatedObj)
    jsFile['objects'] = data
    return jsFile
