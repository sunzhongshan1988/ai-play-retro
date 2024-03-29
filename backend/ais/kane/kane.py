from multiprocessing import Queue
import time
import retro
import cv2
import base64

from ais.kane.worker_factory import Worker_Factory

class Kane:
    """
    About Kane agent is a script-based AI agent that uses the retro environment to play games.
    """
    def __init__(self, game: str, queue: Queue):
        """Initialize Kane
        Args:
            game (str): The name of the game
            queue (Queue): A multiprocessing queue to communicate with the main process
        """
        self.game = game
        self.queue = queue
        self.env = None
        self.running = False
        self.worker = Worker_Factory.get_worker(game)

    def run(self):
        self.env = retro.make(game=self.game, obs_type=retro.Observations.IMAGE)
        obs = self.env.reset()[0]
        self.running = True

        while self.running:
            self.env.render()

            # Get the action from the worker
            action = self.worker.get_action(obs)

            obs, reward, done, _, info = self.env.step(action)

            # Convert to base64 and send to queue
            obs_bgr = cv2.cvtColor(obs, cv2.COLOR_RGB2BGR)
            _, buffer = cv2.imencode('.png', obs_bgr)
            img_base64 = base64.b64encode(buffer).decode("utf-8")
            self.queue.put({"type": "image", "data": img_base64, "ai": "kane"})

            # time.sleep(0.1)

            if done:
                obs = self.env.reset()[0]

        self.env.close()
        self.queue.put({"type": "status", "ai": "kane", "status": "done"})

    def stop(self):
        self.running = False
