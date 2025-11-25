"""
    File   interval_setting
    Author Ryu SeoJoon (call0919@gachon.ac.kr)
    date   25th NOV

    recent 25th NOV

    "이 코드는 인터벌 설정 ui 코드입니다."
 """

import cv2
import numpy as np
import json
import os
import time

# 모드 변수
mode = "SETTING"  # "SETTING" or "TIMER"

# 시간 설정 변수 (초 단위)
prep_time = 0
exercise_time = 0
rest_time = 0
reps = 0

# TIMER 모드 변수
interval_phase = "PREP"  # "PREP", "EXERCISE", "REST"
current_rep = 0
elapsed = 0.0
last_time = time.time()
timer_running = False

# 버튼 위치 정의
# 준비시간 버튼
prep_m_minus_btn = ((50, 150), (110, 190))
prep_s_minus_btn = ((120, 150), (180, 190))
prep_s_plus_btn = ((320, 150), (380, 190))
prep_m_plus_btn = ((390, 150), (450, 190))

# 운동시간 버튼
exercise_m_minus_btn = ((50, 230), (110, 270))
exercise_s_minus_btn = ((120, 230), (180, 270))
exercise_s_plus_btn = ((320, 230), (380, 270))
exercise_m_plus_btn = ((390, 230), (450, 270))

# 휴식시간 버튼
rest_m_minus_btn = ((50, 310), (110, 350))
rest_s_minus_btn = ((120, 310), (180, 350))
rest_s_plus_btn = ((320, 310), (380, 350))
rest_m_plus_btn = ((390, 310), (450, 350))

# 반복횟수 버튼
reps_minus_btn = ((150, 390), (210, 430))
reps_plus_btn = ((290, 390), (350, 430))

# 하단 버튼
save_btn = ((50, 500), (230, 560))
cancel_btn = ((270, 500), (450, 560))

# TIMER 모드 버튼
timer_start_btn = ((50, 450), (245, 500))
timer_pause_btn = ((255, 450), (450, 500))
timer_reset_btn = ((150, 510), (350, 560))

font_timer = cv2.FONT_HERSHEY_SIMPLEX

def load_config():
    """기존 설정 불러오기"""
    global prep_time, exercise_time, rest_time, reps
    try:
        if os.path.exists('interval_config.json'):
            with open('interval_config.json', 'r') as f:
                config = json.load(f)
                prep_time = config.get('prep', 0)
                exercise_time = config.get('exercise', 0)
                rest_time = config.get('rest', 0)
                reps = config.get('reps', 0)
    except:
        pass

def save_config():
    """설정 저장"""
    config = {
        'prep': prep_time,
        'exercise': exercise_time,
        'rest': rest_time,
        'reps': reps
    }
    with open('interval_config.json', 'w') as f:
        json.dump(config, f)

def draw_button(frame, rect, label):
    """버튼 그리기"""
    (x1, y1), (x2, y2) = rect
    cv2.rectangle(frame, (x1, y1), (x2, y2), (60, 60, 60), -1)
    (tw, th), _ = cv2.getTextSize(label, font_timer, 0.7, 2)
    text_x = x1 + (x2 - x1 - tw) // 2
    text_y = y1 + (y2 - y1 + th) // 2
    cv2.putText(frame, label, (text_x, text_y), font_timer, 0.7, (255, 255, 255), 2)

def format_time(seconds):
    """초를 MM:SS 형식으로 변환"""
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"

def start_timer_mode():
    """설정 저장 후 TIMER 모드로 전환"""
    global mode, interval_phase, current_rep, elapsed, last_time, timer_running
    save_config()
    mode = "TIMER"
    interval_phase = "PREP"
    current_rep = 0
    elapsed = prep_time  # 카운트다운: 설정 시간에서 시작
    last_time = time.time()
    timer_running = False

def reset_to_setting():
    """TIMER 모드에서 SETTING 모드로 복귀"""
    global mode, timer_running
    mode = "SETTING"
    timer_running = False

def handle_interval_transition():
    """인터벌 단계 전환 (카운트다운)"""
    global interval_phase, elapsed, current_rep, last_time, timer_running

    if interval_phase == "PREP" and elapsed <= 0:
        timer_running = False  # 단계 종료 시 일시정지
        interval_phase = "EXERCISE"
        elapsed = exercise_time
        current_rep = 1
        last_time = time.time()
    elif interval_phase == "EXERCISE" and elapsed <= 0:
        timer_running = False  # 단계 종료 시 일시정지
        interval_phase = "REST"
        elapsed = rest_time
        last_time = time.time()
    elif interval_phase == "REST" and elapsed <= 0:
        timer_running = False  # 단계 종료 시 일시정지
        if current_rep < reps:
            interval_phase = "EXERCISE"
            current_rep += 1
            elapsed = exercise_time
            last_time = time.time()
        else:
            # 모든 세트 완료
            pass

