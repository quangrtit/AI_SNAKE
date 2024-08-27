import numpy 
import random
import json

class agent: 
    def __init__(self, BLOCK_SIZE, DIS_WIDTH, DIS_HEIGHT, learningRate, epsilon, epsilon_max, epsilon_min, gamma):
        self.BLOCK_SIZE = BLOCK_SIZE 
        self.DIS_WIDTH = DIS_WIDTH
        self.DIS_HEIGHT = DIS_HEIGHT
        self.learningRate = learningRate
        self.epsilon = epsilon
        self.epsilon_max = epsilon_max 
        self.epsilon_min = epsilon_min
        self.gamma = gamma
        self.qtable = self.loadQtable()
        self.history = []
        self.action_covert = {
            0: "right",
            1: "left",
            2: "down",
            3: "up"
        }
        # print(self.qtable) 
    def saveQvalues(self):
        with open("qtable.json", "w") as file: 
            json.dump(self.qtable, file)
    def loadQtable(self):
        qtable = None
        with open("qtable.json", "r") as file: 
            qtable = json.load(file)
        return qtable
    def chooseAction(self, snake, food):
        food_head, state_now = self.getState(snake, food)
        action_now = None
        if random.uniform(0, 1) < self.epsilon: 
            action_now = random.randint(0, 3)
        else: 
            action_now = numpy.argmax(self.qtable[str(state_now)])
        self.history.append({
            "state": str(state_now),
            "action": action_now, 
            "food_head": food_head
        })
        # self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_max)
        return action_now, self.action_covert[action_now]
    def getState(self, snake, food):
        head_snake = snake[-1]
        x_food = food[0]
        y_food = food[1]
        x_head = head_snake[0]
        y_head = head_snake[1]
        # check location state food with head snake 
        x_pos = None
        y_pos = None 
        if x_food > x_head: # food in right  
            x_pos = "0"
        elif x_food < x_head: # food in left 
            x_pos = "1"
        else: 
            x_pos = "WA" # food in head
        if y_food > y_head: # food in down 
            y_pos = "2"
        elif y_food < y_head: # food in up 
            y_pos = "3"
        else: 
            y_pos = "WA" # food in head
        
        # check die for snake base on head_snake
        location_around_head = [(x_head + self.BLOCK_SIZE, y_head), # locatin next to right
                                (x_head - self.BLOCK_SIZE, y_head), # location next to left
                                (x_head, y_head + self.BLOCK_SIZE), # location next to down
                                (x_head, y_head - self.BLOCK_SIZE)] # location next to up
        state_die = []
        for s in location_around_head:
            if s[0] < 0 or s[1] < 0: 
                state_die.append("1")
            elif s[0] > self.DIS_WIDTH or s[1] > self.DIS_HEIGHT:
                state_die.append("1")
            elif s in snake[:-1]: 
                state_die.append("1")
            else: 
                state_die.append("0")
        state_die_str = ''.join(state_die)
        return (x_head, y_head, x_food, y_food), (x_pos, y_pos, state_die_str) # ?????????
    def train(self, reason):
        h = self.history[::-1]
        for i in range(len(h[:-1])):
            if reason: 
                print("nononno: ", reason)
                sta = h[0]["state"]
                act = h[0]["action"]
                reward = -1
                self.qtable[sta][act] = self.qtable[sta][act] + self.learningRate * (reward - self.qtable[sta][act])  
                reason = None
            if not reason: 
                state_now = h[i + 1]["state"] # update this state 
                next_state = h[i]["state"]  # using update for state front
                action = h[i + 1]["action"]
                m1 = h[i + 1]["food_head"][0]
                m2 = h[i + 1]["food_head"][1]
                m11 = h[i + 1]["food_head"][2]
                m22 = h[i + 1]["food_head"][3]
                m3 = h[i]["food_head"][0]
                m4 = h[i]["food_head"][1] 
                m5 = h[i]["food_head"][2]
                m6 = h[i]["food_head"][3]
                # set reward
                if ((m11 != m5) and (m22 != m6)): # eat food
                    reward = 1
                elif ((abs(m1 - m11) > abs(m3 - m5)) or (abs(m2 - m22) > abs(m4 - m6))):#snake near food more get positive reward
                    reward = 1
                else: 
                    reward = -1
                # update qtable 
                self.qtable[state_now][action] = self.qtable[state_now][action] + self.learningRate * (reward + self.gamma * numpy.max(self.qtable[next_state]) - self.qtable[state_now][action])






    