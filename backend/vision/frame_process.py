import numpy as np
from vision.spatial_hash_table import SpatialHashTable


class FrameProcess:
    """
    Class to process frames from the retro environment
    """
    def __init__(self, 
                 width: int, 
                 height: int, 
                 vaild_area: tuple, 
                 block_size: int):
        """Initialize FrameProcess
        Args:
            width (int): Width of the frame
            height (int): Height of the frame
            vaild_area (tuple): (x1, y1, x2, y2) tuple of the vaild area
            block_size (int): Size of the block
            hash_table (SpatialHashTable): SpatialHashTable
            elements (dict): Elements of the game
        """
        self.width = width
        self.height = height
        self.vaild_area = vaild_area
        self.block_size = block_size

    def get_simplify_image(self, frame: np.ndarray) -> np.ndarray:
        """Process the frame
        Args:
            frame (np.ndarray):  A numpy array of the frame image(RGB)
        
        Returns:
            np.ndarray: A numpy array of the simplify image
        """

        # Get the vaild area of the frame
        vaild_frame_area = frame[self.vaild_area[1]:self.vaild_area[3], self.vaild_area[0]:self.vaild_area[2]]

        # Create a new image with the same size
        simplify_image = np.zeros((self.height, self.width, 3), np.uint8)

        # Traverse all blocks
        for y in range(0, self.height, self.block_size):
            for x in range(0, self.width, self.block_size):
                #  Get a block
                block = vaild_frame_area[y:y+self.block_size, x:x+self.block_size]

                # Calculate the average color of the block
                average_color = block.mean(axis=(0, 1))

                # Set the block to the average color
                simplify_image[y:y+self.block_size, x:x+self.block_size] = average_color
        
        return simplify_image

        