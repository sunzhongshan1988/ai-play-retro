import numpy as np

def is_color_similar(color1, color2, tolerance=10) -> bool:
    """ Check if two colors are similar.

    Args:
        color1 (tuple): RGB color tuple
        color2 (tuple): RGB color tuple
        tolerance (int): The tolerance of the difference between the two colors

    Returns:
        bool: True if the two colors are similar, False otherwise
    """
    # Calculate the difference between the two colors
    diff = np.abs(np.array(color1) - np.array(color2))
    
    # Check if the difference is within the tolerance
    return np.all(diff <= tolerance)
