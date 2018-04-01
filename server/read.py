import os
import json

import Calibration_2
import Parser

'''def read_meta_file(name):
    metadata = open('metas/' + name, 'r')
    i = 0
    frame = metadata.readline()[:-1].replace("'", '"').replace("False", "false").replace("True", "true")
    while frame:
        if not os.path.exists('frames/' + name[:-5]):
            os.makedirs('frames/' + name[:-5])
        file = open('frames/' + name[:-5] + '/f' + str(i) + '.json', 'w')
        #edit the line (json) before writing it
        #for objc in frame['objects']:
        #    print(objc['type'])

        file.write(frame)
        frame = metadata.readline()[:-1].replace("'", '"').replace("False", "false").replace("True", "true")
        file.close()
        i += 1
'''


def read_meta_file():
    file = open("C:\\Users\\Avner\\PycharmProjects\\traffic data\\examples\\big_28.12.2017-04_55_56.meta", 'r')
    info_file = open("C:\\Users\\Avner\\PycharmProjects\\traffic data\\examples\\big_28.12.2017-04_55_56.json", 'r')
    return Parser.fix_file(file.read(), json.loads(info_file.read()))



print (read_meta_file())





'''def ReadAllMetas():
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir("metas") if isfile(join("metas", f))]
    for i in range(0, len(onlyfiles)):
        #print(onlyfiles[i])
        read_meta_file(onlyfiles[i])
'''





'''def changeJsons(path):
    slash = len(path)
    for i in range (0, len(path)):
        if path[i]=='/':
            slash=1
            break
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(path[slash:]) if isfile(path[slash:], f)]
    for i in range(0, len(onlyfiles)):
'''

'''def fixFrames():
    from os import listdir
    from os.path import isfile, join
    paths = [f for f in listdir("frames") if isfile(join("frames", f))]
    for i in range(0, len(paths)):
        changeJsons(paths[i])

'''





# if calibration.is_lane([[557, 160], [263,422], [381, 445], [565, 163]], 387, 212) or calibration.is_lane([[591,173],[477,461],[626,461 ],[608,180],[599,176]],387, 212) or calibration.is_lane([[568,166],[377,447],[478,456],[589,172]], 387, 212):
#     print("works")
# is_lane([[591,173],[477,461],[626,461 ],[608,180],[599,176]],387, 212)
# is_lane([568,166],[377,447],[478,456],[589,172], 387, 212)
#print (read_meta_file())
# change_json({"objects": [{"confidence": 0.92, "type": "bus", "static": True, "created_at": "2017-12-28 04:55:02.750086", "times_lost_by_convnet": 1, "speed": 13.65099956558118, "lost": False, "alert_tags": [], "tracking_id": 24488, "bounding_box": [386, 212, 105, 130], "new": False, "counted": False}, {"confidence": 0.58, "type": "car", "static": False, "created_at": "2017-12-28 04:55:41.927352", "times_lost_by_convnet": 1, "speed": 3.138550189376427, "lost": False, "alert_tags": [], "tracking_id": 24491, "bounding_box": [535, 304, 61, 57], "new": False, "counted": False}], "frame_index": 5443497})
