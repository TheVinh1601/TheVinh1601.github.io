import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
import cvzone
import tkinter as tk
import random
import time
from PIL import Image, ImageTk
import pygame

def game_thread():
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    cap.set(3, 1920)
    cap.set(4, 1080)

    # Initialize Hand Detector
    detector = HandDetector(detectionCon=0.8, maxHands=1)
    # STEP 4: Distance Conversion Constants
    X = [350, 300, 250, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
    Y = [15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
    coefficient = np.polyfit(X, Y, 2)
     # Game variables
    cx, cy = 250, 250
    color = (0, 0, 255)
    counter = 0
    score = 0
    timeStart = 0
    Set_up_time = 30
    start = 0
    distanceCM = 0
    is_start = True
    original_distanceCM = 0
    min_delta = 8

    # Initialize Pygame for sounds
    pygame.mixer.init()
    mark_sound_effect = pygame.mixer.Channel(2)
    hit_effect = pygame.mixer.Channel(1)
    background_sound = pygame.mixer.Channel(0)
    sound5 = pygame.mixer.Sound('1.mp3')
    sound10 = pygame.mixer.Sound('2.mp3')
    sound15 = pygame.mixer.Sound('3.mp3')
    sound20 = pygame.mixer.Sound('4.mp3')
    hit_sound = pygame.mixer.Sound('5.mp3')
    end_time_sound = pygame.mixer.Sound('6.mp3')
    back_ground_music = pygame.mixer.Sound('8.mp3')

    while True:
        # Read frame from webcam
        success, img = cap.read()
        img = cv2.flip(img, 1)

        
        
        # Initial Screen
        if start == 0:
            background_sound.play(back_ground_music, -1)
            background_sound.set_volume(0.5)
            cvzone.putTextRect(img, 'Press S to start', (480, 500), scale=2, thickness=2, colorT=(255, 255, 255), colorR=False, offset=10)
            cvzone.putTextRect(img, 'HOW TO PLAY', (490, 50), scale=3, thickness=2, colorT=(255, 255, 255), colorR=(255, 0, 0), offset=10)
            cvzone.putTextRect(img, '1. Put your hand in the circle', (300, 90), scale=1, thickness=2, colorT=(255, 255, 255), colorR=(255, 0, 0), offset=10)
            cvzone.putTextRect(img, '2. Push it toward as a push button action', (300, 140), scale=1, thickness=2, colorT=(255, 255, 255), colorR=(255, 0, 0), offset=10)

        # Start Game
        elif start == 1:
            # Calculate elapsed time
            elapsed_time = time.time() - timeStart

            if elapsed_time < Set_up_time:
                hands = detector.findHands(img, draw=False)
                # Find hands
                hands, img = detector.findHands(img)

                # If hands are detected
                if hands:
                    # Access the first hand in the list
                    hand = hands[0]
                    # Get bounding box info of the hand
                    x, y, w, h = hand['bbox']
                    # Draw rectangle around the hand
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    # Optionally, you can add more info such as landmarks or hand type
                    cv2.putText(img, 'Hand Detected', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                            
                    first_hand = hands[0]
                    if isinstance(first_hand, dict) and 'lmList' in first_hand:
                        lmList = first_hand['lmList']
                        x1, y1 = lmList[5][:2]
                        x2, y2 = lmList[17][:2]
                        distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
                        A, B, C = coefficient
                        distanceCM = int(A * distance ** 2 + B * distance + C)

                        x, y, w, h = first_hand['bbox']
                        cv2.rectangle(img, (x - 10, y - 10), (x + w, y + h), (0, 255, 0), 2)
                        cvzone.putTextRect(img, f'{distanceCM} cm', (x, y - 25), 2, 2, (255, 255, 255), (0, 0, 0))

                        if x < cx < x + w and y < cy < y + h:
                            if is_start:
                                if distanceCM >= 25:
                                    original_distanceCM = distanceCM
                                    is_start = False
                            else:
                                if original_distanceCM - distanceCM >= min_delta:
                                    counter = 1

                if counter:
                    counter += 1
                    color = (0, 255, 0)
                    if counter >= 3:
                        cx = random.randint(100, 1100)
                        cy = random.randint(100, 600)
                        color = (0, 0, 255)
                        score += 1
                        counter = 0
                        is_start = True
                        hit_effect.play(hit_sound, 0)

                cv2.circle(img, (cx, cy), 30, color, cv2.FILLED)
                cv2.circle(img, (cx, cy), 10, (255, 255, 255), cv2.FILLED)
                cv2.circle(img, (cx, cy), 20, (255, 255, 255), 2)
                cv2.circle(img, (cx, cy), 30, (0, 0, 0), 2)

                cvzone.putTextRect(img, f'Time: {int(Set_up_time - elapsed_time)}', (1110, 40), 2, 2, (255, 255, 255), (255, 0, 0), offset=20)
                cvzone.putTextRect(img, f'Score: {score}', (20, 40), 2, 2, (255, 255, 255), (255, 0, 0), offset=20)
            else:
                # Game Over Screen
                start = 2
                cvzone.putTextRect(img, 'GAME OVER', (450, 360), 4, 2, (255, 255, 255), (255, 0, 0), offset=20)
                cvzone.putTextRect(img, f'Your Score: {score}', (445, 425), 3, 2, (255, 255, 255), (255, 0, 0), offset=20)
                cvzone.putTextRect(img, 'Press R to restart', (460, 600), 2, 2, (255, 255, 255), False, offset=20)
                cvzone.putTextRect(img, 'Press E to exit the game', (460, 650), 2, 2, (255, 255, 255), False, offset=20)
                mark_sound_effect.play(end_time_sound, 0)

        elif start == 2:
            # Game Over Screen
            cvzone.putTextRect(img, 'GAME OVER', (450, 360), 4, 2, (255, 255, 255), (255, 0, 0), offset=20)
            cvzone.putTextRect(img, f'Your Score: {score}', (445, 425), 3, 2, (255, 255, 255), (255, 0, 0), offset=20)
            cvzone.putTextRect(img, 'Press R to restart', (460, 600), 2, 2, (255, 255, 255), False, offset=20)
            cvzone.putTextRect(img, 'Press E to exit the game', (460, 650), 2, 2, (255, 255, 255), False, offset=20)

        # Show Image
        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        # Keyboard Controls
        if key == ord('s') and start == 0:
            score = 0
            start = 1
            timeStart = time.time()
        if key == ord('r'):
            score = 0
            start = 0
            is_start = True
        if key == ord('e'):
            break

        # Sound Effects
        if score == 4:
            mark_sound_effect.play(sound5, 0)
        if score == 9:
            mark_sound_effect.play(sound10, 0)
        if score == 14:
            mark_sound_effect.play(sound15, 0)
        if score == 19:
            mark_sound_effect.play(sound20, 0)

    # Close Windows
    cap.release()
    cv2.destroyAllWindows()
    pygame.mixer.stop()

def start_game():
    game_thread()

# Create the main interface window
interface = tk.Tk()
interface.title("Hand Tracking Game")
interface.geometry("1280x720")

# Load and display background image
bia = Image.open("Interface.png")
resizeimage = bia.resize((920, 650))
a = ImageTk.PhotoImage(resizeimage)
img = tk.Label(interface, image=a)
img.grid(column=0, row=0)

# Button to start the game
Btn = tk.Button(interface, text='Start', font=("Times New Roman", 20, "bold"), bg="skyblue", fg='black', command=start_game)
Btn.place(x=170, y=600)

interface.mainloop()


if __name__ == "__main__":
    game_thread()
