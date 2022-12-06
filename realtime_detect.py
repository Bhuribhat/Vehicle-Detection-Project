import cv2
import time
import numpy as np

# Colors and Constant
GREEN  = (0, 255, 0)
RED    = (0, 0, 255)
BLUE   = (176, 130, 39)
ORANGE = (0, 127, 255)

# Create Car Classifier
CLF  = cv2.CascadeClassifier('./Resources/cars.xml')
FONT = cv2.FONT_HERSHEY_COMPLEX

# Configuration
offset     = 6
fps        = 60
min_width  = 80
min_height = 80
linePos    = 550


# get center position of the car
def center_position(x, y, w, h):
    center_x = x + (w // 2)
    center_y = y + (h // 2)
    return center_x, center_y


# real time detection using background subtractor
def count_using_bg_sub(show_detect):
    show_detect = show_detect.lower()
    CAP = cv2.VideoCapture('./Resources/video.mp4')

    # Initialize Background Subtructor
    subtract = cv2.bgsegm.createBackgroundSubtractorMOG()
    kernel   = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    # Configuration for detection
    car_count   = 0
    detect_car  = []

    while CAP.isOpened():
        duration = 1 / fps
        time.sleep(duration)

        # Read each frame of the video
        ret, frame = CAP.read()
        gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur  = cv2.GaussianBlur(gray, (3, 3), 5)

        # Subtract background, fill up object area and clear noise
        img_sub  = subtract.apply(blur)
        dilation = cv2.dilate(img_sub, np.ones((5, 5)))
        opening  = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel)
        contours = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

        # Count if the car pass this line
        cv2.line(frame, (25, linePos), (1200, linePos), BLUE, 2)

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            valid_contour = (w >= min_width) and (h >= min_height)
            if not valid_contour: continue

            cv2.rectangle(frame, (x, y), (x + w, y + h), GREEN, 2)
            center_car = center_position(x, y, w, h)
            detect_car.append(center_car)
            cv2.circle(frame, center_car, 4, RED, -1)

            # if center of the car pass the counting line
            for x, y in detect_car:
                if y < linePos + offset and y > linePos - offset:
                    cv2.line(frame, (25, linePos), (1200, linePos), ORANGE, 3)
                    detect_car.remove((x, y))
                    car_count += 1

        cv2.putText(frame, f"Car Detected: {car_count}", (50, 70), FONT, 2, RED, 3, cv2.LINE_AA)
        cv2.imshow('Cars Detection', frame)
        if show_detect.startswith('y'):
            cv2.imshow('Detector', opening)

        # Press 'ESC' Key to Quit
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()
    CAP.release()

    return car_count


# real time detection using model cars.xml (less accuracy)
def count_using_model_xml():
    CAP = cv2.VideoCapture('./Resources/video.mp4')

    # Configuration for detection
    detect_car = []
    car_count  = 0

    while CAP.isOpened():
        duration = 1 / fps
        time.sleep(duration)

        # Read first frame
        ret, frame = CAP.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 5)

        # Pass frame to our car classifier
        cars = CLF.detectMultiScale(
            blur, 
            scaleFactor = 1.2,    # how much the image size is reduced at each image scale
            minNeighbors = 2,     # how many neighbors each candidate rectangle should have to retain it
            minSize = (min_width, min_height)
        )

        # Count if the car pass this line
        cv2.line(frame, (25, linePos), (1200, linePos), BLUE, 2)

        # Extract bounding boxes for any car identified
        for (x, y, w, h) in cars:
            cv2.rectangle(frame, (x, y), (x + w, y + h), GREEN, 2)

            center = center_position(x, y, w, h)
            detect_car.append(center)
            cv2.circle(frame, center, 4, RED, -1)

            # if center of the car pass the counting line
            for (x, y) in detect_car:
                if (y < (linePos + offset)) and (y > (linePos - offset)):
                    cv2.line(frame, (25, linePos), (1200, linePos), ORANGE, 3)
                    detect_car.remove((x, y))
                    car_count += 1

        cv2.putText(frame, f"Car Detected: {car_count}", (50, 70), FONT, 2, RED, 3, cv2.LINE_AA)
        cv2.imshow('Cars Detection', frame)

        # Press 'ESC' Key to Quit
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()
    CAP.release()

    return car_count