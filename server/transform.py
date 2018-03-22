import numpy as np
import cv2
import matplotlib.pyplot as plt
import Parser


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



def getTransformation(lanes):
    rect = getRect(lanes)
    rect = np.array([rect], dtype = "float32")
    newRect = createRect(Parser.RECT_WIDTH, Parser.RECT_HEIGHT)
    newRect = np.array([newRect], dtype = "float32")
    transform = cv2.getPerspectiveTransform(rect, newRect)
    return transform


def wrap(frame, transformationMatrix):
    vehicles = Parser.getVehicles(frame)
    if len(vehicles) == 0:
        return frame
    
    vehicles = np.array([vehicles], dtype = "float32")

    vehicles = cv2.perspectiveTransform(vehicles, transformationMatrix)[0]
    vehicles = vehicles.tolist()
    i = 0
    for vehicle in vehicles:
        frame['objects'][i]['bounding_box'] = vehicle
        i = i + 1
        
    return frame

