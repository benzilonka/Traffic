import numpy as np
import cv2
import matplotlib.pyplot as plt

RECT_WIDTH = 70
RECT_HEIGHT = 700

def createRect(width, height):
    return [[0, 0], [0, height], [width, height], [width, 0]]

def getRect(lanes):
    leftMost = lanes[0]["points"]
    rightMost = lanes[len(lanes) - 1]["points"]
    rect = [
            leftMost[0],
            leftMost[1],
            rightMost[2],
            rightMost[3]
        ]
    return rect

def getVehicles(frame): 
    points = []
    for vehicle in frame['objects']:
        box = vehicle['bounding_box']
        x = box[0] + (box[2] / 2)
        y = box[1] + (box[3] / 2)
        points.append([x, y])
    return points



def getTransformation(lanes):
    rect = getRect(lanes)
    rect = np.array([rect], dtype = "float32")
    newRect = createRect(RECT_WIDTH, RECT_HEIGHT)
    newRect = np.array([newRect], dtype = "float32")
    transform = cv2.getPerspectiveTransform(rect, newRect)
    return transform


def wrap(frame, transformationMatrix):
    vehicles = getVehicles(frame)
    if len(vehicles) == 0:
        return frame
    
    vehicles = np.array([vehicles], dtype = "float32")
    print(vehicles[-10:])       

    vehicles = cv2.perspectiveTransform(vehicles, transformationMatrix)[0]
    vehicles = vehicles.tolist()
    i = 0
    for vehicle in vehicles:
        frame['objects'][i]['bounding_box'] = vehicle
        i = i + 1
        
    return frame



'''
xs = [point[0] for point in rect]
ys = [point[1] for point in rect]

plt.scatter(xs, ys, c='b')

xs = [point[0] for point in vehicles[0]]
ys = [point[1] for point in vehicles[0]]

plt.scatter(xs, ys, c='r')

plt.show()
'''





'''
xs = [point[0] for point in newRect]
ys = [point[1] for point in newRect]

plt.scatter(xs, ys, c='b')

xs = [point[0] for point in vehicles]
ys = [point[1] for point in vehicles]

plt.scatter(xs, ys, c='r')

plt.show()
'''