def on_mouse(event, x, y, flags, param):
    """마우스 클릭 이벤트 처리"""
    global prep_time, exercise_time, rest_time, reps, running, timer_running, last_time, mode

    if event == cv2.EVENT_LBUTTONDOWN:
        # TIMER 모드 버튼 처리
        if mode == "TIMER":
            if timer_start_btn[0][0] <= x <= timer_start_btn[1][0] and timer_start_btn[0][1] <= y <= timer_start_btn[1][1]:
                timer_running = True
                last_time = time.time()
            elif timer_pause_btn[0][0] <= x <= timer_pause_btn[1][0] and timer_pause_btn[0][1] <= y <= timer_pause_btn[1][1]:
                timer_running = False
            elif timer_reset_btn[0][0] <= x <= timer_reset_btn[1][0] and timer_reset_btn[0][1] <= y <= timer_reset_btn[1][1]:
                reset_to_setting()
            return

        # SETTING 모드 버튼 처리
        # 준비시간 버튼
        if prep_m_minus_btn[0][0] <= x <= prep_m_minus_btn[1][0] and prep_m_minus_btn[0][1] <= y <= prep_m_minus_btn[1][1]:
            prep_time = max(0, prep_time - 60)
        elif prep_s_minus_btn[0][0] <= x <= prep_s_minus_btn[1][0] and prep_s_minus_btn[0][1] <= y <= prep_s_minus_btn[1][1]:
            prep_time = max(0, prep_time - 1)
        elif prep_s_plus_btn[0][0] <= x <= prep_s_plus_btn[1][0] and prep_s_plus_btn[0][1] <= y <= prep_s_plus_btn[1][1]:
            prep_time += 1
        elif prep_m_plus_btn[0][0] <= x <= prep_m_plus_btn[1][0] and prep_m_plus_btn[0][1] <= y <= prep_m_plus_btn[1][1]:
            prep_time += 60

        # 운동시간 버튼
        elif exercise_m_minus_btn[0][0] <= x <= exercise_m_minus_btn[1][0] and exercise_m_minus_btn[0][1] <= y <= exercise_m_minus_btn[1][1]:
            exercise_time = max(0, exercise_time - 60)
        elif exercise_s_minus_btn[0][0] <= x <= exercise_s_minus_btn[1][0] and exercise_s_minus_btn[0][1] <= y <= exercise_s_minus_btn[1][1]:
            exercise_time = max(0, exercise_time - 1)
        elif exercise_s_plus_btn[0][0] <= x <= exercise_s_plus_btn[1][0] and exercise_s_plus_btn[0][1] <= y <= exercise_s_plus_btn[1][1]:
            exercise_time += 1
        elif exercise_m_plus_btn[0][0] <= x <= exercise_m_plus_btn[1][0] and exercise_m_plus_btn[0][1] <= y <= exercise_m_plus_btn[1][1]:
            exercise_time += 60

        # 휴식시간 버튼
        elif rest_m_minus_btn[0][0] <= x <= rest_m_minus_btn[1][0] and rest_m_minus_btn[0][1] <= y <= rest_m_minus_btn[1][1]:
            rest_time = max(0, rest_time - 60)
        elif rest_s_minus_btn[0][0] <= x <= rest_s_minus_btn[1][0] and rest_s_minus_btn[0][1] <= y <= rest_s_minus_btn[1][1]:
            rest_time = max(0, rest_time - 1)
        elif rest_s_plus_btn[0][0] <= x <= rest_s_plus_btn[1][0] and rest_s_plus_btn[0][1] <= y <= rest_s_plus_btn[1][1]:
            rest_time += 1
        elif rest_m_plus_btn[0][0] <= x <= rest_m_plus_btn[1][0] and rest_m_plus_btn[0][1] <= y <= rest_m_plus_btn[1][1]:
            rest_time += 60

        # 반복횟수 버튼
        elif reps_minus_btn[0][0] <= x <= reps_minus_btn[1][0] and reps_minus_btn[0][1] <= y <= reps_minus_btn[1][1]:
            reps = max(0, reps - 1)
        elif reps_plus_btn[0][0] <= x <= reps_plus_btn[1][0] and reps_plus_btn[0][1] <= y <= reps_plus_btn[1][1]:
            reps += 1

        # 저장 및 취소 버튼
        elif save_btn[0][0] <= x <= save_btn[1][0] and save_btn[0][1] <= y <= save_btn[1][1]:
            start_timer_mode()
        elif cancel_btn[0][0] <= x <= cancel_btn[1][0] and cancel_btn[0][1] <= y <= cancel_btn[1][1]:
            cv2.destroyAllWindows()
            running = False

