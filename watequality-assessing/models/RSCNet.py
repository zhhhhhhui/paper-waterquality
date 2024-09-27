import torch
import torch.nn as nn
import torch.nn.functional as F


class RSCBlock(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(RSCBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1)
        self.shortcut = nn.Conv2d(in_channels, out_channels, kernel_size=1)

    def forward(self, x):
        residual = self.shortcut(x)
        x = F.relu(self.conv1(x))
        x = self.conv2(x)
        return F.relu(x + residual)


class RSCNet(nn.Module):
    def __init__(self, num_classes=3):
        super(RSCNet, self).__init__()
        self.encoder = nn.Sequential(
            RSCBlock(3, 64),
            RSCBlock(64, 128)
        )
        self.decoder = nn.Sequential(
            RSCBlock(128, 64),
            RSCBlock(64, 32)
        )
        self.final_conv = nn.Conv2d(32, num_classes, kernel_size=1)

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return self.final_conv(x)
