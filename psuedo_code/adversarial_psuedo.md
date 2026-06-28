### Minimax
def Minimax_Decision(state):
    return argmax(actions, key=lambda a: Min_Value(Result(state, a)))

def Max_Value(state):
    if Terminal_Test(state): return Utility(state)
    v = -infinity
    for action in Actions(state):
        v = max(v, Min_Value(Result(state, action)))
    return v

def Min_Value(state):
    if Terminal_Test(state): return Utility(state)
    v = infinity
    for action in Actions(state):
        v = min(v, Max_Value(Result(state, action)))
    return v
---
### Alpha-Beta Prunning
def Alpha_Beta_Search(state):
    v = Max_Value(state, -infinity, +infinity)
    return action_leading_to_v

def Max_Value(state, alpha, beta):
    if Terminal_Test(state): return Utility(state)
    v = -infinity
    for action in Actions(state):
        v = max(v, Min_Value(Result(state, action), alpha, beta))
        if v >= beta: return v
        alpha = max(alpha, v)
    return v

def Min_Value(state, alpha, beta):
    if Terminal_Test(state): return Utility(state)
    v = +infinity
    for action in Actions(state):
        v = min(v, Max_Value(Result(state, action), alpha, beta))
        if v <= alpha: return v
        beta = min(beta, v)
    return v
---
### Expectimax
def Expectimax_Decision(state):
    return argmax(actions, key=lambda a: Expect_Value(Result(state, a)))

def Expect_Value(state):
    if Terminal_Test(state): return Utility(state)
    v = 0
    actions = Actions(state)
    probability = 1.0 / len(actions) # Phân phối xác suất đều của đối thủ ngẫu nhiên
    for action in actions:
        v += probability * Max_Value(Result(state, action))
    return v