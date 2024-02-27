"""
preperty: passable, protected, destroyable, variable
passable: tank can move through
protected: cannot be attacked
destroyable: can be destroyed

"""
elements = {
    "road": {
        "preperty": "passable",
        "rgb": [0, 0, 0],
        "size": [16, 16]
    },
    "eagle": {
        "preperty": "protected",
        "position": [96, 192],
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
    },
    "basic_tank": {
        "preperty": "killable",
        "image": "./basic_tank.png",
        "size": [16, 16]
    },
    "player1_tank": {
        "preperty": "protected",
        "image": "./player1_tank.png",
        "size": [16, 16]
    }
}

def get_passable_elements():
    passable_elements = []
    for element in elements:
        if elements[element]["preperty"] == "passable":
            passable_elements.append(element)
    return passable_elements