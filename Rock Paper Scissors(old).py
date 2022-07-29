import cv2
import mediapipe
import numpy
import random

cap = cv2.VideoCapture(0)
initHand = mediapipe.solutions.hands  # Initializing mediapipe
# Object of mediapipe with "arguments for the hands module"
mainHand = initHand.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8,max_num_hands=1)
draw = mediapipe.solutions.drawing_utils  # Object to draw the connections between each finger index
wScr, hScr = 1920,1080 #pyautogui.size()  # Outputs the high and width of the screen (1920 x 1080)
pX, pY = 0, 0  # Previous x and y location
cX, cY = 0, 0 

def handLandmarks(colorImg):
    landmarkList = []  # Default values if no landmarks are tracked

    landmarkPositions = mainHand.process(colorImg)  # Object for processing the video input
    landmarkCheck = landmarkPositions.multi_hand_landmarks  # Stores the out of the processing object (returns False on empty)
    if landmarkCheck:  # Checks if landmarks are tracked
        for hand in landmarkCheck:  # Landmarks for each hand
            for index, landmark in enumerate(hand.landmark):  # Loops through the 21 indexes and outputs their landmark coordinates (x, y, & z)
                draw.draw_landmarks(img, hand,initHand.HAND_CONNECTIONS)  # Draws each individual index on the hand with connections
                h, w, c = img.shape  # Height, width and channel on the image
                centerX, centerY = int(landmark.x * w), int(landmark.y * h)  # Converts the decimal coordinates relative to the image for each index
                landmarkList.append([index, centerX, centerY])  # Adding index and its coordinates to a list

    return landmarkList

def fingers(landmarks):
    fingerTips = []  # To store 4 sets of 1s or 0s
    tipIds = [4, 8, 12, 16, 20]  # Indexes for the tips of each finger

    # Check if middle is up
    if landmarks[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
        fingerTips.append(1)
    else:
        fingerTips.append(0)

    # Check if fingers are up except the thumb
    for id in range(1,5):
        if landmarks[tipIds[id]][2] < landmarks[tipIds[id] - 3][2]:  # Checks to see if the tip of the finger is higher than the joint
            fingerTips.append(1)
        else:
            fingerTips.append(0)

    return fingerTips

    


print("Rock Paper Scissors")
while True:
    check, img = cap.read()  # Reads frames from the camera
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Changes the format of the frames from BGR to RGB
    lmList = handLandmarks(imgRGB)

    lst = ["Rock","Paper","Scissors"]
    sys_choice = random.choice(lst)
    
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]  # Gets index 8s x and y values (skips index value because it starts from 1)
        x2, y2 = lmList[12][1:]  # Gets index 12s x and y values (skips index value because it starts from 1)
        finger = fingers(lmList)

        if finger[0]==1 and finger[1]==1 and finger[2]==1 and finger[3]==1 and finger[4]==1:
            print("Your Choice : Paper")
            print("system choice :",sys_choice)
            if (sys_choice=="Rock"):
                print("You Win....(Paper Beats Rock)")
                break
            elif (sys_choice=="Scissors"):
                print("You lose...(Scissors Beat Paper)")
                break
            elif (sys_choice=="Paper"):
                print("Draw the Match...(Both Papers)")
                break
        
        if finger[0]==0 and finger[1]==1 and finger[2]==1 and finger[3]==0 and finger[4]==0:
            print("Your Choice : Scissors")
            print("system choice :",sys_choice)
            if (sys_choice=="Rock"):
                print("You Lose....(Rock Beats Scissors)")
                break
            elif (sys_choice=="Scissors"):
                print("Draw the Match...(Both Scissors)")
                break
            elif (sys_choice=="Paper"):
                print("You Win...(Scissors Beat Paper)")
                break

        if finger[0]==0 and finger[1]==0 and finger[2]==0 and finger[3]==0 and finger[4]==0:
            print("Your Choice : Rock")
            print("system choice :",sys_choice)
            if (sys_choice=="Paper"):
                print("You Lose....(Paper Beats Rock)")
                break
            elif (sys_choice=="Rock"):
                print("Draw the Match...(Both Rock)")
                break
            elif (sys_choice=="Scissors"):
                print("You Win...(Rock Beats Scissors)")
                break
    
    cv2.imshow("Webcam", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
