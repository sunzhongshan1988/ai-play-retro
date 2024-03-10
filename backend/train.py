from ais.abel.tansformer_agent import TransformerAgent

import sys
import os
import retro
import torch
import torch.optim as optim
import torch.nn as nn

if len(sys.argv) < 2:
    print('Usage: python train.py <YourGameName>')
    sys.exit(1)

if torch.cuda.is_available():
    device = torch.device("cuda")
    print("CUDA is available. Training on GPU.")
else:
    device = torch.device("cpu")
    print("CUDA is not available. Training on CPU.")

# Initialize the environment
game = sys.argv[1]
env = retro.make(game=game, obs_type=retro.Observations.RAM)
input_dim = 10240  # Assuming 10240-dimensional input from the RAM
hidden_dim = 256
output_dim = env.action_space.n  # Number of possible actions
num_layers = 3
nhead = 4

# Initialize the model, optimizer, and loss function
model = TransformerAgent(input_dim, hidden_dim, output_dim, num_layers, nhead)
optimizer = optim.Adam(model.parameters(), lr=0.001)
loss_fn = nn.CrossEntropyLoss()

def train(model, env, optimizer, loss_fn, episodes=2, gamma=0.99):
    for episode in range(episodes):
        obs = env.reset()[0]
        done = False
        total_reward = 0
        log_probs = []  # Save the log probabilities of actions
        rewards = []  #  Save the rewards of actions

        if obs.size == 0:
            print("Observation is empty. Skipping this step.")
            continue  # Skip this step if the observation is empty

        while not done:
            obs_tensor = torch.tensor(obs, dtype=torch.float32).unsqueeze(0)  #  Convert observation to tensor and add batch dimension
            action_probs = model(obs_tensor)
            distribution = torch.distributions.Categorical(probs=action_probs)  #  Create a categorical distribution
            action = distribution.sample()  #  Sample an action from the distribution
            log_prob = distribution.log_prob(action)  #  Get the log probability of the action

            # Convert action to the format expected by the environment
            action_index = action.item()
            action_list = [0] * 9
            action_list[action_index] = 1

            obs, reward, done, _, info= env.step(action_list)  #  Execute the action in the environment

            log_probs.append(log_prob)  #  Save the log probability
            rewards.append(reward)  #  Save the reward
            total_reward += reward

        # Calculate the discounted rewards
        discounted_rewards = []
        cumulative_rewards = 0
        for reward in rewards[::-1]:  #  Reverse the rewards list
            cumulative_rewards = reward + cumulative_rewards * gamma
            discounted_rewards.insert(0, cumulative_rewards)  #  Insert the cumulative reward at the beginning of the list

        # Normalize the discounted rewards
        discounted_rewards = torch.tensor(discounted_rewards)
        discounted_rewards = (discounted_rewards - discounted_rewards.mean()) / (discounted_rewards.std() + 1e-9)

        # Calculate the loss
        loss = 0
        for log_prob, reward in zip(log_probs, discounted_rewards):
            loss += -log_prob * reward  # Note: Gradient ascent is used here, so there is a negative sign in front of it
        loss = loss / len(rewards)  #  Average the loss
        
        # Perform backpropagation and optimizer steps
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print(f'Episode {episode+1}, Total Reward: {total_reward}')

train(model, env, optimizer, loss_fn, episodes=30, gamma=0.99)


# Save the model
filename = f'{game}.pth'
save_path = os.path.join("ais/abel/model", filename)
torch.save(model.state_dict(), save_path)