import numpy as np
from collections import deque
from vision.astar_graph import AStarGraph
from vision.frame_process import FrameProcess
from .BattleCity_Nes.elements import elements
from .BattleCity_Nes.actions import Actions


class BattleCityNesWorker:
    """
    This class is responsible for playing the Battle City NES game.
    """
    def __init__(self) -> None:
        """Initialize the BattleCityNesWorker class.
        
        Returns:
            None
        """
        self.frame_process = FrameProcess(208, 208, 16)
        self.action = Actions()
        self.path = []
        self.directions = deque()

    def get_action(self, frame: np.ndarray) -> list[int]:
        """Get the action of the game.
        "buttons": ["B", null, "SELECT", "START", "UP", "DOWN", "LEFT", "RIGHT", "A"].

        Args:
            frame (np.ndarray): A numpy array of the frame image(RGB).
        
        Returns:
            list[int]: A list of 8 integers, each integer represents an action of the game.
        """

        if len(self.directions) == 0:
            self._path_planning(frame)
            self._path_to_directions()
        
        if len(self.directions) > 0:
            action = self.action.get_action([self.directions.popleft(), "FIRE"])
            return action
        else:
            return [0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    def _path_planning(self, frame: np.ndarray) -> None:
        """Get the vision of the game.

        Args:
            frame (np.ndarray): A numpy array of the frame image(RGB).
        
        Returns:
            None
        """

        # Process the frame
        elements_position = self.frame_process.get_elements_position(frame, elements, 0.71)

        enmy_tanks = [(x, y) for element, x, y in elements_position if element["preperty"] == "killable"]
        player1_positions = [(x, y) for element, x, y in elements_position if element["name"] == "player1_tank"]

        obstacles = [(x, y) for element, x, y in elements_position if element["name"] in ["steel", "eagle"]]

        if len(enmy_tanks) == 0 or len(player1_positions) == 0:
            print("No enemy tanks or player1 tank found for path planning.")
            return
        
        player1_position = player1_positions[0]
        #print("player1_position: ", player1_position)

        # Find the nearest enemy tank
        nearest_tank = self._find_nearest_enemy_tank(player1_position, enmy_tanks)
        #print("nearest_tank: ", nearest_tank)

        if nearest_tank is None:
            print("No enemy tanks found for path planning.")
            return

        # Create a graph for A* search
        astar_graph = AStarGraph(width=208//16, height=208//16, obstacles=obstacles)

        # Execute A* search
        start = (int(player1_position[0]), int(player1_position[1]))  # Start point
        goal = (int(nearest_tank[0]), int(nearest_tank[1]))  # End point
        path = astar_graph.a_star_search(start, goal)

        self.path = path

    def _path_to_directions(self):
        """
        Converts a list of path coordinates into tank movement directions.

        Args:
            path (list of tuples): The path as a list of (x, y) tuples.

        Returns:
            list of str: A list of directions ('up', 'down', 'left', 'right').
        """
        for i in range(len(self.path) - 1):
            current_position = self.path[i]
            next_position = self.path[i + 1]
            
            # Calculate the difference between the current position and the next position
            dx = next_position[0] - current_position[0]
            dy = next_position[1] - current_position[1]
            
            # Add the direction to the list
            if dx > 0:
                self.directions.append('RIGHT')
            elif dx < 0:
                self.directions.append('LEFT')
            elif dy > 0:
                self.directions.append('DOWN')
            elif dy < 0:
                self.directions.append('UP')


    @staticmethod
    def _find_nearest_enemy_tank(player_position, enemy_tanks):
        nearest_tank = None
        min_distance = float('inf')
        for tank in enemy_tanks:
            # Skip the player's position, because we don't want to consider it as an enemy tank
            if player_position == (tank[0], tank[1]):
                continue
            distance = ((player_position[0] - tank[0]) ** 2 + (player_position[1] - tank[1]) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                nearest_tank = tank
        return nearest_tank
