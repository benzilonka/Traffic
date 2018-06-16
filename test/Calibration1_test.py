import unittest

import cv2
import numpy as np

from server.Parser import *
from server.Calibration_1 import *

class TestCalibiration1 (unittest.TestCase):

    lanes = [{"id" : 1, "points" : [[557,160],[263,422],[381,445],[565,163]]},{"id" : 2,"points" : [[568,166],[377,447],[478,456],[589,172]]}, {"id" : 3,"points" : [[591,173],[477,461],[626,461],[608,180],[599,176]]}]
    
    def test_wrap(self):
        frames = [{'objects': [{'confidence': 0.8, 'type': 'bus', 'static': True, 'created_at': '2017-12-28 07:39:00.933165', 'times_lost_by_convnet': 1, 'speed': 9.932450653113678, 'lost': False, 'alert_tags': [],\
                'tracking_id': 26598, 'bounding_box': [524, 232, 90, 132], 'new': False, 'counted': False}, {'confidence': 0.82, 'type': 'car', 'static': False, 'created_at': '2017-12-28 07:40:02.417256',\
                'times_lost_by_convnet': 5, 'speed': 7.883500926853487, 'lost': False, 'alert_tags': [], 'tracking_id': 26609, 'bounding_box': [377, 326, 68, 50], 'new': False, 'counted': True}, \
                {'confidence': 0.61, 'type': 'car', 'static': False, 'created_at': '2017-12-28 07:40:03.798450', 'times_lost_by_convnet': 8, 'speed': 6.006274599496227, 'lost': False, 'alert_tags': [],\
                'tracking_id': 26610, 'bounding_box': [424, 280, 41, 32], 'new': False, 'counted': False}], 'frame_index': 6348724},
        {'objects': [{'confidence': 0.67, 'type': 'bus', 'static': True, 'created_at': '2017-12-28 07:39:00.933165', 'times_lost_by_convnet': 0, 'speed': 9.404605335094026, 'lost': False, 'alert_tags': [],\
                'tracking_id': 26598, 'bounding_box': [525, 234, 92, 132], 'new': False, 'counted': False}, {'confidence': 0.82, 'type': 'car', 'static': False, 'created_at': '2017-12-28 07:40:02.417256', \
                'times_lost_by_convnet': 6, 'speed': 7.46454395779037, 'lost': False, 'alert_tags': [], 'tracking_id': 26609, 'bounding_box': [376, 328, 68, 50], 'new': False, 'counted': True}, \
                {'confidence': 0.61, 'type': 'car', 'static': False, 'created_at': '2017-12-28 07:40:03.798450', 'times_lost_by_convnet': 9, 'speed': 5.687080068679144, 'lost': False, 'alert_tags': [],\
                 'tracking_id': 26610, 'bounding_box': [424, 281, 41, 32], 'new': False, 'counted': False}], 'frame_index': 6348732},
        {'objects': [{'confidence': 0.67, 'type': 'bus', 'static': True, 'created_at': '2017-12-28 07:39:00.933165', 'times_lost_by_convnet': 1, 'speed': 0.0, 'lost': False, 'alert_tags': [],\
                'tracking_id': 26598, 'bounding_box': [525, 233, 91, 131], 'new': False, 'counted': False}, {'confidence': 0.82, 'type': 'car', 'static': False, 'created_at': '2017-12-28 07:40:02.417256',\
                'times_lost_by_convnet': 7, 'speed': 6.193790879731843, 'lost': False, 'alert_tags': [], 'tracking_id': 26609, 'bounding_box': [374, 329, 68, 51], 'new': False, 'counted': True},\
                {'confidence': 0.77, 'type': 'car', 'static': False, 'created_at': '2017-12-28 07:40:03.798450', 'times_lost_by_convnet': 0, 'speed': 18.3427258131377, 'lost': False, 'alert_tags': [],\
                 'tracking_id': 26610, 'bounding_box': [414, 289, 49, 35], 'new': False, 'counted': False}], 'frame_index': 6348741},
        {'objects': [{'confidence': 0.72, 'type': 'bus', 'static': True, 'created_at': '2017-12-28 07:39:00.933165', 'times_lost_by_convnet': 0, 'speed': 2.367083004736198, 'lost': False, 'alert_tags': [],\
                'tracking_id': 26598, 'bounding_box': [525, 232, 92, 132], 'new': False, 'counted': False}, {'confidence': 0.82, 'type': 'car', 'static': False, 'created_at': '2017-12-28 07:40:02.417256',\
                'times_lost_by_convnet': 8, 'speed': 8.171683387944562, 'lost': False, 'alert_tags': [], 'tracking_id': 26609, 'bounding_box': [373, 330, 69, 51], 'new': False, 'counted': True},\
                {'confidence': 0.77, 'type': 'car', 'static': False, 'created_at': '2017-12-28 07:40:03.798450', 'times_lost_by_convnet': 1, 'speed': 18.43761832602244, 'lost': False, 'alert_tags': [],\
                 'tracking_id': 26610, 'bounding_box': [413, 290, 49, 35], 'new': False, 'counted': False}], 'frame_index': 6348747},
        {'objects': [{'confidence': 0.72, 'type': 'bus', 'static': True, 'created_at': '2017-12-28 07:39:00.933165', 'times_lost_by_convnet': 0, 'speed': 0.0, 'lost': False, 'alert_tags': [],\
                'tracking_id': 26598, 'bounding_box': [525, 232, 91, 131], 'new': False, 'counted': False}, {'confidence': 0.82, 'type': 'car', 'static': False, 'created_at': '2017-12-28 07:40:02.417256',\
                'times_lost_by_convnet': 8, 'speed': 8.204357854743904, 'lost': False, 'alert_tags': [], 'tracking_id': 26609, 'bounding_box': [372, 331, 70, 52], 'new': False, 'counted': True},\
                {'confidence': 0.77, 'type': 'car', 'static': False, 'created_at': '2017-12-28 07:40:03.798450', 'times_lost_by_convnet': 1, 'speed': 18.51134117483986, 'lost': False, 'alert_tags': [],\
                 'tracking_id': 26610, 'bounding_box': [413, 290, 49, 35], 'new': False, 'counted': False}], 'frame_index': 6348753},
        {'objects': [{'confidence': 0.7, 'type': 'bus', 'static': True, 'created_at': '2017-12-28 07:39:00.933165', 'times_lost_by_convnet': 0, 'speed': 0.0, 'lost': False, 'alert_tags': [],\
                'tracking_id': 26598, 'bounding_box': [525, 232, 91, 134], 'new': False, 'counted': False}, {'confidence': 0.82, 'type': 'car', 'static': False, 'created_at': '2017-12-28 07:40:02.417256',\
                'times_lost_by_convnet': 10, 'speed': 8.614160325384688, 'lost': False, 'alert_tags': [], 'tracking_id': 26609, 'bounding_box': [370, 332, 70, 52], 'new': False, 'counted': True},\
                {'confidence': 0.76, 'type': 'car', 'static': False, 'created_at': '2017-12-28 07:40:03.798450', 'times_lost_by_convnet': 1, 'speed': 23.706263884080034, 'lost': False, 'alert_tags': [],\
                 'tracking_id': 26610, 'bounding_box': [410, 292, 52, 35], 'new': False, 'counted': False}], 'frame_index': 6348759}
        ]
        transformation_matrix = calibrate(self.lanes)

        for frame in frames:
            vehicles = get_vehicles(frame)
            fixed_frame = wrap(frame,transformation_matrix)
            i=0
            for vehicle in vehicles:
                input_vehicle = [vehicle[0],vehicle[1],1]
                result = np.matmul(transformation_matrix,input_vehicle)/(input_vehicle[0]*transformation_matrix[2][0]+input_vehicle[1]*transformation_matrix[2][1]+transformation_matrix[2][2])

                self.assertTrue(result[0]-fixed_frame['objects'][i]['bounding_box'][0]>=-0.001 or result[0]-fixed_frame['objects'][i]['bounding_box'][0]<=0.001)
                i = i+1
            

if __name__=='__main__':
    unittest.main()