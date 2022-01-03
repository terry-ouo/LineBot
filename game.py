import random


def finger_guess_game_player(event):
    hand = ["paper", "剪刀", "石頭"]
    player = hand[event-1]
    return player


def finger_guess_game_pc():
    choice = random.randrange(3)
    hand = ["paper", "剪刀", "石頭"]
    pc = hand[choice]
    return pc


def finger_guess_game_judge(player, pc):
    player = player.lower()
    pc = pc.lower()
    if pc == player:
        return "tie"
    if pc == "paper" and player == "剪刀":
        return "player win!"
    elif pc == "paper" and player == "石頭":
        return "pc win!"
    if pc == "剪刀" and player == "paper":
        return "pc win!"
    elif pc == "剪刀" and player == "石頭":
        return "player win!"
    if pc == "石頭" and player == "paper":
        return "player win!"
    elif pc == "石頭" and player == "剪刀":
        return "pc win!"


print(finger_guess_game_judge(finger_guess_game_player(int(input("input:"))), finger_guess_game_pc()))
