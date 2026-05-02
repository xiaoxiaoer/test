"""
五子棋（双人对局，图形界面）：15×15，黑先，五连胜。
运行: python3 gomoku.py

macOS Tahoe / 26 若启动即崩溃并出现:
    macOS 26 (...) or later required, have instead 16 (...) !
原因是当前 Python 自带的 Tcl/Tk 与系统「版本兼容」报告不一致（旧 SDK 二进制会看到 16）。
可任选其一:
  1) 在**同一终端、启动 Python 之前**执行:
       export SYSTEM_VERSION_COMPAT=0
       python3 gomoku.py
  2) 使用 Homebrew / python.org 上较新的 Python 3.12+（随 Xcode 新 SDK 构建的 Tk）。
  3) 不依赖图形界面时运行终端版:
       python3 gomoku_cli.py

若出现 ModuleNotFoundError: No module named '_tkinter'（常见于 Homebrew 的 python@3.x）:
  与主程序同主版本安装 Tk 扩展即可，例如 Python 3.11:
       brew install python-tk@3.11
  装好后仍用该版本的解释器运行，例如:
       python3.11 gomoku.py
  （_tkinter 是随 Python 编译的扩展，pip 无法安装；SYSTEM_VERSION_COMPAT 与此无关。）
"""

from __future__ import annotations

import sys
import tkinter as tk
from tkinter import messagebox

from gomoku_core import BOARD_SIZE, GomokuState

# 状态栏字体：尽量用系统常见无衬线字体以显示中文
if sys.platform == "win32":
    _UI_FONT = ("Microsoft YaHei UI", 14)
elif sys.platform == "darwin":
    _UI_FONT = ("PingFang SC", 14)
else:
    _UI_FONT = ("Noto Sans CJK SC", 14)

CELL = 36
MARGIN = 28


class GomokuApp:
    def __init__(self) -> None:
        self.state = GomokuState()
        self.root = tk.Tk()
        self.root.title("五子棋")
        self.canvas_size = MARGIN * 2 + (BOARD_SIZE - 1) * CELL
        self.canvas = tk.Canvas(
            self.root,
            width=self.canvas_size,
            height=self.canvas_size,
            bg="#dcb35c",
            highlightthickness=0,
        )
        self.canvas.pack(padx=8, pady=(8, 4))

        bar = tk.Frame(self.root)
        bar.pack(fill=tk.X, padx=8, pady=(0, 8))
        self.status = tk.Label(bar, text="黑方落子", font=_UI_FONT)
        self.status.pack(side=tk.LEFT)
        tk.Button(bar, text="新局", command=self.new_game).pack(side=tk.RIGHT)

        self.canvas.bind("<Button-1>", self.on_click)

        self.draw_board()

    def draw_board(self) -> None:
        self.canvas.delete("all")
        for i in range(BOARD_SIZE):
            x0 = MARGIN + i * CELL
            self.canvas.create_line(x0, MARGIN, x0, MARGIN + (BOARD_SIZE - 1) * CELL, fill="#333", width=1)
            y0 = MARGIN + i * CELL
            self.canvas.create_line(MARGIN, y0, MARGIN + (BOARD_SIZE - 1) * CELL, y0, fill="#333", width=1)
        stars = [3, 7, 11]
        for r in stars:
            for c in stars:
                cx, cy = MARGIN + c * CELL, MARGIN + r * CELL
                self.canvas.create_oval(cx - 3, cy - 3, cx + 3, cy + 3, fill="#333", outline="")

        self.redraw_pieces()

    def redraw_pieces(self) -> None:
        self.canvas.delete("piece")
        r_piece = CELL // 2 - 2
        g = self.state.grid
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                v = g[r][c]
                if v == 0:
                    continue
                cx, cy = MARGIN + c * CELL, MARGIN + r * CELL
                fill = "#111" if v == 1 else "#f5f5f5"
                outline = "#000" if v == 1 else "#888"
                self.canvas.create_oval(
                    cx - r_piece,
                    cy - r_piece,
                    cx + r_piece,
                    cy + r_piece,
                    fill=fill,
                    outline=outline,
                    width=2,
                    tags="piece",
                )

    def pixel_to_cell(self, x: float, y: float) -> tuple[int, int] | None:
        c = round((x - MARGIN) / CELL)
        r = round((y - MARGIN) / CELL)
        if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
            cx, cy = MARGIN + c * CELL, MARGIN + r * CELL
            if abs(x - cx) <= CELL // 2 + 2 and abs(y - cy) <= CELL // 2 + 2:
                return r, c
        return None

    def on_click(self, event: tk.Event) -> None:
        pos = self.pixel_to_cell(event.x, event.y)
        if pos is None:
            return
        r, c = pos
        ok, end_msg = self.state.place(r, c)
        if not ok:
            return
        self.redraw_pieces()
        if end_msg:
            self.status.config(text=end_msg)
            messagebox.showinfo("五子棋", end_msg)
            return
        self.status.config(text="黑方落子" if self.state.current == 1 else "白方落子")

    def new_game(self) -> None:
        self.state.reset()
        self.status.config(text="黑方落子")
        self.draw_board()

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    GomokuApp().run()


if __name__ == "__main__":
    main()
