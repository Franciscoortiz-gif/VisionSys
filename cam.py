import cv2


#capture from camera at location 0
cap = cv2.VideoCapture(1)
#set the width and height, and UNSUCCESSFULLY set the exposure time
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1024)
cap.set(cv2.CAP_PROP_EXPOSURE, 0.1)
#cap.set(cv2.CAP_PROP_POS_MSEC) #Current position of the video file in milliseconds.
#cap.set(cv2.CAP_PROP_POS_FRAMES)# 0-based index of the frame to be decoded/captured next.
#cap.set(cv2.CAP_PROP_POS_AVI_RATIO)# Relative position of the video file
#cap.set(cv2.CAP_PROP_FRAME_WIDTH)# Width of the frames in the video stream.
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT)# Height of the frames in the video stream.
cap.set(cv2.CAP_PROP_FPS, 30)# Frame rate.
#cap.set(cv2.CAP_PROP_FOURCC)# 4-character code of codec.
#cap.set(cv2.CAP_PROP_FRAME_COUNT)# Number of frames in the video file.
#cap.set(cv2.CAP_PROP_FORMAT )#Format of the Mat objects returned by retrieve() .
#cap.set(cv2.CAP_PROP_MODE)# Backend-specific value indicating the current capture mode.
cap.set(cv2.CAP_PROP_BRIGHTNESS, 56)# Brightness of the image (only for cameras).
cap.set(cv2.CAP_PROP_CONTRAST, 56)# Contrast of the image (only for cameras).
cap.set(cv2.CAP_PROP_SATURATION, 127)# Saturation of the image (only for cameras).
cap.set(cv2.CAP_PROP_HUE, 127)# Hue of the image (only for cameras).
cap.set(cv2.CAP_PROP_GAIN, 1)# Gain of the image (only for cameras).
cap.set(cv2.CAP_PROP_EXPOSURE, 110.0)# Exposure (only for cameras).
#cap.set(cv2.CAP_PROP_CONVERT_RGB)# Boolean flags indicating whether images should be converted to RGB.
#cap.set(cv2.CAP_PROP_WHITE_BALANCE, 5200.0)# Currently unsupported
#cap.set(cv2.CAP_PROP_RECTIFICATION)# 

while True:
    ret, img = cap.read()
    cv2.imshow("input", img)
    #cv2.imshow("thresholded", imgray*thresh2)

    key = cv2.waitKey(10)
    if key == 27:
        break


cv2.destroyAllWindows() 
cv2.VideoCapture(0).release()
