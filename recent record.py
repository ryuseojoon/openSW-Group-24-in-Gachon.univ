#러닝 페이스 기록 기능
import cv2
import numpy as np
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class RunRecord:
    #러닝 기록 데이터
    distance_km: float
    total_time_sec: int
    pace_per_km_sec: float
    timestamp: datetime
    pace_change_percent: Optional[float] = None
    pace_change_direction: Optional[str] = None  # up(faster)/down(slower)/same


class RunningPaceTracker:
    #기록 저장, 정렬, 페이스 변화율 계산 등 핵심 로직

    def __init__(self):
        self.records: List[RunRecord] = []

    # 문자열 초 변환
    @staticmethod
    def parse_time_to_seconds(time_str: str) -> int:
        parts = time_str.strip().split(":")
        if len(parts) == 2:
            h, m, s = 0, int(parts[0]), int(parts[1])
        elif len(parts) == 3:
            h, m, s = int(parts[0]), int(parts[1]), int(parts[2])
        else:
            raise ValueError("Time must be MM:SS or HH:MM:SS.")
        total = h*3600 + m*60 + s
        if total <= 0:
            raise ValueError("Time must be > 0.")
        return total

    @staticmethod
    def format_pace_short(sec: float) -> str:
        sec = int(round(sec))
        return f"{sec//60}:{sec%60:02d}/km"

    @staticmethod
    def parse_timestamp(ts_str: str) -> datetime:
        return datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
    
    # 전체 페이스 변화 재계산
    def _recompute_changes(self):
        if not self.records:
            return
        for i, rec in enumerate(self.records):
            if i == 0:
                rec.pace_change_percent = None
                rec.pace_change_direction = None
            else:
                prev = self.records[i-1]
                diff = prev.pace_per_km_sec - rec.pace_per_km_sec
                if diff == 0:
                    rec.pace_change_percent = 0
                    rec.pace_change_direction = "same"
                else:
                    pct = abs(diff)/prev.pace_per_km_sec*100
                    rec.pace_change_percent = pct
                    rec.pace_change_direction = "up" if diff > 0 else "down"

    # 기록 추가
    def add_record(self, dist: float, time_str: str, ts: Optional[str]):
        total_sec = self.parse_time_to_seconds(time_str)
        pace = total_sec / dist
        timestamp = self.parse_timestamp(ts) if ts else datetime.now()

        rec = RunRecord(dist, total_sec, pace, timestamp)
        self.records.append(rec)
        self.records.sort(key=lambda r: r.timestamp)
        self._recompute_changes()

    # 특정 기록 삭제
    def delete_record(self, idx: int):
        if 0 <= idx < len(self.records):
            self.records.pop(idx)
            self._recompute_changes()


