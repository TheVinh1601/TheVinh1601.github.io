import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
import cvzone
import tkinter as tk
from tkinter import messagebox
import random
import time
from PIL import Image, ImageTk
import pygame
import threading
import traceback

def game_thread():
    try:
        cap = cv2.VideoCapture(0)
        cap.set(3, 1920)
        cap.set(4, 1080)

        # STEP 2: Initialize Hand Detector
        detector = HandDetector(detectionCon=0.8, maxHands=1)

        # STEP 4: Distance Conversion Constants
        X = [350, 300, 250, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
        Y = [15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
        coefficient = np.polyfit(X, Y, 2)

        # Game variables
        cx, cy = 250, 250
        color = (0,0,255)
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
        back_ground_music = pygame.mixer.Sound('7.mp3')

        # Main Loop
        while True:
            success, img = cap.read()
            img = cv2.flip(img, 1)
            # img = cv2.resize(img, (1080, 1080))
            # Initial Screen
            if start == 0:
                background_sound.play(back_ground_music, -1)
                background_sound.set_volume(0.5)
                cvzone.putTextRect(img, 'Press S to start', (480, 500), scale=2, thickness=2, colorT=(255, 255, 255), colorR=False, offset=10)
                cvzone.putTextRect(img, 'HOW TO PLAY', (490, 50), scale=3, thickness=2, colorT=(255, 255, 255), colorR=(255, 0, 0), offset=10)
                cvzone.putTextRect(img, '1. Put your hand in the circle', (300, 90), scale=1, thickness=2, colorT=(255, 255, 255), colorR=(255, 0, 0), offset=10)
                cvzone.putTextRect(img, '2. Push it toward as a push button action', (300, 140), scale=1, thickness=2, colorT=(255, 255, 255), colorR=(255, 0, 0), offset=10)

            # Start Game
            if start == 1:
                if time.time() - timeStart < Set_up_time:
                    hands = detector.findHands(img, draw=False)
                    if hands:
                        lmList = hands[0]['lmList']
                        x1, y1 = lmList[5][:2]
                        x2, y2 = lmList[17][:2]
                        distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
                        A, B, C = coefficient
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

                        cvzone.putTextRect(img, f'Time: {int(Set_up_time - (time.time() - timeStart))}', (1110, 40), 2, 2, (255, 255, 255), (255, 0, 0), offset=20)
                        cvzone.putTextRect(img, f'Score: {score}', (20, 40), 2, 2, (255, 255, 255), (255, 0, 0), offset=20)
                    else:
                        cvzone.putTextRect(img, 'GAME OVER', (450, 360), 4, 2, (255, 255, 255), (255, 0, 0), offset=20)
                        cvzone.putTextRect(img, f'Your Score: {score}', (445, 425), 3, 2, (255, 255, 255), (255, 0, 0), offset=20)
                        cvzone.putTextRect(img, 'Press R to restart', (460, 600), 2, 2, (255, 255, 255), False, offset=20)
                        cvzone.putTextRect(img, 'Press E to exit the game', (460, 650), 2, 2, (255, 255, 255), False, offset=20)
                        if int(Set_up_time - (time.time() - timeStart)) == 0:
                            mark_sound_effect.play(end_time_sound, 0)


    except Exception as e:
        # In ra traceback để xem chi tiết lỗi (để debug)
        traceback.print_exc()

        # Hiển thị thông báo lỗi trong cửa sổ Tkinter
        error_message = "Lỗi: {}".format(str(e))
        messagebox.showerror("Lỗi", error_message)
