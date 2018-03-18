def get_incline(p1, p2):
    if p1[0] == p2[0] and p1[1] > p2[1]:
        return -9999999
    if p1[0] == p2[0] and p1[1] < p2[1]:
        return 9999999
    return (p1[1] - p2[1]) / (p1[0] - p2[0])


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
    # print("min y:", min_y)
    # print("min x:", min_x)
    # print("max y:", max_y)
    # print("max x:", max_x)
    if min_x[0] > x or max_x[0] < x:
        return False
    if min_y[1] > y or max_y[1] < y:
        return False
    if get_incline(min_x, min_y) > get_incline(min_x, [x, y]):
        return False
    if max_y[0] < x and get_incline(max_y, max_x) < get_incline(max_y, [x, y]):
        return False
    if max_y[0] > x and get_incline(min_x, max_y) < get_incline(min_x, [x, y]):
        return False
    if min_y[0] < x and get_incline(min_y, max_x) > get_incline(min_y, [x, y]):

        return False
    return True


def get_lane(bb, info):
    lanes = [info[0], info[1], info[2]]
    vehicle_box = [[bb[0], bb[1]], [bb[0] + bb[2], bb[1]], [bb[0], bb[1] + bb[3]], [bb[0] + bb[2], bb[1] + bb[3]]]
    points_on_lane = [0, 0, 0]
    for i in range(0, 3):
        for j in range(0, 4):
            if is_lane(lanes[i], vehicle_box[j]):
                points_on_lane[i] += 1
    if max(points_on_lane) > 2:
        return points_on_lane.index(max(points_on_lane))*100 + 450
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
        y = object['bounding_box'][2] * 583.04
        object['bounding_box'][1] = y / vehicle_width
        ans.append(object)
    return ans


def fix_json(json_object):
    for i in range(0, len(json_object)):
        json_object[i] = fix_frame(0, json_object[i])


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

