import torch
import torch.nn as nn
import random
from transformers import BertConfig, BertModel

class BertEncoder(nn.Module):
    def __init__(self, vocab_size, n_actions):
        super(BertEncoder, self).__init__()
        self.config = BertConfig(
                                vocab_size_or_config_json_file=vocab_size,
                                hidden_size=768,
                                num_hidden_layers=2,
                                num_attention_heads=12,
                                intermediate_size=3072,
                                hidden_act="gelu",
                                hidden_dropout_prob=0.1,
                                attention_probs_dropout_prob=0.1,
                                max_position_embeddings=512,
                                type_vocab_size=2,
                                initializer_range=0.02,
                                layer_norm_eps=1e-12,
                                )
        self.bert = BertModel(self.config)
        self.linear = nn.Linear(self.config.hidden_size, n_actions)

    def train(self, mode=True):
        self.bert.train()

    def eval(self):
        self.bert.eval()

    def forward(self, ids):
        output = self.bert(input_ids=ids)[0]
        return self.linear(output[:, 0, :])


class RuleEncoder(nn.Module):

    def __init__(self, tokenizer, device):
        super(RuleEncoder, self).__init__()

        self.tokenizer = tokenizer
        self.device = device
        self.sentence_net = BertEncoder(tokenizer.vocab_size, 2).cuda(device)
        self.term_net = BertEncoder(tokenizer.vocab_size, 2).cuda(device)
        self.predicate_net = BertEncoder(tokenizer.vocab_size, tokenizer.n_predicates).cuda(device)
        self.connective_net = BertEncoder(tokenizer.vocab_size, tokenizer.n_connectives).cuda(device)
        self.function_net = BertEncoder(tokenizer.vocab_size, tokenizer.n_functions).cuda(device)
        self.constant_net = BertEncoder(tokenizer.vocab_size, tokenizer.n_constants).cuda(device)
        self.variable_net = BertEncoder(tokenizer.vocab_size, 1).cuda(device)

    def q_value(self, rule):
        state2net = {'SelectSentence':self.sentence_net, 'SelectTerm':self.term_net, 
                    'SelectPredicate':self.predicate_net, 'SelectFunction':self.function_net, 
                    'SelectConstant':self.constant_net, 'SelectConnective':self.connective_net, 
                    'SelectVariable':self.variable_net}
        net = state2net[rule.state]
        ids = self.tokenizer.encode(rule)
        ids = torch.tensor([ids]).cuda(self.device)
        return net(ids)[0]

    def episilon_greedy(self, valid_actions, values, episilon=0.1):
        if random.random() < episilon:
            action_id = torch.argmax(values)
        else:
            action_id = random.randint(0, len(valid_actions)-1)
        action = valid_actions[action_id]
        return action, action_id