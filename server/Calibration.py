
def inside_polygon(point, points):
    """
    Return True if a coordinate (x, y) is inside a polygon defined by
    a list of verticies [(x1, y1), (x2, x2), ... , (xN, yN)].

    Reference: http://www.ariel.com.au/a/python-point-int-poly.html
    """
    x = point[0]
    y = point[1]
    n = len(points)
    inside = False
    p1x, p1y = points[0]
    for i in range(1, n + 1):
        p2x, p2y = points[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def get_incline(p1, p2):
    if p1[0] == p2[0] and p1[1] > p2[1]:
        return -9999999
    if p1[0] == p2[0] and p1[1] < p2[1]:
        return 9999999
    return (p1[1] - p2[1]) / (p1[0] - p2[0])


def is_lane_2(lane,point):

    return 0

def get_box(lane_points):
    ans =[]
    lane_points = sorted(lane_points)
    if lane_points[0][1] < lane_points[1][1]:
        ans.append(lane_points[1])
        ans.append(lane_points[0])
    else:
        ans.append(lane_points[0])
        ans.append(lane_points[1])
    if len(lane_points) == 4:
        if lane_points[3][1] < lane_points[2][1]:
            ans.append(lane_points[3])
            ans.append(lane_points[2])
        else:
            ans.append(lane_points[2])
            ans.append(lane_points[3])
    return ans

def is_lane(lane, point):
    lane = lane['points']

    min_x = lane[0]
    min_y = lane[0]
    max_x = lane[0]
    max_y = lane[0]
    x = point[0]
    y = point[1]
    for i in range(0, 4):
        if min_x[0] > lane[i][0]:
            min_x = lane[i]
        if max_x[0] < lane[i][0]:
            max_x = lane[i]
    for i in range(0, 4):
        if min_y[1] > lane[i][1] != min_x[1] and lane[i][0] != min_x[0]:
            min_y = lane[i]
        if max_y[1] < lane[i][1] != max_x[1] and lane[i][0] != max_x[0]:
            max_y = lane[i]
    lane_points_x = [min_y[0],min_x[0],max_x[0],max_y[0]]
    lane_points_y = [min_y[1],min_x[1],max_x[1],max_y[1]]
    if min(lane_points_x) > x or max(lane_points_x) < x:
        print("1")
        return False

    if min(lane_points_y) > y or max(lane_points_y) < y:
        print("2")
        return False
    if max_y[0] < x and get_incline(max_y, max_x) < get_incline(max_y, [x, y]):
        print("3")
        return False

    if max_y[0] > x and get_incline(min_x, max_y) < get_incline(min_x, [x, y]):
        print("4")
        return False

    if min_y[0] < x and get_incline(min_y, max_x) > get_incline(min_y, [x, y]):
        print("5")
        return False
    return True


def get_lane(bb, info):
    lanes = [info[0], info[1], info[2]]
    vehicle_box = [[bb[0], bb[1]], [bb[0] + bb[2], bb[1]], [bb[0], bb[1] + bb[3]], [bb[0] + bb[2], bb[1] + bb[3]]]
    #print(vehicle_box)
    points_on_lane = [0, 0, 0]
    for i in range(0, 3):
        for j in range(0, 4):
            if inside_polygon(vehicle_box[j], lanes[i]['points']):
                points_on_lane[i] += 1
    # print(points_on_lane)
    # if max(points_on_lane) >= 2:
    return points_on_lane.index(max(points_on_lane))*75 + 475
    # print("x:",x ,"y:",y)
    x = bb[0]
    y = bb[1]
    if y > 270:
        if x > 500:
            return 550
        elif x > 400:
            return 500
        else:
            return 450
    elif y > 200:
        if x > 500:
            return 550
        elif x > 440:
            return 500
        else:
            return 450
    elif y > 180:
        if x > 500:
            return 550
        elif x > 490:
            return 500
        else:
            return 450
    else:
        if x > 510:
            return 550
        elif x > 500:
            return 500
        else:
            return 450


def fix_frame(frame, info):
    ans = []
    for i in range(0, len(frame['objects'])):
        object = frame['objects'][i]
        lane = get_lane(object['bounding_box'], info)
        object['bounding_box'][0] = lane
        vehicle_width = 1.85
        if object['type'] == 'bus':
            vehicle_width = 2.59
        y = vehicle_width * 583.04
        object['bounding_box'][1] = 350 - (10 * (y / object['bounding_box'][2]))
        ans.append(object)
    return ans


def fix_json(json_object):
    for i in range(0, len(json_object)):
        json_object[i] = fix_frame(0, json_object[i])





#
# print(get_lane([535, 306, 61, 55], [[[557, 160], [263, 422], [381, 445], [565, 163]], [[568, 166], [377, 447],
#                               [478, 456], [589, 172]], [[591, 173], [477, 461], [626, 461], [608, 180], [599, 176]]]))
#
# print(get_lane([387, 212, 105, 130], [[[557, 160], [263, 422], [381, 445], [565, 163]], [[568, 166], [377, 447],
#                               [478, 456], [589, 172]], [[591, 173], [477, 461], [626, 461], [608, 180], [599, 176]]]))
# print(is_lane([[557, 160], [263, 422], [381, 445], [565, 163]], 387, 212))
# print(is_lane([[557, 160], [263, 422], [381, 445], [565, 163]], 387, 212))
# print(is_lane([[557, 160], [263, 422], [381, 445], [565, 163]], 387, 212))
# print(is_lane([[557, 160], [263, 422], [381, 445], [565, 163]], 387, 212))
# print(is_lane([[557, 160], [263, 422], [381, 445], [565, 163]], 387, 212))
# print(is_lane([[557, 160], [263, 422], [381, 445], [565, 163]], 387, 212))

