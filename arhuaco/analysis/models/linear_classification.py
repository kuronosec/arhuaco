import torch.nn as nn
import torch.nn.functional as F

from arhuaco.analysis.abstract_model import AbstractModel

# Set some hyper parameters
learning_rate = 0.001
batch_size = 32
epochs = 1

class LinearNetwork(nn.Module):

    def __init__(self, in_features, out_features):
        super(LinearNetwork, self).__init__()

        self.fc = nn.Linear(in_features, out_features)

    def forward(self, x):

        logits = self.fc(x)

        probs = F.relu(logits)

        return probs, logits

class LinearClassification(AbstractModel):

    def __init__(self):
        super(LinearClassification, self).__init__()

    def load_data(self, train_loader, val_loader):
        self.train_loader = train_loader
        self.val_loader = val_loader

    def train_model(self, model, optim):
        # Set train mode
        model.train()
        for epoch in range(epochs):
            for iter, (vectors, targets) in enumerate(self.train_loader):
                # Zero out previous gradients
                optim.zero_grad()

                # Predict sentiment probabilities
                probs, logits = model(vectors)

                # Compute loss and accuracy
                loss = ((probs -  targets)**2).sum()

                # Get the predicted labels
                preds = probs.argmax(dim=1)
                targets = targets.argmax(dim=1)

                # Compute the prediction accuracy
                accuracy = (preds == targets).sum()
                accuracy = 100 * (accuracy / batch_size)

                # Backpropagate the loss
                loss.backward()

                # Update weights
                optim.step()
                print(accuracy)
                print(loss)

    def test_model(self, model):
        """ Perform validation on exactly one batch """
        # Set validation mode
        model.eval()
        for vectors, targets in self.val_loader:
            probs, logits = model(vectors)

            loss = ((probs -  targets)**2).sum()

            preds = probs.argmax(dim=1)
            targets = targets.argmax(dim=1)

            accuracy = preds.eq(targets).sum()
            accuracy = 100 * (accuracy / batch_size)
            print(accuracy)
            print(loss)