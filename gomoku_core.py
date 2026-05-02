"""五子棋规则与状态（无 GUI 依赖，供 gomoku.py / gomoku_cli.py 共用）。"""

from __future__ import annotations

BOARD_SIZE = 15
WIN_LEN = 5


class GomokuState:
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.grid: list[list[int]] = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.current = 1  # 1 黑 2 白
        self.game_over = False

    def _count_line(self, r: int, c: int, dr: int, dc: int) -> int:
        color = self.grid[r][c]
        n = 1
        rr, cc = r + dr, c + dc
        while 0 <= rr < BOARD_SIZE and 0 <= cc < BOARD_SIZE and self.grid[rr][cc] == color:
            n += 1
            rr += dr
            cc += dc
        rr, cc = r - dr, c - dc
        while 0 <= rr < BOARD_SIZE and 0 <= cc < BOARD_SIZE and self.grid[rr][cc] == color:
            n += 1
            rr -= dr
            cc -= dc
        return n

    def _check_win(self, r: int, c: int) -> bool:
        for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
            if self._count_line(r, c, dr, dc) >= WIN_LEN:
                return True
        return False

    def _board_full(self) -> bool:
        return all(self.grid[r][c] != 0 for r in range(BOARD_SIZE) for c in range(BOARD_SIZE))

    def place(self, r: int, c: int) -> tuple[bool, str | None]:
        """
        在 (r,c) 落子。返回 (是否落子成功, 终局提示或 None 表示继续)。
        失败时第二项为原因说明。
        """
        if self.game_over:
            return False, "本局已结束"
        if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE):
            return False, "坐标越界"
        if self.grid[r][c] != 0:
            return False, "该处已有棋子"

        self.grid[r][c] = self.current
        if self._check_win(r, c):
            self.game_over = True
            name = "黑方" if self.current == 1 else "白方"
            return True, f"{name} 获胜！"
        if self._board_full():
            self.game_over = True
            return True, "和棋（棋盘已满）"

        self.current = 2 if self.current == 1 else 1
        return True, None
