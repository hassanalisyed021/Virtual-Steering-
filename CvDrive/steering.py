import cv2
import mediapipe as mp
import keyinput  # Ensure this library is correctly installed and imported
import math
import handtrackingmodule as htm
import time

# Initialize MediaPipe Hands and drawing utilities
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
pTime = 0

# Capture video from the webcam
cap = cv2.VideoCapture(0)
wCam, hCam = 640, 480
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(detectionCon=0.7)

def draw_steering_wheel(image, center, radius):
    # Draw a circle representing the steering wheel
    cv2.circle(image, center, radius, (195, 255, 62), 15)

def calculate_angle(x1, y1, x2, y2):
    return math.degrees(math.atan2(y2 - y1, x2 - x1))

while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture image")
        break

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) >= 2:
        x1, y1 = lmList[0][1:3]
        x2, y2 = lmList[1][1:3]
        xm, ym = (x1 + x2) // 2, (y1 + y2) // 2
        radius = 150

        angle = calculate_angle(x1, y1, x2, y2)
        draw_steering_wheel(img, (xm, ym), radius)

        if angle > 45:  # Adjust the angle threshold as needed
            print("Turn left.")
            keyinput.release_key('s')
            keyinput.release_key('d')
            keyinput.press_key('a')
        elif angle < 45:  # Adjust the angle threshold as needed
            print("Turn right.")
            keyinput.release_key('s')
            keyinput.release_key('a')
            keyinput.press_key('d')
        else:
            print("Keeping straight.")
            keyinput.release_key('s')
            keyinput.release_key('a')
            keyinput.release_key('d')
            keyinput.press_key('w')
    elif len(lmList) == 1:
        print("Moving back.")
        keyinput.release_key('a')
        keyinput.release_key('d')
        keyinput.release_key('w')
        keyinput.press_key('s')

    # Display the frame with hand landmarks and steering wheel
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 8, 255), 3)
    cv2.imshow("Hand Detection Frame", cv2.flip(img, 1))

    # Wait for the desired frame time and exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the window
cap.release()
cv2.destroyAllWindows()
