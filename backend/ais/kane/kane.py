import time
from fastapi import WebSocket
import retro
import random
import cv2
import base64
from starlette.websockets import WebSocketDisconnect

from ais.kane.actions import Actions
from ais.kane.vision import write_image

class Kane:
    def __init__(self, game, ws):
        self.game = game
        self.ws = ws
        self.env = None
        self.running = False

    async def run(self):
        acts = Actions()

        # Create the environment
        self.env = retro.make(game=self.game, obs_type=retro.Observations.IMAGE)

        # Reset the environment
        self.env.reset()
        self.running = True

        # Run the game loop
        while self.running:
            # Render the game on the screen
            self.env.render()

            #print("Observation space:", env.observation_space)
            #print("Action space:", env.action_space)

            # Select a random action
            action = self.env.action_space.sample()

            #action = acts.get_action('shot')

            # Perform the action
            obs, reward, done, _, info =self.env.step(action)
            
            if self.ws:
                # Convert the observation to a BGR image
                obs_bgr = cv2.cvtColor(obs, cv2.COLOR_RGB2BGR)
                # Encode the image as a PNG
                _, buffer = cv2.imencode('.png', obs_bgr)
                # Convert the image to a base64 string
                img_base64 = base64.b64encode(buffer).decode("utf-8")
                # Send the image to the client
                try:
                    await self.ws.send_json({"type": "image", "data": img_base64, "ai": "kane"})
                except WebSocketDisconnect:
                    break
            else:
                break

            # Save the observation image
            # write_image(obs, f'{i}.png')

            # time.sleep(0.1)

            # If the game is over, reset the environment
            if done:
                obs = self.env.reset()

        # Close the environment
        self.env.close()
        if self.ws:
            try:
                await self.ws.send_json({"type": "status", "ai": "kane", "status": "done"})
            except WebSocketDisconnect:
                pass
    
    def stop(self):
        self.running = False
