"""
五子棋终端版：无 tkinter，避免 macOS 上 Tcl/Tk 与系统版本报告冲突导致的崩溃。
用法: python3 gomoku_cli.py
落子: 输入两行 0–14 的整数 行 列，例如先输入 7 再输入 7 表示天元附近；输入 q 退出。
"""

from __future__ import annotations

from gomoku_core import BOARD_SIZE, GomokuState


def cell_char(v: int) -> str:
    if v == 1:
        return "●"
    if v == 2:
        return "○"
    return "·"


def print_board(state: GomokuState) -> None:
    header = "    " + "".join(f"{i % 10:2d}" for i in range(BOARD_SIZE))
    print(header)
    for r in range(BOARD_SIZE):
        row = f"{r:3d} " + " ".join(cell_char(state.grid[r][c]) for c in range(BOARD_SIZE))
        print(row)
    print()


def read_int(prompt: str) -> int | None:
    while True:
        s = input(prompt).strip()
        if s.lower() == "q":
            return None
        try:
            return int(s)
        except ValueError:
            print("请输入整数或 q。")


def main() -> None:
    state = GomokuState()
    print("五子棋（终端）15×15，黑先。输入行、列（0–14），q 退出。\n")
    while True:
        print_board(state)
        if state.game_over:
            again = input("再开一局? [y/N]: ").strip().lower()
            if again == "y":
                state.reset()
                continue
            break

        who = "黑方(●)" if state.current == 1 else "白方(○)"
        print(f"{who} 落子")
        r = read_int("  行 (0-14): ")
        if r is None:
            print("再见。")
            break
        c = read_int("  列 (0-14): ")
        if c is None:
            print("再见。")
            break

        ok, msg = state.place(r, c)
        if not ok:
            print(msg or "无法落子")
            continue
        if msg:
            print(msg)


if __name__ == "__main__":
    main()
