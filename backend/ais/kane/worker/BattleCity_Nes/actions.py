import numpy as np
class Actions:
    """BattleCity actions.
    buttons: ["B", null, "SELECT", "START", "UP", "DOWN", "LEFT", "RIGHT", "A"]

    """
    def __init__(self):
        self.fire = False

    def get_action(self, action: list[str]):
        """Convert the action to the game action.
        Args:
            action (list[str]): A list of some actions.

        Returns:
            list[int]: A list of 9 integers, each integer represents an action of the game.

        """
        actions = []
        for a in action:
            if a == "UP":
                actions.append(np.array([0, 0, 0, 0, 1, 0, 0, 0, 0]))
            elif a == "DOWN":
                actions.append(np.array([0, 0, 0, 0, 0, 1, 0, 0, 0]))
            elif a == "LEFT":
                actions.append(np.array([0, 0, 0, 0, 0, 0, 1, 0, 0]))
            elif a == "RIGHT":
                actions.append(np.array([0, 0, 0, 0, 0, 0, 0, 1, 0]))
            elif a == "FIRE":
                actions.append(np.array([0, 0, 0, 0, 0, 0, 0, 0, 1 if self.fire else 0]))
                self.fire = not self.fire # Toggle the fire flag only when "FIRE" action is present

        return  np.bitwise_or.reduce(actions)
