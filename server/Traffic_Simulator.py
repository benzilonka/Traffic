import math
import random


e = 2.71828182846
def get_first_frame():
    return {'frame_index': 0, 'objects': []}


def add_car(vehicalList, lane):
    object = {'speed': 0, 'new': False, 'alert_tags': [], 'static': False, 'bounding_box': [0, 0, 0, 0], 'confidence': 1.0,
              'times_lost_by_convnet': 0, 'type': 'car', 'created_at': '2017-12-25 16:05:01.223143', 'lost': False, 'tracking_id': 10000, 'counted': False}
    pass


def get_cars():
    pass

def stopping_distences(x):
    return ((2.0502645502645*pow(10, -15)*pow(x, 10))
         - (1.4605379188712*pow(10, -12)*pow(x, 9))
         + (4.56944444444*pow(10, -10)*pow(x, 8))
         - (8.25072751322*pow(10, -8)*pow(x, 7))
         + (9.499625000000*pow(10, -6)*pow(x, 6))
         - (0.000726897*pow(x, 5))+(0.0373303*pow(x, 4))
         - (1.26654*pow(x, 3)) + (27.081*x*x) - (327.869*x) + 1703.8)

def get_frame(current_frame, lane, light, traffic_density):
    #x = (pow(traffic_density, 3) * pow(e, (-1 * traffic_density)))/6
    x = random.uniform(0, 1)
    frame_index = current_frame['frame_index']
    frame_index += 1
    ans = {'frame_index': frame_index, 'objects': []}
    if x >= traffic_density:
        ans = add_car(ans, lane[int(random.uniform(0,len(lane)))])
    cars_in_lanes = get_cars()
    for cars_in_lane in cars_in_lanes:
        for i in range(0, len(cars_in_lane)):
            if i == 0:
                if light == "green":
                    cars_in_lane[i]['speed'] += random.uniform(-4.5, 4.5)*((34 - cars_in_lane[i]['speed']) / 34)
                elif light == "orange":
                      dis = cars_in_lane[i + 1]['bounding_box'][1] - cars_in_lane[i]['bounding_box'][1]
                      dis *= 5  # the ratio between real distance and pixels on the screen
                      if cars_in_lane[i]['speed']*3 < dis:
                          cars_in_lane[i]['speed'] += random.uniform(-4.5, 4.5) * ((34 - cars_in_lane[i]['speed']) / 34)
                      else:
                          cars_in_lane[i]['speed'] += random.uniform(-4.5, 0) * ((34 - cars_in_lane[i]['speed']) / 34)
                else:
                    dis = cars_in_lane[i + 1]['bounding_box'][1] - cars_in_lane[i]['bounding_box'][1]
                    dis *= 5  # the ratio between real distance and pixels on the screen
                    sd = stopping_distences(cars_in_lane[i]['speed'] * 3.6)
                    if dis < sd:
                        cars_in_lane[i]['speed'] += random.uniform(-4.5, -1)
                    else:
                        cars_in_lane[i]['speed'] += random.uniform(-4.5, 0)
            else:
                dis = cars_in_lane[i + 1]['bounding_box'][1] - cars_in_lane[i]['bounding_box'][1]
                dis *= 5  # the ratio between real distance and pixels on the screen
                ttc = dis / cars_in_lane[i]['speed']
                if ttc > 2:
                    cars_in_lane[i]['speed'] += random.uniform(-2, 4.5) * ((34 - cars_in_lane[i]['speed']) / 34)
                elif 1 < ttc < 2:
                    cars_in_lane[i]['speed'] += random.uniform(-2.5, 2.5) * ((34 - cars_in_lane[i]['speed']) / 34)
                else:
                    cars_in_lane[i]['speed'] += random.uniform(-4.5, -1)
             # else:
    return ans
print(stopping_distences(120))