import torch.nn as nn
import torch.nn.functional as F

from arhuaco.analysis.abstract_model import AbstractModel

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
        # Create the classifier
        self.model = LinearNetwork(in_features = 300, out_features = 2)
        self.optim = optim.SGD(params = classifier.parameters(),
                          lr = learning_rate)

    def load_data(self, train_loader, val_loader):
        self.train_loader = train_loader
        self.valloader = val_loader

    def train_model(self, model, optim):
        # Set train mode
        model.train()
        for epoch in range(epochs):
            for iter, (vectors, targets) in enumerate(self.trainloader):
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
                accuracy = accuracy.get().float_precision()
                accuracy = 100 * (accuracy / batch_size)

                # Backpropagate the loss
                loss.backward()

                # Update weights
                optim.step()

    def test_model(self, model):
        """ Perform validation on exactly one batch """
        # Set validation mode
        model.eval()
        for vectors, targets in self.valloader:
            probs, logits = model(vectors)

            loss = ((probs -  targets)**2).sum()

            preds = probs.argmax(dim=1)
            targets = targets.argmax(dim=1)

            accuracy = preds.eq(targets).sum()
            accuracy = accuracy.get().float_precision()
            accuracy = 100 * (accuracy / batch_size)

            loss = loss.get().float_precision()
            print(loss)