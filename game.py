# 猜拳遊戲
from random import random
import config


def finger_guess_game_player(event):
    hand = ["paper", "剪刀", "石頭"]
    player = hand[event - 1]
    return player


def finger_guess_game_pc():
    choice = random.randrange(3)
    hand = ["布", "剪刀", "石頭"]
    pc = hand[choice]
    return pc


def finger_guess_game_judge(even):
    player = finger_guess_game_player(even)
    pc = finger_guess_game_pc()
    if pc == player:
        return pc + "\n\ntie!ಠ_ರೃ"
    if pc == "布" and player == "剪刀":
        return pc + "\n\nplayer win!(｡◝‿◜｡)"
    elif pc == "布" and player == "石頭":
        return pc + "\n\npc win!(;´Д`)×"
    if pc == "剪刀" and player == "布":
        return pc + "\n\npc win!⁽͑˙˚̀⚐˚́˙⁾̉"
    elif pc == "剪刀" and player == "石頭":
        return pc + "\n\nplayer win!(´︶｀)"
    if pc == "石頭" and player == "paper":
        return pc + "\n\nplayer win!(≧◡≦)"
    elif pc == "石頭" and player == "剪刀":
        return pc + "\n\npc win!(╯︵╰,)"


# 圈圈叉叉
def circle_game_return():
    table = config.table
    result = ""
    for row in table:
        for line in row:
            result += line
        result += "\n"
    return result


def circle_game_write(player, position):
    if player == "player":
        if position == "1":
            config.table[0][0] = "O"
        elif position == "2":
            config.table[0][2] = "O"
        elif position == "3":
            config.table[0][4] = "O"
        elif position == "4":
            config.table[2][0] = "O"
        elif position == "5":
            config.table[2][2] = "O"
        elif position == "6":
            config.table[2][4] = "O"
        elif position == "7":
            config.table[4][0] = "O"
        elif position == "8":
            config.table[4][2] = "O"
        elif position == "9":
            config.table[4][4] = "O"
    if player == "pc":
        if position == "1":
            config.table[0][0] = "X"
        elif position == "2":
            config.table[0][2] = "X"
        elif position == "3":
            config.table[0][4] = "X"
        elif position == "4":
            config.table[2][0] = "X"
        elif position == "5":
            config.table[2][2] = "X"
        elif position == "6":
            config.table[2][4] = "X"
        elif position == "7":
            config.table[4][0] = "X"
        elif position == "8":
            config.table[4][2] = "X"
        elif position == "9":
            config.table[4][4] = "X"
    return circle_game_return()


def circle_game_judge():
    result = ""
    if config.table[0, 0] == config.table[0, 2] == config.table[0, 4]:
        if config.table[0, 0] == "O":
            result = "player win!"
        else:
            result = "pc win!"
    elif config.table[2, 0] == config.table[2, 2] == config.table[2, 4]:
        if config.table[2, 0] == "O":
            result = "player win!"
        else:
            result = "pc win!"
    elif config.table[4, 0] == config.table[4, 2] == config.table[4, 4]:
        if config.table[5, 0] == "O":
            result = "player win!"
        else:
            result = "pc win!"
    elif config.table[0, 0] == config.table[2, 0] == config.table[4, 0]:
        if config.table[0, 0] == "O":
            result = "player win!"
        else:
            result = "pc win!"
    elif config.table[0, 2] == config.table[2, 2] == config.table[4, 2]:
        if config.table[0, 2] == "O":
            result = "player win!"
        else:
            result = "pc win!"
    elif config.table[0, 4] == config.table[2, 4] == config.table[4, 4]:
        if config.table[0, 4] == "O":
            result = "player win!"
        else:
            result = "pc win!"
    elif config.table[0, 0] == config.table[2, 2] == config.table[4, 4]:
        if config.table[0, 0] == "O":
            result = "player win!"
        else:
            result = "pc win!"
    elif config.table[0, 4] == config.table[2, 2] == config.table[4, 0]:
        if config.table[0, 4] == "O":
            result = "player win!"
        else:
            result = "pc win!"
    reply = ""
    if result != "":
        reply = result
        result = ""
        config.table = [
            [" ", "|", " ", "|", " "],
            ["-", "-", "-", "-", "-"],
            [" ", "|", " ", "|", " "],
            ["-", "-", "-", "-", "-"],
            [" ", "|", " ", "|", " "]
        ]
        return reply


def reset():
    config.table = [
        [" ", "|", " ", "|", " "],
        ["-", "-", "-", "-", "-"],
        [" ", "|", " ", "|", " "],
        ["-", "-", "-", "-", "-"],
        [" ", "|", " ", "|", " "]
    ]


