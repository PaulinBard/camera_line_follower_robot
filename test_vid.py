import cv2

cap = cv2.VideoCapture(0)
cap.set(3,320)
cap.set(4,240)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
#    gray = transfo(frame)#cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
#    frame= cv2.resize(frame, (320,240))
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
