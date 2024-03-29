import numpy as np
import cv2
from utils.color import is_color_similar


class FrameProcess:
    """
    Class to process frames from the retro environment.
    """
    def __init__(self, 
                 width: int, 
                 height: int, 
                 block_size: int):
        """Initialize FrameProcess.
        Args:
            width (int): Width of the frame.
            height (int): Height of the frame.
            block_size (int): Size of the block.
            elements (dict): Elements of the game.
        """
        self.width = width
        self.height = height
        self.block_size = block_size

    def get_elements_position(self, frame: np.ndarray, elements: dict, image_threshold = 0.8) -> list[tuple]:
        """Process the frame.
        Args:
            frame (np.ndarray):  A numpy array of the frame image(RGB).
        
        Returns:
            np.ndarray: A numpy array of the simplify image.
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
                    if is_color_similar(average_color, element['rgb'], 10):
                        elements_position.append((element, x//16, y//16))

        # Fiexed elements
        for element in elements["fixed"]:
            elements_position.append((element, element["fixed"][0]//16, element["fixed"][1]//16))
        
        # Find the position of the image elements in the frame
        for element in elements["images"]:

            # Read the template image and convert it to RGB
            template = cv2.imread(element["image"])
            template = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)

            # Find the position of the element in the frame
            result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)


            # Get the position of the element
            yloc, xloc = np.where(result >= image_threshold)

            # Add the position of the element to the list
            for (x, y) in zip(xloc, yloc):
                elements_position.append((element, x//16, y//16))

        return elements_position

        