import torch
import torch.nn as nn
from model import Car_LSTM
from data import CarDataset

car_set = CarDataset('data/train/Cybersecurity_Car_Hacking_S_training-0.csv')
train_loader = torch.utils.data.DataLoader(car_set, batch_size=1000)

model = Car_LSTM(11, 512, 2)

loss_func = nn.NLLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.003)

epochs = 5

for epoch in range(epochs):
    running_loss = 0

    for features, labels in train_loader:

        output = model(features)
        loss = loss_func(output, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
