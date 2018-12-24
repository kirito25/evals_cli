import os
import numpy as np
import cv2
import contour
from score_bubbles import *
import network2
import shutil
 
def alignImages(im1, im2):
    """
    Align one image to another.
    The first argument is the image you want to align to
    The second argument is the image you want to aling.
    """
    MAX_FEATURES = 500
    GOOD_MATCH_PERCENT = 0.15
    # Convert images to grayscale
    try:
        im1Gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
        im2Gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
    except:
        im1Gray = im1
        im2Gray = im2


    # Detect ORB features and compute descriptors.
    orb = cv2.ORB_create(MAX_FEATURES)
    keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
    keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)

    # Match features.
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(descriptors1, descriptors2, None)

    # Sort matches by score
    matches.sort(key=lambda x: x.distance, reverse=False)

    # Remove not so good matches
    numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
    matches = matches[:numGoodMatches]

    #imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
    #cv2.imwrite("matches.jpg", imMatches)
    #sys.exit(-1)

    # Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt

    # Find homography
    h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

    # Use homography
    height, width, channels = im2.shape
    return cv2.warpPerspective(im1, h, (width, height))


def bubbles(bubble_path, net, debug_path=None, align=False):
    i = 0
    bubble_path = shutil.abspath(bubble_path)
    bubble_files        = sorted(os.listdir(bubble_path))
    top_img             = cv2.imread(bubble_path + "/" + bubble_files[i])
    bubble_locations    = contour.grab_bubbles(top_img)
    # use a copy because we want the top img to remain unchanged
    score               = score_bubbles(top_img.copy() , net, bubble_locations)

    result = score[0]
    if not debug_path is None:
        analyzed_image_path = "%s/%05d.jpg" % (debug_path, i)
        #print "Input file %s to %s" % (bubble_files[0], analyzed_image_path)
        cv2.imwrite(analyzed_image_path, score[1])

    i += 1
    for bubble in bubble_files[1:]:
        img =  cv2.imread(bubble_path + "/" + bubble)
        if not align:
            bubble_locations = contour.grab_bubbles(img)
        else:
            img = alignImages(img, top_img)
        score   = score_bubbles(img, net, bubble_locations)
        result += score[0]
        if not debug_path is None:
            analyzed_image_path = "%s/%05d.jpg" % (debug_path, i)
            #print "Input file %s to %s" % (bubble, analyzed_image_path)
            cv2.imwrite(analyzed_image_path, score[1])
        i += 1
    return result


def longforms(longform_path, dest, decide=False):
    longform_path = shutil.abspath(longform_path)
    longforms_files     = sorted(os.listdir(longform_path))
    top_img             = cv2.imread(longform_path + "/" + longforms_files[0])
    questions_location  = contour.grab_answers(top_img)
    result = {}
    for i, longform in enumerate(longforms_files):
        img     = cv2.imread(longform_path  + "/" + longform)
#        img     = alignImages(img, top_img)
        for j, question_contour in enumerate(questions_location):
            (x, y, w, h) = question_contour
            question_img = img[y : y + h , x : x + w ]

            if decide:
                question_img = cv2.cvtColor(question_img, cv2.COLOR_BGR2GRAY)
                ret, thresh = cv2.threshold(question_img, 240, 255, cv2.THRESH_BINARY_INV)
                if cv2.countNonZero(thresh) > 5500:
                    print "GOOD %d  %s/q%02d-%s" % (cv2.countNonZero(thresh), dest, j, longform)
                    cv2.imwrite("%s/q%02d-%s" % (dest, j, longform), question_img)
                else:
                    print "BAD %d  %s/bad-q%02d-%s" % (cv2.countNonZero(thresh), dest, j, longform)
                    cv2.imwrite("%s/bad-q%02d-%s" % (dest, j, longform), question_img)
            else:
                cv2.imwrite("%s/q%02d-%s" % (dest, j, longform), question_img)
            try:
                result[j].append("%s/q%02d-%s" % (dest, j, longform))
            except KeyError:
                result[i] = [ "%s/q%02d-%s" % (dest, j, longform) ]
    return result


 
if __name__ == '__main__':
    import sys
    #net = network2.load(header.network)
    #pprint.pprint(analyze_pdf(sys.argv[1], net, debug=True))
    longforms(sys.argv[1], "/tmp")


