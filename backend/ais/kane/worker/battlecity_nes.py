import numpy as np
from vision.spatial_hash_table import SpatialHashTable
from vision.frame_process import FrameProcess
from .BattleCity_Nes.elements import elements


class BattleCityNesWorker:
    """
    This class is responsible for playing the Battle City NES game.
    """
    def __init__(self) -> None:
        """Initialize the BattleCityNesWorker class.
        
        Returns:
            None
        """
        # Create a spatial hash table to store the vision of the game, for battle city, the game area is 208x208, and each cell is 8x8
        self.hash_table = SpatialHashTable(208, 208, 4)
        self.frame_process = FrameProcess(208, 208, 4)


    def get_action(self) -> list[int]:
        """Get the action of the game.
        "buttons": ["B", null, "SELECT", "START", "UP", "DOWN", "LEFT", "RIGHT", "A"].

        Args:
            frame (np.ndarray): A numpy array of the frame image(RGB).
        
        Returns:
            list[int]: A list of 8 integers, each integer represents an action of the game.
        """

        self.hash_table.print_elements_positions(["player1_tank", "basic_tank"])
        
        return [0, 0, 0, 0, 1, 0, 0, 0, 0]
    
    def vision(self, frame: np.ndarray) -> None:
        """Get the vision of the game.

        Args:
            frame (np.ndarray): A numpy array of the frame image(RGB).
        
        Returns:
            None
        """

        # Process the frame
        elements_position = self.frame_process.get_elements_position(frame, elements)

        # Update the spatial hash table
        for element_p in elements_position:
            self.hash_table.insert(
                element_p[0]["name"], # The element name
                element_p[1], # The x position of the element
                element_p[2], # The y position of the element
                element_p[0]["size"][0], # The width of the element
                element_p[0]["size"][1] # The height of the element
            )
        