import cv2
import header
import numpy as np

def score_bubbles(img, net, bubbles, number_of_choices=5):
    """
    Returns a numpy matrix of the choices made in the image
    Args:
        img -- opencv imaged
        net -- NN classifier to use
        bubble -- list of (x,y,w,h), gotten from contour.grab_bubbles
        debug -- flag to to write a nice image
        number_of_choices -- choices for each question
    """

    def count_pixels(img):
        ret, thresh = cv2.threshold(question_img, 240, 255, cv2.THRESH_BINARY_INV)
        return cv2.countNonZero(thresh)

    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    except:
        gray = img
    matrix = []
    temporary_row  = []
    for (x,y,w,h) in bubbles:
        x = x - 2
        y = y - 2 
        w = w + 4 
        h = h + 4
        padded_bubble = gray[y : y + h , x : x + w ]
        resized_bubble = cv2.resize(padded_bubble, (26,26))
        resized_bubble = resized_bubble.flatten() / 255.0
        resized_bubble = resized_bubble.reshape(len(resized_bubble), 1)
        result = net.feedforward(resized_bubble)
        if np.argmax(result) == header.EMPTY:
            temporary_row.append(0)
            cv2.rectangle(img, (x,y), (x + w, y + h), (255,0,0),2) 
        else:
            temporary_row.append(1)
            cv2.rectangle(img, (x,y), (x + w, y + h), (0,255,0),2) 

        if len(temporary_row) == number_of_choices:
            matrix.append(temporary_row)
            temporary_row = []

    return (np.matrix(matrix), img)

if __name__ == '__main__':
    import contour
    import pprint
    import cPickle
    import network2
    import sys
    import header
    network = network2.load(header.network)
    img = cv2.imread(sys.argv[1])
    bubble_locations = contour.grab_bubbles(img, number_of_choices=5)
    scores = score_bubbles(img, network, bubble_locations)
    pprint.pprint(scores[0])
    



       

