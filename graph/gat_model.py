# gat_model.py

import torch
import torch.nn as nn
from torch_geometric.nn import GATConv


class ServiceFailureGAT(nn.Module):
    def __init__(self, in_dim, hidden_dim):
        super().__init__()
        self.gat1 = GATConv(in_dim, hidden_dim, heads=2)
        self.gat2 = GATConv(hidden_dim * 2, 1)

    def forward(self, x, edge_index):
        x = self.gat1(x, edge_index)
        x = torch.relu(x)
        x = self.gat2(x, edge_index)
        return torch.sigmoid(x)
