import torch
import torch.nn as nn
from torch.nn import TransformerEncoder, TransformerEncoderLayer

class TransformerAgent(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, num_layers, nhead):
        super(TransformerAgent, self).__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        
        self.encoder_layer = TransformerEncoderLayer(d_model=self.hidden_dim, nhead=nhead)
        self.transformer_encoder = TransformerEncoder(self.encoder_layer, num_layers=num_layers)
        self.fc1 = nn.Linear(self.input_dim, self.hidden_dim)
        self.fc2 = nn.Linear(self.hidden_dim, self.output_dim)

    def forward(self, src):
        src = self.fc1(src)
        src = src.unsqueeze(1)  # Add batch dimension
        output = self.transformer_encoder(src)
        output = self.fc2(output.squeeze(1))
        action_probs = torch.softmax(output, dim=-1)  # 应用softmax来获得概率分布

        return action_probs