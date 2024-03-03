class Node:
    """
    A class to represent a node in the grid.
    """
    def __init__(self, x, y):
        """Initialize the node with the given x and y position.
        Args:
            x (int): The x position of the node.
            y (int): The y position of the node.
        """
        self.x = x
        self.y = y
        self.neighbors = []
        self.parent = None
        self.g = float('inf')
        self.h = float('inf')
        self.f = float('inf')
        self.is_obstacle = False  # True if the node is an obstacle

    def __lt__(self, other):
        """Compare the node with another node.
        Args:
            other (Node): Another node.
        
        Returns:
            bool: True if the node is less than the other node, False otherwise.
        """
        return self.f < other.f

    def add_neighbor(self, neighbor):
        """Add a neighbor to the node.
        Args:
            neighbor (Node): The neighbor node.

        Returns:
            None
        """
        self.neighbors.append(neighbor)
