"""
Defines the actions that the agent can take.
The action mapping for the Stable-Retro NES emulator is as follows:
['A', 'B', 'SELECT', 'START', 'UP', 'DOWN', 'LEFT', 'RIGHT', 'NOOP']
"""
class Actions:
    def __init__(self):
        # For many games, pressing the A or B key does not trigger continuous actions,
        # so we need to record this state and reset it the next time the action is called.
        self.shot_state = False

        self.shot = [1, 0, 0, 0, 0, 0, 0, 0, 0]
        self.up = [0, 0, 0, 0, 1, 0, 0, 0, 0]
        self.down = [0, 0, 0, 0, 0, 1, 0, 0, 0]
        self.left = [0, 0, 0, 0, 0, 0, 1, 0, 0]
        self.right = [0, 0, 0, 0, 0, 0, 0, 1, 0]
        self.none = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    def get_action(self, action):
        if action == 'shot':
            # If action is shot, then toggle the shot state and return the shot action.
            self.shot_state = not self.shot_state
            if not self.shot_state:
                return self.none
            else:
                return self.shot
        elif action == 'up':
            return self.up
        elif action == 'down':
            return self.down
        elif action == 'left':
            return self.left
        elif action == 'right':
            return self.right
        else:
            return self.none