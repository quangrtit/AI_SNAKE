import src.Snake as game
import pygame
import json

def Try(j, qtable, qtables):
    for i in range(0, 2):
        qtable[j] = str(i)
        if j == 3: 
            # print(qtable)
            qtable_copy = qtable[:]
            qtables.append(''.join(qtable_copy))
        else: 
            Try(j + 1, qtable, qtables)
def initQtable():
    qtable = [str(0) for x in range(4)]
    qtables = []
    Try(0, qtable, qtables)
    w = ['0', '1', 'WA'] # right, left, in
    h = ['2', '3', 'WA'] # down, up, in
    states = {}
    for i in w: 
        for j in h: 
            for e in qtables:
                states[str((i, j, e))] = [0, 0, 0, 0]
    with open("qtable.json", "w") as file: 
        json.dump(states, file)
if __name__ == "__main__":
    initQtable()
    game = game.snake()
    cnt = 1
    while True:   
        game.reset()
        score, reason = game.gameLoop()
        print("episol:", cnt, "score:", score, "die because:", reason)
        cnt += 1
        if cnt % 200 == 0: 
            game.ai.epsilon = 0.0
            game.ai.saveQvalues()
        