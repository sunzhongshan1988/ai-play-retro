from multiprocessing import Queue
import time
import retro
import cv2
import base64

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
        self.env = retro.make(game=self.game, obs_type=retro.Observations.IMAGE)
        obs = self.env.reset()[0]
        self.running = True

        while self.running:
            self.env.render()

            action = self.env.action_space.sample()

            obs, reward, done, _, info = self.env.step(action)

            # Convert to base64 and send to queue
            obs_bgr = cv2.cvtColor(obs, cv2.COLOR_RGB2BGR)
            _, buffer = cv2.imencode('.png', obs_bgr)
            img_base64 = base64.b64encode(buffer).decode("utf-8")
            self.queue.put({"type": "image", "data": img_base64, "ai": "abel"})

            # time.sleep(0.1)

            if done:
                obs = self.env.reset()

        self.env.close()
        self.queue.put({"type": "status", "ai": "abel", "status": "done"})

    def stop(self):
        self.running = False
