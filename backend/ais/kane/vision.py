import cv2
import os

def write_image(array_image, filename):
    """Write an image to disk."""

    # Only keep the game activity portion of the screenshot
    # array_image = array_image[8:216, 8:216]
    
    # Convert to BGR format
    array_image = cv2.cvtColor(array_image, cv2.COLOR_RGB2BGR)

    # Write to disk
    relative_path = 'screenshot'
    if not os.path.exists(relative_path):
        os.makedirs(relative_path)
    full_path = os.path.join(relative_path, filename)

    try:
        cv2.imwrite(full_path, array_image)
    except Exception as e:
        print(e)