# 텍스트
def draw_text(img, text, pos, scale=1, color=(255,255,255), thick=2, center=False):
    font = cv2.FONT_HERSHEY_SIMPLEX
    if center:
        (w, h), _ = cv2.getTextSize(text, font, scale, thick)
        pos = (pos[0]-w//2, pos[1]+h//2)
    cv2.putText(img,text,pos,font,scale,color,thick,cv2.LINE_AA)


# 대시보드
def draw_dashboard(tracker, delete_mode=False):
    h, w = 620, 480
    img = np.zeros((h,w,3), np.uint8)

    # 타이틀
    draw_text(img, "RUNNING PACE", (w//2, 40), 1.2, (0,255,255), 3, center=True)

    # 상단 버튼
    cv2.rectangle(img,(20,80),(210,115),(200,200,200),2)
    draw_text(img,"recent record",(35,103),0.75)

    cv2.rectangle(img,(330,80),(460,115),(200,200,200),2)
    draw_text(img,"back",(350,103),0.75)

    # 리스트
    row_boxes = []
    start_y = 135
    row_h = 85
    recs = tracker.records
    for i in range(min(len(recs),5)):
        idx = len(recs)-1-i
        rec = recs[idx]
        y1,y2 = start_y+i*row_h, start_y+i*row_h+75
        color = (0,150,255) if delete_mode else (150,150,150)
        cv2.rectangle(img,(20,y1),(460,y2),color,2)

        row_boxes.append((20,y1,460,y2,idx))

        draw_text(img, rec.timestamp.strftime("%Y.%m.%d"), (30,y1+30),0.7)
        draw_text(img, rec.timestamp.strftime("%H:%M:%S"), (30,y1+55),0.7)

        # 페이스 비교
        if rec.pace_change_percent is not None:
            pct = int(round(rec.pace_change_percent))
            if rec.pace_change_direction=="up":
                col=(0,0,255); txt=f"{pct}% up"
            else:
                col=(255,0,0); txt=f"{pct}% down"
            draw_text(img,txt,(190,y1+45),0.8,col)

        draw_text(img,tracker.format_pace_short(rec.pace_per_km_sec),
                  (330,y1+45),0.9,(0,255,0))

    # 도움말
    mode_msg = "DELETE MODE: Click row to delete (press X to exit)" if delete_mode \
               else "Press A to add, X to delete mode, Q to quit"
    draw_text(img,mode_msg,(w//2,600),0.55,(200,200,200),center=True)

    return img, row_boxes


#기록 입력
def draw_input(fields, active, err):
    h,w = 620,480
    img = np.zeros((h,w,3),np.uint8)

    draw_text(img,"ADD RECORD",(w//2,60),1.1,(0,255,255),3,center=True)

    labels=["Distance (km)","Time (MM:SS or HH:MM:SS)","Timestamp (optional)"]
    y=130
    inputs=[]

    for i,label in enumerate(labels):
        draw_text(img,label,(40,y-20),0.7)
        x1,x2 = 40,440
        y1,y2 = y,y+40
        cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,255) if i==active else (150,150,150),2)
        draw_text(img,fields[i],(x1+10,y+30),0.8,(0,255,0))
        inputs.append((x1,y1,x2,y2))
        y+=90

    draw_text(img,"If empty, current time will be used.",
              (w//2,inputs[2][3]+22),0.55,(200,200,200),center=True)

    draw_text(img,"[Tab/Enter] Next  [S] Save  [ESC] Cancel",
              (w//2,580),0.6,(200,200,200),center=True)

    if err:
        draw_text(img,err,(w//2,610),0.6,(0,0,255),center=True)

    return img


def main():
    tracker=RunningPaceTracker()
    cv2.namedWindow(WINDOW_NAME)

    mode="list"
    fields=["","",""]
    active=0
    err=""
    delete_mode=False
    row_boxes=[]

    def mouse(event,x,y,flags,param):
        nonlocal delete_mode, mode, row_boxes, tracker
        if mode!="list": return
        if event==cv2.EVENT_LBUTTONDOWN and delete_mode:
            for (x1,y1,x2,y2,idx) in row_boxes:
                if x1<=x<=x2 and y1<=y<=y2:
                    tracker.delete_record(idx)

    cv2.setMouseCallback(WINDOW_NAME, mouse)

    while True:
        # draw
        if mode=="list":
            img,row_boxes = draw_dashboard(tracker, delete_mode)
        else:
            img = draw_input(fields,active,err)

        cv2.imshow(WINDOW_NAME,img)
        key=cv2.waitKey(30)&0xFF
        if key==255: continue

        # 리스트 모드
        if mode=="list":
            if key in (ord('q'),27):
                break
            if key==ord('a'):
                mode="input"
                active=0
                err=""
                # timestamp 자동 채우기
                fields=["","", datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            if key==ord('x'):
                delete_mode=not delete_mode
            continue

        # 입력 모드
        if key==27:
            mode="list"
            err=""
            continue

        if key in (9,13):
            active=(active+1)%3
        elif key==8:
            if fields[active]:
                fields[active]=fields[active][:-1]
        elif key in (ord('s'),ord('S')):
            try:
                dist=float(fields[0])
                time_str=fields[1]
                ts=fields[2] if fields[2] else None
                tracker.add_record(dist,time_str,ts)
                mode="list"
                err=""
            except Exception as e:
                err=str(e)
        else:
            ch=chr(key)
            if active==0 and (ch.isdigit() or ch=='.'):
                fields[0]+=ch
            elif active==1 and (ch.isdigit() or ch==':'):
                fields[1]+=ch
            elif active==2 and (ch.isdigit() or ch in ['-',':',' ']):
                fields[2]+=ch

    cv2.destroyAllWindows()


if __name__=="__main__":
    WINDOW_NAME="RUNNING PACE"
    main()
