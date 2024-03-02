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
        

    def get_actions(self):
        return self.actions