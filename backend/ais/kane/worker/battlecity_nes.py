class BattleCityNesWorker:
    """
    This class is responsible for playing the Battle City NES game.
    """
    def __init__(self) -> None:
        pass

    def get_action(self) -> list[int]:
        """Get the action of the game
        Args:
            frame (np.ndarray): A numpy array of the frame image(RGB)
        
        Returns:
            list[int]: A list of 8 integers, each integer represents an action of the game
        """
        return [0, 0, 0, 0, 1, 0, 0, 0, 0]