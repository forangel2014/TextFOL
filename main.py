from distutils.command.config import config
from logic.textfol import *
from model.tokenizer import *
from model.bert import *
from utils.memory import *
import torch.optim as optim
import copy

class Config():

    def __init__(self, batch_size, gamma, episilon, lr):
        self.batch_size = batch_size
        self.gamma = gamma
        self.episilon = episilon
        self.lr = lr

class Trainer():

    def __init__(self, config, environment, model, optimizer, rep):
        self.config = config
        self.environment = environment
        self.model = model
        self.optimizer = optimizer
        self.rep = rep

    def generate_rule(self):
        rule = self.environment.controller.init_rule()
        
        while self.environment.controller.state != 'BEGIN':
            print(str(rule))
            state = copy.deepcopy(rule)
            values = self.model.q_value(rule)
            valid_actions = self.environment.controller.valid_action()
            action, action_id = self.model.episilon_greedy(valid_actions, values, episilon=self.config.episilon)
            rule = self.environment.controller.take_action(action)
            reward = self.environment.get_reward(rule)
            next_state = copy.deepcopy(rule)
            end = self.environment.controller.state == 'BEGIN'
            self.rep.push(state, action_id, next_state, reward, end)

        print(str(rule))

    def mse_loss(self):
        loss = 0
        samples = self.rep.sample(self.config.batch_size)
        for sample in samples:
            state, action_id, next_state, reward, end = sample
            y_real = self.model.q_value(state)[action_id]
            if end:
                y_expect = reward
            else:
                y_expect = reward + self.config.gamma*torch.max(self.model.q_value(next_state))
            loss += (y_real - y_expect)**2
        return loss

    def train(self):
        for _ in range(10):
            self.config.episilon += 0.1
            self.rep.__init__()
            for _ in range(10):
                self.generate_rule()
            for _ in range(100):
                loss = self.mse_loss()
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
                print(loss)

#datadir = 'data/bc5cdr/'
#dataset = NERDataset(datadir)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
datadir = 'data/trec/'
dataset = TRECDataset(datadir)

constants = dataset.create_constants()
config = Config(batch_size=1, gamma=0.9, episilon=0, lr=1e-5)

controller = Controller(predicates, connectives, functions, constants, tags=dataset.tags)
tokenizer = Tokenizer(predicates, connectives, functions, constants, tags=dataset.tags)

environment = TextFOL(dataset, controller)
model = RuleEncoder(tokenizer, device)
optimizer = optim.RMSprop(model.parameters(), config.lr)
rep = ReplayMemory()

trainer = Trainer(config, environment, model, optimizer, rep)


trainer.train()
