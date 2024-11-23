import torchvision
from torchvision import transforms, models
import numpy as np # linear algebra
import os
import torch
from django.conf import settings


model = models.resnet50(pretrained=True)


model.fc = torch.nn.Linear(model.fc.in_features, 2)
loss = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1.0e-4)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=7, gamma=0.1)

path1 = os.path.join(settings.MODELS, "model.pt")
path2 = os.path.join(settings.MODELS, "optimizer.pt")
path3 = os.path.join(settings.MODELS, "scheduler.pt")
model.load_state_dict(torch.load(path1))
optimizer.load_state_dict(torch.load(path2))
scheduler.load_state_dict(torch.load(path3))

model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

