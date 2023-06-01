import datetime
import math
import urllib

import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

import cv2
from fastapi import FastAPI, HTTPException

from schemas import AuthDetails


class Star:
    def __init__(self, id_star, name, x, y, r):
        self.x = x
        self.y = y
        self.name = name
        self.id = str(id_star)
        self.r = r


def get_names(image_url):
    image = cv2.imread(image_url)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to the image
    _, thresh = cv2.threshold(gray, 180, 220, cv2.THRESH_BINARY)

    # Find the contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize variables
    coordinates = []
    check = []
    count = 0

    # Loop through the contours
    for i, c in enumerate(contours):
        # Get the coordinates and size of the bounding rectangle around the contour
        x, y, w, h = cv2.boundingRect(c)

        # Calculate the radius of the circle that encloses the rectangle
        r = float((w + h) / 4)

        # Calculate the average brightness of the region inside the rectangle
        b = int(gray[y:y + h, x:x + w].mean())

        # Calculate the center coordinates of the rectangle
        x = x + w / 2
        y = y + h / 2

        # Create a Star object with the calculated parameters
        st = Star(count, "name" + str(count), x, y, r)

        # Check if the coordinates have already been added
        ans = (x, y)
        if ans in check:
            continue

        # Add the Star object to the list of coordinates
        coordinates.append(st)
        check.append(ans)
        count += 1

    st = "["
    count = 0
    for i in coordinates:
        if count != 0:
            st += ","
        s = "(" + str(i.id) + "," + str(i.name) + "," + str(i.x) + "," + str(i.y) + "," + str(i.r) + ")"
        count += 1
        st += s
    st += "]"
    if st.__eq__("[]"):
        return ""
    return st


app = FastAPI()


@app.post('/algorithm')
def login(auth_details: AuthDetails):
    ImagePath = auth_details.ImagePath
    file_path = 'image.jpeg'
    urllib.request.urlretrieve(ImagePath, file_path)
    ans = get_names(file_path)
    return {'stars_id': ans}
