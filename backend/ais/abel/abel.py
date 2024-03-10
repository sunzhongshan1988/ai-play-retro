from multiprocessing import Queue
import os
import time
import retro
import cv2
import base64
import torch
from ais.abel.tansformer_agent import TransformerAgent

class Abel:
    """
    About Abel agent is a script-based AI agent that uses the retro environment to play games.
    """
    def __init__(self, game: str, queue: Queue):
        """Initialize Abel
        Args:
            game (str): The name of the game
            queue (Queue): A multiprocessing queue to communicate with the main process
        """
        self.game = game
        self.queue = queue
        self.env = None
        self.running = False

    def run(self):
        self.env = retro.make(game=self.game, obs_type=retro.Observations.RAM)
        obs = self.env.reset()[0]
        self.running = True

        input_dim = 10240  # Assuming 128-dimensional input from the RAM
        hidden_dim = 256
        output_dim = self.env.action_space.n  # Number of possible actions
        num_layers = 3
        nhead = 4

        filename = f'{self.game}.pth'
        file_path = os.path.join("ais/abel/model", filename)

        # Check if model file exists
        if not os.path.exists(file_path):
            print(f"Model file {file_path} does not exist. Exiting.")
            self.queue.put({"type": "status", "ai": "abel", "status": "error"})
            return

        model = TransformerAgent(input_dim, hidden_dim, output_dim, num_layers, nhead)
        model.load_state_dict(torch.load(file_path))
        model.eval()  # Set the model to evaluation mode
        model = model.to('cuda' if torch.cuda.is_available() else 'cpu')  # Move model to GPU if available


        while self.running:
            self.env.render()

            obs = torch.tensor(obs, dtype=torch.float32).unsqueeze(0)  # Convert observation to tensor and add batch dimension
            obs = obs.to('cuda' if torch.cuda.is_available() else 'cpu')  # Move obs to GPU if available

            with torch.no_grad():  # 不计算梯度
                action_probs = model(obs)
            action = torch.argmax(action_probs, dim=1).item()  # 选择概率最高的动作

            # 转换动作格式以匹配环境期望
            action_list = [0] * 9
            action_list[action] = 1

            obs, reward, done, _, info = self.env.step(action_list)

            # Convert to base64 and send to queue
            obs_bgr = cv2.cvtColor(obs, cv2.COLOR_RGB2BGR)
            _, buffer = cv2.imencode('.png', obs_bgr)
            img_base64 = base64.b64encode(buffer).decode("utf-8")
            self.queue.put({"type": "image", "data": img_base64, "ai": "abel"})

            # time.sleep(0.1)

            if done:
                obs = self.env.reset()[0]

        self.env.close()
        self.queue.put({"type": "status", "ai": "abel", "status": "done"})

    def stop(self):
        self.running = False
