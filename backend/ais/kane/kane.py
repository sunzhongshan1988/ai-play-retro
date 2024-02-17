import time
from fastapi import WebSocket
import retro
import random
import cv2
import base64
from starlette.websockets import WebSocketDisconnect

from ais.kane.actions import Actions
from ais.kane.vision import write_image

async def run(game: str, global_ws: WebSocket):
    acts = Actions()

    # Create the environment
    env = retro.make(game=game, obs_type=retro.Observations.IMAGE)

    # Reset the environment
    obs = env.reset()

    # Run the game loop
    while True:
        # Render the game
        env.render()

        #print("Observation space:", env.observation_space)
        #print("Action space:", env.action_space)

        # Select a random action
        action = env.action_space.sample()

        #action = acts.get_action('shot')

        # Perform the action
        obs, reward, done, _, info = env.step(action)
        
        if global_ws:
            # Convert the observation to a BGR image
            obs_bgr = cv2.cvtColor(obs, cv2.COLOR_RGB2BGR)
            # Encode the image as a PNG
            _, buffer = cv2.imencode('.png', obs_bgr)
            # Convert the image to a base64 string
            img_base64 = base64.b64encode(buffer).decode("utf-8")
            # Send the image to the client
            try:
                await global_ws.send_json({"type": "image", "data": img_base64, "ai": "kane"})
            except WebSocketDisconnect:
                break
        else:
            break

        # Save the observation image
        # write_image(obs, f'{i}.png')

        # time.sleep(0.1)

        # If the game is over, reset the environment
        if done:
            obs = env.reset()

    # Close the environment
    env.close()
    if global_ws:
        try:
            await global_ws.send_json({"type": "status", "ai": "kane", "status": "done"})
        except WebSocketDisconnect:
            pass
