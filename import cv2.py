import cv2
import numpy as np
import random

# Kích thước màn hình
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Kích thước bóng
BALL_RADIUS = 20

# Tốc độ di chuyển của bóng
BALL_SPEED = 5

# Điểm ban đầu
score = 0

def update_score():
    global score
    score += 1
    print("Score:", score)

def main():
    cap = cv2.VideoCapture(0)

    # Khởi tạo vị trí ban đầu của bóng
    ball_x = random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS)
    ball_y = random.randint(BALL_RADIUS, SCREEN_HEIGHT - BALL_RADIUS)

    # Hướng di chuyển ban đầu của bóng
    direction_x = random.choice([-1, 1])
    direction_y = random.choice([-1, 1])

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        # Chuyển đổi hình ảnh sang không gian màu HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Đặt ngưỡng cho màu da
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        mask = cv2.inRange(hsv, lower_skin, upper_skin)

        # Áp dụng các phép biến đổi hình thái để làm sạch ảnh
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=2)
        mask = cv2.dilate(mask, kernel, iterations=2)

        # Tìm đường viền của bàn tay
        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            # Vẽ hình chữ nhật bao quanh bàn tay
            cnt = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Kiểm tra va chạm giữa bàn tay và bóng
            if (x + w // 2 - BALL_RADIUS < ball_x < x + w // 2 + BALL_RADIUS) and \
               (y + h // 2 - BALL_RADIUS < ball_y < y + h // 2 + BALL_RADIUS):
                update_score()
                ball_x = random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS)
                ball_y = random.randint(BALL_RADIUS, SCREEN_HEIGHT - BALL_RADIUS)
                direction_x = random.choice([-1, 1])
                direction_y = random.choice([-1, 1])

        # Di chuyển bóng
        ball_x += direction_x * BALL_SPEED
        ball_y += direction_y * BALL_SPEED

        # Kiểm tra va chạm với biên
        if ball_x <= BALL_RADIUS or ball_x >= SCREEN_WIDTH - BALL_RADIUS:
            direction_x *= -1
        if ball_y <= BALL_RADIUS or ball_y >= SCREEN_HEIGHT - BALL_RADIUS:
            direction_y *= -1

        # Vẽ bóng
        cv2.circle(frame, (ball_x, ball_y), BALL_RADIUS, (0, 0, 255), -1)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
