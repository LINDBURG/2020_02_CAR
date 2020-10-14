import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.functional as F
import torch.optim as optim

class Car_LSTM(nn.Module):

    def __init__(self, input_dim, hidden_dim, num_class):
        super(Car_LSTM).__init__()

        self.input_dim = input_dim
        self.hidden_dim = hidden_dim

        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers=1)

        self.fc = nn.Linear(hidden_dim, num_class)
        self.softmax = nn.LogSoftmax()

        self.dropout_layer = nn.Dropout(p=0.2)

    def init_hidden(self, batch_size):
        return (autograd.Variable(torch.randn(1, batch_size, self.hidden_dim)),
                autograd.Variable(torch.randn(1, batch_size, self.hidde_dim)))

    def forward(self, batch):
        self.hidden = self.init_hidden(batch.size(-1))

        outputs, (ht, ct) = self.lstm(batch, self.hidden)

        output = self.dropout_layer(ht[-1])
        output = self.fc(output)
        output = self.softmax(output)

        return output
