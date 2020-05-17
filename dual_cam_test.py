import cv2
cap0 = cv2.VideoCapture(0);
cap0.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap0.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

cap1 = cv2.VideoCapture(2);
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
        ret0, frame1 = cap0.read()
        ret1, frame2 = cap1.read()

        print('Retval cap0: ' ,ret0)
        print('Retval cap1: ', ret1)

        if ret0:
                cv2.imshow('frame1', frame1)
        if ret1:
                cv2.imshow('frame2', frame2)

        if cv2.waitKey(1) & 0xFF == ord('q'):
                break

cap0.release()
cap1.release()
cv2.destroyAllWindows()
