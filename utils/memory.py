import random

class ReplayMemory():

    def __init__(self):
        #self.size = size
        self.memory = []

    def push(self, state, action, next_state, reward, end):
        self.memory.append([state, action, next_state, reward, end])

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)