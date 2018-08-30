# -*- coding: utf-8 -*-\
# Made by Renhao Huang
from tkinter import *
from PIL import Image, ImageTk  # require "pip install pillow"
from math import *
import time, random, sys, os

window = Tk()
frame = Frame()
frame.pack()
bg = Image.open("bg.jpg").resize((800, 800))
bg = ImageTk.PhotoImage(bg)
canvas = Canvas(window, width=800, height=800, bg='white')
canvas.pack()
canvas.create_image(400, 400, image=bg)
score = canvas.create_text(10, 10, anchor="nw")
canvas.itemconfig(score, text="Score: ")
p = PhotoImage(file="plane.png")
Enermy_img=[]
bubble1 = PhotoImage(file="bubble.png").subsample(5, 5)
bubble2 = PhotoImage(file="bubble-2.png").subsample(5,5)
#candy = PhotoImage(file="candy.png").subsample(20,20)
Enermy_img.append(bubble1)
Enermy_img.append(bubble2)
#Enermy_img.append(candy)
#add more materials here

def pause():
    global speed
    speed = 0


def easy():
    global speed
    speed = 1


def middle():
    global speed
    speed = 2


def hard():
    global speed
    speed = 5


def restart_program():  # stackoverflow
    python = sys.executable
    os.execl(python, python, *sys.argv)

#buttons
speed = 0
easy = Button(frame, text="简单", width=21, command=easy)
mid = Button(frame, text="中等", width=21, command=middle)
high = Button(frame, text="难", width=21, command=hard)
pause = Button(frame, text="暂停", width=21, command=pause)
restart = Button(frame, text="重新开始", width=21, command=restart_program)
easy.pack(side=LEFT)
mid.pack(side=LEFT)
high.pack(side=LEFT)
pause.pack(side=LEFT)
restart.pack(side=LEFT)


class Field:
    def __init__(self, shuttle):
        self.plane = shuttle
        self.score = 0
        self.enermy = []

    def create_enermies(self, n):
        for i in range(0, n):
            enermy = Enermy()
            if not self.enermy_is_covered(enermy):
                self.enermy.append(enermy)
                enermy.drawEnermy()

    def enermy_attack(self):
        self.create_enermies(random.randint(3, 10))
        for i in range(0, 12):
            for enermy in self.enermy:
                enermy.move()

    def enermy_is_covered(self, en):
        for enermy in self.enermy:
            delta_x = abs(en.x - enermy.x)
            delta_y = abs(en.y - enermy.y)
            dist = sqrt(pow(delta_x, 2) + pow(delta_y, 2))
            if dist < 2 * enermy.r + 20:
                return True
        return False

    def isHitted(self, bullet):
        for enermy in self.enermy:
            if bullet.x >= enermy.x - enermy.r and bullet.x <= enermy.x + enermy.r and bullet.y >= enermy.y - enermy.r and bullet.y <= enermy.y + enermy.r:
                return enermy
        return None

    def hit(self, bullet, enermy):
        canvas.delete(enermy.id)
        canvas.delete(bullet.id)
        self.plane.remove_bullet(bullet)
        self.enermy.remove(enermy)
        self.score = self.score + 5
        mark = self.score
        canvas.itemconfig(score, text="Score: ")
        canvas.insert(score, 12, self.score)

    def loss(self, enermy):
        global speed
        if enermy.y > 800:
            speed = 0
            canvas.create_text(400, 400, text="Game Over, Score: " + str(self.score), font=('arial 45 bold'),
                               fill='red')
            canvas.master.update()
            self.freeEnermy()
            for button in [easy, mid, high]:
                button.config(state=DISABLED)

    def freeEnermy(self):
        canvas.delete('enermy')
        self.enermy = []


class Plane:
    def __init__(self):
        self.x_from = 260
        self.x_to = 330
        self.y_from = 660
        self.y_to = 750
        self.bullet = []
        self.id = 0

    def isInside(self, x, y):
        if x < self.x_from or x > self.x_to or y < self.y_from or y > self.y_to:
            return False
        else:
            delta_y = abs(self.y_to - self.y_from)
            delta_x = abs(self.x_to - self.x_from)
            degree = atan(2 * delta_y / delta_x)
            gap_y = abs(self.y_to - y)
            gap_x = gap_y / tan(degree)
            if x > (self.x_from + gap_x) and x < (self.x_to - gap_x):
                return True
            else:
                return False

    def reset(self, move_x, move_y):
        self.x_from = self.x_from + move_x
        self.x_to = self.x_to + move_x
        self.y_from = self.y_from + move_y
        self.y_to = self.y_to + move_y

    @property
    def XOutBound(self):
        if self.x_from < 10:
            return True
        if self.x_to > 790:
            return True

    @property
    def YOutBound(self):
        if self.y_from < 10:
            return True
        if self.y_to > 790:
            return True

    def shoot(self):
        y = self.y_from
        x = (self.x_to + self.x_from) / 2
        bullet = Bullet(x, y)
        self.bullet.append(bullet)
        bullet.drawBullet()
        bullet.move()

    def remove_bullet(self, bullet):
        self.bullet.remove(bullet)

    def create_plane(self):
        self.id = canvas.create_image(300, 700, image=p)
    
    def move_plane(self,delta_x,delta_y):
        self.reset(delta_x, delta_y)
        if self.XOutBound:
            self.reset(-delta_x, 0)
            delta_x = 0
        if self.YOutBound:
            self.reset(0, -delta_y)
            delta_y = 0
        canvas.move(self.id, delta_x, delta_y)


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.id = 0

    def drawBullet(self):
        x = self.x
        y = self.y
        bullet = canvas.create_oval(x - 2, y - 4, x + 2, y + 4, outline='black', fill='white')
        self.id = bullet

    def move(self):
        bullet = self.id
        top = self.y - 4
        while top > 0:
            canvas.move(bullet, 0, -2)
            canvas.update()
            top = top - 2
            self.y = self.y - 2
            enermy = field.isHitted(self)
            if enermy != None:
                field.hit(self, enermy)
                return
        canvas.delete(bullet)


class Enermy:
    def __init__(self):
        self.x = random.randint(120, 680)
        self.y = 0
        self.r = 40
        self.id = 0

    def drawEnermy(self):
        x = self.x
        y = self.y
        r = self.r
        enermy = canvas.create_image(x, y, tags='enermy', image=random.choice(Enermy_img))
        self.id = enermy

    def move(self):
        global speed
        time.sleep(0.01)
        canvas.move(self.id, 0, speed)
        canvas.update()
        self.y = self.y + speed
        field.loss(self)


plane = Plane()
plane.create_plane()
field = Field(plane)


def position(event):
    global x, y
    x = event.x
    y = event.y


def plane_move(event):
    global x, y
    if plane.isInside(x, y):
        delta_x = event.x - x
        delta_y = event.y - y
        plane.move_plane(delta_x,delta_y)
        x = event.x
        y = event.y


def shoot(event):
    if speed != 0:
        plane.shoot()


canvas.bind("<ButtonPress-1>", position)
canvas.bind("<B1-Motion>", plane_move)
canvas.bind("<Button-3>", shoot)
try:
    while True:
        field.enermy_attack()
        speed = speed * 1.05
except TclError:
    pass

window.mainloop()
