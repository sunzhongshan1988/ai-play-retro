import numpy as np
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
        self.directions = []

    def get_action(self) -> list[int]:
        """Get the action of the game.
        "buttons": ["B", null, "SELECT", "START", "UP", "DOWN", "LEFT", "RIGHT", "A"].

        Args:
            frame (np.ndarray): A numpy array of the frame image(RGB).
        
        Returns:
            list[int]: A list of 8 integers, each integer represents an action of the game.
        """

        if len(self.directions) == 0:
            self.path_to_directions()
        
        if len(self.directions) > 0:
            action = self.action.get_action([self.directions.pop(0), "FIRE"])
            return action
        else:
            return self.action.get_action(["FIRE"])
    
    def path_planning(self, frame: np.ndarray) -> None:
        """Get the vision of the game.

        Args:
            frame (np.ndarray): A numpy array of the frame image(RGB).
        
        Returns:
            None
        """

        if len(self.path) > 0:
            return

        # Process the frame
        elements_position = self.frame_process.get_elements_position(frame, elements)

        enmy_tanks = [(x, y) for element, x, y in elements_position if element["preperty"] == "killable"]
        player1_positions = [(x, y) for element, x, y in elements_position if element["name"] == "player1_tank"]

        obstacles = [(x, y) for element, x, y in elements_position if element["name"] in ["steel", "water"]]

        if len(enmy_tanks) == 0 or len(player1_positions) == 0:
            print("No enemy tanks or player1 tank found for path planning.")
            return
        
        player1_position = player1_positions[0]

        # 找到最近的 basic_tank
        nearest_tank = self._find_nearest_enemy_tank(player1_position, enmy_tanks)

        if nearest_tank is None:
            print("No enemy tanks found for path planning.")
            return

        # 初始化 AStarGraph 对象
        astar_graph = AStarGraph(width=208, height=208, obstacles=obstacles)

        # 进行 A* 搜索
        start = (int(player1_position[0]), int(player1_position[1]))  # 起点
        goal = (int(nearest_tank[0]), int(nearest_tank[1]))  # 终点
        path = astar_graph.a_star_search(start, goal)

        # 输出路径
        self.path = path

    def path_to_directions(self):
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
            
            # 计算坐标差异
            dx = next_position[0] - current_position[0]
            dy = next_position[1] - current_position[1]
            
            # 确定方向
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
            distance = ((player_position[0] - tank[0]) ** 2 + (player_position[1] - tank[1]) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                nearest_tank = tank
        return nearest_tank
