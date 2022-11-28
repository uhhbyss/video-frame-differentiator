import scipy
import os
import numpy as np
import cv2
from skimage.metrics import structural_similarity as ssim


def count_frames(path):
    video = cv2.VideoCapture(path)
    total = 0

    total = video.get(cv2.CAP_PROP_FRAME_COUNT)
    video.release()
    return total


'''getting input name'''
print("Input the name of the video\n")
newPath = input("PATH: ")
cap = cv2.VideoCapture(newPath + str(".mp4"))
frames = count_frames(newPath + str(".mp4"))
fps = cap.get(cv2.CAP_PROP_FPS)

current = 1

'''captures initial frame'''
cap.set(cv2.CAP_PROP_POS_FRAMES, current)
_, currentFrame = cap.read()


'''loops through all frames at each 3 seconds to see if they are matching or not'''
while (current <= frames):
    '''recaptures the frame'''
    cap.set(cv2.CAP_PROP_POS_FRAMES, current)
    _, nextFrame = cap.read()

    '''converts images to greyscale'''
    grayA = cv2.cvtColor(currentFrame, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(nextFrame, cv2.COLOR_BGR2GRAY)

    '''compares the frames'''
    (simIndex, diff) = ssim(grayA, grayB, full=True)

    '''saves image if it is new'''
    if (simIndex < 0.9):
        cv2.imwrite("frame%d.jpg" % current, nextFrame)
        print("saved frame %d out of %d" % (current, frames))
    '''shifts the frame window'''
    currentFrame = nextFrame
    '''increments frame count by around 3 seconds'''
    current += (10*fps)

cap.release()
os.remove(newPath + str(".mp4"))
print("DONE!\nfilename: %s" % (newPath))
