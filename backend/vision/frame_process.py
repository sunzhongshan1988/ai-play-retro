import numpy as np
import cv2
from utils.color import is_color_similar


class FrameProcess:
    """
    Class to process frames from the retro environment
    """
    def __init__(self, 
                 width: int, 
                 height: int, 
                 block_size: int):
        """Initialize FrameProcess
        Args:
            width (int): Width of the frame
            height (int): Height of the frame
            block_size (int): Size of the block
            elements (dict): Elements of the game
        """
        self.width = width
        self.height = height
        self.block_size = block_size

    def get_elements_position(self, frame: np.ndarray, elements: dict) -> list[tuple]:
        """Process the frame
        Args:
            frame (np.ndarray):  A numpy array of the frame image(RGB)
        
        Returns:
            np.ndarray: A numpy array of the simplify image
        """

        # Store the position of the elements
        elements_position = []

        # Get the position of the rgb elements in the frame
        for y in range(0, self.height, self.block_size):
            for x in range(0, self.width, self.block_size):
                #  Get a block
                block = frame[y:y+self.block_size, x:x+self.block_size]

                # Calculate the average color of the block
                average_color = block.mean(axis=(0, 1))

                # Check if the average color is similar to the color of the elements
                for element in elements["rgb"]:
                    if is_color_similar(average_color, elements[element]["rgb"]):
                        elements_position.append((element, x, y))

        # Fiexed elements
        for element in elements["fixed"]:
            elements_position.append((element, element["fixed"][0], element["fixed"][1]))
        
        # Find the position of the image elements in the frame
        for element in elements["images"]:
            cv2.imread(element["image"])
            # Find the position of the element in the frame
            position = cv2.matchTemplate(frame, element["image"], cv2.TM_CCOEFF_NORMED)
            # Get the position of the element
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(position)
            # Add the position of the element to the list
            elements_position.append((element, max_loc[0], max_loc[1]))

        return elements_position

        