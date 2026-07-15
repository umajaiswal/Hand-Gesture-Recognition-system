

import cv2
import time
import numpy as np
import handtrack as htm

# -----------------------------
# Camera Setup
# -----------------------------
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = htm.handDetector()

tipIds = [4, 8, 12, 16, 20]

pTime = 0

while True:

    success, img = cap.read()

    if not success:
        break

    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    gesture = "No Hand"
    letter = "-"
    totalFingers = 0

    if len(lmList) >= 21:

        fingers = []

        # Thumb
        if lmList[4][1] > lmList[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Index to Pinky
        for i in range(1,5):

            if lmList[tipIds[i]][2] < lmList[tipIds[i]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers = fingers.count(1)

        # -------------------------
        # Gesture Recognition
        # -------------------------

        if fingers == [0,0,0,0,0]:
            gesture="FIST"
            letter="A"

        elif fingers == [1,1,1,1,1]:
            gesture="OPEN HAND"
            letter="B"

        elif fingers == [0,1,0,0,0]:
            gesture="ONE"
            letter="D"

        elif fingers == [0,1,1,0,0]:
            gesture="PEACE"
            letter="V"

        elif fingers == [0,1,1,1,0]:
            gesture="THREE"
            letter="W"

        elif fingers == [1,0,0,0,0]:
            gesture="THUMBS UP"
            letter="Y"

    # ----------------------------
    # FPS
    # ----------------------------

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime

    # ----------------------------
    # Dashboard
    # ----------------------------

    dashboard=np.zeros((550,1000,3),dtype=np.uint8)

    dashboard[:]=(35,35,35)

    img=cv2.resize(img,(640,480))

    dashboard[40:520,20:660]=img

    # Title

    cv2.putText(
        dashboard,
        "HAND GESTURE RECOGNITION SYSTEM",
        (170,25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255,255,255),
        2
    )

    # Camera Border

    cv2.rectangle(
        dashboard,
        (18,38),
        (662,522),
        (255,255,255),
        2
    )

    # Right Panel

    cv2.rectangle(
        dashboard,
        (700,40),
        (980,520),
        (70,70,70),
        2
    )

    cv2.putText(
        dashboard,
        "SYSTEM INFO",
        (760,70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0,255,255),
        2
    )

        # Gesture
    cv2.putText(
        dashboard,
        "Gesture",
        (730,120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0,255,255),
        2
    )

    cv2.putText(
        dashboard,
        gesture,
        (730,155),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255,255,255),
        2
    )

    # Letter
    cv2.putText(
        dashboard,
        "Letter",
        (730,215),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0,255,255),
        2
    )

    cv2.putText(
        dashboard,
        letter,
        (730,250),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0,255,0),
        3
    )

    # Finger Count
    cv2.putText(
        dashboard,
        "Finger Count",
        (730,310),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0,255,255),
        2
    )

    cv2.putText(
        dashboard,
        str(totalFingers),
        (730,345),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255,255,255),
        3
    )

    # FPS
    cv2.putText(
        dashboard,
        "FPS",
        (730,405),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0,255,255),
        2
    )

    cv2.putText(
        dashboard,
        str(int(fps)),
        (730,440),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255,255,255),
        3
    )

    # Status
    if len(lmList) >= 21:
        status = "Hand Detected"
        color = (0,255,0)
    else:
        status = "No Hand"
        color = (0,0,255)

    cv2.putText(
        dashboard,
        "Status",
        (730,485),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0,255,255),
        2
    )

    cv2.putText(
        dashboard,
        status,
        (820,485),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        color,
        2
    )

    # Bottom Instructions
    cv2.putText(
        dashboard,
        "Press Q to Exit",
        (20,542),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (180,180,180),
        1
    )

    cv2.putText(
        dashboard,
        "Show only one hand for best accuracy",
        (330,542),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (180,180,180),
        1
    )

    # Display
    cv2.imshow("Hand Gesture Recognition", dashboard)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
