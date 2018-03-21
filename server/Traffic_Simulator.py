import math
import random

e = 2.71828182846
def get_first_frame():
    return {'frame_index': 0, 'objects': []}


def add_car(ans):
    object = {'speed': 0, 'new': False, 'alert_tags': [], 'static': False, 'bounding_box': [0, 0, 0, 0], 'confidence': 1.0,
              'times_lost_by_convnet': 0, 'type': 'car', 'created_at': '2017-12-25 16:05:01.223143', 'lost': False, 'tracking_id': 10000, 'counted': False}
    pass


def get_frame(current_frame, light, traffic_density):
    # x = (pow(traffic_density, 3) * pow(e, (-1 * traffic_density)))/6
    x = random.uniform(0, 1)
    ans  = {'frame_index': 7765, 'objects': []}
    if x >= traffic_density:
        ans = add_car(ans)
    print(x)
    return 0
get_frame(0, 0, 1)