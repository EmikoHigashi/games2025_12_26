import tkinter as tk

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motorcar.py
矢印キー（Left / Right）で動くおもちゃの車（tkinter）
"""


WIDTH, HEIGHT = 600, 300
CAR_WIDTH, CAR_HEIGHT = 120, 50
WHEEL_RADIUS = 12
GROUND_Y = HEIGHT - 40
SPEED = 6  # ピクセル/更新

class MotorcarApp:
    def __init__(self, root):
        self.root = root
        root.title("おもちゃの車 - Left/Rightで操作")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#ccf0ff")
        self.canvas.pack()

        # 地面
        self.canvas.create_rectangle(0, GROUND_Y, WIDTH, HEIGHT, fill="#87d068", outline="")

        # 初期車位置（中央下）
        x = WIDTH // 2
        y = GROUND_Y - 10
        self.car_items = self._create_car(x, y)

        # 移動状態
        self.moving_left = False
        self.moving_right = False

        # キーイベント取得
        root.bind("<KeyPress-Left>", lambda e: self._start_move("left"))
        root.bind("<KeyRelease-Left>", lambda e: self._stop_move("left"))
        root.bind("<KeyPress-Right>", lambda e: self._start_move("right"))
        root.bind("<KeyRelease-Right>", lambda e: self._stop_move("right"))

        # フォーカスを確保
        self.canvas.focus_set()
        # アニメーションループ開始
        self._update()

    def _create_car(self, cx, cy):
        # 車体は長方形、屋根は台形、タイヤは丸
        left = cx - CAR_WIDTH // 2
        right = cx + CAR_WIDTH // 2
        top = cy - CAR_HEIGHT
        body = self.canvas.create_rectangle(left, top, right, cy, fill="#ff4444", outline="#880000")
        # 屋根（台形）
        roof = self.canvas.create_polygon(
            left + 20, top,
            left + 50, top - 20,
            right - 50, top - 20,
            right - 20, top,
            fill="#ff8888", outline="#880000"
        )
        # タイヤ
        wheel1 = self.canvas.create_oval(left + 15 - WHEEL_RADIUS, cy - WHEEL_RADIUS,
                                         left + 15 + WHEEL_RADIUS, cy + WHEEL_RADIUS,
                                         fill="#222", outline="#000")
        wheel2 = self.canvas.create_oval(right - 15 - WHEEL_RADIUS, cy - WHEEL_RADIUS,
                                         right - 15 + WHEEL_RADIUS, cy + WHEEL_RADIUS,
                                         fill="#222", outline="#000")
        # 車のパーツをまとめるタグ
        items = [body, roof, wheel1, wheel2]
        for it in items:
            self.canvas.addtag_withtag("car", it)
        return items

    def _start_move(self, direction):
        if direction == "left":
            self.moving_left = True
        elif direction == "right":
            self.moving_right = True

    def _stop_move(self, direction):
        if direction == "left":
            self.moving_left = False
        elif direction == "right":
            self.moving_right = False

    def _update(self):
        dx = 0
        if self.moving_left and not self.moving_right:
            dx = -SPEED
        elif self.moving_right and not self.moving_left:
            dx = SPEED

        if dx != 0:
            # 現在の車の境界を取得してキャンバス内に収める
            coords = self.canvas.bbox("car")  # (x1, y1, x2, y2)
            if coords:
                x1, y1, x2, y2 = coords
                # 左端チェック
                if x1 + dx < 0:
                    dx = -x1
                # 右端チェック
                if x2 + dx > WIDTH:
                    dx = WIDTH - x2
            if dx != 0:
                self.canvas.move("car", dx, 0)

        # 30msごとに更新（約33fps）
        self.root.after(30, self._update)

if __name__ == "__main__":
    root = tk.Tk()
    app = MotorcarApp(root)
    root.mainloop()