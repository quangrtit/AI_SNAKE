import yaml
import pygame 
import random
import numpy
import src.Agent

class snake: 
    def __init__(self):
        self.YELLOW = (255, 255, 102)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (50, 153, 213)
        self.dead = False
        self.reason = None
        self.size_snake = 1
        pygame.init()
        with open("config.yml", "r") as file:
            self.config = yaml.load(file, Loader=yaml.FullLoader)
        self.ai = src.Agent.agent(self.config["BLOCK_SIZE"], self.config["DIS_WIDTH"], self.config["DIS_HEIGHT"], self.config["learningRate"],
                                  self.config["epsilon"], self.config["epsilon_max"], self.config["epsilon_min"], self.config["gamma"])
        self.clock = pygame.time.Clock() 
        self.display = pygame.display.set_mode((self.config["DIS_WIDTH"], self.config["DIS_HEIGHT"]))
        pygame.display.set_caption("ANH QUẢNG")
        x = 4 * self.config["BLOCK_SIZE"]
        y = 4 * self.config["BLOCK_SIZE"]
        self.snake_body = [(x, y)]
        self.x_food = random.randint(0, self.config["DIS_WIDTH"] - self.config["BLOCK_SIZE"]) // self.config["BLOCK_SIZE"] * self.config["BLOCK_SIZE"]
        self.y_food = random.randint(0, self.config["DIS_HEIGHT"] - self.config["BLOCK_SIZE"]) // self.config["BLOCK_SIZE"] * self.config["BLOCK_SIZE"]
    def gameLoop(self):
        while not self.dead:
            action_val, action = self.ai.chooseAction(self.snake_body, (self.x_food, self.y_food))
            x, y = self.snake_body[-1][0], self.snake_body[-1][1]
            if action == "right": 
                x += self.config["BLOCK_SIZE"]
            elif action == "left":
                x -= self.config["BLOCK_SIZE"]
            elif action == "down":
                y += self.config["BLOCK_SIZE"]
            elif action == "up":
                y -= self.config["BLOCK_SIZE"]
            
            self.snake_body.append((x, y))
            if (x, y) in self.snake_body[:-1]:
                self.dead = True 
                self.reason = "TAIL"
            if x < 0 or y < 0 or x >= self.config["DIS_WIDTH"] or y >= self.config["DIS_HEIGHT"]:
                self.dead = True 
                self.reason = "WALL"
            if (x, y) != (self.x_food, self.y_food): 
                self.snake_body.pop(0)
            else: 
                self.size_snake += 1
                self.x_food = random.randint(0, self.config["DIS_WIDTH"] - self.config["BLOCK_SIZE"]) // self.config["BLOCK_SIZE"] * self.config["BLOCK_SIZE"]
                self.y_food = random.randint(0, self.config["DIS_HEIGHT"] - self.config["BLOCK_SIZE"]) // self.config["BLOCK_SIZE"] * self.config["BLOCK_SIZE"]
            

            self.display.fill(self.BLUE)
            self.drawSnake()
            self.drawFood()
            self.drawScore()
            pygame.display.update()

            #update q value
            self.ai.train(self.reason)


            self.clock.tick(self.config["FRAMESPEED"])
        return self.size_snake - 1, self.reason
    def reset(self):
        self.clock = pygame.time.Clock() 
        self.display = pygame.display.set_mode((self.config["DIS_WIDTH"], self.config["DIS_HEIGHT"]))
        pygame.display.set_caption("ANH QUẢNG")
        self.ai.history = []
        self.dead = False
        self.reason = None
        self.size_snake = 1
        x = 4 * self.config["BLOCK_SIZE"]
        y = 4 * self.config["BLOCK_SIZE"]
        self.snake_body = [(x, y)]
        self.x_food = random.randint(0, self.config["DIS_WIDTH"] - self.config["BLOCK_SIZE"]) // self.config["BLOCK_SIZE"] * self.config["BLOCK_SIZE"]
        self.y_food = random.randint(0, self.config["DIS_HEIGHT"] - self.config["BLOCK_SIZE"]) // self.config["BLOCK_SIZE"] * self.config["BLOCK_SIZE"]
    def drawSnake(self):
        for body in self.snake_body:
            pygame.draw.rect(self.display, self.YELLOW, (body[0], body[1], self.config["BLOCK_SIZE"], self.config["BLOCK_SIZE"]))
    def drawFood(self):
        pygame.draw.rect(self.display, self.BLACK, (self.x_food, self.y_food, self.config["BLOCK_SIZE"], self.config["BLOCK_SIZE"]))
    def drawScore(self):
        font = pygame.font.SysFont("comicsansms", 35)
        value = font.render(f"Score: {self.size_snake - 1}", True, self.GREEN)
        self.display.blit(value, [0, 0])