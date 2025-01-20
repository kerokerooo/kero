import numpy as np
import random
from kogi_canvas import play_othello

BLACK = 1
WHITE = 2
EMPTY = 0

# 四隅の座標を定義
CORNERS = [(0, 0), (0, 5), (5, 0), (5, 5)]

# 評価関数
def evaluate(board, stone):
    score = 0
    opponent = 3 - stone
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == stone:
                score += 1
            elif board[y][x] == opponent:
                score -= 1
    # 角の価値を高くする
    for corner in CORNERS:
        x, y = corner
        if board[y][x] == stone:
            score += 5
        elif board[y][x] == opponent:
            score -= 5
    return score

# ミニマックスアルゴリズムの実装
def minimax(board, stone, depth, alpha, beta, maximizing_player):
    if depth == 0 or is_game_over(board):
        return evaluate(board, stone)
    
    valid_moves_list = valid_moves(board, stone)
    if maximizing_player:
        max_eval = float('-inf')
        for move in valid_moves_list:
            x, y = move
            new_board = np.copy(board) # board.copy() から np.copy(board) に変更
            place_move(new_board, x, y, stone)
            eval = minimax(new_board, stone, depth-1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        opponent = 3 - stone
        for move in valid_moves_list:
            x, y = move
            new_board = np.copy(board) # board.copy() から np.copy(board) に変更
            place_move(new_board, x, y, opponent)
            eval = minimax(new_board, stone, depth-1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# AIの動き選択
class KerokeroAI(object): # クラスの定義
    def face(self):
        return "★"  # 強いAIを示すアイコン

    def place(self, board, stone):
        best_move = None
        best_value = float('-inf')
        for move in valid_moves(board, stone):
            x, y = move
            new_board = np.copy(board) # board.copy() から np.copy(board) に変更
            place_move(new_board, x, y, stone)
            board_value = minimax(new_board, stone, 3, float('-inf'), float('inf'), False)  # 深さ3で探索
            if board_value > best_value:
                best_value = board_value
                best_move = (x, y)
        return best_move if best_move else (-1, -1)

# サポート関数
def can_place_x_y(board, stone, x, y):
    if board[y][x] != 0:
        return False
    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        found_opponent = False
        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            found_opponent = True
        if found_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            return True
    return False

def valid_moves(board, stone):
    moves = []
    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, stone, x, y):
                moves.append((x, y))
    return moves

def place_move(board, x, y, stone):
    board[y][x] = stone
    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        stones_to_flip = []
        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            stones_to_flip.append((nx, ny))
            nx += dx
            ny += dy
        if 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            for flip_x, flip_y in stones_to_flip:
                board[flip_y][flip_x] = stone

def is_game_over(board):
    return not valid_moves(board, BLACK) and not valid_moves(board, WHITE)
