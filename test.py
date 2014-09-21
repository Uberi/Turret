# this program requires OpenCV

import numpy
import cv2

import time

CAMERA_INDEX = 0

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

def overlay(image, overlay, x, y, w = None, h = None):
    w, h = min(w or overlay.shape[1], image.shape[1]), min(h or overlay.shape[0], image.shape[0])
    try:
        overlay = cv2.resize(overlay, (w, h), 0, 0, 0, cv2.INTER_NEAREST)
    except Exception, e:
        print e
        input()
    alpha = overlay[:, :, 3] / 255.0
    remaining_alpha = 1.0 - alpha
    for channel in range(0,3):
        image[y:y + h, x:x + w, channel] = overlay[:, :, channel] * alpha + image[y:y + h, x:x + w, channel] * remaining_alpha

import os.path as path

base_path = path.dirname(__file__)
hud = cv2.imread(path.join(base_path, "hud.png"), -1) # load image with alpha channel
face_cascade = cv2.CascadeClassifier(path.join(base_path, "haarcascade_frontalface_default.xml"))
assert hud != None and face_cascade != None
camera = cv2.VideoCapture(CAMERA_INDEX)
if not camera.isOpened(): raise Exception("Could not open camera.")
name = "detect"
cv2.namedWindow(name, cv2.WINDOW_AUTOSIZE)
while True:
    faces, image, grayscale = detect(camera)
    image = cv2.cvtColor(grayscale, cv2.COLOR_GRAY2BGR) # create color image from greyscale
    width, height = image.shape[1], image.shape[0]
    cx, cy = width / 2, height / 2
    overlay(image, hud, 0, 0, width, height)
    color = (255, 255, 255)
    if len(faces):
        x, y, w, h = max(faces, key=lambda face: face[2] * face[3])
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 5)
        cv2.putText(image, "MEATBAG", (x, y + h + w / 8), cv2.FONT_HERSHEY_SIMPLEX, w / 300.0, (0, 0, 255), 2)
        if x + w < cx or x > cx or y + h < cy or y > cy:
            cv2.putText(image, "TARGET AQUIRED", (20, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        else:
            color = (0, 0, 255)
            cv2.putText(image, "TARGET LOCKED", (20, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.line(image, (x + w / 2, y + h / 2), (cx, cy), (0, 0, 255), 2)
    cv2.line(image, (cx - 40, cy), (cx + 40, cy), color, 2)
    cv2.line(image, (cx, cy - 40), (cx, cy + 40), color, 2)
    cv2.ellipse(image, (cx, cy), (20, 20), 0, 0, 360, color, 2)
    
    cv2.imshow(name, image)
    k = cv2.waitKey(100)
    if k == 27: # escape key
        break
cv2.destroyWindow(name)
