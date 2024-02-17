import time

import retro
import random

from ais.kane.actions import Actions
from ais.kane.vision import write_image

def run():
    acts = Actions()

    # Create the environment
    env = retro.make(game='BattleCity-Nes', obs_type=retro.Observations.IMAGE)

    # Reset the environment
    obs = env.reset()

    # Run the game loop
    while True:
        # Render the game
        env.render()

        print("Observation space:", env.observation_space)
        print("Action space:", env.action_space)

        for i in range(10000):
            # Select a random action
            action = env.action_space.sample()

            #action = acts.get_action('shot')

            # Perform the action
            obs, reward, done, _, info = env.step(action)

            # Save the observation image
            # write_image(obs, f'{i}.png')

            # time.sleep(0.1)

            # If the game is over, reset the environment
            if done:
                obs = env.reset()

        
        

    # Close the environment
    env.close()
