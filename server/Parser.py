import json
import Calibration
import Clean_Data
import Knowledge_Base


def fix_file(data,info):
    jsons = Clean_Data.clean(data)
    ans = []
    for frame in jsons:
        if frame:
            frame = strip_json(frame)
            frame = Calibration.fix_frame(frame, info['tracking_params']['lanes'])
            ans.append(frame)
        Knowledge_Base.store(ans)
    return ans


def strip_json(json_file):
    data = []
    jsFile = json.loads(json_file)
    for objc in jsFile['objects']:
        updatedObj = {"type": objc['type'], "created_at": objc['created_at'], "tracking_id": objc['tracking_id'],
                      "bounding_box": objc['bounding_box']}
        data.append(updatedObj)
    jsFile['objects'] = data
    return jsFile