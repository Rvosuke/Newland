import cv2
import time

capture_instance = cv2.VideoCapture(0)
time.sleep(2)

print("The camera is now {capture_instance.isOpened()} to capture images.")

capture_instance.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
capture_instance.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

cv2.namedWindow("image_window", flags=cv2.WINDOW_NORMAL|cv2.WINDOW_KEEPRATIO|cv2.WINDOW_GUI_EXPANDED)

ret, frame = capture_instance.read()

cv2.imshow("image_window", frame)
cv2.waitKey(100)

cv2.imwrite("1.png", frame)

capture_instance.release()
cv2.destroyAllWindows()