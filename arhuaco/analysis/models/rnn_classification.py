import warnings
warnings.filterwarnings('ignore')

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import syft as sy
import numpy as np

from arhuaco.analysis.abstract_model import AbstractModel
from torch.utils.data import DataLoader
from data_loader import DataLoader as SikuaniLoader
from arguments import Arguments
from torch.utils.tensorboard import SummaryWriter
from sikuani_dataset import SikuaniDataset

class Rnn(nn.Module):
    def __init__(self, number_inputs, number_outputs):
        super(Network, self).__init__()
        self.args = Arguments()
        # Initiating the models
        # Dropout layer
        self.dropout = nn.Dropout(p=self.args.dropout)
        # GRU Cell
        self.gru_cell = syft_nn.GRU(input_size=self.args.embedding_dim,
                               hidden_size=self.args.hidden_dim,
                               num_layers=self.args.hidden_layers,
                               dropout=self.args.dropout)
        # Fully-connected layer
        self.fc = nn.Linear(self.args.hidden_dim, number_outputs)
        # Sigmoid layer
        self.sigmoid = nn.Sigmoid()

    def forward(self, x, h):
        batch_size = x.shape[1]

        if h.shape[1] != batch_size:
            h = h[:,:batch_size].contiguous()

        x, h = self.gru_cell(x, h)
        out = h.contiguous().view(-1, self.args.hidden_dim)

        out = self.dropout(out)
        sig_out = self.sigmoid(self.fc(out))

        return sig_out, h

class RnnClassification(AbstractModel):

    def __init__(self):
        super(RnnClassification, self).__init__()
        # Initiating the model
        self.model = Rnn(number_inputs=ec.args.embedding_dim,
                         number_outputs=ec.args.number_outputs)
        # Defining loss and optimizer
        # criterion = nn.BCELoss()
        self.optim = optim.SGD(model.parameters(), lr=ec.args.lr)

    def load_data(self, train_data, val_data):
        self.train_loader = train_data
        self.val_loader = tval_data

    def train_model(self, args, model):
        model.train()
        for epoch in range(self.args.epochs):
            for iter, (data, target) in enumerate(self.train_loader):
                # Initialize hidden state and send it to worker
                h = torch.Tensor(np.zeros((args.hidden_layers,
                                           args.batch_size,
                                           args.hidden_dim)))
                # Setting accumulated gradients to zero before backward step
                optim.zero_grad()
                data = torch.unsqueeze(data, 0)
                # Output from the model
                output, _ = model(data, h)
                # Compute loss and accuracy
                loss = ((output -  targets)**2).sum()
                # Get the predicted labels
                preds = output.argmax(dim=1)
                targets = targets.argmax(dim=1)
                # Compute the prediction accuracy
                accuracy = (preds == targets).sum()
                accuracy = 100 * (accuracy / self.batch_size)
                # Backpropagate the loss
                loss.backward()
                # Update weights
                optim.step()
                # Decrypt the loss for logging
                print(loss)

    def test_model(self, args, model, test_loader):
        model.eval()
        test_loss = 0
        for data, target in self.val_loader:
            # Initialize hidden state and send it to worker
            h = torch.Tensor(np.zeros((args.hidden_layers,
                                       args.test_batch_size,
                                       args.hidden_dim)))
            data = torch.transpose(data, 0, 1)
            output, _ = model(data, h)
            preds = output.argmax(dim=1)
            targets = targets.argmax(dim=1)

            accuracy = preds.eq(targets).sum()
            accuracy = 100 * (accuracy / batch_size)

            print(loss)