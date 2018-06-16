import numpy as np
import cv2
from server import Parser


def create_rect(width, height):
    return [[0, 0], [0, height], [width, height], [width, 0]]


def get_rect(lanes):
    leftMost = lanes[0]["points"]
    rightMost = lanes[len(lanes) - 1]["points"]
    rect = [
        leftMost[0],
        leftMost[1],
        rightMost[2],
        rightMost[3]
    ]
    return rect


def calibrate(lanes):
    rect = get_rect(lanes)
    rect = np.array([rect], dtype="float32")
    newRect = create_rect(Parser.RECT_WIDTH, Parser.RECT_HEIGHT)
    newRect = np.array([newRect], dtype="float32")
    transform = cv2.getPerspectiveTransform(rect, newRect)
    return transform


def wrap(frame, transformation_matrix):
    vehicles = Parser.get_vehicles(frame)
    if len(vehicles) == 0:
        return frame
    vehicles = np.array([vehicles], dtype="float32")
    vehicles = cv2.perspectiveTransform(vehicles, transformation_matrix)[0]
    vehicles = vehicles.tolist()
    i = 0
    for vehicle in vehicles:
        frame['objects'][i]['bounding_box'] = vehicle
        i = i + 1
    return frame
