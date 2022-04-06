import cv2
import numpy as np

cap = cv2.VideoCapture(0)


while(True):

    ret, frame = cap.read()

    b, g, r = cv2.split(frame)

    processed = 1.0*r+0.5*g-1.5*b
    rect, thresh = cv2.threshold(processed,50,255,0)

    M = cv2.moments(thresh)

    cX = 0
    cY = 0


    if M['m00'] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
        cv2.putText(frame, "loptica", (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)



    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    black = cv2.inRange(hsv,(0,0,0),(255,120,90))

    indencies = np.where(black == 255)

    ymin = np.amin(indencies[0])
    ymax = np.amax(indencies[0])

    xmin = np.amin(indencies[1])
    xmax = np.amax(indencies[1])

    plate_cx = xmin + (xmax - xmin)/2
    plate_cy = ymin + (ymax - ymin)/2

    x_pos = cX - plate_cx
    y_pos = plate_cy - cY

    cv2.putText(frame, "X : {}".format(x_pos), (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, "Y : {}".format(y_pos), (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 150, 0), 2)

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
