import torch
from ais.abel.tansformer_agent import TransformerAgent
from torchviz import make_dot

# Model parameters
input_dim = 10240  # Assuming 10240-dimensional input from the RAM
hidden_dim = 256
output_dim = 5  # Number of possible actions
num_layers = 3
nhead = 4

# Initialize the model
model = TransformerAgent(input_dim, hidden_dim, output_dim, num_layers, nhead)

#Create a dummy input that matches the model input dimensions
# unsqueeze(0) here is to add batch dimensions
x = torch.randn(1, input_dim)

# Perform forward propagation through the model to get the output
# Need to use the model's evaluation mode to ensure that some layers (such as Dropout) behave differently from the training mode
model.eval()
y = model(x)

# Use make_dot to generate plots from output
dot = make_dot(y, params=dict(list(model.named_parameters()) + [('input', x)]))

# Render the image to a file (such as PDF)
dot.render('transformer_agent_visualization', format='pdf')
