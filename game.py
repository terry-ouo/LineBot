import random


def finger_guess_game_player(event):
    hand = ["paper", "scissor", "stone"]
    player = hand[event-1]
    return player


def finger_guess_game_pc():
    choice = random.randrange(3)
    hand = ["paper", "scissor", "stone"]
    pc = hand[choice]
    return pc


def finger_guess_game_judge(player, pc):
    player = player.lower()
    pc = pc.lower()
    if pc == player:
        return "tie"
    if pc == "paper" and player == "scissor":
        return "player win!"
    elif pc == "paper" and player == "stone":
        return "pc win!"
    if pc == "scissor" and player == "paper":
        return "pc win!"
    elif pc == "scissor" and player == "stone":
        return "player win!"
    if pc == "stone" and player == "paper":
        return "player win!"
    elif pc == "stone" and player == "scissor":
        return "pc win!"


print(finger_guess_game_judge(finger_guess_game_player(int(input("input:"))), finger_guess_game_pc()))
