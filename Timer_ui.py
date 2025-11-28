"""
    File   Timer_UI
    Author Ryu SeoJoon (call0919@gachon.ac.kr)
    date   21st NOV
    
    recent 15:32 21st NOV
    
    "이 코드는 타이머 ui 코드입니다."
 """   
import cv2
import numpy as np
import time
import os
import subprocess
import sys

running = False 						#동작 점검 변수
elapsed = 0.0							#기본 시간 변수
last_time = time.time()

start_btn = ((50, 450), (245, 500))				#버튼 크기, 위치
pause_btn = ((255, 450), (450, 500))
reset_btn = ((150, 510), (350, 560))
record_btn = ((360, 510), (450, 560))
menu_btn = ((50, 510), (140, 560))

font_timer = cv2.FONT_HERSHEY_SIMPLEX				#폰트 설정

records = []							#기록 저장 리스트
MAX_RECORDS = 7							#최대 기록 개수

menu_open = False						#메뉴 활성화 점검
interval_setting_btn = ((50, 120), (250, 180))			#interval setting 버튼
recent_record_btn = ((50, 200), (250, 260))			#recent_record 버튼
alarm_btn = ((50, 280), (250, 340))				#alarm 버튼	

def is_button_clicked(btn, x, y):				#버튼 클릭 확인 헬퍼 함수
    return btn[0][0] <= x <= btn[1][0] and btn[0][1] <= y <= btn[1][1]

def open_interval_setting():					#interval setting 창 열기
    global menu_open
    menu_open = False
    subprocess.Popen([sys.executable, 'interval_setting.py'], cwd=os.getcwd())

def open_recent_record():
    global menu_open
    menu_open = False
    subprocess.Popen([sys.executable, 'recent_record.py'], cwd=os.getcwd())

def open_alarm():
    global menu_open
    menu_open = False
    subprocess.Popen([sys.executable, 'alarm.py'], cwd=os.getcwd())

def on_mouse(event, x, y, flags, param):			#마우스 동작 감지시 on_mouse 함수 호출
    global running, elapsed, last_time, records, total, menu_open

    if event != cv2.EVENT_LBUTTONDOWN:
        return

    # MENU 창에서의 클릭 처리
    if menu_open:
        if is_button_clicked(interval_setting_btn, x, y):
            open_interval_setting()
            return
        elif is_button_clicked(recent_record_btn, x, y):
            open_recent_record()
            return
        elif is_button_clicked(alarm_btn, x, y):
            open_alarm()
            return
        
    # TIMER 창에서의 클릭 처리
    if is_button_clicked(start_btn, x, y):
        running = True
        last_time = time.time()
    elif is_button_clicked(pause_btn, x, y):
        running = False
    elif is_button_clicked(reset_btn, x, y):
        running = False
        elapsed = 0.0
        records = []
    elif is_button_clicked(record_btn, x, y) and total != 0 and running:
        records.append(elapsed)
        if len(records) > MAX_RECORDS:
            records.pop(0)
    elif is_button_clicked(menu_btn, x, y):
        menu_open = not menu_open

def draw_button(frame, rect, label):				#버튼 화면 출력 함수
    (x1, y1), (x2, y2) = rect
    cv2.rectangle(frame, (x1, y1), (x2, y2), (60, 60, 60), -1)
    (tw, th), _ = cv2.getTextSize(label, font_timer, 0.7, 2)
    text_x = x1 + (x2 - x1 - tw) // 2
    text_y = y1 + (y2 - y1 + th) // 2
    cv2.putText(frame, label, (text_x, text_y), font_timer, 0.7, (255, 255, 255), 2)

cv2.namedWindow("TIMER")
cv2.setMouseCallback("TIMER", on_mouse)				#마우스 동작 감지

while True:							#실시간 동작
    frame = np.zeros((600, 500, 3), dtype=np.uint8)		#프레임 정의

    if running:							#동작 확인
        now = time.time()
        elapsed += now - last_time
        last_time = now

    total = elapsed						#시간 변수 설정 초,분,미리초
    minute = int(total // 60)
    second = total % 60
    timer_text = f"{minute:02d}:{int(second):02d}"
    frac_part = f".{int((second - int(second)) * 100):02d}"

    cv2.putText(frame, timer_text, (115, 200), font_timer, 3, (0, 255, 0), 5)
    cv2.putText(frame, frac_part, (380, 200), font_timer, 1, (0,255,0), 2)
    
    draw_button(frame, start_btn, "Start")			#버튼 화면 출력
    draw_button(frame, pause_btn, "Pause")
    draw_button(frame, reset_btn, "Reset")
    draw_button(frame, record_btn, "Rec")
    draw_button(frame, menu_btn, "menu")
    
    base_x = 60
    base_y = 260
    line_gap = 25

    for idx, t in enumerate(records):				#기록 저장 반복문
        total_r = t
        m = int(total_r // 60)
        s = total_r % 60
        text_int  = f"{m:02d}:{int(s):02d}"
        text_frac = f".{int((s - int(s)) * 100):02d}"
        record_text = f"{idx+1:02d}) {text_int}{text_frac}"
        y = base_y + idx * line_gap
        cv2.putText(frame, record_text, (base_x, y), font_timer, 0.7, (200, 200, 200), 1)
                    
    if menu_open:
        menu_frame = np.zeros((400, 300, 3), dtype=np.uint8)
        cv2.putText(menu_frame, "MENU", (40, 80), font_timer, 1, (0, 255, 255), 2)
        draw_button(menu_frame, interval_setting_btn, "Interval Setting")
        draw_button(menu_frame, recent_record_btn, "recent record")
        draw_button(menu_frame, alarm_btn, "alarm")
        cv2.imshow("MENU", menu_frame)
        cv2.setMouseCallback("MENU", on_mouse)
    else:
        try:
            cv2.destroyWindow("MENU")
        except:
            pass
    
    cv2.imshow("TIMER", frame)
    if cv2.waitKey(50) & 0xFF == ord('q'):			#"q" 누를시 창 종료
        break

cv2.destroyAllWindows()
