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

def Program_screen():
    # Khởi tạo webcam
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    # Khởi tạo bộ phát hiện tay
    detector = HandDetector(detectionCon=0.8, maxHands=1)

    # Khởi tạo biến trò chơi
    cx, cy = 250, 250  # Vị trí ban đầu của hình tròn
    counter = 0
    score = 0
    timeStart = 0
    Set_up_time = 30
    start = 0
    distanceCM = 0
    is_start = True
    original_distanceCM = 0
    min_delta = 8

    # Khởi tạo âm thanh
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
    back_ground_music = pygame.mixer.Sound('7.mp3')

    # Vòng lặp chính
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)

        if start == 0:
            background_sound.play(back_ground_music, -1)
            background_sound.set_volume(0.5)
            # Hiển thị hướng dẫn và thông tin trò chơi
            # (Bạn có thể thay đổi vị trí và nội dung tùy thích)
        if start == 1:
            if time.time() - timeStart < Set_up_time:
                hands = detector.findHands(img, draw=False)
                if hands:
                    lmList = hands[0]['lmList']
                    x1, y1 = lmList[5][:2]
                    x2, y2 = lmList[17][:2]
                    distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
                    A, B, C = np.polyfit(V, Y, 2)
                    distanceCM = int(A * distance ** 2 + B * distance + C)
                    x, y, w, h = hands[0]['bbox']
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
                    cv2.circle(img, (cx, cy), 20, (255, 255, 255), 2), cv2.circle(img, (cx, cy), 30, (0, 0, 0), 2)
                    cvzone.putTextRect(img, f'Time: {int(Set_up_time - (time.time() - timeStart))}', (1110, 40), 2, 2,
                                       (255, 255, 255), (255, 0, 0), offset=20)
                    cvzone.putTextRect(img, f'Score: {score}', (20, 40), 2, 2, (255, 255, 255), (255, 0, 0), offset=20)
                else:
                    cvzone.putTextRect(img, 'GAME OVER', (450, 360), 4, 2, (255, 255, 255), (255, 0, 0), offset=20)
                    cvzone.putTextRect(img, f'Your Score: {score}', (445, 425), 3, 2, (255, 255, 255), (255, 0, 0),
                                       offset=20)
                    cvzone.putTextRect(img, 'Press R to restart', (460, 600), 2, 2, (255, 255, 255), False, offset=20)
                    cvzone.putTextRect(img, 'Press E to exit the game', (460, 650), 2, 2, (255, 255, 255), False,
                                       offset=20)
                    if int(Set_up_time - (time.time() - timeStart)) == 0:
                        mark_sound_effect.play(end_time_sound, 0)
        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        if key == ord('s'):
            start = 1
            timeStart = time.time()
        if key == ord('r'):
            score = 0
            start = 0
            is_start = True
        if key == ord('e'):
            break
        if score == 4:
            mark_sound_effect.play(sound5, 0)
        if score == 9:
            mark_sound_effect.play(sound10, 0)
        if score == 14:
            mark_sound_effect.play(sound15, 0)
        if score == 19:
            mark_sound_effect.play(sound20, 0)

    cv2.destroyAllWindows()
    pygame.mixer.stop()

# Tạo giao diện chính
interface = tk.Tk()
interface.title("Hand tracking game")
resizeimage = Image.open("Interface.png").resize((940, 788))
a = ImageTk.PhotoImage(resizeimage)
img = tk.Label(interface, image=a)
img.grid(column=0, row=0)
Btn = tk.Button(interface, text='Start', font=("Times New Roman", 20, "bold"),
                bg="skyblue", fg='black', command=Program_screen)
Btn.place(x=400, y=550)
interface.mainloop()
