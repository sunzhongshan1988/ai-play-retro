import numpy as np
from vision.spatial_hash_table import SpatialHashTable
from vision.frame_process import FrameProcess


class BattleCityNesWorker:
    """
    This class is responsible for playing the Battle City NES game.
    """
    def __init__(self) -> None:
        """Initialize the BattleCityNesWorker class
        
        Returns:
            None
        """
        # Create a spatial hash table to store the vision of the game, for battle city, the game area is 208x208, and each cell is 8x8
        self.hash_table = SpatialHashTable(208, 208, 4)
        self.frame_process = FrameProcess(208, 208, 4)


    def get_action(self) -> list[int]:
        """Get the action of the game
        "buttons": ["B", null, "SELECT", "START", "UP", "DOWN", "LEFT", "RIGHT", "A"]

        Args:
            frame (np.ndarray): A numpy array of the frame image(RGB)
        
        Returns:
            list[int]: A list of 8 integers, each integer represents an action of the game
        """
        return [0, 0, 0, 0, 1, 0, 0, 0, 0]
    
    def vision(self, frame: np.ndarray) -> None:
        """Get the vision of the game

        Args:
            frame (np.ndarray): A numpy array of the frame image(RGB)
        
        Returns:
            None
        """

        # Process the frame
        elements_position = self.frame_process.get_elements_position(frame, elements)

        # Update the spatial hash table
        for element in elements_position:
            self.hash_table.insert(element, element[1], element[2], 4, 4)
        