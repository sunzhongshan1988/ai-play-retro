"""
preperty: passable, protected, destroyable, variable
passable: tank can move through
protected: cannot be attacked
destroyable: can be destroyed

"""
import os

current_dir = os.path.dirname(__file__)

rgb_elements = {
    "road": {
        "preperty": "passable",
        "rgb": [0, 0, 0],
        "size": [16, 16]
    },
    "brick": {
        "preperty": "destroyable",
        "rgb": [153, 68, 41],
        "size": [4, 4]
    },
    "steel": {
        "preperty": "obstructive",
        "rgb": [175, 179, 175],
        "size": [8, 8]
    },
    "water": {
        "preperty": "obstructive",
        "rgb": [],
        "size": [16, 16]
    },
    "bush": {
        "preperty": "passable",
        "rgb": [],
        "size": [16, 16]
    },
    "ice": {
        "preperty": "passable",
        "rgb": [],
        "size": [16, 16]
    }
}

fixed_elements = {
    "eagle": {
        "preperty": "protected",
        "fixed": [96, 192],
        "size": [16, 16]
    }
}


images_elements = {
    "basic_tank": {
        "preperty": "killable",
        "image": os.path.join(current_dir, "basic_tank.png"),
        "size": [16, 16]
    },
    "player1_tank": {
        "preperty": "protected",
        "image": os.path.join(current_dir, "player1_tank.png"),
        "size": [16, 16]
    }
}

elements = {
    "rgb": rgb_elements,
    "fixed": fixed_elements,
    "images": images_elements
}