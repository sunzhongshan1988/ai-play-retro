import multiprocessing
from multiprocessing import Queue
import retro
import cv2
import base64
import random

class Abel:
    def __init__(self, game, queue: Queue):
        self.game = game
        self.queue = queue
        self.env = None
        self.running = False

    # 改为同步方法
    def run(self):
        self.env = retro.make(game=self.game, obs_type=retro.Observations.IMAGE)
        self.env.reset()
        self.running = True

        while self.running:
            self.env.render()
            action = self.env.action_space.sample()
            obs, reward, done, _, info = self.env.step(action)

            # 处理游戏帧并放入队列
            obs_bgr = cv2.cvtColor(obs, cv2.COLOR_RGB2BGR)
            _, buffer = cv2.imencode('.png', obs_bgr)
            img_base64 = base64.b64encode(buffer).decode("utf-8")
            self.queue.put({"type": "image", "data": img_base64, "ai": "abel"})

            if done:
                obs = self.env.reset()

        self.env.close()
        self.queue.put({"type": "status", "ai": "kane", "status": "done"})

    def stop(self):
        self.running = False
