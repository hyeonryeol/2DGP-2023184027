# pico2d / LEC11 시험용 참고 자료 (실행용 아님, 전부 주석)

# ===============================================================
# ===================== 시험용 참고 자료 ===========================
# ===============================================================
#
# ---------------- [1] pico2d 함수 정리 ----------------
# open_canvas()                 : 800 x 600 창 생성 (기본값)
# open_canvas(w, h)             : 원하는 크기로 창 생성. 예) open_canvas(1280, 1024)
# close_canvas()                : 창 닫기
# clear_canvas()                : 화면 지우기
# update_canvas()               : 그린 것을 화면에 표시
# delay(초)                     : 대기. delay(0.05) = 0.05초
# get_time()                    : 프로그램 시작 후 경과 시간(초, 실수)
# hide_cursor() / show_cursor() : 마우스 커서 숨기기/보이기
#
# img = load_image('파일.png')  : 이미지 로드 (반드시 open_canvas() 뒤에!)
# img.w, img.h                  : 이미지 폭, 높이
# img.draw(x, y)                : 이미지 중심을 (x, y)에 그림
# img.draw(x, y, w, h)          : 크기를 w x h로 바꿔서 그림
# img.clip_draw(l, b, w, h, x, y)        : 시트에서 (l,b)부터 w x h 잘라서 (x,y)에 그림
# img.clip_draw(l, b, w, h, x, y, W, H)  : 잘라서 W x H 크기로 그림
# img.clip_composite_draw(l, b, w, h, 각도(라디안), 'h', x, y, W, H)
#     -> 'h' = 좌우 반전, 'v' = 상하 반전, '' = 반전 없음
#     -> 왼쪽으로 달리는 그림이 없을 때 좌우 반전에 사용
#        예) self.image.clip_composite_draw(self.frame*100, 0, 100, 100, 0, 'h', self.x, self.y, 100, 100)
# draw_rectangle(x1, y1, x2, y2): 사각형 테두리 그리기 (충돌 박스 확인용)
#
# 좌표계: 왼쪽 아래가 (0, 0), 위로 갈수록 y 증가
#   -> 마우스 event.y는 위가 0이므로 뒤집어야 함:  y = 600 - 1 - event.y
#      (캔버스 높이가 다르면 600 대신 그 높이. 예: TUK_HEIGHT - 1 - event.y)
#
# ---------------- [2] 이 폴더 이미지 크기 ----------------
# grass.png                 802 x 62    -> draw(400, 30)
# run_animation.png         802 x 102   -> 100x100 프레임 8장 (한 줄)
# animation_sheet.png       802 x 402   -> 100x100 프레임 8장 x 4줄
#     (아래 줄부터) bottom=0   : 왼쪽으로 달리기
#                   bottom=100 : 오른쪽으로 달리기
#                   bottom=200 : 왼쪽 보고 서 있기(idle)
#                   bottom=300 : 오른쪽 보고 서 있기(idle)
#     예) 오른쪽 달리기: img.clip_draw(frame * 100, 100, 100, 100, x, y)
# zombie_run_animation.png  4300 x 519  -> 프레임 10장 (한 장 430 x 519, 그대로 그리면 너무 커서 절반으로 그림)
# character.png             42 x 92     -> 한 장짜리. draw(x, y)
# ball21x21.png             작은 공      -> draw(x, y)
# ball41x41.png             큰 공        -> draw(x, y)
#
# ---------------- [3] 이벤트(입력) 처리 패턴 ----------------
# def handle_events():
#     global running, dx, x, y          # 바꾸는 전역 변수는 전부 global 선언
#     events = get_events()
#     for event in events:
#         if event.type == SDL_QUIT:
#             running = False
#         elif event.type == SDL_KEYDOWN:            # 키 누름
#             if event.key == SDLK_ESCAPE:
#                 running = False
#             elif event.key == SDLK_RIGHT:
#                 dx += 1
#             elif event.key == SDLK_LEFT:
#                 dx -= 1
#         elif event.type == SDL_KEYUP:              # 키 뗌 (누르고 있는 동안만 움직이게 할 때)
#             if event.key == SDLK_RIGHT:
#                 dx -= 1
#             elif event.key == SDLK_LEFT:
#                 dx += 1
#         elif event.type == SDL_MOUSEMOTION:        # 마우스 이동
#             x, y = event.x, 600 - 1 - event.y
#         elif event.type == SDL_MOUSEBUTTONDOWN:    # 마우스 클릭
#             if event.button == SDL_BUTTON_LEFT:
#                 pass
#
# 키 상수: SDLK_ESCAPE, SDLK_SPACE, SDLK_RETURN(엔터),
#          SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN,
#          SDLK_a ~ SDLK_z, SDLK_0 ~ SDLK_9
# 마우스: SDL_BUTTON_LEFT, SDL_BUTTON_RIGHT
#
# ---------------- [4] 새 게임 객체 추가하는 법 ----------------
# 1) 클래스 만들기: __init__ / update / draw 세 개 필수
# 2) reset_world()에서 생성해서 world에 추가
# 이것만 하면 update_world(), render_world()가 알아서 처리함
#
# 예) 위에서 떨어지는 공 (작은 공/큰 공 랜덤, 속도 랜덤, 잔디 위에서 멈춤)
# class Ball:
#     def __init__(self):
#         self.x, self.y = random.randint(100, 700), 599   # 화면 위쪽에서 시작
#         self.speed = random.randint(5, 15)               # 떨어지는 속도 랜덤
#         if random.randint(0, 1) == 0:                    # 반반 확률로 작은 공/큰 공
#             self.image = load_image('ball21x21.png')
#             self.r = 10                                  # 반지름 (21 // 2)
#         else:
#             self.image = load_image('ball41x41.png')
#             self.r = 20                                  # 반지름 (41 // 2)
#     def update(self):
#         self.y -= self.speed                     # 아래로 이동
#         if self.y - self.r < 60:                 # 공 아래쪽이 잔디 윗면(약 60)에 닿으면
#             self.y = 60 + self.r                 # 잔디 위에 딱 맞춰 놓고
#             self.speed = 0                       # 멈춤
#     def draw(self):
#         self.image.draw(self.x, self.y)
#
# reset_world()에 추가:
#     balls = [Ball() for i in range(20)]
#     world += balls
#
# ---------------- [5] 자주 쓰는 패턴 ----------------
# - 화면 끝에서 방향 전환:
#       if self.x > 800 or self.x < 0: self.dir *= -1
# - 화면 밖으로 못 나가게 막기:
#       self.x = clamp(0, self.x, 800)        # pico2d의 clamp(최소, 값, 최대)
# - 프레임 반복: self.frame = (self.frame + 1) % 프레임수
# - 랜덤: random.randint(a, b)  -> a 이상 b 이하 정수 (b 포함!)
# - 반복하면서 world에서 객체 삭제할 때는 복사본으로 돌기:
#       for o in world[:]:
#           if 조건: world.remove(o)
# - 객체 여러 개 생성: [Boy() for i in range(11)]
# - 그리는 순서 = world에 넣은 순서 (배경을 제일 먼저 넣기)
#
# ---------------- [6] 자주 나는 에러 ----------------
# - load_image 에러          : open_canvas() 전에 이미지를 로드함 / 파일 이름 오타 / 실행 폴더가 다름
# - 값이 안 바뀜             : 함수 안에서 global 선언 안 함
# - 'xxx' object has no attribute 'update' : 클래스에 update/draw 빠뜨림 (Grass처럼 pass라도 써야 함)
# - 화면이 안 바뀜           : update_canvas() 빠뜨림
# - 잔상이 남음              : clear_canvas() 빠뜨림
# - 창이 바로 꺼짐/멈춤       : while 루프 안에 handle_events() 빠뜨림
#
# ---------------- [7] 공 차기 (소년이 공에 닿으면 공이 날아감) ----------------
# 핵심 아이디어
#  1) 공은 속도 dx, dy를 가짐 (가만히 있으면 둘 다 0)
#  2) 매 프레임 "소년과 공이 닿았는지" 검사 -> 닿으면 공에 속도를 줌(= 차기)
#  3) 공은 update에서 dy에 중력을 빼서 포물선으로 날아가고, 잔디에 닿으면 튕김
#
# class Ball:
#     def __init__(self):
#         self.x, self.y = random.randint(200, 700), 60 + 10   # 잔디 위에 놓인 작은 공
#         self.r = 10                                          # 반지름 (ball21x21 -> 10)
#         self.dx, self.dy = 0, 0                              # 처음엔 멈춰 있음
#         self.image = load_image('ball21x21.png')
#     def kick(self):
#         self.dx = random.randint(10, 20)     # 오른쪽으로 (소년이 오른쪽으로 달리니까)
#         self.dy = random.randint(10, 20)     # 위로 띄우기
#     def update(self):
#         self.x += self.dx
#         self.y += self.dy
#         if self.y - self.r > 60 or self.dy > 0:   # 공중에 있으면
#             self.dy -= 1                           # 중력 (매 프레임 아래쪽으로 속도 감소)
#         if self.y - self.r < 60:                   # 잔디에 닿으면
#             self.y = 60 + self.r                   # 잔디 위로 올려놓고
#             self.dy = -self.dy * 0.6               # 튕김 (0.6 = 탄성, 작을수록 덜 튐)
#             self.dx *= 0.8                         # 땅에 닿을 때마다 굴러가는 속도 감소(마찰)
#             if abs(self.dy) < 2: self.dy = 0       # 거의 안 튀면 멈춤
#         if self.x > 800 - self.r or self.x < self.r:   # 화면 양 끝 벽에 튕기기
#             self.dx = -self.dx
#             self.x = clamp(self.r, self.x, 800 - self.r)
#     def draw(self):
#         self.image.draw(self.x, self.y)
#
# 충돌(닿았는지) 검사 - 둘 중 하나 사용
#  (a) 거리로: 소년 중심과 공 중심의 거리가 가까우면
#        def is_touch(boy, ball):
#            return abs(boy.x - ball.x) < 30 and abs(boy.y - ball.y) < 50
#  (b) 사각형으로(정석): 두 사각형이 겹치는지
#        boy 영역 : (x-20, y-50) ~ (x+20, y+50)     ball 영역 : (x-r, y-r) ~ (x+r, y+r)
#        def is_touch(boy, ball):
#            bl, bb, br, bt = boy.x - 20, boy.y - 50, boy.x + 20, boy.y + 50
#            ll, lb, lr, lt = ball.x - ball.r, ball.y - ball.r, ball.x + ball.r, ball.y + ball.r
#            if br < ll or bl > lr: return False   # 좌우로 안 겹침
#            if bt < lb or bb > lt: return False   # 위아래로 안 겹침
#            return True
#        (확인용) draw()에서 draw_rectangle(bl, bb, br, bt) 로 박스를 그려볼 수 있음
#
# reset_world()에서 boys, balls를 따로 리스트로 만들고 global로 기억해 둠:
#     global boys, balls
#     boys = [Boy() for i in range(11)]
#     balls = [Ball() for i in range(5)]
#     world += boys
#     world += balls
#
# update_world()에서 모든 객체 update 후 충돌 검사:
#     def update_world():
#         for o in world:
#             o.update()
#         for boy in boys:
#             for ball in balls:
#                 if is_touch(boy, ball) and ball.dx < 5:   # 이미 날아가는(빠른) 공은 또 안 차게
#                     ball.kick()
#
# [변형] 스페이스바를 눌렀을 때만 차기
#  - handle_events()의 KEYDOWN에서:  elif event.key == SDLK_SPACE: kick_pressed = True  (global 선언!)
#  - update_world()에서:             if kick_pressed and is_touch(boy, ball): ball.kick()
#                                    검사 끝나면 kick_pressed = False
# [변형] 소년이 왼쪽으로 달릴 때는 dx를 음수로:  self.dx = random.randint(10, 20) * boy.dir
#        (kick(self, dir) 처럼 방향을 인자로 받기)
# ===============================================================
