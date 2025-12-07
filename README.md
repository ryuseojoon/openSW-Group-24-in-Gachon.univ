##Exercise Timer & Tracker

러닝 페이스 기록 · 스톱워치 · 운동 알람 · 인터벌 설정 메뉴 통합 프로그램
그룹 24: 류서준(조장), 윤해민, 최하연, 김민주, 구한결

#사용 기술

Python 3
OpenCV (cv2)
Tkinter
time / datetime
numpy
subprocess / sys / os

참고자료 : ChatGPT


# Timer_UI (메인 타이머 UI)

Timer_UI는 모든 기능(스톱워치, 인터벌 설정, 최근 기록, 알람)을 중앙에서 실행할 수 있는 메인 화면이다.

핵심 기능

1) 스톱워치 기능 포함
-시작(Start)
-일시정지(Pause)
-초기화(Reset)
-랩 기록 저장(Rec)
-최대 7개 기록 표시

2) 버튼 클릭 UI
OpenCV 창에서 마우스를 클릭하면 버튼이 작동한다.
버튼 목록:
Start
Pause
Reset
Rec
Menu

3) MENU 버튼 → 서브 기능 실행 (MENU를 열면 아래 모듈들이 실행된다.)
-버튼	실행되는 파일---(Interval Setting -> interval_setting.py,    Recent Record ->	recent_record.py,     Alarm	-> alarm.py)
-각 기능은 subprocess.Popen으로 별도의 창에서 실행된다.

4) 타이머 표시 방식
-MM:SS.xx 포맷
-초의 소수점 두 자리까지 표시
-실시간 업데이트

5) Lap 기록 표시
-최대 7개 저장
-오래된 기록부터 삭제


# Stopwatch

타이머 UI 내부에서 동작하는 스톱워치 기능의 독립 버전.

기능

-Start : 타이머 증가
-Pause : 일시정지
-Reset : 0으로 초기화
-Lap(Rec) : 랩 타임 저장

# Running Pace Tracker (OpenCV 기반)

러닝 기록을 자동 계산하며, 페이스 변화율까지 비교해주는 기능.

1)기능 요약
-페이스 자동 계산
-거리(km), 시간 입력 → 1km 페이스 자동 계산
-페이스 변화율 비교
-빨라지면 빨간 up
-느려지면 파란 down
-퍼센트 변화율 함께 표시
-Timestamp 자동 저장
-현재 시간 자동 기록
-과거 기록 입력 시 자동 정렬
-변화율 전체 재계산

2)삭제 모드
-X 키 → 삭제 모드 전환
-기록 클릭 → 삭제

3)단축키

메인 화면
-A : 기록 추가
-X : 삭제모드
-Q/ESC : 종료

기록 추가 화면
-Tab/Enter : 다음 칸
-S : 저장
-ESC : 취소

# 운동 알람 기능 (Tkinter 기반)

지정한 시간에 알림 팝업을 띄움.

1)기능

-알람 추가 (hour, minute, label, memo)
-1초마다 시간 체크
-시간 일치 시 팝업 띄움

2)팝업 구성
-알람 제목
-메모
-운동 여부 버튼 - [운동함]/[오늘 건너뛰기] → 콘솔에 기록됨

# Interval Setting 기능

인터벌 트레이닝을 위한 타이머 기능. 준비시간 → 운동 → 휴식을 설정한 횟수만큼 반복한다.

1) 기능 요약

-2가지 모드 : SETTING(설정), TIMER(실행)
-준비시간, 운동시간, 휴식시간 각각 설정 가능
-반복횟수(Repetitions) 설정
-자동 단계 전환 (카운트다운 방식)
-설정 저장 (interval_config.json)

2) SETTING 모드

-시간 조정 버튼
-각 단계(준비/운동/휴식)마다 +1s, -1s, +1m, -1m 버튼 제공
-MM:SS 형식으로 시간 표시
-반복횟수 설정
-+/- 버튼으로 조정
-하단 버튼
-Save & Start : 설정 저장 후 TIMER 모드로 전환
-Cancel : 종료

3) TIMER 모드

-3가지 단계 표시 (색상 구분)
-PREP (준비) : 노란색
-EXERCISE (운동) : 초록색
-REST (휴식) : 주황색
-Rep 카운터 : 현재 회차/전체 회차 표시
-카운트다운 타이머
-MM:SS.xx 형식 (소수점 두 자리)
-각 단계 종료 시 자동 일시정지
-단계 전환 후 Start 버튼으로 재개
-버튼
-Start : 타이머 시작/재개
-Pause : 일시정지
-Back to Setting : SETTING 모드로 복귀

4) 데이터 저장

-interval_config.json 파일에 설정 자동 저장
-프로그램 재실행 시 이전 설정 자동 불러오기

5) 단축키

-Q : 프로그램 종료
