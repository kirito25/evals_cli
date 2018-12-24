import cv2
from  imutils import contours
import imutils
import numpy as np
import sys

def grab_bubbles(img, number_of_choices=5):
    """
    Takes as input an opencv image and returns a list
    of (x, y, w, h) where x, y is the top left of
    the rectangle enclosing a circle
    """
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    except:
        gray = img # must already have been in gray scale
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    list_of_contours = []
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)
        area = cv2.contourArea(c)
        if w >= 15 and w <= 70 and h >= 15 and h <= 50 and ar >= 0.5 and ar <= 3.1 and area <= 500:
            list_of_contours.append(c)
    cnts = []
    list_of_contours = contours.sort_contours(list_of_contours, method="top-to-bottom")[0]
    for (q, i) in enumerate(np.arange(0, len(list_of_contours), number_of_choices)):
        cnts.append(contours.sort_contours(list_of_contours[i:i+number_of_choices])[0])

    result = []
    for i in cnts:
        for c in i:
            (x, y, w, h) = cv2.boundingRect(c)
            result.append((x, y, w, h))

    return result

def grab_answers(img):
    """
    Takes as input an opencv image and returns a list
    of (x, y, w, h) where x, y is the top left of
    the rectangle enclosing a circle
    """
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    except:
        gray = img # must already have been in gray scale
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    list_of_contours = []
    for c in cnts:
        area = cv2.contourArea(c)
        if area >= 1000:
            list_of_contours.append(c)
    return [ cv2.boundingRect(c) for c in contours.sort_contours(list_of_contours, method="top-to-bottom")[0] ]


if __name__ == '__main__':
    filename = sys.argv[1]
    img = cv2.imread(filename)
    rectangles = grab_answers(img)
    cv2.drawContours(img, rectangles, -1, (0,255,0), 3)
    cv2.imwrite("test.jpg", img)
