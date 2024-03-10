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

# 初始化环境
game = sys.argv[1]
env = retro.make(game=game, obs_type=retro.Observations.RAM)  # 替换'YourGameName'为实际游戏名
input_dim = 10240  # Assuming 128-dimensional input from the RAM
hidden_dim = 256
output_dim = env.action_space.n  # Number of possible actions
num_layers = 3
nhead = 4

# 初始化模型和优化器
model = TransformerAgent(input_dim, hidden_dim, output_dim, num_layers, nhead)
optimizer = optim.Adam(model.parameters(), lr=0.001)
loss_fn = nn.CrossEntropyLoss()

def train(model, env, optimizer, loss_fn, episodes=2, gamma=0.99):
    for episode in range(episodes):
        obs = env.reset()[0]
        done = False
        total_reward = 0
        log_probs = []  # 用于存储每一步的log概率
        rewards = []  # 用于存储每一步的奖励

        if obs.size == 0:
            print("Observation is empty. Skipping this step.")
            continue  # 跳过当前步骤，或采取其他适当的行动

        while not done:
            obs_tensor = torch.tensor(obs, dtype=torch.float32).unsqueeze(0)  # 添加批次维度
            action_probs = model(obs_tensor)
            distribution = torch.distributions.Categorical(probs=action_probs)  # 现在action_probs是有效的概率分布
            action = distribution.sample()  # 从分布中采样一个动作
            log_prob = distribution.log_prob(action)  # 计算取得该动作的log概率

            # 转换动作格式以匹配环境期望
            action_index = action.item()
            action_list = [0] * 9
            action_list[action_index] = 1

            obs, reward, done, _, info= env.step(action_list)  # 执行动作

            log_probs.append(log_prob)  # 保存log概率
            rewards.append(reward)  # 保存奖励
            total_reward += reward

        # 计算累计回报
        discounted_rewards = []
        cumulative_rewards = 0
        for reward in rewards[::-1]:  # 反向遍历奖励
            cumulative_rewards = reward + cumulative_rewards * gamma
            discounted_rewards.insert(0, cumulative_rewards)  # 将累计回报插入到列表前端

        # 标准化回报
        discounted_rewards = torch.tensor(discounted_rewards)
        discounted_rewards = (discounted_rewards - discounted_rewards.mean()) / (discounted_rewards.std() + 1e-9)

        # 计算损失
        loss = 0
        for log_prob, reward in zip(log_probs, discounted_rewards):
            loss += -log_prob * reward  # 注意：这里使用的是梯度上升，因此前面有负号
        loss = loss / len(rewards)  # 取平均损失

        # 执行反向传播和优化器步骤
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print(f'Episode {episode+1}, Total Reward: {total_reward}')

train(model, env, optimizer, loss_fn, episodes=1, gamma=0.99)


# 获取当前文件的目录
current_dir = os.path.dirname(os.path.realpath(__file__))
filename = f'{game}.pth'
save_path = os.path.join("ais/abel/model", filename)

# 保存模型参数
torch.save(model.state_dict(), save_path)