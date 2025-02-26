import ffmpeg
import cv2

vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#cv2.imshow('frame', frame)

record = (
    ffmpeg
    .input(vid)
    .output('out.mp4')
    .run()
)

record