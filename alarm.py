import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# 알람
alarms = []

def check_alarms():
    now = datetime.now()
    current_key = now.strftime("%Y-%m-%d %H:%M")

    for alarm in alarms:
        if not alarm["enabled"]:
            continue

        if alarm["hour"] == now.hour and alarm["minute"] == now.minute:
            if alarm.get("last_triggered") != current_key:
                alarm["last_triggered"] = current_key
                show_alarm_popup(alarm)

    root.after(1000, check_alarms)


#알람 팝업 기능
def show_alarm_popup(alarm):
    popup = tk.Toplevel(root)
    popup.title("운동 알람")
    popup.attributes("-topmost", True) 

    tk.Label(popup, text=f"[{alarm['label']}]", font=("맑은 고딕", 12, "bold")).pack(padx=20, pady=5)
    tk.Label(popup, text=alarm["memo"], font=("맑은 고딕", 10)).pack(padx=20, pady=5)

    note_var = tk.StringVar()

    tk.Label(popup, text="간단 기록(선택):").pack(padx=20, pady=(10, 0))
    tk.Entry(popup, textvariable=note_var, width=30).pack(padx=20, pady=5)

#파일 저장
    def done(status):
        print("----- 알람 기록 -----")
        print("시간 :", f"{alarm['hour']:02d}:{alarm['minute']:02d}")
        print("제목 :", alarm["label"])
        print("메모 :", alarm["memo"])
        print("상태 :", status)
        print("추가 메모 :", note_var.get())
        print("---------------------")
        popup.destroy()

    btn_frame = tk.Frame(popup)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="운동함", width=10, command=lambda: done("운동함")).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="오늘은 건너뛰기", width=15, command=lambda: done("건너뜀")).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="닫기", width=8, command=popup.destroy).grid(row=0, column=2, padx=5)

'''알람 추가'''
def add_alarm():
    try:
        hour = int(hour_var.get())
        minute = int(min_var.get())
    except ValueError:
        messagebox.showerror("입력 오류", "시와 분은 숫자로 입력해주세요.")
        return

    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        messagebox.showerror("입력 오류", "시간 형식이 올바르지 않습니다. (0~23시, 0~59분)")
        return

    label = label_var.get().strip()
    memo = memo_var.get().strip()

    if label == "":
        label = "운동 알람"

    alarm = {
        "hour": hour,
        "minute": minute,
        "label": label,
        "memo": memo,
        "enabled": True,
        "last_triggered": None
    }

    alarms.append(alarm)
    listbox.insert(tk.END, f"{hour:02d}:{minute:02d} | {label}")
    label_var.set("")

# 선택 알람 삭제
def delete_alarm():
    sel = listbox.curselection()
    if not sel:
        return
    index = sel[0]
    listbox.delete(index)
    alarms.pop(index)


# 메인
root = tk.Tk()
root.title("메모가 있는 운동 알람")

# 입력 기능
input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=10)

hour_var = tk.StringVar(value="7")
min_var = tk.StringVar(value="0")
label_var = tk.StringVar(value="아침 운동")
memo_var = tk.StringVar(value="예: 스쿼트 3세트, 런닝 20분")

tk.Label(input_frame, text="시").grid(row=0, column=0)
tk.Entry(input_frame, textvariable=hour_var, width=5).grid(row=0, column=1)

tk.Label(input_frame, text="분").grid(row=0, column=2)
tk.Entry(input_frame, textvariable=min_var, width=5).grid(row=0, column=3)

tk.Label(input_frame, text="제목").grid(row=1, column=0, pady=(5, 0))
tk.Entry(input_frame, textvariable=label_var, width=25).grid(row=1, column=1, columnspan=3, pady=(5, 0))

tk.Label(input_frame, text="메모").grid(row=2, column=0, pady=(5, 0))
tk.Entry(input_frame, textvariable=memo_var, width=25).grid(row=2, column=1, columnspan=3, pady=(5, 0))

tk.Button(input_frame, text="알람 추가", command=add_alarm).grid(row=3, column=0, columnspan=2, pady=8, sticky="we")
tk.Button(input_frame, text="알람 삭제", command=delete_alarm).grid(row=3, column=2, columnspan=2, pady=8, sticky="we")

# 알람 리스트
listbox = tk.Listbox(root, width=40)
listbox.pack(padx=10, pady=(0, 10))

# 알람 체크 시작
check_alarms()

root.mainloop()
