# RPS.py

import random

transition_table = {a + b: {"R": 0, "P": 0, "S": 0} for a in "RPS" for b in "RPS"}
sequence_memory = {}

def predict_markov(opponent_history):
    if len(opponent_history) < 2:
        return random.choice(["R", "P", "S"])
    last_two = "".join(opponent_history[-2:])
    next_moves = transition_table.get(last_two, {})
    return max(next_moves, key=next_moves.get, default=random.choice(["R", "P", "S"]))

def predict_sequence(opponent_history):
    if len(opponent_history) < 4:
        return None
    seq = "".join(opponent_history[-3:])
    if seq in sequence_memory:
        weighted = sequence_memory[seq]
        return max(weighted, key=weighted.get)
    return None

def detect_rotation(opponent_history):
    for size in range(2, 6):  # Check cycles of 2 to 5
        if len(opponent_history) >= size * 2:
            recent = opponent_history[-size*2:]
            if recent[:size] == recent[size:]:
                return recent[len(opponent_history) % size]
    return None

def player(prev_play, opponent_history=[]):
    if prev_play:
        opponent_history.append(prev_play)

    # Update Markov table
    if len(opponent_history) >= 3:
        key = "".join(opponent_history[-3:-1])
        next_move = opponent_history[-1]
        if key in transition_table:
            transition_table[key][next_move] += 1

    # Update sequence memory with weighted decay
    if len(opponent_history) >= 4:
        seq = "".join(opponent_history[-4:-1])
        next_move = opponent_history[-1]
        if seq not in sequence_memory:
            sequence_memory[seq] = {"R": 0, "P": 0, "S": 0}
        sequence_memory[seq][next_move] += 3  # Weight recent moves more

    # Try rotation detection
    rotation_guess = detect_rotation(opponent_history)
    if rotation_guess:
        return {"R": "P", "P": "S", "S": "R"}[rotation_guess]

    # Try sequence prediction
    seq_guess = predict_sequence(opponent_history)
    if seq_guess:
        return {"R": "P", "P": "S", "S": "R"}[seq_guess]

    # Fallback to Markov prediction
    predicted = predict_markov(opponent_history)
    return {"R": "P", "P": "S", "S": "R"}[predicted]
