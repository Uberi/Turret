# PYSERIAL AND OPENCV IS REQUIRED TO RUN THIS PROGRAM

import numpy
import cv2

import serial
import serial.tools.list_ports

import sys
import time

CAMERA_INDEX = 1
MOVEMENT_SCALE_X = 0.1
MOVEMENT_SCALE_Y = 0.3
GRAVITY_COEFFICIENT = 0.0003
NAME = "detect"

def convert_image(image):
    "Convert an OpenCV image into a PyGame image."
    return pygame.image.frombuffer(image.tostring(), image.shape[1::-1], "RGB")

def detect(camera):
    s, image = camera.read()
    if not s: raise Exception("Could not read from camera.")
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # create grayscale version of image
    cv2.equalizeHist(grayscale, grayscale)
    faces = face_cascade.detectMultiScale(
        grayscale,
        scaleFactor = 1.3, # image scaling factor for classifier levels
        minNeighbors = 4,
        flags = cv2.cv.CV_HAAR_SCALE_IMAGE,
        minSize = (30, 30), # smallest possible detection size
    )
    return faces, image, grayscale

import os.path as path

def init_camera(name):
    assert face_cascade != None
    camera = cv2.VideoCapture(CAMERA_INDEX)
    if not camera.isOpened(): raise Exception("Could not open camera.")
    cv2.namedWindow(name, cv2.WINDOW_AUTOSIZE)
    return camera

def init_serial():
    # obtain a list of available COM ports
    try: hardware_name, description, _ = next(serial.tools.list_ports.comports())
    except StopIteration:
        print("No serial ports found.")
        sys.exit(1)

    print("Opening serial port " + hardware_name + ": " + description)
    return serial.Serial(hardware_name)

def port_move(port, yaw, pitch):
    if yaw < 0: yaw = 0
    if yaw > 180: yaw = 180
    if pitch < 0: pitch = 0
    if pitch > 180: pitch = 180
    print("Moving turret position to yaw " + str(yaw) + " and pitch " + str(pitch))
    #port.write(bytes("y %d\n" % yaw, "UTF-8"))
    #port.write(bytes("p %d\n" % pitch, "UTF-8"))
    port.write(bytes("y %d\n" % yaw))
    port.write(bytes("p %d\n" % pitch))

def fire(port):
    #port.write(bytes("f\n", "UTF-8"))
    port.write(bytes("f\n"))

base_path = path.dirname(__file__)
face_cascade = cv2.CascadeClassifier(path.join(base_path, "haarcascade_frontalface_default.xml"))

camera = init_camera(NAME)
port = init_serial()

x, y, w, h = None, None, None, None
try:
    while True:
        faces, image, grayscale = detect(camera)
        image = cv2.cvtColor(grayscale, cv2.COLOR_GRAY2BGR) # create color image from greyscale
        width, height = image.shape[1], image.shape[0]
        color = (255, 255, 255)
        if len(faces):
            x, y, w, h = max(faces, key=lambda face: face[2] * face[3])
            
            # compensate for gravity
            gravity = int(GRAVITY_COEFFICIENT * (width - w) ** 2)
            y -= gravity
            
            cx, cy = width / 2, height / 2
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 5)
            center_x, center_y = x + w / 2, y + h / 2
            cv2.line(image, (center_x, center_y), (center_x, center_y + gravity), (0, 0, 255), 2)
            port_move(port, (width - x) * MOVEMENT_SCALE_X, y * MOVEMENT_SCALE_Y)
            print x, width
        
        cv2.imshow(NAME, image)
        k = cv2.waitKey(100)
        if k == 27: # escape key
            break
        elif k == 32: # space key
            fire(port)
finally:
    cv2.destroyWindow(NAME)
    port.close()
sys.exit(0)