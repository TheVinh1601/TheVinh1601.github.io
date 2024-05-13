import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
import cvzone
from tkinter import *
import tkinter as tk
import random
import time
from PIL import ImageTk
import pygame

def Program_screen():
    # Step_1: Webcam
    cap=cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,720)
    #Step_2: Hand_detector
    detector=HandDetector(detectionCon=0.8,maxhand=1)
    #Step_4b: find function
    X=[350,300,250,200,170,145,130,112,103,93,87,75,70,67,62,59,57]
    Y=[15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]
    coefficient = np.polyfit(X,Y,2)
    #Game variables
    cx,cy=250,250
    color = (0,0,255)
    counter = 0
    score = 0
    timeStart = 0
    Set_up_time = 0
    Start = 0
    distanceCM = 0
    is_start = True 
    original_distanceCM = 0
    min_delta = 8
    #Add music to the game
    pygame.mixer.init()
    mark_sound_effect = pygame.mixer.Channel(2)
    hit_effect = pygame.mixer.Channel(1)
    background_sound = pygame.mixer.Channel(0)

    sound5 = pygame.mixer.Sound('...')
    hit_sound = pygame.mixer.Sound()