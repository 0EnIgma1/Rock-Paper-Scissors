import cv2
import random
import cvzone
import time
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)

#setting webcam resolution
cap.set(3,640)
cap.set(4,480)

detector = HandDetector(maxHands=1)  #confidence default value = 0.5

timer = 0
StateResult = False
GameStart = False
PlayerMove = ""
scores = [0,0]  #[AI, player]
won = 0

while True:
    #reading background image
    imgBG = cv2.imread("Resources/bg.png")

    #assigning webcam input to img
    success, img = cap.read()

    #Rescaling webcam input based on the BG image player box region (width = 793:1141)px (height = 211:624)px
    #height resize param(0.86) is caluculated by (624-211)/480 difference in BG region height by webcam height 

    imgScale = cv2.resize(img,(0,0),None,0.86,0.86)

    #width rescale param is caluculated by ((640x0.86)-348)/2 : 550.4-101.2 ; webcam width with height resize value - BG region width difference by 2 : webcam width with height resize value - previous value
    imgScale = imgScale[:,101:449]  
    
    #detecting hands
    hands, img = detector.findHands(imgScale)
    cv2.putText(imgBG,str("Press \'s\' to play"),(190,690),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),2)
    cv2.putText(imgBG,str("Press \'q\' to Exit"),(815,690),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),2)
    
    if GameStart:

        if StateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG,str(int(timer)),(617,405),cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),5)     #dimension, font, size, color, thickness

            if timer>3:
                StateResult = True
                timer = 0

                if hands:
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0,0,0,0,0]:
                        PlayerMove = "rock"
                    if fingers == [0,1,1,0,0]:
                        PlayerMove = "scissors"
                    if fingers == [1,1,1,1,1]:
                        PlayerMove = "paper"
                    
                    lst = ["rock","paper","scissors"]
                    AIchoice = random.choice(lst)
                    print("AI move :",AIchoice)
                    imgAI = cv2.imread(f"Resources/{AIchoice}.png",cv2.IMREAD_UNCHANGED)
                    #imgBG = cvzone.overlayPNG(imgBG,imgAI,(153,212))
                    
                    #player win
                    if (PlayerMove == "rock" and AIchoice == "scissors") or \
                        (PlayerMove == "paper" and AIchoice == "rock") or \
                            (PlayerMove == "scissors" and AIchoice == "paper"):
                            scores[1] += 1
                            won = 1
                    
                    
                    #AI win
                    if (PlayerMove == "rock" and AIchoice == "paper") or \
                        (PlayerMove == "paper" and AIchoice == "scissors") or \
                            (PlayerMove == "scissors" and AIchoice == "rock"):
                            scores[0] += 1
                            won = 2
                    
                    #draw
                    if (PlayerMove == "rock" and AIchoice == "rock") or \
                        (PlayerMove == "paper" and AIchoice == "paper") or \
                            (PlayerMove == "scissors" and AIchoice == "scissors"):
                            won = 0
                    

                    print("player move :",PlayerMove)

    
    imgBG[211:624,793:1141] = imgScale

    if StateResult:
        imgBG = cvzone.overlayPNG(imgBG,imgAI,(153,250))
        cv2.putText(imgBG,str("Press \'s\' to play"),(190,690),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),2)
        cv2.putText(imgBG,str("Press \'q\' to Exit"),(815,690),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),2)

        if (won==1):
            cv2.putText(imgBG,str("Player WON"),(500,220),cv2.FONT_HERSHEY_PLAIN,3,(102,205,0),5)
        elif (won==2):
            cv2.putText(imgBG,str("AI WON"),(550,200),cv2.FONT_HERSHEY_PLAIN,3,(0,0,255),5)
        elif (won==0):
            cv2.putText(imgBG,str("DRAW"),(570,200),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),5)

    cv2.putText(imgBG,str(scores[0]),(395,190),cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),5)
    cv2.putText(imgBG,str(scores[1]),(1050,190),cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),5)

    cv2.imshow("BG",imgBG)
    key = cv2.waitKey(1)
    if key == ord("s"):
        GameStart = True
        initialTime = time.time()
        StateResult = False
    
    if key == ord("q"):
        break