# 초기 설정 불러오기
load_config()

cv2.namedWindow("INTERVAL SETTING")
cv2.setMouseCallback("INTERVAL SETTING", on_mouse)

running = True

while running:
    frame = np.zeros((600, 500, 3), dtype=np.uint8)

    # TIMER 모드 처리 (카운트다운)
    if timer_running:
        now = time.time()
        elapsed -= now - last_time  # 카운트다운: 시간 감소
        last_time = now
        handle_interval_transition()

    if mode == "TIMER":
        # TIMER 모드 화면
        # 현재 phase 표시
        phase_color = (0, 255, 255) if interval_phase == "PREP" else (0, 255, 0) if interval_phase == "EXERCISE" else (255, 165, 0)
        cv2.putText(frame, interval_phase, (150, 100), font_timer, 1.5, phase_color, 3)

        # Rep 카운트 표시
        if interval_phase != "PREP":
            rep_text = f"Rep: {current_rep}/{reps}"
            cv2.putText(frame, rep_text, (170, 140), font_timer, 0.8, (255, 255, 255), 2)

        # 타이머 표시 (카운트다운)
        total = max(0, elapsed)  # 음수 방지
        minute = int(total // 60)
        second = total % 60
        timer_text = f"{minute:02d}:{int(second):02d}"
        frac_part = f".{int((second - int(second)) * 100):02d}"

        cv2.putText(frame, timer_text, (115, 250), font_timer, 3, (0, 255, 0), 5)
        cv2.putText(frame, frac_part, (380, 250), font_timer, 1, (0, 255, 0), 2)

        # 버튼 표시
        draw_button(frame, timer_start_btn, "Start")
        draw_button(frame, timer_pause_btn, "Pause")
        draw_button(frame, timer_reset_btn, "Back to Setting")

    else:
        # SETTING 모드 화면
        # 제목
        cv2.putText(frame, "INTERVAL SETTING", (90, 50), font_timer, 1.2, (0, 255, 255), 2)

        # 준비시간
        cv2.putText(frame, "Preparation:", (50, 120), font_timer, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, format_time(prep_time), (210, 175), font_timer, 1.2, (0, 255, 0), 2)
        draw_button(frame, prep_m_minus_btn, "-1m")
        draw_button(frame, prep_s_minus_btn, "-1s")
        draw_button(frame, prep_s_plus_btn, "+1s")
        draw_button(frame, prep_m_plus_btn, "+1m")

        # 운동시간
        cv2.putText(frame, "Exercise:", (50, 200), font_timer, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, format_time(exercise_time), (210, 255), font_timer, 1.2, (0, 255, 0), 2)
        draw_button(frame, exercise_m_minus_btn, "-1m")
        draw_button(frame, exercise_s_minus_btn, "-1s")
        draw_button(frame, exercise_s_plus_btn, "+1s")
        draw_button(frame, exercise_m_plus_btn, "+1m")

        # 휴식시간
        cv2.putText(frame, "Rest:", (50, 280), font_timer, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, format_time(rest_time), (210, 335), font_timer, 1.2, (0, 255, 0), 2)
        draw_button(frame, rest_m_minus_btn, "-1m")
        draw_button(frame, rest_s_minus_btn, "-1s")
        draw_button(frame, rest_s_plus_btn, "+1s")
        draw_button(frame, rest_m_plus_btn, "+1m")

        # 반복횟수
        cv2.putText(frame, "Repetitions:", (50, 360), font_timer, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, f"{reps:02d}", (240, 415), font_timer, 1.2, (0, 255, 0), 2)
        draw_button(frame, reps_minus_btn, "-")
        draw_button(frame, reps_plus_btn, "+")

        # 저장 및 취소 버튼
        draw_button(frame, save_btn, "Save & Start")
        draw_button(frame, cancel_btn, "Cancel")

    cv2.imshow("INTERVAL SETTING", frame)

    key = cv2.waitKey(50) & 0xFF
    if key == ord('q'):
        running = False

cv2.destroyAllWindows()
