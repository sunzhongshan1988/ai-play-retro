"""
preperty: passable, protected, destroyable, variable
passable: tank can move through
protected: cannot be attacked
destroyable: can be destroyed

"""
import os

current_dir = os.path.dirname(__file__)

rgb_elements = [
    {
        "name": "brick",
        "preperty": "destroyable",
        "rgb": [153, 68, 41],
        "size": [4, 4]
    },
    {
        "name": "steel",
        "preperty": "obstructive",
        "rgb": [175, 179, 175],
        "size": [8, 8]
    },
    {
        "name": "water",
        "preperty": "obstructive",
        "rgb": [0, 0, 255],
        "size": [16, 16]
    },
    {
        "name": "bush",
        "preperty": "passable",
        "rgb": [0, 255, 0],
        "size": [16, 16]
    },
    {
        "name": "ice",
        "preperty": "passable",
        "rgb": [255, 255, 255],
        "size": [16, 16]
    }
]

fixed_elements = [
    {
        "name": "eagle",
        "preperty": "protected",
        "fixed": [96, 192],
        "size": [16, 16]
    
    }
]

images_elements = [
    {
        "name": "basic_tank",
        "preperty": "killable",
        "image": os.path.join(current_dir, "./assets/basic_tank.png"),
        "size": [16, 16]
    },
    {
        "name": "player1_tank",
        "preperty": "protected",
        "image": os.path.join(current_dir, "./assets/player1_tank.png"),
        "size": [16, 16]
    }
]

elements = {
    "rgb": rgb_elements,
    "fixed": fixed_elements,
    "images": images_elements
}
