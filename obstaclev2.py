import cv2
import numpy as np
import RPi.GPIO as GPIO
import time

# --- GPIO SETUP FOR ZY ELECTRONICS (L298N) ---
IN1 = 17
IN2 = 18
ENA = 22

IN3 = 23
IN4 = 24
ENB = 25

# --- GPIO SETUP FOR HC-SR04 ULTRASONIC SENSOR ---
TRIG = 5
ECHO = 6

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Cài đặt chân động cơ
motor_pins =
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)

# Cài đặt chân siêu âm
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

pwm_A = GPIO.PWM(ENA, 50)
pwm_B = GPIO.PWM(ENB, 50)
pwm_A.start(0)
pwm_B.start(0)

# Hàm điều khiển động cơ
def move_robot(left_speed, right_speed):
    if left_speed >= 0:
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        pwm_A.ChangeDutyCycle(left_speed)
    else:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        pwm_A.ChangeDutyCycle(abs(left_speed))
        
    if right_speed >= 0:
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
        pwm_B.ChangeDutyCycle(right_speed)
    else:
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
        pwm_B.ChangeDutyCycle(abs(right_speed))

# Hàm đo khoảng cách
def get_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start = time.time()
    pulse_end = time.time()
    timeout = time.time()

    # Chống treo chương trình nếu lỏng dây
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if time.time() - timeout > 0.1: 
            return 999
            
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if time.time() - timeout > 0.1:
            return 999

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

# --- CAMERA SETUP ---
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

print("He thong khoi dong. Dat robot len line...")
time.sleep(2)

BASE_SPEED = 35
Kp = 0.3

last_error = 0
missing_frames = 0

try:
    while True:
        # 1. ĐO KHOẢNG CÁCH VÀ KIỂM TRA VẬT CẢN TRƯỚC
        dist = get_distance()
        
        if dist <= 20.0:
            print(f">>> CANH BAO: Phat hien vat can o {dist} cm. DUNG XE!")
            move_robot(0, 0) # Phanh khẩn cấp
            time.sleep(0.1)
            continue # Bỏ qua phần dò line bên dưới để ưu tiên dừng lại
        else:
            print(f"Duong trong (Khoang cach: {dist} cm). Dang bam line...")

        # 2. XỬ LÝ CAMERA DÒ LINE
        ret, frame = cap.read()
        if not ret:
            break
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)

        roi = thresh[160:240, 0:320]
        contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            
            if M["m00"]!= 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                
                cv2.circle(frame, (cx, cy + 160), 5, (0, 0, 255), -1)
                
                error = cx - 160 
                last_error = error
                missing_frames = 0 
                
                correction = error * Kp
                left_motor_speed = BASE_SPEED + correction
                right_motor_speed = BASE_SPEED - correction
                
                left_motor_speed = max(0, min(100, left_motor_speed))
                right_motor_speed = max(0, min(100, right_motor_speed))
                
                move_robot(left_motor_speed, right_motor_speed)
        else:
            # --- XỬ LÝ KHI BỊ ĐỨT LINE ---
            missing_frames += 1
            if missing_frames < 10:
                move_robot(BASE_SPEED, BASE_SPEED)
            else:
                if last_error < 0:
                    move_robot(-35, 35)
                else:
                    move_robot(35, -35)

        cv2.imshow("Camera View", frame)
        cv2.imshow("Line ROI", roi)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Nguoi dung da dung chuong trinh.")

finally:
    move_robot(0, 0)
    pwm_A.stop()
    pwm_B.stop()
    GPIO.cleanup()
    cap.release()
    cv2.destroyAllWindows()