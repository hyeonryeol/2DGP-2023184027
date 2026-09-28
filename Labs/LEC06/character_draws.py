from pico2d import *
import math
open_canvas(800, 600)

character = load_image('character.png')

cx, cy = 400, 300   # 원운동 중심
r = 200             # 원운동 반지름
frame_delay = 0.01  # 한 프레임마다 기다리는 시간

# 화면을 지우고 (x, y)에 캐릭터를 한 프레임 그리기
def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(frame_delay)

# 사각형 위 변: 왼쪽 위에서 오른쪽 위로
def move_top():
    print("Top")
    for x in range(50, 750, 5):
        draw_character(x, 550)

# 사각형 오른쪽 변: 오른쪽 위에서 오른쪽 아래로
def move_right():
    print("Right")
    for y in range(550, 50, -5):
        draw_character(750, y)

# 사각형 아래 변: 오른쪽 아래에서 왼쪽 아래로
def move_bottom():
    print("Bottom")
    for x in range(750, 50, -5):
        draw_character(x, 50)

# 사각형 왼쪽 변: 왼쪽 아래에서 왼쪽 위로
def move_left():
    print("Left")
    for y in range(50, 550, 5):
        draw_character(50, y)

# 삼각형 아래 변: 왼쪽 아래에서 오른쪽 아래로
def move_triangle_bottom():
    print("Triangle Bottom")
    for x in range(50, 750, 5):
        draw_character(x, 50)

# 삼각형 오른쪽 변: 오른쪽 아래에서 꼭짓점으로
def move_triangle_right():
    print("Triangle Right")
    for i in range(0, 100):
        x = 750 + (400 - 750) * i / 100
        y = 50 + (550 - 50) * i / 100
        draw_character(x, y)

# 삼각형 왼쪽 변: 꼭짓점에서 왼쪽 아래로
def move_triangle_left():
    print("Triangle Left")
    for i in range(0, 100):
        x = 400 + (50 - 400) * i / 100
        y = 550 + (50 - 550) * i / 100
        draw_character(x, y)

# 중심 (cx, cy), 반지름 r인 원을 5도씩 한 바퀴 돌기
def move_circle():
    print("Circle")
    for deg in range(0, 360, 5):
        angle = math.radians(deg)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        draw_character(x, y)

# 사각형 네 변을 차례로 돌기
def move_rectangle():
    print("Rectangle")
    move_top()
    move_right()
    move_bottom()
    move_left()

# 삼각형 세 변을 차례로 돌기
def move_triangle():
    print("Triangle")
    move_triangle_bottom()
    move_triangle_right()
    move_triangle_left()


# 원 -> 사각형 -> 삼각형 운동을 무한 반복
while True:
    move_circle()
    move_rectangle()
    move_triangle()

close_canvas()