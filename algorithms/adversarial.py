import math
import random
from .core import Game

class TicTacToeGame(Game):
    def actions(self, state):
        board = state
        return [i for i, v in enumerate(board) if v == 0]

    def result(self, state, action, player):
        new_board = list(state)
        new_board[action] = player
        return tuple(new_board)

    def is_terminal(self, state):
        return self.utility(state) is not None

    def utility(self, state):
        board = state
        win_lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], # cols
            [0, 4, 8], [2, 4, 6]             # diagonals
        ]
        for line in win_lines:
            s = board[line[0]] + board[line[1]] + board[line[2]]
            if s == 3: return 1
            if s == -3: return -1
        if 0 not in board:
            return 0 # Draw
        return None # Not finished


def Min_Value(game, state):
    if game.is_terminal(state): return game.utility(state)
    v = math.inf
    for action in game.actions(state):
        v = min(v, Max_Value(game, game.result(state, action, -1)))
    return v

def Max_Value(game, state):
    if game.is_terminal(state): return game.utility(state)
    v = -math.inf
    for action in game.actions(state):
        v = max(v, Min_Value(game, game.result(state, action, 1)))
    return v

def Minimax_Search(game, state, is_max):
    prefix = "[Lượt X]" if is_max else "[Lượt O]"
    actions = game.actions(state)
    if not actions or game.is_terminal(state):
        yield {"status": f"{prefix} Kết thúc", "scores": {}, "best_action": None, "done": True}
        return
        
    scores = {}
    player = 1 if is_max else -1
    
    for a in actions:
        next_state = game.result(state, a, player)
        if is_max:
            score = Min_Value(game, next_state)
        else:
            score = Max_Value(game, next_state)
        scores[a] = score
        yield {"status": f"{prefix} Đang tính Minimax ô {a}...", "scores": scores.copy(), "best_action": None, "done": False}
        
    best_score = max(scores.values()) if is_max else min(scores.values())
    best_actions = [a for a, s in scores.items() if s == best_score]
    best_action = random.choice(best_actions)
    yield {"status": f"{prefix} Chọn ô {best_action} (Điểm: {best_score})", "scores": scores.copy(), "best_action": best_action, "done": True}


def AB_Min_Value(game, state, alpha, beta):
    if game.is_terminal(state): return game.utility(state)
    v = math.inf
    for action in game.actions(state):
        v = min(v, AB_Max_Value(game, game.result(state, action, -1), alpha, beta))
        if v <= alpha: return v
        beta = min(beta, v)
    return v

def AB_Max_Value(game, state, alpha, beta):
    if game.is_terminal(state): return game.utility(state)
    v = -math.inf
    for action in game.actions(state):
        v = max(v, AB_Min_Value(game, game.result(state, action, 1), alpha, beta))
        if v >= beta: return v
        alpha = max(alpha, v)
    return v

def Alpha_Beta_Search(game, state, is_max):
    prefix = "[Lượt X]" if is_max else "[Lượt O]"
    actions = game.actions(state)
    if not actions or game.is_terminal(state):
        yield {"status": f"{prefix} Kết thúc", "scores": {}, "best_action": None, "done": True}
        return
        
    scores = {}
    player = 1 if is_max else -1
    alpha = -math.inf
    beta = math.inf
    
    for a in actions:
        next_state = game.result(state, a, player)
        if is_max:
            score = AB_Min_Value(game, next_state, alpha, beta)
            scores[a] = score
            alpha = max(alpha, score)
        else:
            score = AB_Max_Value(game, next_state, alpha, beta)
            scores[a] = score
            beta = min(beta, score)
            
        yield {"status": f"{prefix} Đang tính Alpha-Beta ô {a}...", "scores": scores.copy(), "best_action": None, "done": False}
        
    best_score = max(scores.values()) if is_max else min(scores.values())
    best_actions = [a for a, s in scores.items() if s == best_score]
    best_action = random.choice(best_actions)
    yield {"status": f"{prefix} Chọn ô {best_action} (Điểm: {best_score})", "scores": scores.copy(), "best_action": best_action, "done": True}

def Exp_Utility_For_X(game, state):
    w = game.utility(state)
    if w is not None: return w
    actions = game.actions(state)
    v = 0
    prob = 1.0 / len(actions)
    for a in actions:
        v += prob * Exp_Max_Value(game, game.result(state, a, -1))
    return v

def Exp_Max_Value(game, state):
    w = game.utility(state)
    if w is not None: return w
    v = -math.inf
    for a in game.actions(state):
        v = max(v, Exp_Utility_For_X(game, game.result(state, a, 1)))
    return v

def Exp_Utility_For_O(game, state):
    w = game.utility(state)
    if w is not None: return w
    actions = game.actions(state)
    v = 0
    prob = 1.0 / len(actions)
    for a in actions:
        v += prob * Exp_Min_Value(game, game.result(state, a, 1))
    return v

def Exp_Min_Value(game, state):
    w = game.utility(state)
    if w is not None: return w
    v = math.inf
    for a in game.actions(state):
        v = min(v, Exp_Utility_For_O(game, game.result(state, a, -1)))
    return v

def Expectimax_Search(game, state, is_max):
    prefix = "[Lượt X]" if is_max else "[Lượt O]"
    actions = game.actions(state)
    if not actions or game.is_terminal(state):
        yield {"status": f"{prefix} Kết thúc", "scores": {}, "best_action": None, "done": True}
        return
        
    scores = {}
    player = 1 if is_max else -1
    
    for a in actions:
        next_state = game.result(state, a, player)
        if is_max:
            score = Exp_Utility_For_X(game, next_state)
        else:
            score = Exp_Utility_For_O(game, next_state)
            
        scores[a] = round(score, 2)
        yield {"status": f"{prefix} Đang tính Expectimax ô {a}...", "scores": scores.copy(), "best_action": None, "done": False}
        
    best_score = max(scores.values()) if is_max else min(scores.values())
    best_actions = [a for a, s in scores.items() if s == best_score]
    best_action = random.choice(best_actions)
    yield {"status": f"{prefix} Chọn ô {best_action} (Kỳ vọng: {best_score})", "scores": scores.copy(), "best_action": best_action, "done": True}



def minimax_gen(board, is_max):
    game = TicTacToeGame()
    state = tuple(board)
    for step_data in Minimax_Search(game, state, is_max):
        yield step_data

def alphabeta_gen(board, is_max):
    game = TicTacToeGame()
    state = tuple(board)
    for step_data in Alpha_Beta_Search(game, state, is_max):
        yield step_data

def expectimax_gen(board, is_max):
    game = TicTacToeGame()
    state = tuple(board)
    for step_data in Expectimax_Search(game, state, is_max):
        yield step_data

def check_winner(board):
    game = TicTacToeGame()
    return game.utility(tuple(board))
