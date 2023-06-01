import os
import urllib
import cv2
import requests


class Star:
    def __init__(self, id_star, name, x, y, r):
        self.x = x
        self.y = y
        self.name = name
        self.id = str(id_star)
        self.r = r


def draw_image(img_path, st: str):
    coordinates = []
    if st == "":
        image = cv2.imread(img_path)
        filename = "%s_processed.jpg" % img_path
        cv2.imwrite(filename, image)
        return filename
    st_split = st.split('[')[1].split(']')[0].split(',')
    count = 0
    for s in st_split:
        if '(' in s:
            count = 1
            id_star = int(s.split('(')[1])
        elif ')' in s:
            count = 0
            r = float(s.split(')')[0])
            new_star = Star(id_star, name, x, y, r)
            coordinates.append(new_star)
        else:
            count += 1
            if count == 2:
                name = s
            elif count == 3:
                x = float(s)
            elif count == 4:
                y = float(s)

    # Load image from file
    image = cv2.imread(img_path)

    # Draw circles on the image where there are stars
    for star in coordinates:
        cv2.circle(image, (int(star.x), int(star.y)), int(star.r) + 5, (0, 255, 255), 5)
        if star.y <= 20:
            id_y = int(star.y) + 65
        elif star.y > image.shape[0]:
            id_y = int(star.y) - 65
        else:
            id_y = int(star.y)
        if int(star.x) + int(star.r) + 5 <= 30:
            id_x = int(star.x) + int(star.r) + 70
        elif int(star.x) + int(star.r) + 400 > image.shape[1]:
            if int(star.x) + int(star.r) + 5 > image.shape[1]:
                id_x = int(star.x) + int(star.r) - 70
            else:
                id_x = int(star.x) + int(star.r) + 5
        else:
            id_x = int(star.x) + int(star.r) + 5
        text_position = (id_x, id_y)
        cv2.putText(image, star.id, text_position,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2.5,
                    (0, 255, 255), 5)
    filename = "%s_processed.jpg" % img_path
    cv2.imwrite(filename, image)
    return filename


def draw_by_id(img_path, st: str):
    file_path = 'image.jpeg'
    urllib.request.urlretrieve(img_path, file_path)
    str_split = st.split(',')
    id_star = int(str_split[0])
    name_star = str_split[1]
    x_star = float(str_split[2])
    y_star = float(str_split[3])
    r_star = float(str_split[4])
    image = cv2.imread(file_path)
    cv2.circle(image, (int(x_star), int(y_star)), int(r_star) + 5, (0, 255, 255), 5)

    if y_star <= 20:
        id_y = int(y_star) + 65
        name_y = int(y_star) + 150
    elif y_star > image.shape[0]:
        id_y = int(y_star) - 65
        name_y = int(y_star) - 150
    else:
        id_y = int(y_star)
        name_y = int(y_star) - 100
    if int(x_star) + int(r_star) + 5 <= 30:
        id_x = int(x_star) + int(r_star) + 70
        name_x = int(x_star) + int(r_star) + 55
    elif int(x_star) + int(r_star) + 400 > image.shape[1]:
        if int(x_star) + int(r_star) + 5 > image.shape[1]:
            id_x = int(x_star) + int(r_star) - 70
        else:
            id_x = int(x_star) + int(r_star) + 5
        name_x = int(x_star) + int(r_star) - 120
    else:
        id_x = int(x_star) + int(r_star) + 5
        name_x = int(x_star) + int(r_star) + 5
    name_position = (name_x, name_y)
    text_position = (id_x, id_y)
    cv2.putText(image, str(id_star), text_position,
                cv2.FONT_HERSHEY_SIMPLEX,
                2.5,
                (0, 255, 255), 5)
    cv2.putText(image, str(name_star), name_position,
                cv2.FONT_HERSHEY_SIMPLEX,
                2.5,
                (0, 255, 255), 5)

    filename = "%s_processed.jpg" % file_path
    cv2.imwrite(filename, image)
    return filename


def show_all(img_path, st: str):
    file_path = 'image.jpeg'
    urllib.request.urlretrieve(img_path, file_path)
    coordinates = []
    if st == "":
        image = cv2.imread(file_path)
        filename = "%s_processed.jpg" % file_path
        cv2.imwrite(filename, image)
        return filename
    st_split = st.split('[')[1].split(']')[0].split(',')
    count = 0
    for s in st_split:
        if '(' in s:
            count = 1
            id_star = int(s.split('(')[1])
        elif ')' in s:
            count = 0
            r = float(s.split(')')[0])
            new_star = Star(id_star, name, x, y, r)
            coordinates.append(new_star)
        else:
            count += 1
            if count == 2:
                name = s
            elif count == 3:
                x = float(s)
            elif count == 4:
                y = float(s)
    # Load image from file
    image = cv2.imread(file_path)
    # Draw circles on the image where there are stars
    for star in coordinates:
        cv2.circle(image, (int(star.x), int(star.y)), int(star.r) + 5, (0, 255, 255), 5)
        if star.y <= 20:
            id_y = int(star.y) + 65
            name_y = int(star.y) + 150
        elif star.y > image.shape[0]:
            id_y = int(star.y) - 65
            name_y = int(star.y) - 150
        else:
            id_y = int(star.y)
            name_y = int(star.y) - 100
        if int(star.x) + int(star.r) + 5 <= 30:
            id_x = int(star.x) + int(star.r) + 70
            name_x = int(star.x) + int(star.r) + 55
        elif int(star.x) + int(star.r) + 400 > image.shape[1]:
            if int(star.x) + int(star.r) + 5 > image.shape[1]:
                id_x = int(star.x) + int(star.r) - 70
            else:
                id_x = int(star.x) + int(star.r) + 5
            name_x = int(star.x) + int(star.r) - 120
        else:
            id_x = int(star.x) + int(star.r) + 5
            name_x = int(star.x) + int(star.r) + 5
        name_position = (name_x, name_y)
        text_position = (id_x, id_y)
        cv2.putText(image, star.id, text_position,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2.5,
                    (0, 255, 255), 5)
        cv2.putText(image, str(star.name), name_position,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2.5,
                    (0, 255, 255), 5)

    # Save the processed image to file
    filename = "%s_processed.jpg" % file_path
    cv2.imwrite(filename, image)
    return filename

s = "3,name3,2875.5,3193.0,4.25"
draw_by_id("https://firebasestorage.googleapis.com/v0/b/startracker-40c8d.appspot.com/o/processed%2FU2x5l9PazFPsqwCu56liBefZ0wl1%2F1685283513697?alt=media&token=aed5b260-93d1-43c6-84f7-89216d3a9c03", s)
